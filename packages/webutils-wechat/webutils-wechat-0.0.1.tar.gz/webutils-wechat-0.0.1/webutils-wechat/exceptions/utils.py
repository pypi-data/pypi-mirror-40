# -*- coding: utf-8 -*-

from .base import BaseAppException


class UtilsException(BaseAppException):
    # category
    # utils: 99
    category = 'utils'

    # sub category:
    #   - http.get 10
    #   - http.post 11
    #   - wechat.access_token.retrieving 20
    #   - wechat.user.exchange_code_for_session_info 21
    #   - wechat.user.decryption 22
    #   - wechat.qrcode.generation 23

    co_msg_mapping = {
        991050: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'http.get'
        },
        991150: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'http.post'
        },
        992001: {
            'message': 'Tencent returned error',
            'http_code': 500,
            'sub_category': 'wechat.access_token.retrieving'
        },
        992002: {
            'message': 'Missing access token in tencent returned data',
            'http_code': 400,
            'sub_category': 'wechat.access_token.retrieving'
        },
        992050: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'wechat.access_token.retrieving'
        },
        992051: {
            # loading access token from redis
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'wechat.access_token.retrieving'
        },
        992052: {
            # persisting access token from redis
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'wechat.access_token.retrieving'
        },
        992101: {
            'message': 'Wechat returns error',
            'http_code': 500,
            'sub_category': 'wechat.user.exchange_code_for_session_info',
        },
        992150: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'wechat.user.exchange_code_for_session_info',
        },
        992250: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'wechat.user.decryption',
        },
        992301: {
            'message': 'Illegal char in scene',
            'http_code': 400,
            'sub_category': 'wechat.qrcode.generation',
        },
        992302: {
            'message': 'Retrieving access token failed',
            'http_code': 400,
            'sub_category': 'wechat.qrcode.generation',
        },
        992303: {
            'message': 'Wechat returns error',
            'http_code': 400,
            'sub_category': 'wechat.qrcode.generation',
        },
        992350: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'wechat.qrcode.generation',
        },
    }
