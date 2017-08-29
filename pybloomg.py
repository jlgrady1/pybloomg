from grpc import insecure_channel

from bloom_pb2 import (
    BloomStub,
    FilterRequest,
    KeyRequest,
    ListRequest,
)


class BloomgClient(object):
    def __init__(self, server):
        self.channel = insecure_channel(server)
        self.conn = BloomStub(self.channel)

    def _make_key_request(self, name, keys):
        req = KeyRequest()
        req.Name = name
        for key in keys:
            req.Keys.append(key)
        return req

    def create(self, name):
        req = FilterRequest()
        req.Name = name
        self.conn.CreateFilter(req)

    def list(self):
        req = ListRequest()
        resp = self.conn.ListFilters(req)
        if resp:
            return resp.Names
        return []

    def add(self, name, keys):
        req = KeyRequest()
        req.Name = name
        for key in keys:
            req.Keys.append(key)
        self.conn.Add(req)

    def info(self):
        req = ListRequest()
        resp = self.conn.Info(req)
        if resp:
            return resp.Filters
        return []

    def has(self, name, keys):
        req = self._make_key_request(name, keys)
        resp = self.conn.Has(req)
        if resp:
            return resp.Has
        return []

    def clear(self, name):
        req = FilterRequest()
        req.Name = name
        self.conn.Clear(req)

    def drop(self, name):
        req = FilterRequest()
        req.Name = name
        self.conn.Drop(req)
