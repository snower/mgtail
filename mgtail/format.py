# -*- coding: utf-8 -*-
# 17/9/13
# create by: snower

class Format(object):
    def __init__(self, name):
        self._name = name

    def format(self, value):
        return value

class IntFormat(Format):
    def format(self, value):
        try:
            return int(value)
        except ValueError:
            return 0

class FloatFormat(Format):
    def format(self, value):
        try:
            return float(value)
        except ValueError:
            return 0

FORMATS = {
    "int": IntFormat,
    "float": FloatFormat,
}

def get_format(exp):
    return FORMATS.get(exp)