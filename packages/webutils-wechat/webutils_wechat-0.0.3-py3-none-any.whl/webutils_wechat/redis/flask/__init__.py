# -*- coding: utf-8 -*-

import redis

from ..client import RedisClient


class FlaskRedisClient(RedisClient):
    def __init__(self, app=None):
        super().__init__()

        self.app = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.host = app.config.setdefault('REDIS_HOST', 'localhost')
        self.port = app.config.setdefault('REDIS_PORT', 6379)
        self.db = app.config.setdefault('REDIS_DB', 7)
        self.password = app.config.setdefault('REDIS_PASSWORD', None)

        self.pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
        )
        self.client = redis.StrictRedis(connection_pool=self.pool)

        self.user_expiration = app.config.setdefault('USER_REDIS_EXPIRATION', 60 * 60 * 24 * 2)
        self.user_id_attr_name = app.config.get('USER_ID_ATTR_NAME')
        self.admin_id_attr_name = app.config.get('ADMIN_ID_ATTR_NAME')

        self.app = app
        app.redis = self
        app.redis_cli = self.client
