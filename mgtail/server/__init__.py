# -*- coding: utf-8 -*-
# 18/2/8
# create by: snower

import logging
from tornado.ioloop import IOLoop
from thrift.protocol.TBinaryProtocol import TBinaryProtocolAcceleratedFactory
from torthrift.transport import TIOStreamTransportFactory
from torthrift.server import TTornadoServer
from .processor.Mgtail import Processor
from .handler import Handler, process_pull
from ..manager import Manager
from ..collection import Collection
from .. import config

class ThriftServer(object):
    def __init__(self):
        self.server = None
        self.manager = Manager(self)

    def serve(self):
        handler = Handler(self.manager)
        processor = Processor(handler)
        tfactory = TIOStreamTransportFactory()
        protocol = TBinaryProtocolAcceleratedFactory()
        self.server = TTornadoServer(processor, tfactory, protocol)
        self.server.processor._processMap["pull"] = process_pull


        bind_address = config.get("BIND_ADDRESS", "127.0.0.1")
        port = config.get("PORT", 6455)
        self.server.bind(port, bind_address)
        self.server.start(1)

        ioloop = IOLoop.instance()
        self.manager.start()
        logging.info("starting server by %s:%s", bind_address, port)
        ioloop.start()

    def get_manager(self):
        return self.manager

    def init(self):
        for collection_name in config.get("collections", []):
            collection = Collection(collection_name, self.manager)
            self.manager.register_collection(collection)
        self.manager.load_session()

    def start(self):
        try:
            self.init()
            self.server()
        except Exception as e:
            logging.error("server error: %s", e)

    def stop(self):
        IOLoop.current().add_callback(lambda :IOLoop.current().stop())
        logging.info("server stoping")