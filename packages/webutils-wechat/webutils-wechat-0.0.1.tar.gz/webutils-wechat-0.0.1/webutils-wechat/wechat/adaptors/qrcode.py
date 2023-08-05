# -*- coding: utf-8 -*-

import logging
import traceback

from ...exceptions import BaseAppException, UtilsException
from .base import BaseAdaptor

logger = logging.getLogger(__name__)


class QrcodeAdaptor(BaseAdaptor):
    name = 'qrcode'
    qrcode_url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.qrcode_allowed_char = "!#$&'()*+,/:;=?@-._~" \
                                   + ''.join(chr(ord('a') + i) for i in range(26)) \
                                   + ''.join(chr(ord('A') + i) for i in range(26)) \
                                   + ''.join(str(i) for i in range(10))

    @property
    def access_token(self):
        return self.wrapper.access_token

    def get_wechat_qrcode(self, scene_data, page=None, data=None):
        try:
            if isinstance(scene_data, dict):
                scene_data = ['='.join((k, str(v))) for k, v in scene_data.items()]
                scene = ','.join(scene_data)
            else:
                scene = str(scene_data)
            for i in scene:
                if i not in self.qrcode_allowed_char:
                    logger.error(
                        'Illegal char. EXIT. %s',
                        scene,
                    )
                    raise UtilsException(
                        params={
                            'scene': scene,
                        },
                        errcode=992301,
                    )

            try:
                access_token = self.access_token
            except BaseAppException:
                logger.error(
                    'Retrieving access token failed. EXIT.'
                )
                raise UtilsException(
                    errcode=992302,
                )
            params = {
                'access_token': access_token,
            }
            data = data or {}
            data.update(scene=scene)
            if page:
                data.update(page=page)

            ret = self.http_client.post(
                self.qrcode_url,
                json_payload=data,
                params=params,
                raw=True
            )
            try:
                error = ret.json()
            except:
                pass
            else:
                logger.error(
                    'Wechat returned error while retrieving share-qrcode. params: %s err_info: %s',
                    params,
                    error,
                )
                raise UtilsException(
                    message=error.get('errmsg'),
                    errcode=992303,
                )
        except BaseAppException:
            raise
        except:
            logger.error(
                'Error while retrieving qrcode from wechat. %s %s %s Err: %s',
                scene_data,
                page,
                data,
                traceback.format_exc(),
            )
            raise UtilsException(
                errcode=992350,
            )
        else:
            return ret.content
