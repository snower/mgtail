# -*- coding: utf-8 -*-
# 15/5/6
# create by: snower

import logging
import traceback
from bson.objectid import ObjectId
from tornado import gen
from tornado.ioloop import IOLoop
import motor
from . import config

class Collection(object):
    _clients = {}

    def __init__(self, name_or_url, manager):
        self._mongo_url = config.get("MONGO_URL", "127.0.0.1")
        self._name = name_or_url
        self._db = None
        self._collection = None
        self._exps = {}
        self._filters = {}
        self._manager = manager
        self._last_log_id = None
        self._stoped = False

    @property
    def name(self):
        return self._name

    async def start(self):
        IOLoop.current().add_future(self.loop())

    async def stop(self):
        self._stoped = True

    def store_session(self):
        if self._last_log_id:
            return {
                "last_log_id": str(self._last_log_id)
            }
        return {}

    def load_session(self, session):
        self._last_log_id = session.get("last_log_id")
        if self._last_log_id:
            try:
                self._last_log_id = ObjectId(self._last_log_id)
            except:
                self._last_log_id = None

    def register_filter(self, filter):
        self._filters[filter.name] = filter
        self.build_exps()

    def unregister_filter(self, filter):
        if filter.name not in self._filters:
            del self._filters[filter.name]
            self.build_exps()

    def build_exps(self):
        self._exps = {}
        for _, filter in self._filters.items():
            for exp in filter.get_expressions():
                self._exps[exp.id] = exp

    def format(self, log, pkey=""):
        result = {}
        for key, value in log.items():
            if isinstance(value, dict):
                result.update(self.format(value, "%s." % key))
            else:
                result[pkey + key] = value
        return result

    async def loop(self):
        logging.info("collection %s %s %s %s loop start", self._name, self._db_name, self._collection, self._last_log_id)
        try:
            if not self._last_log_id:
                last_log = list((await self.db[self._db_name][self._collection].find().sort("_id", -1).limit(1).to_list(None)))[0]
                if last_log:
                    self._last_log_id = last_log["_id"]

            if self._last_log_id:
                cursor = self.db[self._db_name][self._collection].find({"_id": {"$gt": ObjectId(self._last_log_id)}}, tailable=True, await_data=True)
            else:
                cursor = self.db[self._db_name][self._collection].find({}, tailable=True, await_data=True)

            await cursor.fetch_next
            log = cursor.next_object()

            logging.info("collection %s %s %s %s started", self._name, self._db_name, self._collection, self._last_log_id)
            while cursor.alive:
                try:
                    if self._stoped:
                        break

                    if log:
                        self._last_log_id = log["_id"]
                        log = self.format(log)
                        exp_results = {}
                        for exp_id, exp in self._exps.items():
                            exp_results[exp_id] = exp.execute(log)

                        for _, filter in self._filters.items():
                            filter.push(self, self._exps, log, exp_results)

                    await cursor.fetch_next
                    log = cursor.next_object()
                except StopIteration:
                    break
                except Exception as e:
                    logging.info("collection handler log error %s\n%s", e, traceback.format_exc())
        except Exception as e:
            logging.error("collection loop error %s\n%s", e, traceback.format_exc())

        if not self._stoped:
            self._manager.store_session()
            IOLoop.current().call_later(15, lambda : IOLoop.current().add_future(self.loop()))