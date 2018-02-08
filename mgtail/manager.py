# -*- coding: utf-8 -*-
# 17/9/13
# create by: snower

import logging
import json
from tornado.ioloop import IOLoop
from expression import get_expression
from format import get_format
from processor.ttypes import FilterExpression, Filter as ThriftFilter
from filter import Filter
import settings

class Manager(object):
    _instance = None

    def __init__(self, server):
        self._server = server
        self._filters = {}
        self._loggings = {}
        self._expressions = {}
        self._formats = {}
        self._closed = False
        self.__class__._instance = self

    def get_server(self):
        return self._server

    def store_session(self):
        session = {
            "filters": [],
            "loggings": {},
            "v": 1
        }

        for name, filter in self._filters.iteritems():
            exps = []
            for exp in filter._origin.exps:
                exps.append({
                    "name": exp.name,
                    "exp": exp.exp,
                    "vtype": exp.vtype,
                    "value": exp.value,
                })

            session["filters"].append({
                "logging": filter._origin.logging,
                "name": filter._origin.name,
                "exps": exps,
                "fields": filter._origin.fields,
                "formats": filter._origin.formats,
                "notify_url": filter._origin.notify_url,
                "max_queue_size": filter._origin.max_queue_size,
                "expried_time": filter._origin.expried_time,
            })

        for name, glogging in self._loggings.iteritems():
            session["loggings"][name] = glogging.store_session()

        try:
            with open(settings.SESSION_PATH + "/session.json", "w") as fp:
                json.dump(session, fp)
        except Exception as e:
            logging.error("store session error %s", e)
        else:
            logging.info("store session %s", session)

    def load_session(self):
        try:
            with open(settings.SESSION_PATH + "/session.json") as fp:
                session = json.load(fp)
                for name, glogging_session in session.get("loggings", {}).iteritems():
                    if name in self._loggings and glogging_session:
                        self._loggings[name].load_session(glogging_session)

                for filter in session["filters"]:
                    exps = []
                    for exp in filter["exps"]:
                        exps.append(FilterExpression(**exp))
                    filter["exps"] = exps
                    self.register_filter(Filter(self, ThriftFilter(**filter)))
            logging.info("load session %s", session)
        except Exception as e:
            logging.error("load session error %s", e)

    def close(self):
        for name, glogging in self._loggings.iteritems():
            glogging.stop()
        self._closed = True
        logging.info("manager close")

    def register_filter(self, filter):
        self._filters[filter.name] = filter
        if filter.logging in self._loggings:
            self._loggings[filter.logging].register_filter(filter)
        logging.info("register filter %s", filter.name)

    def unregister_filter(self, filter):
        if filter.logging in self._loggings:
            self._loggings[filter.logging].unregister_filter(filter)
        if filter.name in self._filters:
            del self._filters[filter.name]
        logging.info("unregister filter %s", filter.name)

    def get_filter(self, name):
        if name in self._filters:
            return self._filters[name]
        return None

    def register_logging(self, glogging):
        self._loggings[glogging.name] = glogging
        logging.info("register logging %s", glogging.name)

    def unregister_logging(self, glogging):
        if glogging.name not in self._loggings:
            del self._loggings[glogging.name]
        logging.info("unregister logging %s", glogging.name)

    def get_expression(self, name, exp, vtype, value):
        exp_id = (name, exp, vtype, value).__hash__()
        if exp_id in self._expressions:
            return self._expressions[exp_id]

        exp_class = get_expression(exp)
        if not exp_class:
            return None

        exp = exp_class(exp_id, name, vtype, value)
        self._expressions[exp_id] = exp
        return exp

    def get_format(self, format):
        if format in self._formats:
            return self._formats[format]

        format_class = get_format(format)
        if not format_class:
            return None

        format_instance = format_class(format)
        self._formats[format] = format_instance
        return format_instance

    def start_session_store_timeout(self):
        IOLoop.current().call_later(60, self.on_session_store_timeout)

    def on_session_store_timeout(self):
        if not self._closed:
            self.store_session()
            IOLoop.current().call_later(60, self.on_session_store_timeout)