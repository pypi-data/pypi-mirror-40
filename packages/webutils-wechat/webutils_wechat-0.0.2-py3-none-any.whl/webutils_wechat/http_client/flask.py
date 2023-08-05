# -*- coding: utf-8 -*-

from .base import BaseHttpClient


class FlaskHttpClient(BaseHttpClient):
    def __init__(self, app=None):
        super().__init__()
        self.app = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.http_client = self
