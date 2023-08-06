#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def hex2dec(string_num):
    return long(string_num.upper(), 16)


def get_hash(key):
    m2 = hashlib.md5()
    m2.update(key)
    hex_keys = m2.hexdigest()
    byte_keys = bytearray.fromhex(hex_keys)
    hash_code = long(((byte_keys[3]) & 0xff) << 24) | long(((byte_keys[2]) & 0xFF) << 16) | long(
        (byte_keys[1] & 0xFF) << 8) | long(byte_keys[0] & 0xFF)
    return hash_code
