#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
FileCrypto.py

Crypto functions

'''

from os import urandom
from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode
from Utils import DEBUG
import sys

TEST_LICENSING = len(sys.argv) > 1 and sys.argv[1] == '--test-licensing'
if TEST_LICENSING:
    import Licensing
else:
    import NullLicensing as Licensing


def PadStr(clearText):
    padSize = AES.block_size - (len(clearText) % AES.block_size)
    DEBUG('padSize=' + str(padSize))
    return clearText + padSize * chr(padSize)


def UnpadStr(cypherText):
    padSize = ord(cypherText[-1])
    DEBUG('padSize=' + str(padSize))
    return cypherText[0:-padSize]


def EncryptStr(clearText, key):
    if not Licensing.EncryptionModuleLicensed():
        return

    iv = urandom(AES.block_size)
    clearText = PadStr(clearText)
    crypto = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + crypto.encrypt(clearText))


def DecryptStr(cypherText, key):
    if not Licensing.EncryptionModuleLicensed():
        return

    cypherText = b64decode(cypherText)
    iv = cypherText[0:AES.block_size]
    crypto = AES.new(key, AES.MODE_CBC, iv)
    return UnpadStr(crypto.decrypt(cypherText[AES.block_size:]))


def EncryptFile(in_file, out_file, key):
    bs = AES.block_size
    iv = urandom(bs)
    out_file.write(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            chunk = PadStr(chunk)
            finished = True
        out_file.write(cipher.encrypt(chunk))


def DecryptFile(in_file, out_file, key):
    bs = AES.block_size
    iv = in_file.read(bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            chunk = UnpadStr(chunk)
            finished = True
        out_file.write(chunk)

