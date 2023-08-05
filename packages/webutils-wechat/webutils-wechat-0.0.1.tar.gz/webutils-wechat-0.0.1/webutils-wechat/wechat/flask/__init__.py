# -*- coding: utf-8 -*-

from ..adaptors import UserAdaptor, QrcodeAdaptor
from .adaptors import FlaskAccessTokenAdaptor


class Wechat(object):
    registering_adaptors = (
        FlaskAccessTokenAdaptor,
        UserAdaptor,
        QrcodeAdaptor,
    )

    def __init__(self, app=None):
        self.app = None
        self.redis = None
        self.http_client = None

        self.wxapp_id = None
        self.wxapp_secret = None

        self.adaptors = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.redis = app.redis
        self.http_client = app.http_client

        self.wxapp_id = app.config['WXAPP_ID']
        self.wxapp_secret = app.config['WXAPP_SECRET']

        self.app = app
        app.wechat = self

        self.register_adaptor()

    def register_adaptor(self):
        for adaptor in self.registering_adaptors:
            self.adaptors[adaptor.name] = adaptor(self)

    @property
    def access_token(self):
        return self.adaptors['access_token'].access_token

    def decrypt_user_info(self, session_key, iv, encrypted):
        return self.adaptors['user'].decrypt(session_key, iv, encrypted)

    def code_to_session_info(self, code):
        return self.adaptors['user'].code_to_session_info(code)

    def get_wechat_qrcode(self, scene_data, page=None, data=None):
        return self.adaptors['qrcode'].get_wechat_qrcode(self, scene_data, page, data)
