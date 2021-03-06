#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class FilterExpression(object):
    """
    Attributes:
     - name
     - exp
     - vtype
     - value

    """


    def __init__(self, name=None, exp="=", vtype="string", value="",):
        self.name = name
        self.exp = exp
        self.vtype = vtype
        self.value = value

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.exp = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.vtype = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.value = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('FilterExpression')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.exp is not None:
            oprot.writeFieldBegin('exp', TType.STRING, 2)
            oprot.writeString(self.exp.encode('utf-8') if sys.version_info[0] == 2 else self.exp)
            oprot.writeFieldEnd()
        if self.vtype is not None:
            oprot.writeFieldBegin('vtype', TType.STRING, 3)
            oprot.writeString(self.vtype.encode('utf-8') if sys.version_info[0] == 2 else self.vtype)
            oprot.writeFieldEnd()
        if self.value is not None:
            oprot.writeFieldBegin('value', TType.STRING, 4)
            oprot.writeString(self.value.encode('utf-8') if sys.version_info[0] == 2 else self.value)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Filter(object):
    """
    Attributes:
     - collection
     - name
     - exps
     - fields
     - formats
     - max_queue_size
     - expried_time

    """


    def __init__(self, collection=None, name=None, exps=None, fields={
    }, formats={
    }, max_queue_size=67108864, expried_time=3600,):
        self.collection = collection
        self.name = name
        self.exps = exps
        if fields is self.thrift_spec[4][4]:
            fields = {
            }
        self.fields = fields
        if formats is self.thrift_spec[5][4]:
            formats = {
            }
        self.formats = formats
        self.max_queue_size = max_queue_size
        self.expried_time = expried_time

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.collection = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.LIST:
                    self.exps = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = FilterExpression()
                        _elem5.read(iprot)
                        self.exps.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.MAP:
                    self.fields = {}
                    (_ktype7, _vtype8, _size6) = iprot.readMapBegin()
                    for _i10 in range(_size6):
                        _key11 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val12 = iprot.readByte()
                        self.fields[_key11] = _val12
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.MAP:
                    self.formats = {}
                    (_ktype14, _vtype15, _size13) = iprot.readMapBegin()
                    for _i17 in range(_size13):
                        _key18 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val19 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.formats[_key18] = _val19
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.I32:
                    self.max_queue_size = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.I32:
                    self.expried_time = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Filter')
        if self.collection is not None:
            oprot.writeFieldBegin('collection', TType.STRING, 1)
            oprot.writeString(self.collection.encode('utf-8') if sys.version_info[0] == 2 else self.collection)
            oprot.writeFieldEnd()
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 2)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.exps is not None:
            oprot.writeFieldBegin('exps', TType.LIST, 3)
            oprot.writeListBegin(TType.STRUCT, len(self.exps))
            for iter20 in self.exps:
                iter20.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.fields is not None:
            oprot.writeFieldBegin('fields', TType.MAP, 4)
            oprot.writeMapBegin(TType.STRING, TType.BYTE, len(self.fields))
            for kiter21, viter22 in self.fields.items():
                oprot.writeString(kiter21.encode('utf-8') if sys.version_info[0] == 2 else kiter21)
                oprot.writeByte(viter22)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.formats is not None:
            oprot.writeFieldBegin('formats', TType.MAP, 5)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.formats))
            for kiter23, viter24 in self.formats.items():
                oprot.writeString(kiter23.encode('utf-8') if sys.version_info[0] == 2 else kiter23)
                oprot.writeString(viter24.encode('utf-8') if sys.version_info[0] == 2 else viter24)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.max_queue_size is not None:
            oprot.writeFieldBegin('max_queue_size', TType.I32, 6)
            oprot.writeI32(self.max_queue_size)
            oprot.writeFieldEnd()
        if self.expried_time is not None:
            oprot.writeFieldBegin('expried_time', TType.I32, 7)
            oprot.writeI32(self.expried_time)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class FilterResult(object):
    """
    Attributes:
     - result
     - msg

    """


    def __init__(self, result=0, msg="",):
        self.result = result
        self.msg = msg

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.BYTE:
                    self.result = iprot.readByte()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.msg = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('FilterResult')
        if self.result is not None:
            oprot.writeFieldBegin('result', TType.BYTE, 1)
            oprot.writeByte(self.result)
            oprot.writeFieldEnd()
        if self.msg is not None:
            oprot.writeFieldBegin('msg', TType.STRING, 2)
            oprot.writeString(self.msg.encode('utf-8') if sys.version_info[0] == 2 else self.msg)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Log(object):
    """
    Attributes:
     - collection
     - name
     - log

    """


    def __init__(self, collection=None, name=None, log=None,):
        self.collection = collection
        self.name = name
        self.log = log

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.collection = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.log = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Log')
        if self.collection is not None:
            oprot.writeFieldBegin('collection', TType.STRING, 1)
            oprot.writeString(self.collection.encode('utf-8') if sys.version_info[0] == 2 else self.collection)
            oprot.writeFieldEnd()
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 2)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.log is not None:
            oprot.writeFieldBegin('log', TType.STRING, 3)
            oprot.writeString(self.log.encode('utf-8') if sys.version_info[0] == 2 else self.log)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(FilterExpression)
FilterExpression.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'name', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'exp', 'UTF8', "=", ),  # 2
    (3, TType.STRING, 'vtype', 'UTF8', "string", ),  # 3
    (4, TType.STRING, 'value', 'UTF8', "", ),  # 4
)
all_structs.append(Filter)
Filter.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'collection', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'name', 'UTF8', None, ),  # 2
    (3, TType.LIST, 'exps', (TType.STRUCT, [FilterExpression, None], False), None, ),  # 3
    (4, TType.MAP, 'fields', (TType.STRING, 'UTF8', TType.BYTE, None, False), {
    }, ),  # 4
    (5, TType.MAP, 'formats', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), {
    }, ),  # 5
    (6, TType.I32, 'max_queue_size', None, 67108864, ),  # 6
    (7, TType.I32, 'expried_time', None, 3600, ),  # 7
)
all_structs.append(FilterResult)
FilterResult.thrift_spec = (
    None,  # 0
    (1, TType.BYTE, 'result', None, 0, ),  # 1
    (2, TType.STRING, 'msg', 'UTF8', "", ),  # 2
)
all_structs.append(Log)
Log.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'collection', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'name', 'UTF8', None, ),  # 2
    (3, TType.STRING, 'log', 'UTF8', None, ),  # 3
)
fix_spec(all_structs)
del all_structs
