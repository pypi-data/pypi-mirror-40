from __future__ import absolute_import

from redis import StrictRedis

from . import loader


class Base(object):
    def __init__(self, key):
        self._key = key
        self._redis = None
        
    def __len__(self):
        return None

    def load_script(self, command):
        return loader.load(command)
        
    def connect(self):
        if self._redis is None:
            self._redis = StrictRedis(decode_responses=True)
        return self._redis
    
    def getkey(self):
        return self._key
    
    def setkey(self, key):
        self._key = key

    def expire(self, ttl):
        return self.connect().expire(self._key, ttl)

    def expireat(self, timestamp):
        return self.connect().expireat(self._key, timestamp)

    def pexpire(self, ttl):
        return self.connect().pexpire(self._key, ttl)

    def pexpireat(self, timestamp):
        return self.connect().pexpireat(self._key, timestamp)
    
    def ttl(self):
        return self.connect().ttl(self._key)
    
    def pttl(self):
        return self.connect().pttl(self._key)

    def length(self):
        return self.__len__()

    def destruct(self):
        return self.connect().delete(self._key)

    def _make_members(self, members):
        return members if isinstance(members, list) else [members]

    def _run_lua_script(self, script, keys=(), args=()):
        func = self.connect().register_script(script)
        return func(keys=keys, args=args)
