# -*- coding: utf-8 -*-
# 17/9/13
# create by: snower

import re

class Expression(object):
    def __init__(self, expression_id, name, vtype, value):
        self._expression_id = expression_id
        self._name = name
        self._vtype = vtype
        self._value = value

        if self._vtype == "int":
            self.get_value = self.get_int_value
        elif self._vtype == "float":
            self.get_value = self.get_float_value
        else:
            self.get_value = self.get_string_value

        self._value = self.get_value({self._name: self._value})

    @property
    def id(self):
        return self._expression_id

    def get_int_value(self, log):
        try:
            return int(log.get(self._name, 0))
        except ValueError:
            return 0

    def get_float_value(self, log):
        try:
            return float(log.get(self._name, 0))
        except ValueError:
            return 0

    def get_string_value(self, log):
        value = log.get(self._name, '')
        if isinstance(value, str):
            return value

        try:
            return str(value)
        except ValueError:
            return ''

    def execute(self, log):
        return False

class GtExpression(Expression):
    def execute(self, log):
        value = self.get_value(log)
        if value is None:
            return False
        return value > self._value

class LtExpression(Expression):
    def execute(self, log):
        value = self.get_value(log)
        if value is None:
            return False
        return value < self._value

class GteExpression(Expression):
    def execute(self, log):
        value = self.get_value(log)
        if value is None:
            return False
        return value >= self._value

class LteExpression(Expression):
    def execute(self, log):
        value = self.get_value(log)
        if value is None:
            return False
        return value <= self._value

class EqualExpression(Expression):
    def execute(self, log):
        value = self.get_value(log)
        if value is None:
            return False
        return value == self._value

class NotEqualExpression(Expression):
    def execute(self, log):
        value = self.get_value(log)
        if value is None:
            return False
        return value != self._value

class RegexpExpression(Expression):
    def __init__(self, *args, **kwargs):
        super(RegexpExpression, self).__init__(*args, **kwargs)

        if isinstance(self._value, bytes):
            self._value = self._value.encode("utf-8")
        self._value = re.compile(self._value)
        self.get_value = self.get_string_value

    def execute(self, log):
        value = self.get_value(log)
        if isinstance(value, bytes):
            value = value.encode("utf-8")
        if self._value.match(value):
            return True
        return False

EXPS = {
    ">": GtExpression,
    ">=": GteExpression,
    "<": LtExpression,
    "<=": LteExpression,
    "==": EqualExpression,
    "!=": NotEqualExpression,
    "regexp": RegexpExpression,
}

def get_expression(exp):
    return EXPS.get(exp)