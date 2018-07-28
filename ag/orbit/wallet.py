# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

from . import API
from .config import dir
from .encryption import encrypt, decrypt

from bitcash import PrivateKey

from os.path import exists, join, split
from base64 import urlsafe_b64encode, urlsafe_b64decode
from glob import glob


def path(name):
    if not name or len(name) < 2:
        raise ValueError('Name must have at least 2 characters')

    return join(dir, urlsafe_b64encode(name.encode('utf-8')).decode('ascii') + ".wallet")

def list():
    wallets = []
    files = glob(join(dir, "*.wallet"))

    for filename in files:
        filename = split(filename)[1][:-7]
        name = urlsafe_b64decode(filename).decode('utf-8')
        wallets.append(name)

    return wallets

def create(wpath=None, get_key=None, get_password=None, show_address=None, unencrypted_warning=None):
    if wpath and exists(wpath):
        raise ValueError("A wallet already exists at this path! Please delete it first.")

    if get_key:
        try:
            wallet = PrivateKey.from_hex(get_key())
        except ValueError:
            raise ValueError("Not a valid key")
    else:
        wallet = PrivateKey()

    if show_address:
        show_address(wallet.address)

    key = wallet.to_hex()
    key = key.encode('charmap')

    if wpath:
        password = get_password() if get_password else None

        if password:
            data = b"%E%" + encrypt(API.PREAMBLE + key, password.encode('utf-8'))
        else:
            if unencrypted_warning:
                unencrypted_warning()

            data = b"%D%" + key

        with open(wpath, 'wb') as out:
            out.write(data)

    return wallet

def access(wpath, get_password=None):
    if not exists(wpath):
        raise ValueError("Wallet does not exist")

    with open(wpath, 'rb') as fin:
        data = fin.read()

    if len(data) < 4:
        raise ValueError("Not a valid wallet file")

    if data.startswith(b'%E%'):
        encrypted = True
    elif data.startswith(b'%D%'):
        encrypted = False
    else:
        raise ValueError("Not a valid wallet file")

    data = data[3:]
 
    if encrypted:
        password = get_password() if get_password else None

        if not password:
            raise ValueError("Password may not be empty")

        key = decrypt(data, password.encode('utf-8'))

        if not key.startswith(API.PREAMBLE):
            raise ValueError("Password is not correct")

        key = key[len(API.PREAMBLE):]

    else:
        key = data

    key = key.decode('charmap')

    return PrivateKey.from_hex(key)

