# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

from . import Abstract

from decimal import Decimal


class Create(Abstract):

    BYTES_SUPPLY = 8
    BYTES_DECIMALS = 1
    CHARS_MAX_SYMBOL = 7
    INVALID_TYPES_SYMBOL = ['Mc', 'P', 'Z', 'C'] # no spacing marks, punctuation, separators, or control codes
    INVALID_TYPES_NAME = ['Zl', 'Zp', 'C'] # no line/paragraph separator or control codes

    def __init__(self, supply, decimals, symbol, name=None, main_uri=None, image_uri=None):
        self.supply = supply
        self.decimals = decimals
        self.symbol = symbol
        self.name = name
        self.main_uri = main_uri
        self.image_uri = image_uri

        self.validate()

    def __str__(self, indent=None):
        normalized = Decimal(self.supply) / 10**self.decimals
        return self.to_string(indent=indent, supply=self.supply, decimals=self.decimals, normalized=normalized,
                symbol=self.symbol, name=self.name, main_uri=self.main_uri, image_uri=self.image_uri)

    def admin(self):
        return True # admin only

    def validate(self):
        self.validate_range_bytesize('Supply', self.supply, self.BYTES_SUPPLY, allow_zero=False)
        self.validate_range_bytesize('Decimals', self.decimals, self.BYTES_DECIMALS)

        self.validate_range('Symbol length', len(self.symbol), 1, self.CHARS_MAX_SYMBOL)
        if not self.is_safe_unicode(self.symbol, self.INVALID_TYPES_SYMBOL):
            raise ValueError('Symbol has invalid characters')

        if self.name is not None and (len(self.name) < 1 or not self.is_safe_unicode(self.name, self.INVALID_TYPES_NAME)):
            raise ValueError('Name is empty or has invalid characters')

        if self.main_uri is not None and (len(self.main_uri) < 1 or not self.is_link_uri(self.main_uri)):
            raise ValueError('Main URI is not a valid link URI')

        if self.image_uri is not None and (len(self.image_uri) < 1 or not self.is_src_uri(self.image_uri)):
            raise ValueError('Image URI is not a valid src URI')

    def prepare(self):
        message = (self.supply.to_bytes(self.BYTES_SUPPLY, self.ENDIAN) +
                self.decimals.to_bytes(self.BYTES_DECIMALS, self.ENDIAN) +
                self.symbol.encode(self.ENCODING))

        if self.name is not None or self.main_uri is not None or self.image_uri is not None:
            message += self.SEPARATOR

            if self.name is not None:
                message += self.name.encode(self.ENCODING)

            if self.main_uri is not None or self.image_uri is not None:
                message += self.SEPARATOR

                if self.main_uri is not None:
                    message += self.main_uri.encode('ascii')
            
                if self.image_uri is not None:
                    message += self.SEPARATOR
                    message += self.image_uri.encode('ascii')

        return message

    @classmethod
    def parse(cls, data):
        if len(data) < cls.BYTES_SUPPLY:
            raise ValueError('Not enough data while reading supply')
        supply = int.from_bytes(data[:cls.BYTES_SUPPLY], cls.ENDIAN)
        
        data = data[cls.BYTES_SUPPLY:]
        if len(data) < cls.BYTES_DECIMALS:
            raise ValueError('Not enough data while reading decimals')
        decimals = int.from_bytes(data[:cls.BYTES_DECIMALS], cls.ENDIAN)

        data = data[cls.BYTES_DECIMALS:]
        if len(data) < 1:
            raise ValueError('Not enough data while reading symbol')
        symbol, count, done = cls.read_text(data)

        if done:
            return Create(supply, decimals, symbol)

        data = data[count+1:]
        if len(data) < 1:
            raise ValueError('Not enough data while reading name')
        name, count, done = cls.read_text(data)

        if done:
            return Create(supply, decimals, symbol, name)

        data = data[count+1:]
        if len(data) < 1:
            raise ValueError('Not enough data while reading main URI')
        main_uri, count, done = cls.read_text(data, 'ascii')

        if done:
            return Create(supply, decimals, symbol, name, main_uri)

        data = data[count+1:]
        if len(data) < 1:
            raise ValueError('Not enough data while reading image URI')
        image_uri, count, done = cls.read_text(data, 'ascii')

        #if not done:
        #    raise ValueError('Unexpected extra data after reading image URI')

        return Create(supply, decimals, symbol, name, main_uri, image_uri)

