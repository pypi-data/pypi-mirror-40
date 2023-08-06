#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import codecs
import datetime
import decimal
import json


def jsonencoder_default(encoder, obj):
    if hasattr(obj, 'as_json_serializable'):
        return obj.as_json_serializable()
    datetime_types = datetime.datetime, datetime.date, datetime.time
    if isinstance(obj, datetime_types):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.total_seconds()

    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return encoder.default(vars(obj))


class JSONEncoderExt(json.JSONEncoder):
    default = jsonencoder_default


def indented_json_dumps(obj, **kwargs):
    kwargs.setdefault('indent', 4)
    kwargs.setdefault('ensure_ascii', False)
    kwargs.setdefault('cls', JSONEncoderExt)
    return json.dumps(obj, **kwargs)


def indented_json_print(obj, **kwargs):
    print_kwargs = {}
    for k in ['sep', 'end', 'file', 'flush']:
        if k in kwargs:
            print_kwargs[k] = kwargs.pop(k)
    s = indented_json_dumps(obj, **kwargs)
    print(s, **print_kwargs)


# might be useless
def indented_json_print_legacy(obj, **kwargs):
    # https://stackoverflow.com/a/12888081/2925169
    decoder = codecs.getdecoder('unicode_escape')
    print_kwargs = {}
    for k in ['sep', 'end', 'file', 'flush']:
        if k in kwargs:
            print_kwargs[k] = kwargs.pop(k)
    kwargs.setdefault('indent', 4)
    s = json.dumps(obj, **kwargs)
    print(decoder(s)[0], **print_kwargs)
