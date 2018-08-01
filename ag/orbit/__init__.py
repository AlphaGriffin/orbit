# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

"""Op_Return Bitcoin-Implemented Tokens

ORBIT is a specification and API for tokens on Bitcoin Cash.

.. module:: ag.orbit
   :platform: Unix
   :synopsis: Op_Return Bitcoin-Implemented Tokens
.. moduleauthor:: Shawn Wilson <lannocc@alphagriffin.com>
"""

from .__version__ import __version__
print ("ORBIT API version %s" % (__version__))

from .ops import Abstract
#from .ops.address import Address
from .ops.create import Create
from .ops.transfer import Transfer

import math


class API:

    class Version:
        def __init__(self, version):
            dot = version.find('.')
            if dot < 0:
                major = int(version)
                minor = None
            elif dot < 1:
                raise ValueError('expecting major version number before decimal point: {}'.format(version))
            else:
                major = int(version[:dot])

                mdot = version.find('.', dot + 1)
                if mdot < 0:
                    minor = int(version[dot+1:])
                elif mdot == dot + 1:
                    raise ValueError('expecting minor version number before second decimal point: {}'.format(version))
                else:
                    minor = int(version[dot+1:mdot])
            
            if major < 0 or major > 255:
                raise ValueError('major version number must be >= 0 and < 256: {}'.format(version))

            if minor < 0:
                raise ValueError('minor version number must be >= 0: {}'.format(version))

            self.major = major
            self.minor = minor
            self.encoded = (chr(major)).encode('ascii')

        def __repr__(self):
            if self.minor is not None:
                return '{}.{}'.format(self.major, self.minor)
            else:
                return '{}'.format(self.major)

    version = Version(__version__)
    #genesis = 540155 # block height containing the first compatible ORBIT transaction
    genesis = 541337 # block height containing the first compatible ORBIT transaction

    # WARNING: preamble is also used in wallet decryption verification!
    PREAMBLE = b'\xA4\x20\x19\x81'

    VERSION = version.encoded

    # required operation, designates the token and the user (signer)
    #OP_ADDRESS = b'\x00'

    # admin-only main operations
    OP_CREATE = b'\xA1'
    #OP_DESTROY = b'\xA2'
    #OP_ADVERTISE = b'\xA3'
    #OP_DISPENSE_CLOSE = b'\xA4'

    # admin-only edit (alter) operations
    #OP_ALTER_SYMBOL = b'\xE0'
    #OP_ALTER_NAME = b'\xE1'
    #OP_ALTER_WEBSITE = b'\xE2'
    #OP_ALTER_IMAGE = b'\xE3'

    # general operations (user or admin)
    OP_TRANSFER = b'\x10'

    # user-only operations
    #OP_SUBSCRIBE = b'\xB0'

    # reserved for future use
    OP_RESERVED_BEGIN = 'b\xF0'
    OP_RESERVED_END = 'b\xFF'

    def parse(self, data, combined=False):
        data = self._parse1(data)

        if not data:
            return None

        if len(data) < 2:
            raise ValueError('Not enough data for a proper ORBIT transaction')

        if not combined and int.from_bytes(data[0:1], 'big') != 0:
            raise ValueError('Multi-return transaction indicated and combined=False; ' +
                    'combine the data segments first or use parse_all() instead')
        data = data[1:]

        return self._parse2(data)

    def _parse1(self, data):
        if not data.startswith(self.PREAMBLE):
            return None
        data = data[len(self.PREAMBLE):]

        if not data.startswith(self.VERSION):
            raise ValueError('Not a supported ORBIT version')
        data = data[len(self.VERSION):]

        return data

    def _parse2(self, data):
        #if data.startswith(self.OP_ADDRESS):
        #    return Address.parse(data[len(self.OP_ADDRESS):])

        address, data = Abstract.deserialize_address(data)

        if data.startswith(self.OP_CREATE):
            op = Create.parse(data[len(self.OP_CREATE):])

        elif data.startswith(self.OP_TRANSFER):
            op = Transfer.parse(data[len(self.OP_TRANSFER):])

        else:
            raise ValueError('Not a supported ORBIT operation')

        return (address, op)

    '''
    def parse_all(self, vouts):
        continues = 0
        orbiting = None
        ops = []

        for vout in vouts:
            asmhex = vout['scriptPubKey']['hex']

            if not asmhex.startswith('6a'): # OP_RETURN
                if orbiting:
                    raise ValueError('Continuation tx requires OP_RETURN to follow')
                else:
                    continue

            data = bytearray.fromhex(asmhex[4:]) # we skip the next byte too)

            if orbiting:
                orbiting += data
                --continues

            else:
                data = self._parse1(data)

                if not data:
                    continue

                if len(data) < 2:
                    raise ValueError('Not enough data for a proper ORBIT transaction')

                continues = int.from_bytes(data[0:1], 'big')
                data = data[1:]
                orbiting = data

            if orbiting and continues < 1:
                ops.append(self._parse2(orbiting))
                orbiting = None

        return ops
    '''

    def prepare(self, address, op, limit=0):
        if not isinstance(op, Abstract):
            raise ValueError('Operation must inherit the Abstract class: {}', type(op))

        begin = self.PREAMBLE + self.VERSION
        data = Abstract.serialize_address(address)

        #if isinstance(op, Address):
        #    data = self.OP_ADDRESS

        if isinstance(op, Create):
            data += self.OP_CREATE

        elif isinstance(op, Transfer):
            data += self.OP_TRANSFER

        else:
            raise ValueError('Unsupported operation type: {}', type(op))

        data += op.prepare()

        if limit > 0: # this is not actually used unless and until multiple OP_RETURN outputs are supported by BCH nodes
            messages = []

            header = len(begin) + 1
            size = header + len(data)

            if size > limit:
                continues = size // limit
                if size % limit == 0:
                    continues -= 1

                messages.append(begin + continues.to_bytes(1, 'big') + data[:limit-header])
                data = data[limit-header:]

                while len(data) > limit:
                    messages.append(data[:limit])
                    data = data[limit:]

                if len(data) > 0:
                    messages.append(data)

            else:
                messages.append(begin + (0).to_bytes(1, 'big') + data)

            return messages

        else:
            return begin + (0).to_bytes(1, 'big') + data

