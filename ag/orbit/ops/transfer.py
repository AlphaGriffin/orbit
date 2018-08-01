# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

from . import Abstract

from decimal import Decimal


class Transfer(Abstract):

    BYTES_UNITS = 8

    def __init__(self, to, units=None):
        self.validate_address('To', to)
        self.to = to

        if units:
            self.validate_range('Units', units, 1, 2**(8 * self.BYTES_UNITS) - 1)
        self.units = units

    def __str__(self, indent=None):
        return self.to_string(indent=indent, units=(self.units if self.units else "ALL"), to=self.to)

    def admin(self):
        return None # admin okay but not required

    def prepare(self):
        message = self.serialize_address(self.to)

        if self.units:
            message += self.units.to_bytes(self.BYTES_UNITS, self.ENDIAN)

        return message

    @classmethod
    def parse(cls, data):
        to, data = cls.deserialize_address(data)

        if len(data) > 0:
            if len(data) < cls.BYTES_UNITS:
                raise ValueError('Not enough data while reading units')

            units = int.from_bytes(data[:cls.BYTES_UNITS], cls.ENDIAN)
        else:
            units = None

        return Transfer(to, units)

