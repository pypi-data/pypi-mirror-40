"""
Minimal template loader used when not used in conjunction with Emrichen.
"""

import os
import json


def load_json(str_or_stream):
    if hasattr(str_or_stream, 'read'):
        str_or_stream = str_or_stream.read()
    return [json.loads(str_or_stream)]


def load_yaml(str_or_stream):
    import yaml
    return list(yaml.safe_load_all(str_or_stream))


PARSERS = {
    'yaml': load_yaml,
    'json': load_json,
}


def determine_format(filename, choices, default):
    if filename:
        ext = os.path.splitext(filename)[1].lstrip('.').lower()
        if ext in choices:
            return ext
    return default


def parse(data, format=None, filename=None):
    if filename is None and hasattr(data, 'name') and data.name:
        filename = data.name

    if format is None:
        format = determine_format(filename, PARSERS, 'yaml')

    if format in PARSERS:
        return PARSERS[format](data)
    else:
        raise ValueError('No parser for format {format}'.format(format=format))
