# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

from . import Abstract


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

