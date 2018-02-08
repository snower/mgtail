# -*- coding: utf-8 -*-
# 17/9/14
# create by: snower

import datetime
import random
import string
import json
import argparse
import re

parser = argparse.ArgumentParser(description='tail of the glotcat')
parser.add_argument('-H', dest='host', default="127.0.0.1", help='glogcat host (default: 127.0.0.1)')
parser.add_argument('-P', dest='port', default=7002, type=int, help='glogcat port (default: 7002)')
parser.add_argument('-L', dest='logging', default="logging", help='glogcat logging')
parser.add_argument('-E', dest='exps', default=[], action="append", help='glogcat filters (expression: "==", "!=", ">", ">=", "<", "<=", "=regexp"')
parser.add_argument('-F', dest='fields', default=[], action="append", help='glogcat fields')
parser.add_argument('-f', dest='formats', default=[], action="append", help='glogcat formats (example: a:int or a:float)')
parser.add_argument('-t', dest='timefields', default=[], action="append", help='glogcat timefields (default: )')

args = parser.parse_args()

if args.logging not in ["logging", "logistic"]:
    print "unknown logging", args.logging
    exit()

INT_RE = re.compile("^\d+$")
FLOAT_RE = re.compile("^\d+?\.\d+$")

EXPS = ["==", "!=", ">=", "<=", ">", "<", "=regexp",]
FORMATS = ["int", "float"]

import default_settings

if args.host:
    default_settings.GLOGCAT["host"] = args.host

if args.port:
    default_settings.GLOGCAT["port"] = int(args.port)

from thriftclient import register_filter, unregister_filter, pull, FilterExpression, Filter

exps = []
for aexp in args.exps:
    for exp in EXPS:
        if exp in aexp:
            aexp = aexp.split(exp)
            if len(aexp) == 2:
                if exp == "=regexp":
                    if aexp[1][0] == '(' and aexp[1][-1] == ')':
                        vtype = "string"
                        value = aexp[1][1:-1]
                        try:
                            re.compile(value)
                        except:
                            break
                        exp = "regexp"
                    else:
                        break
                elif (aexp[1][0] == '"' and aexp[1][-1] == '"') or (aexp[1][0] == "'" and aexp[1][-1] == "'"):
                    vtype = "string"
                    value = aexp[1][1:-1]
                elif FLOAT_RE.match(aexp[1]):
                    vtype = "float"
                    value = aexp[1]
                elif INT_RE.match(aexp[1]):
                    vtype = "int"
                    value = aexp[1]
                else:
                    vtype = "string"
                    value = aexp[1]
                exps.append(FilterExpression(aexp[0], exp, vtype, value))
            break

fields = {}
for field in args.fields:
    fields[field] = 1

formats = {}
for format in args.formats:
    format = format.split(":")
    if len(format) != 2:
        continue

    if format[1] in FORMATS:
        formats[format[0]] = format[1]

notify_url ="pull://"
name = "tail_" + "".join([random.choice(string.digits + string.letters) for _ in range(16)])
filter = Filter(args.logging, name, exps=exps, fields=fields, formats=formats, notify_url=notify_url, expried_time=5)

result = register_filter(filter)
if result.result != 0:
    print "register error", name, result.msg
    exit()

print "register", name, filter
try:
    cursor = pull(name)
    while True:
        log = cursor.next()
        if not log:
            break
        if args.fields:
            flogs = []
            try:
                log = json.loads(log)
            except:
                print log.encode("utf-8")
                continue

            for field in args.fields:
                if field in args.timefields:
                    ts = log.get(field, 0)
                    try:
                        ts = int(ts)
                    except:
                        pass

                    if isinstance(ts, basestring):
                        flogs.append(ts)
                    else:
                        flogs.append(datetime.datetime.fromtimestamp(ts).isoformat())
                elif formats and field in formats:
                    if formats[field] not in ("int", "float"):
                        flogs.append("'%s'" % log.get(field, ""))
                    else:
                        flogs.append(str(log.get(field, 0)))
                else:
                    flogs.append("'%s'" % log.get(field, ""))
            print " ".join(flogs).encode("utf-8")
        else:
            print log.encode("utf-8")
except KeyboardInterrupt:
    pass
finally:
    result = unregister_filter(name)
    print "unregister", name, result.msg