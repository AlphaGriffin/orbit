# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

from . import Abstract


class Register(Abstract):

    BYTES_UNITS = 8

    def __init__(self, units_max=None):
        self.units_max = units_max

        self.validate()

    def __str__(self, indent=None):
        return self.to_string(indent=indent, units_max=self.units_max)

    def admin(self):
        return False # admin not allowed

    def validate(self):
        self.validate_range_bytesize('Maximum units', self.units_max, self.BYTES_UNITS,
                optional=True, allow_zero=False)

    def prepare(self):
        units_max = self.units_max if self.units_max else 0

        message = units_max.to_bytes(self.BYTES_UNITS, self.ENDIAN)

        return message

    @classmethod
    def parse(cls, data):
        if len(data) < cls.BYTES_UNITS:
            raise ValueError('Not enough data while reading maximum units')
        units_max = int.from_bytes(data[:cls.BYTES_UNITS], cls.ENDIAN)
        if units_max == 0:
            units_max = None
        data = data[cls.BYTES_UNITS:]

        return Register(units_max)

