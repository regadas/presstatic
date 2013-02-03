# -*- coding: utf-8 -*-

import hashlib


def hashfile(path, algorithm='md5', blocksize=65536):
    hasher = hashlib.new(algorithm)
    with open(path, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        return hasher.hexdigest()
