# -*- coding: utf-8 -*-
# 17/9/13
# create by: snower

import logging
import json
from tornado.ioloop import IOLoop
from .expression import get_expression
from .format import get_format
from .server.processor.ttypes import FilterExpression, Filter as ThriftFilter
from .filter import Filter
from . import config

class Manager(object):
    _instance = None

    def __init__(self, server):
        self._server = server
        self._filters = {}
        self._collections = {}
        self._expressions = {}
        self._formats = {}
        self._closed = False
        self.__class__._instance = self

    def get_server(self):
        return self._server

    def store_session(self):
        session = {
            "filters": [],
            "collections": {},
            "v": 1
        }

        for name, filter in self._filters.items():
            exps = []
            for exp in filter._origin.exps:
                exps.append({
                    "name": exp.name,
                    "exp": exp.exp,
                    "vtype": exp.vtype,
                    "value": exp.value,
                })

            session["filters"].append({
                "collection": filter._origin.collection,
                "name": filter._origin.name,
                "exps": exps,
                "fields": filter._origin.fields,
                "formats": filter._origin.formats,
                "notify_url": filter._origin.notify_url,
                "max_queue_size": filter._origin.max_queue_size,
                "expried_time": filter._origin.expried_time,
            })

        for name, collection in self._collections.items():
            session["collections"][name] = collection.store_session()

        try:
            with open(config.get("SESSION_PATH", "/tmp") + "/mgtail.session", "w") as fp:
                json.dump(session, fp)
        except Exception as e:
            logging.error("store session error %s", e)
        else:
            logging.info("store session %s", session)

    def load_session(self):
        try:
            with open(config.get("SESSION_PATH", "/tmp") + "/session.json") as fp:
                session = json.load(fp)
                for name, collection_session in session.get("collections", {}).items():
                    if name in self._collections and collection_session:
                        self._collections[name].load_session(collection_session)

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
        for name, collection in self._collections.items():
            collection.stop()
        self._closed = True
        logging.info("manager close")

    def register_filter(self, filter):
        self._filters[filter.name] = filter
        if filter.collection in self._collections:
            self._collections[filter.collection].register_filter(filter)
        logging.info("register filter %s", filter.name)

    def unregister_filter(self, filter):
        if filter.collection in self._collections:
            self._collections[filter.collection].unregister_filter(filter)
        if filter.name in self._filters:
            del self._filters[filter.name]
        logging.info("unregister filter %s", filter.name)

    def get_filter(self, name):
        if name in self._filters:
            return self._filters[name]
        return None

    def register_collection(self, collection):
        self._collections[collection.name] = collection
        logging.info("register collection %s", collection.name)

    def unregister_collection(self, collection):
        if collection.name not in self._collections:
            del self._collections[collection.name]
        logging.info("unregister collection %s", collection.name)

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

    def start(self):
        for collection in self._collections:
            IOLoop.current().add_callback(collection.start)
        self.start_session_store_timeout()

    def start_session_store_timeout(self):
        IOLoop.current().call_later(60, self.on_session_store_timeout)

    def on_session_store_timeout(self):
        if not self._closed:
            self.store_session()
            IOLoop.current().call_later(60, self.on_session_store_timeout)