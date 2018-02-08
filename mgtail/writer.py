# -*- coding: utf-8 -*-
# 17/9/13
# create by: snower

from cStringIO import StringIO
from collections import deque
import json
import logging
import traceback
from tornado import gen
from common.mgtord.notify import notify
from processor.GLogcat import pull_result, TMessageType
from processor.ttypes import Log

class Writer(object):
    def __init__(self, filter, max_buffer_size = 64 * 1024 * 1024):
        self._filter = filter
        self._max_buffer_size = max_buffer_size
        self._buffer = deque()
        self._buffer_size = 0

    def update(self, max_buffer_size):
        self._max_buffer_size = max_buffer_size

    def close(self):
        self._filter = None
        self._buffer.clear()
        self._buffer_size = 0

    def write(self, log):
        pass

class PullWriter(Writer):
    def __init__(self, *args, **kwargs):
        super(PullWriter, self).__init__(*args, **kwargs)

        self._seqid = None
        self._iprot = None
        self._oprot = None

        self._writing = False
        self._stoped = True
        self._result_future = None

        self._otrans = None

    def write(self, log):
        if self._stoped:
            return

        while self._buffer_size > self._max_buffer_size:
            llog = self._buffer.popleft()
            self._buffer_size -= len(llog)

        if not isinstance(log, basestring):
            log = json.dumps(log, default=str, ensure_ascii=False)
        log = Log(self._filter.logging, self._filter.name, log)
        result = pull_result()
        result.success = log
        msg_type = TMessageType.REPLY
        self._oprot.writeMessageBegin("pull", msg_type, self._seqid)
        result.write(self._oprot)
        self._oprot.writeMessageEnd()

        log = self._oprot.trans.getvalue()
        self._oprot.trans = StringIO()

        self._buffer.append(log)
        self._buffer_size += len(log)

        if not self._writing:
            self._writing = True
            self.do_write()

    def pull(self, seqid, iprot, oprot):
        if self._result_future:
            self._oprot.trans = self._otrans
            self._result_future.set_result(True)

        self._seqid = seqid
        self._iprot = iprot
        self._oprot = oprot

        self._writing = False
        self._stoped = False
        self._result_future = gen.Future()

        self._otrans = self._oprot.trans
        self._oprot.trans = StringIO()

        if self._buffer and not self._writing:
            self._writing = True
            self.do_write()

        return self._result_future

    def close(self, result = True):
        if not self._stoped:
            filter = self._filter
            oprot = self._oprot

            if result:
                super(PullWriter, self).close()

            self._seqid = None
            self._iprot = None
            self._oprot = None

            self._writing = False
            self._stoped = True

            oprot.trans = self._otrans
            self._otrans = None
            result_future, self._result_future = self._result_future, None
            result_future.set_result(result)
            if not result:
                filter.start_timeout()
            logging.info("writer close %s", filter.name)

    @gen.coroutine
    def do_write(self):
        while self._buffer:
            log = self._buffer.popleft()
            self._buffer_size -= len(log)
            try:
                yield self._otrans._stream.write(log)
            except:
                self.close(False)
                break

        self._writing = False

class NotifyWriter(Writer):
    def __init__(self, notify_url, *args, **kwargs):
        super(NotifyWriter, self).__init__(*args, **kwargs)

        self._notify_url = notify_url
        self._writing = False

    def write(self, log):
        while self._buffer_size > self._max_buffer_size:
            self._buffer.popleft()
            self._buffer_size -= 1

        self._buffer.append(log)
        self._buffer_size += 1
        if not self._writing:
            self._writing = True
            self.do_write()

    @gen.coroutine
    def do_write(self):
        while self._buffer:
            log = self._buffer.popleft()
            self._buffer_size -= 1
            try:
                yield notify(self._notify_url, **log)
            except Exception as e:
                logging.error("notify error %s %s %s\n%s", self._notify_url, e, log, traceback.format_exc())
                continue

        self._writing = False