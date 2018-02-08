# -*- coding: utf-8 -*-
# 15/5/6
# create by: snower

import logging
from tornado import gen
from filter import Filter
from .processor.Mgtail import pull_args, pull_result, TMessageType, TTransport, TApplicationException
from .processor.ttypes import FilterResult, Log

def process_pull(self, seqid, iprot, oprot):
    args = pull_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = pull_result()
    try:
        result.success = self._handler.pull(seqid, iprot, oprot, args.name)
        msg_type = TMessageType.REPLY
    except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
        raise
    except Exception as ex:
        msg_type = TMessageType.EXCEPTION
        logging.exception(ex)
        result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

    if result.success is None:
        raise EOFError()

    oprot.writeMessageBegin("pull", msg_type, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

class Handler(object):
    def __init__(self, manager):
        self.manager = manager

    @gen.coroutine
    def init(self):
        self.manager.get_server().server.processor._processMap["pull"] = process_pull

    @gen.coroutine
    def register_filter(self, filter):
        gfilter = self.manager.get_filter(filter.name)
        if gfilter:
            gfilter.update(filter)
        else:
            gfilter = Filter(self.manager, filter)
            self.manager.register_filter(gfilter)
        self.manager.store_session()
        logging.info("register_filter %s", filter)
        raise gen.Return(FilterResult(0, ''))

    @gen.coroutine
    def unregister_filter(self, name):
        gfilter = self.manager.get_filter(name)
        if gfilter:
            gfilter.close()
        logging.info("unregister_filter %s", name)
        raise gen.Return(FilterResult(0, ''))

    @gen.coroutine
    def pull(self, seqid, iprot, oprot, name):
        gfilter = self.manager.get_filter(name)
        if not gfilter:
            raise gen.Return(Log('', '', ''))

        result = yield gfilter.pull_writer(seqid, iprot, oprot)
        if result:
            logging.info("pull %s", name)
            raise gen.Return(Log(gfilter.logging, gfilter.name, ''))
        logging.info("pull %s", name)
        raise gen.Return(None)

    @gen.coroutine
    def get_all_filters(self):
        filtes = []
        for _, filter in self.manager._filters.iteritems():
            filtes.append(filter._origin)
        logging.info("get_all_filters")
        raise gen.Return(filtes)