# -*- coding: utf-8 -*-
# 17/9/13
# create by: snower

import logging
from tornado import gen
from tornado.ioloop import IOLoop
from .writer import PullWriter

class Filter(object):
    def __init__(self, manager, filter):
        self._origin = filter
        self._manager = manager
        self._collection = filter.collection
        self._name = filter.name
        self._exps = self.init_expressions(filter.exps)
        self._fields = filter.fields
        self._formats = self.init_formats(filter.formats)
        self._max_queue_size = filter.max_queue_size
        self._expried_time = filter.expried_time
        self._writer = None
        self._timeout = None

        self.init_writer()

    @property
    def collection(self):
        return self._collection

    @property
    def name(self):
        return self._name

    def init_expressions(self, oexps):
        exps = []
        for exp in oexps:
            exp = self._manager.get_expression(exp.name, exp.exp, exp.vtype, exp.value)
            if exp:
                exps.append(exp)
        return exps

    def init_formats(self, oformats):
        formats = {}
        for name, format in oformats.iteritems():
            format = self._manager.get_format(format)
            if format:
                formats[name] = format
        return formats

    def init_writer(self):
        if self._writer:
            self._writer.close()
            self._writer = None

        self._writer = PullWriter(self, self._max_queue_size)
        self.start_timeout()
        return self._writer

    def close(self):
        self._writer.close()
        self._manager.unregister_filter(self)
        self._manager.store_session()
        self._manager = None
        logging.info("filter close %s", self._name)

    def update(self, filter):
        self._origin = filter
        self._collection = filter.collection
        self._name = filter.name
        self._exps = self.init_expressions(filter.exps)
        self._fields = filter.fields
        self._formats = self.init_formats(filter.formats)
        self._max_queue_size = filter.max_queue_size
        self._expried_time = filter.expried_time

        if self._writer:
            self._writer.update(self._max_queue_size)
        logging.info("filter update %s", self._name)

    def pull_writer(self, seqid, iprot, oprot):
        future = gen.Future()
        future.set_result(True)
        return future

    def push(self, collection_name, exps, log, exp_results):
        if not self._writer:
            return

        for exp in self._exps:
            exp_id = exp.id
            if exp_id not in exp_results or not exp_results[exp_id]:
                return

        result_log = {}
        for key, value in log.iteritems():
            if self._fields:
                if key not in self._fields or not self._fields[key]:
                    continue

            if key in self._formats:
                try:
                    value = self._formats[key].format(value)
                except:
                    continue

            result_log[key] = value

        if result_log:
            self._writer.write(result_log)

    def get_expressions(self):
        return self._exps

    def start_timeout(self):
        if self._timeout:
            IOLoop.current().remove_timeout(self._timeout)
            self._timeout = None

        if self._expried_time:
            self._timeout = IOLoop.current().call_later(self._expried_time, self.on_timeout)
            logging.info("start timeout %s", self._name)

    def on_timeout(self):
        self.close()