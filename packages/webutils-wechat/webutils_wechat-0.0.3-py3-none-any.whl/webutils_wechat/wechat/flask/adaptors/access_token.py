# -*- coding: utf-8 -*-


from ...adaptors import AccessTokenAdaptor


class FlaskAccessTokenAdaptor(AccessTokenAdaptor):
    def register(self, **kwargs):
        self.access_token_default_expiration = self.app.config['TENCENT_ACCESS_TOKEN_DEFAULT_EXPIRATION']
        self.access_token_expiration_tolerance = self.app.config['TENCENT_ACCESS_TOKEN_EXPIRATION_TOLERANCE']
