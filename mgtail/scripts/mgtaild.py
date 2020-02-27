# -*- coding: utf-8 -*-
# 18/2/8
# create by: snower

import sys
import os
import atexit
import argparse
import multiprocessing
from .. import config
from ..server import ThriftServer

parser = argparse.ArgumentParser(description='tail of the mongodb caped collection')
parser.add_argument('--conf', dest='conf', default="/etc/mgtail.conf", help='host (default: /etc/mgtail.conf)')
parser.add_argument('--nodemon', dest='nodemon', nargs='?', const=True, default=False, type=bool, help='run no demon mode')
parser.add_argument('--bind', dest='bind_host', default="", help='bind host (default: 127.0.0.1)')
parser.add_argument('--port', dest='bind_port', default=0, type=int, help='bind port (default: 6455)')
parser.add_argument('--log', dest='log_file', default='', type=str, help='log file')
parser.add_argument('--log-level', dest='log_level', default='', type=str, help='log level (default: INFO)')
parser.add_argument('--session', dest='session_path', default='', type=str, help='session path (default: /tmp')
parser.add_argument('--mongo_url', dest='mongo_url', default='', type=str, help='mongo server url (default: 127.0.0.1')
parser.add_argument('--collection', dest='collections', default=[], action="append", type=str, help='collection name')

def main():
    args = parser.parse_args()

    if args.conf:
        try:
            config.load_conf(args.conf)
        except Exception as e:
            print("load conf file error ", str(e))
            exit(1)

    if not args.nodemon:
        def run():
            try:
                server = ThriftServer()

                sys.stdin.close()
                sys.stdin = open(os.devnull)

                sys.stdout.close()
                sys.stdout = open(os.devnull, 'w')

                sys.stderr.close()
                sys.stderr = open(os.devnull, 'w')

                server.start()
            except Exception as e:
                print(e)
                exit(1)

        p = multiprocessing.Process(target=run, name=" ".join(sys.argv))
        p.start()
        atexit._clear()
    else:
        try:
            server = ThriftServer()
            server.start()
        except Exception as e:
            print(e)
            exit(1)

if __name__ == "__main__":
    main()