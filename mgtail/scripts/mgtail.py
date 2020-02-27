# -*- coding: utf-8 -*-
# 17/9/14
# create by: snower

import datetime
import random
import string
import json
import argparse
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol.TBinaryProtocol import TBinaryProtocolAccelerated
from .client.ttypes import Filter, FilterExpression
from .client.Mgtail import Client

parser = argparse.ArgumentParser(description='tail of the mongodb caped collection')
parser.add_argument('-H', dest='host', default="127.0.0.1", help='host (default: 127.0.0.1)')
parser.add_argument('-P', dest='port', default=6455, type=int, help='port (default: 6455)')
parser.add_argument('-C', dest='collection', default="name", help='collection name')
parser.add_argument('-E', dest='exps', default=[], action="append", help='filters (expression: "==", "!=", ">", ">=", "<", "<=", "=regexp"')
parser.add_argument('-F', dest='fields', default=[], action="append", help='fields')
parser.add_argument('-f', dest='formats', default=[], action="append", help='formats (example: a:int or a:float)')
parser.add_argument('-t', dest='timefields', default=[], action="append", help='timefields (default: )')

def main():
    args = parser.parse_args()

    INT_RE = re.compile("^\d+$")
    FLOAT_RE = re.compile("^\d+?\.\d+$")

    EXPS = ["==", "!=", ">=", "<=", ">", "<", "=regexp",]
    FORMATS = ["int", "float"]

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

    name = "tail_" + "".join([random.choice(string.digits + string.ascii_letters) for _ in range(16)])
    filter = Filter(args.collection, name, exps=exps, fields=fields, formats=formats, expried_time=5)

    transport = TSocket(args.host, args.port)
    transport = TBufferedTransport(transport)
    protocol = TBinaryProtocolAccelerated(transport)
    client = Client(protocol)
    transport.open()

    result = client.register_filter(filter)
    if result.result != 0:
        print("register error", name, result.msg)
        exit()

    print("register", name, filter)
    try:
        cursor = client.pull(name)
        while True:
            log = cursor.next()
            if not log:
                break
            if args.fields:
                flogs = []
                try:
                    log = json.loads(log)
                except:
                    print(log.encode("utf-8"))
                    continue

                for field in args.fields:
                    if field in args.timefields:
                        ts = log.get(field, 0)
                        try:
                            ts = int(ts)
                        except:
                            pass

                        if isinstance(ts, str):
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
                print(" ".join(flogs).encode("utf-8"))
            else:
                print(log.encode("utf-8"))
    except KeyboardInterrupt:
        pass
    finally:
        result = client.unregister_filter(name)
        print("unregister", name, result.msg)
        transport.close()

if __name__ == "__main__":
    main()