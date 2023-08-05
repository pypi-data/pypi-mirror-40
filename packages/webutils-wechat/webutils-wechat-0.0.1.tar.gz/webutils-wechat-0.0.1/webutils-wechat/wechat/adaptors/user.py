# -*- coding: utf-8 -*-

import base64
import json
import logging
import traceback

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7

from ...exceptions import BaseAppException, UtilsException
from .base import BaseAdaptor

logger = logging.getLogger(__name__)


class UserAdaptor(BaseAdaptor):
    name = 'user'

    jscode2session_url = 'https://api.weixin.qq.com/sns/jscode2session'

    def code_to_session_info(self, code):
        try:
            params = {
                'appid': self.wxapp_id,
                'secret': self.wxapp_secret,
                'grant_type': 'authorization_code',
                'js_code': code,
            }
            ret = self.http_client.get(self.jscode2session_url, params=params)
            errcode = ret.get('errcode')
            if errcode:
                logger.error(
                    'Tencent return error while exchanging code for session_info. code: %s msg: %s',
                    errcode,
                    ret.get('errmsg'),
                )
                raise UtilsException(
                    return_data={
                        'errcode': errcode,
                        'errmsg': ret.get('errmsg'),
                    },
                    errcode=992101,
                )
        except BaseAppException:
            raise
        except:
            logger.error(
                'Error while exchanging code for session_info: %s Err: %s',
                code,
                traceback.format_exc(),
            )
            raise UtilsException(
                errcode=992150,
            )
        return ret

    def decrypt(self, session_key, iv, encrypted):
        try:
            key = base64.b64decode(session_key)
            iv = base64.b64decode(iv)
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend(),
            )
            decryptor = cipher.decryptor()
            plain = decryptor.update(base64.b64decode(encrypted)) + decryptor.finalize()
            unpadder = PKCS7(128).unpadder()
            decrypted = unpadder.update(plain)
            decrypted += unpadder.finalize()
            decrypted = json.loads(decrypted.decode('utf8'))
        except UtilsException:
            raise
        except:
            logger.error(
                'Error while decrypting message(simple): %s Err: %s',
                encrypted,
                traceback.format_exc(),
            )
            raise UtilsException(
                errcode=992250,
            )
        return decrypted
