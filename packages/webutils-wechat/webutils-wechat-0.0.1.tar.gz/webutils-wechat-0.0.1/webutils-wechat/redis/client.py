# -*- coding: utf-8 -*-

import logging
import traceback

import msgpack

from ..exceptions import UtilsException
from .constants import FrontendKeys, WechatAppKeys


logger = logging.getLogger(__name__)


class RedisClient(object):
    def __init__(self):
        self.client = None

        self.host = None
        self.port = None
        self.db = None
        self.password = None
        self.pool = None

        self.user_expiration = None
        self.user_id_attr_name = None
        self.admin_id_attr_name = None

    def _get_user_id(self, user):
        if self.user_id_attr_name:
            return getattr(user, self.user_id_attr_name, None)
        return getattr(user, 'id_', None) or getattr(user, 'id', None) or getattr(user, 'pk', None)

    def _get_admin_id(self, user):
        if self.admin_id_attr_name:
            return getattr(user, self.admin_id_attr_name, None)
        return getattr(user, 'id_', None) or getattr(user, 'id', None) or getattr(user, 'pk', None)

    def login_user(self, user, user_type=None):
        if user_type is None:
            user_type = user.user_type
        if user_type == 'wechat':
            uid = self._get_user_id(user)
        else:
            uid = self._get_admin_id(user)
        try:
            key = FrontendKeys.user.format(user_type, uid)
            payload = msgpack.dumps(user.redis_payload)
            self.client.setex(key, self.user_expiration, payload)
        except:
            logger.error(
                'Persisting user info to redis error, user: %s Err: %s',
                uid,
                traceback.format_exc(),
            )
            return False
        else:
            logger.debug(
                'Persisted user info to redis. user: %s',
                uid,
            )
            return True

    def load_user(self, uid, user_type):
        try:
            key = FrontendKeys.user.format(user_type, uid)
            info = self.client.get(key)
            if info is not None:
                info = msgpack.loads(info, raw=False)
        except:
            logger.error(
                'Loading user info from redis error. user: %s user_type: %s Err: %s',
                uid,
                user_type,
                traceback.format_exc(),
            )
            return None
        else:
            logger.debug(
                "Loaded user info from redis. user: %s %s -> %s",
                uid,
                user_type,
                info,
            )
            return info

    def persist_access_token(self, access_token, expiration):
        try:
            key = WechatAppKeys.access_token
            self.client.setex(key, expiration, access_token)
        except:
            logger.error(
                'Error while persist wechat access token. access_token: %s Err: %s',
                access_token,
                traceback.format_exc(),
            )
            raise UtilsException(
                errcode=992052,
            )

    def load_access_token(self):
        try:
            key = WechatAppKeys.access_token
            access_token = self.client.get(key)
            if access_token is not None:
                access_token = access_token.decode('utf8')
        except:
            logger.error(
                'Error while loading access token from redis: %s',
                traceback.format_exc(),
            )
            raise UtilsException(
                errcode=992051,
            )
        else:
            return access_token
