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
from .ops.create import Create


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
    genesis = 540155 # block height containing the first compatible ORBIT transaction

    PREAMBLE = b'\xA4\x20'
    VERSION = version.encoded

    OP_NULL = b'\x00'

    OP_CREATE = b'\x01'
    #OP_DESTROY = b'\x02'
    #OP_TRANSFER = b'\x03'
    #OP_ADVERTISE = b'\x04'
    #OP_SUBSCRIBE = b'\x05'
    #OP_DISPENSE_CLOSE = b'\x06'

    #OP_ALTER_SYMBOL = b'\xA0'
    #OP_ALTER_NAME = b'\xA1'
    #OP_ALTER_WEBSITE = b'\xA2'
    #OP_ALTER_IMAGE = b'\xA3'

    OP_RESERVED = 'b\xFF'

    def parse(self, data):
        if not data.startswith(self.PREAMBLE):
            return None
        data = data[len(self.PREAMBLE):]

        if not data.startswith(self.VERSION):
            raise ValueError('Not a supported ORBIT version')
        data = data[len(self.VERSION):]

        if data.startswith(self.OP_NULL):
            raise ValueError('The NULL operation is ignored')

        elif data.startswith(self.OP_CREATE):
            return Create.parse(data[len(self.OP_CREATE):])

        elif data.startswith(self.OP_RESERVED):
            raise ValueError('The RESERVED operation may not be used')

        else:
            raise ValueError('Not a supported ORBIT operation')

    def prepare(self, op):
        if not isinstance(op, Abstract):
            raise ValueError('Operation must inherit the Abstract class: {}', type(op))

        message = self.PREAMBLE + self.VERSION

        if isinstance(op, Create):
            message += self.OP_CREATE
        else:
            raise ValueError('Unsupported operation type: {}', type(op))

        message += op.prepare()
        return message

