# Copyright (C) 2017 Alpha Griffin
# @%@~LICENSE~@%@

"""DummyScript

This package-init script currently simply handles namespace sharing.

.. module:: dummyscript
   :synopsis: DummyScript Namespace
"""
#    (from http://github.com/google/protobuf)

try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

