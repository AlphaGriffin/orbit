# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

from ag.orbit.ops import Abstract


class Advertise(Abstract):

    BYTES_EXCHANGE = 8
    BYTES_UNITS = 8
    BYTES_BLOCK = 4

    def __init__(self, exchange_rate=None, units_avail=None, units_min=None, units_max=None,
            block_begin=None, block_end=None, block_deliver=None, preregister=False):

        self.exchange_rate = exchange_rate
        self.units_avail = units_avail
        self.units_min = units_min
        self.units_max = units_max
        self.block_begin = block_begin
        self.block_end = block_end
        self.block_deliver = block_deliver
        self.preregister = preregister

        self.validate()

    def __str__(self, indent=None):
        return self.to_string(indent=indent,
                exchange_rate=("1/{}".format(self.exchange_rate) if self.exchange_rate < 0 else self.exchange_rate),
                units_avail=(self.units_avail if self.units_avail else "ALL"), units_min=self.units_min,
                units_max=self.units_max, block_begin=self.block_begin, block_end=self.block_end,
                block_deliver=self.block_deliver, preregister=self.preregister)

    def admin(self):
        return True # admin only

    def validate(self):
        self.validate_range_bytesize('Exchange rate', self.exchange_rate, self.BYTES_EXCHANGE,
                optional=True, allow_zero=False, signed=True)

        #if self.units_avail is not False:
        self.validate_range_bytesize('Available units', self.units_avail, self.BYTES_UNITS,
                optional=True, allow_zero=False)

        self.validate_range_bytesize('Minimum units per user', self.units_min, self.BYTES_UNITS,
                optional=True, allow_zero=False)
        if self.units_avail:
            self.validate_range('Minimum units per user', self.units_min, None, self.units_avail, optional=True)
        if self.exchange_rate < 0:
            self.validate_rante('Minimum units per user', self.units_min, -1 * self.exchange_rate, None, optional=True)

        self.validate_range_bytesize('Maximum units per user', self.units_max, self.BYTES_UNITS,
                optional=True, allow_zero=False)
        if self.units_min:
            self.validate_range('Maximum units per user', self.units_max, self.units_min, None, optional=True)
        if self.units_avail:
            self.validate_range('Maximum units per user', self.units_max, 1, self.units_avail, optional=True)

        self.validate_range_bytesize('Beginning block', self.block_begin, self.BYTES_BLOCK,
                optional=True, allow_zero=False)

        self.validate_range_bytesize('Ending block', self.block_end, self.BYTES_BLOCK,
                optional=True, allow_zero=False)
        if self.block_begin:
            self.validate_range('Ending block', self.block_deliver, self.block_begin, None, optional=True)

        self.validate_range_bytesize('Delivery block', self.block_deliver, self.BYTES_BLOCK,
                optional=True, allow_zero=False)
        if self.block_begin:
            self.validate_range('Delivery block', self.block_deliver, self.block_begin, None, optional=True)

        if self.preregister == True:
            if not self.exchange_rate or not self.block_begin:
                raise ValueError("Preregister only allowed when exchange rate and beginning block are specified")
        elif self.preregister != False:
            raise ValueError("Preregister flag must be True or False")

    def prepare(self):
        exchange_rate = self.exchange_rate if self.exchange_rate else 0
        units_avail = self.units_avail if self.units_avail else 0
        units_min = self.units_min if self.units_min else 0
        units_max = self.units_max if self.units_max else 0
        block_begin = self.block_begin if self.block_begin else 0
        block_end = self.block_end if self.block_end else 0
        block_deliver = self.block_deliver if self.block_deliver else 0
        preregister = self.preregister

        message = exchange_rate.to_bytes(self.BYTES_EXCHANGE, self.ENDIAN, signed=True)
        message += units_avail.to_bytes(self.BYTES_UNITS, self.ENDIAN)
        message += units_min.to_bytes(self.BYTES_UNITS, self.ENDIAN)
        message += units_max.to_bytes(self.BYTES_UNITS, self.ENDIAN)
        message += block_begin.to_bytes(self.BYTES_BLOCK, self.ENDIAN)
        message += block_end.to_bytes(self.BYTES_BLOCK, self.ENDIAN)
        message += block_deliver.to_bytes(self.BYTES_BLOCK, self.ENDIAN)

        # since we use a whole byte to store a single bit, we have some room for future options here
        message += (1).to_bytes(1, self.ENDIAN) if preregister else (0).to_bytes(1, self.ENDIAN)

        return message

    @classmethod
    def parse(cls, data):
        if len(data) < cls.BYTES_EXCHANGE:
            raise ValueError('Not enough data while reading exchange rate')
        exchange_rate = int.from_bytes(data[:cls.BYTES_EXCHANGE], cls.ENDIAN, signed=True)
        if exchange_rate == 0:
            exchange_rate = None
        data = data[cls.BYTES_EXCHANGE:]

        if len(data) < cls.BYTES_UNITS:
            raise ValueError('Not enough data while reading available units')
        units_avail = int.from_bytes(data[:cls.BYTES_UNITS], cls.ENDIAN)
        if units_avail == 0:
            units_avail = None
        data = data[cls.BYTES_UNITS:]

        if len(data) < cls.BYTES_UNITS:
            raise ValueError('Not enough data while reading minimum units')
        units_min = int.from_bytes(data[:cls.BYTES_UNITS], cls.ENDIAN)
        if units_min == 0:
            units_min = None
        data = data[cls.BYTES_UNITS:]

        if len(data) < cls.BYTES_UNITS:
            raise ValueError('Not enough data while reading maximum units')
        units_max = int.from_bytes(data[:cls.BYTES_UNITS], cls.ENDIAN)
        if units_max == 0:
            units_max = None
        data = data[cls.BYTES_UNITS:]

        if len(data) < cls.BYTES_BLOCK:
            raise ValueError('Not enough data while reading beginning block')
        block_begin = int.from_bytes(data[:cls.BYTES_BLOCK], cls.ENDIAN)
        if block_begin == 0:
            block_begin = None
        data = data[cls.BYTES_BLOCK:]

        if len(data) < cls.BYTES_BLOCK:
            raise ValueError('Not enough data while reading ending block')
        block_end = int.from_bytes(data[:cls.BYTES_BLOCK], cls.ENDIAN)
        if block_end == 0:
            block_end = None
        data = data[cls.BYTES_BLOCK:]

        if len(data) < cls.BYTES_BLOCK:
            raise ValueError('Not enough data while reading delivery block')
        block_deliver = int.from_bytes(data[:cls.BYTES_BLOCK], cls.ENDIAN)
        if block_deliver == 0:
            block_deliver = None
        data = data[cls.BYTES_BLOCK:]

        if len(data) < 1:
            raise ValueError('Not enough data while reading peregister flag')
        preregister = int.from_bytes(data[0:1], cls.ENDIAN)
        if preregister == 1:
            preregister = True
        elif preregister == 0:
            preregister = False
        else:
            raise ValueError('Invalid value for preregister flag')
        data = data[1:]

        return Advertise(exchange_rate, units_avail, units_min, units_max, block_begin, block_end, block_deliver, preregister)


class Cancel(Abstract):

    BYTES_HASH_SIZE = 1

    def __init__(self, txhash):
        self.txhash = txhash

        self.validate()

    def __str__(self, indent=None):
        return self.to_string(indent=inent, txhash=self.txhash)

    def admin(self):
        return True # admin only

    def validate(self):
        if not self.txhash:
            raise ValueError("Transaction hash is required")

    def prepare(self):
        txhash = bytes(bytearray.fromhex(self.txhash))
        message = len(txhash).to_bytes(self.BYTES_HASH_SIZE, self.ENDIAN)
        message += txhash

        return message

    @classmethod
    def parse(cls, data):
        if len(data) < cls.BYTES_HASH_SIZE:
            raise ValueError('Not enough data while reading tx hash size')
        size = int.from_bytes(data[0:cls.BYTES_HASH_SIZE], cls.ENDIAN)
        data = data[cls.BYTES_HASH_SIZE:]

        if len(data) < size:
            raise ValueError('Not enough data while reading tx hash')
        txhash = data[0:size]
        data = data[size:]

        return Cancel(txhash)


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


class Unregister(Abstract):

    BYTES_UNITS = 8

    def __init__(self):
        self.validate()

    def __str__(self, indent=None):
        return self.to_string(indent=indent)

    def admin(self):
        return False # admin not allowed

    def validate(self):
        pass

    def prepare(self):
        return None

    @classmethod
    def parse(cls, data):
        return Unregister()

