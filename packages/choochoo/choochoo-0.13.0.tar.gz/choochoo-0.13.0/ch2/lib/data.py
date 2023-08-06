
from binascii import hexlify
from collections import namedtuple
from re import sub


class WarnDict(dict):

    def __init__(self, log, msg):
        self.__log = log
        self.__msg = msg
        super().__init__()

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            msg = self.__msg % (item,)
            self.__log.debug(msg)
            raise KeyError(msg)


class WarnList(list):

    def __init__(self, log, msg):
        self.__log = log
        self.__msg = msg
        super().__init__()

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except IndexError:
            msg = self.__msg % item
            self.__log.debug(msg)
            raise IndexError(msg)


def tohex(data):
    return hexlify(data).decode('ascii')


def assert_attr(instance, *attrs):
    for attr in attrs:
        if getattr(instance, attr) is None:
            raise Exception('No %s defined' % attr)


def dict_to_attr(_rename=False, **kargs):
    if _rename:
        kargs = dict((sub(r' ', '_', name), value) for name, value in kargs.items())
    return namedtuple('Attr', kargs.keys())(**kargs)


class AttrDict(dict):

    def __init__(self, *args, none=False, **kargs):
        self.__none = none
        super().__init__(*args, **kargs)

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattr__(name)
        else:
            try:
                return self[name]
            except KeyError:
                if self.__none:
                    return None
                else:
                    raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def _to_dict(self):
        return self.__dict__
