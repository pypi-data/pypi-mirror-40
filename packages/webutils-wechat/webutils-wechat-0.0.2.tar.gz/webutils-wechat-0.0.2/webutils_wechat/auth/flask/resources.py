# -*- coding: utf-8 -*-

from flask import current_app
from flask_restplus import Resource, reqparse

from .adaptor import current_user, admin_required, login_required


class BaseResource(Resource):
    def __init__(self, *args, **kwargs):
        from application import db
        super().__init__(*args, **kwargs)
        self.parser = reqparse.RequestParser()
        self.app = current_app
        self.user = current_user
        self.db = db


class AdminResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_decorators = [admin_required]


class LoggedInUserResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_decorators = [login_required]
