#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os
import random
import time
from os.path import join

import yaml


class Rumor(object):
    __slots__ = ['attributes']

    def __init__(self, **attributes):
        self.attributes = attributes

    def __getattr__(self, item):
        try:
            return self.attributes[item]
        except KeyError:
            return random.randrange(10000)


class ContextFile(object):
    def __init__(self, path, ttl=None):
        self._data = {}
        self._mtime = None
        self._xtime = None
        self.path = path
        self.ttl = ttl

    def _load_from_file(self):
        mtime = os.path.getmtime(self.path)
        if mtime - (self._mtime or 0) < 0.001:
            return
        data = yaml.load(open(self.path))
        if not isinstance(data, dict):
            raise TypeError('the contextmap file is not dict-like')
        self._data = data
        self._mtime = mtime

    def get(self, key, default=None):
        current_time = time.time()
        if self._xtime and self._xtime < current_time:
            self._load_from_file()
            self._xtime = current_time
        return self._data.get(key, default)

    def setdefault(self, key, default=None):
        return self._data.setdefault(key, default)


class ContextDirectory(object):
    def __init__(self, dir_path, ttl=None):
        if not os.path.isdir(dir_path):
            raise ValueError('requires a directory')
        self._cache = {}
        self._xtime = {}
        self._mtime = {}
        self.path = dir_path
        self.ttl = ttl

    def _load_from_file(self, key):
        """
        Update _mtime and _cache if yaml.load() is called.
        Do NOT touch _xtime in this method.
        """
        path = join(self.path, key + '.yml')
        mtime = os.path.getmtime(path)

        # avoid float equality test
        if mtime - self._mtime.get(key, 0) < 0.001:
            try:
                return self._cache[key]
            except KeyError:
                pass
        value = yaml.load(open(path))
        self._mtime[key] = mtime
        self._cache[key] = value
        return value

    def setdefault(self, key, default=None):
        return self._cache.setdefault(key, self.get(key, default))

    def get(self, key, default=None):
        """
        Update _xtime if _load_from_file() is called and ttl available.
        Do NOT touch _cache and _mtime in this method;
        it is the job of _load_from_file.
        """
        current_time = time.time()
        expire_time = self._xtime.get(key)

        # not expired
        if not expire_time or current_time < expire_time:
            try:
                return self._cache[key]
            except KeyError:
                pass
        try:
            value = self._load_from_file(key)
        except FileNotFoundError:
            return default

        try:
            ttl = value['_ttl']
        except (TypeError, LookupError):
            ttl = self.ttl

        # try to del _xtime[key] if ttl not available
        if ttl is None:
            self._xtime.pop(key, None)
        else:
            self._xtime[key] = current_time + ttl
        return value
