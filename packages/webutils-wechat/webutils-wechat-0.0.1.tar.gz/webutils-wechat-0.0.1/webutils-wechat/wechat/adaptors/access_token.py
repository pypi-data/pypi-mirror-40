# -*- coding: utf-8 -*-

import logging
import traceback

from ...exceptions import BaseAppException, UtilsException
from .base import BaseAdaptor

logger = logging.getLogger(__name__)


class AccessTokenAdaptor(BaseAdaptor):
    name = 'access_token'
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'

    def __init__(self, wrapper):
        self.access_token_default_expiration = 60 * 60 * 2
        self.access_token_expiration_tolerance = 200

        super().__init__(wrapper)

    @property
    def access_token(self):
        try:
            token = self.redis.load_access_token()
            if token:
                return token
            logger.info('Token may expired, retrieving it from tencent')
            token, expiration = self._get_access_token()
            try:
                self.redis.persist_access_token(token, expiration)
            except:
                pass
        except BaseAppException:
            raise
        except:
            logger.error(
                'Error while retrieving access token: %s',
                traceback.format_exc(),
            )
            raise UtilsException(
                errcode=992050,
            )
        else:
            return token

    def _get_access_token(self):
        params = {
            'grant_type': 'client_credential',
            'appid': self.wxapp_id,
            'secret': self.wxapp_secret,
        }
        ret = self.http_client.get(self.access_token_url, params=params)
        errcode = ret.get('errcode')
        if errcode:
            logger.error(
                'Tencent return error while retrieving access token. code: %s msg: %s',
                errcode,
                ret.get('errmsg'),
            )
            raise UtilsException(
                errcode=992001,
                return_data={
                    'errcode': errcode,
                    'errmsg': ret.get('errmsg'),
                }
            )
        access_token = ret.get('access_token')
        if not access_token:
            raise UtilsException(
                errcode=992002,
            )

        expiration = ret.get('expires_in', self.access_token_default_expiration)
        try:
            expiration = int(expiration)
        except:
            expiration = self.access_token_default_expiration
        expiration -= self.access_token_expiration_tolerance

        return access_token, expiration
