# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

# Basic process from https://stackoverflow.com/a/6462056

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import hashlib

# WARNING
# WARNING: Changing anything in this file will make any previously encrypted wallets inaccessible!
# WARNING

SALT_SIZE = 24
ITERATIONS = 99
AES_CHUNKS = 16
MODE = AES.MODE_ECB


# data and password both must be byte arrays
def encrypt(data, password):
    if not password:
        raise ValueError("Password cannot be empty")

    salt = get_random_bytes(SALT_SIZE)
    key = mkkey(password, salt)
    cipher = AES.new(key, MODE)
    data = pad(data)
    data = cipher.encrypt(data)
    data = salt + data

    return data

# data and password both must be byte arrays
def decrypt(data, password):
    salt = data[:SALT_SIZE]
    data = data[SALT_SIZE:]
    key = mkkey(password, salt)
    cipher = AES.new(key, MODE)
    data = cipher.decrypt(data)
    data = unpad(data)

    return data



def mkkey(password, salt):
    key = password + salt

    for i in range(ITERATIONS):
        key = hashlib.sha256(key).digest()

    return key

def pad(data):
    extra = len(data) % AES_CHUNKS
    size = AES_CHUNKS - extra
    padding = chr(size).encode('charmap') * size
    data += padding

    return data

def unpad(data):
    size = data[-1]
    data = data[:-size]

    return data

