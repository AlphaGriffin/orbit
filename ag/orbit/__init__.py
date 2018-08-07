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

from .ops import Abstract, allocation, advertisement

import math


class API:
    """Main API for ORBIT events.
    """

    class Version:
        """Simple version parser.

        Separates a version string into major and minor components,
        and provides an encoded representation (major component only).

        :param version: Version string to parse.
        :type version: ``str``
        :raises ValueError: If the version string is not valid.
        """
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

        def __str__(self):
            if self.minor is not None:
                return '{}.{}'.format(self.major, self.minor)
            else:
                return '{}'.format(self.major)

    version = Version(__version__)
    launched = 542161 # block height containing the first compatible ORBIT transaction

    # WARNING: preamble is also used in wallet decryption verification!
    PREAMBLE = b'\xA4\x20\x19\x81'

    VERSION = version.encoded

    # required operation, designates the token and the user (signer)
    #OP_ADDRESS = b'\x00'

    # admin-only main operations
    OP_CREATE = b'\xA1'
    OP_ADVERTISE = b'\xAA'
    OP_ADVERTISE_CANCEL = b'\xAC'

    # admin-only edit (alter) operations
    #OP_ALTER_SYMBOL = b'\xE0'
    #OP_ALTER_NAME = b'\xE1'
    #OP_ALTER_WEBSITE = b'\xE2'
    #OP_ALTER_IMAGE = b'\xE3'

    # general operations (user or admin)
    OP_TRANSFER = b'\x10'
    #OP_DESTROY = b'\x11' # burn tokens

    # user-only operations
    OP_REGISTER = b'\xB0'
    OP_UNREGISTER = b'\xB1'

    # reserved for future use
    OP_RESERVED_BEGIN = 'b\xF0'
    OP_RESERVED_END = 'b\xFF'

    def prepare(self, address, op, limit=0):
        """Prepare a serialized byte stream to be stored as OP_RETURN data.

        :param address: Bitcoin cash address for the token.
        :type address: ``str``
        :param op: The operation to serialize.
        :type op: ``Abstract``
        :returns: Serialized representation of the operation.
        :rtype: ``bytes``
        :raises ValueError: If there is a problem serializing the operation.
        """
        if not isinstance(op, Abstract):
            raise ValueError('Operation must inherit the Abstract class: {}', type(op))

        op.validate()

        begin = self.PREAMBLE + self.VERSION
        data = Abstract.serialize_address(address)

        #if isinstance(op, Address):
        #    data = self.OP_ADDRESS

        if isinstance(op, allocation.Create):
            data += self.OP_CREATE

        elif isinstance(op, allocation.Transfer):
            data += self.OP_TRANSFER

        elif isinstance(op, advertisement.Advertise):
            data += self.OP_ADVERTISE

        elif isinstance(op, advertisement.Cancel):
            data += self.OP_ADVERTISE_CANCEL

        elif isinstance(op, advertisement.Register):
            data += self.OP_REGISTER

        elif isinstance(op, advertisement.Unregister):
            data += self.OP_UNREGISTER

        else:
            raise ValueError('Unsupported operation type: {}', type(op))

        opdata = op.prepare()
        if opdata:
            data += opdata

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

    def parse(self, data, combined=False):
        """Parse serialized bytes retrieved from OP_RETURN data.

        :param data: The serialized bytes to parse.
        :type data: ``bytes``
        :returns: An operation representing the data.
        :rtype: ``Abstract``
        :raises ValueError: If the byte stream does not represent a valid operation.
        """
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
            op = allocation.Create.parse(data[len(self.OP_CREATE):])

        elif data.startswith(self.OP_TRANSFER):
            op = allocation.Transfer.parse(data[len(self.OP_TRANSFER):])

        elif data.startswith(self.OP_ADVERTISE):
            op = advertisement.Advertise.parse(data[len(self.OP_ADVERTISE):])

        elif data.startswith(self.OP_ADVERTISE_CANCEL):
            op = advertisement.Cancel.parse(data[len(self.OP_ADVERTISE_CANCEL):])

        elif data.startswith(self.OP_REGISTER):
            op = advertisement.Register.parse(data[len(self.OP_REGISTER):])

        elif data.startswith(self.OP_UNREGISTER):
            op = advertisement.Unregister.parse(data[len(self.OP_UNREGISTER):])

        else:
            raise ValueError('Not a supported ORBIT operation')

        op.validate()
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

