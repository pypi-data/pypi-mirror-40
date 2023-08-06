#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import base64
import hashlib
import os

from joker.cast import want_bytes, want_unicode


class HashedPassword(object):
    def __init__(self, digest, algo, salt):
        self.digest = digest
        self.algo = algo
        self.salt = salt

    @staticmethod
    def gen_random_string(length):
        n = 1 + int(length * 0.625)
        return base64.b32encode(os.urandom(n)).decode()[:length]

    @classmethod
    def parse(cls, s):
        digest, algo, salt = s.split(':')
        return cls(digest, algo, salt)

    @classmethod
    def generate(cls, password, algo='sha512', salt=None):
        if salt is None:
            salt = cls.gen_random_string(16)
        p = want_bytes(password)
        s = want_bytes(salt)
        h = hashlib.new(algo, p + s)
        return cls(h.hexdigest(), algo, want_unicode(salt))

    def __str__(self):
        return '{}:{}:{}'.format(self.digest, self.algo, self.salt)

    def verify(self, password):
        hp1 = self.generate(password, self.algo, self.salt)
        return self.digest == hp1.digest
