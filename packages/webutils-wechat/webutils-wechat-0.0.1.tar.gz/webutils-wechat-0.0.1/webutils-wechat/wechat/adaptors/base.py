# -*- coding: utf-8 -*-


class BaseAdaptor(object):
    name = None

    def __init__(self, wrapper, **kwargs):
        self.wrapper = wrapper
        self.register(**kwargs)

    @property
    def app(self):
        return self.wrapper.app

    @property
    def wxapp_id(self):
        return self.wrapper.wxapp_id

    @property
    def wxapp_secret(self):
        return self.wrapper.wxapp_secret

    @property
    def redis(self):
        return self.wrapper.redis

    @property
    def http_client(self):
        return self.wrapper.http_client

    def register(self, **kwargs):
        # initializing config with wrapper here
        pass
