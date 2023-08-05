# -*- coding: utf-8 -*-

from functools import wraps
import logging
import traceback

from flask import has_request_context, _request_ctx_stack, current_app, request
from werkzeug.local import LocalProxy
from werkzeug.utils import import_string
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature, BadTimeSignature

from flask_restplus import reqparse, Resource

from ...exceptions import AuthException

logger = logging.getLogger(__name__)

current_user = LocalProxy(lambda: _get_user())


class Auth(object):
    def __init__(self, app=None):
        self.app = None

        self.secret_key = None
        self.session_expiration = None
        self.serializer = None

        self.user_cls = None
        self.admin_cls = None

        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'Authorization',
            location='headers',
            dest='token',
            required=True,
            help='Missing session token data',
        )

        self.wechat = None

        self.redis = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.secret_key = app.config['SECRET_KEY']
        self.session_expiration = app.config['SESSION_EXPIRATION']
        logger.info('Set serializer expiration: %s', self.session_expiration)

        self.serializer = TimedJSONWebSignatureSerializer(
            self.secret_key,
            self.session_expiration,
        )

        self.user_cls = import_string(
            app.config.setdefault('AUTH_USER_CLASS', 'models.User')
        )
        self.admin_cls = import_string(
            app.config.setdefault('AUTH_ADMIN_CLASS', 'models.Admin')
        )

        self.wechat = app.wechat
        self.redis = app.redis

        self.app = app
        app.auth = self

    def _get_wx_session_info(self, code):
        try:
            session_info = self.wechat.code_to_session_info(code=code)
        except:
            logger.error(
                'Exchange session key FAILED. %s Err: %s',
                code,
                traceback.format_exc(),
            )
            raise AuthException(
                errcode=981201,
            )
        else:
            logger.debug('Retrieved user info %s -> %s', code, session_info)
        return session_info

    def login(self, code=None, username=None, password=None):
        if not code and not username and not password:
            logger.warning('Missing login credentials, EXIT')
            raise AuthException(
                errcode=981101,
            )
        if code is not None:
            session_info = self._get_wx_session_info(code)
            user = self.user_cls.login(session_info)
            try:
                user_type = user.user_type or 'wechat'
            except:
                user_type = 'wechat'
            token = self.serializer.dumps({
                'uid': user.id_,
                'user_type': user_type,
                'openid': user.openid,
                'site': 'annualReport'
            }).decode('utf8')
        else:
            user = self.admin_cls.login(username, password)
            try:
                user_type = user.user_type or 'admin'
            except:
                user_type = 'admin'
            token = self.serializer.dumps({
                'uid': user.id_,
                'user_type': user_type,
                'site': 'annualReport',
            }).decode('utf8')
        logger.debug(
            'Generated token. code: %s username: %s token: %s',
            code,
            username,
            token,
        )
        self.redis.login_user(user, user_type)
        return user, token

    def verify_session_token(self, token):
        try:
            data = self.serializer.loads(token)
        except SignatureExpired:
            logger.info(
                'Token expired for %s',
                token,
            )
            raise AuthException(
                errcode=981102,
            )
        except (BadSignature, BadTimeSignature):
            logger.info(
                'Token data corrupted: %s',
                token,
            )
            raise AuthException(
                errcode=981103,
            )
        logger.debug('Deserialized user token: %s -> %s', token, data)
        return self._get_user_from_token(data)

    def _get_user_from_token(self, data):
        user_type = data.get('user_type')
        uid = data.get('openid') or data.get('uid')
        site = data.get('site')

        if not uid:
            raise AuthException(
                errcode=981104,
            )
        user_info = self.redis.load_user(uid, user_type)

        if user_type in ('wechat',):
            if user_info is not None and isinstance(user_info, dict):
                user = self.user_cls.get_proxy(**user_info)
                if user is not None:
                    user.login_type = 'wechat'
                    logger.debug('Loaded wechat user proxy for %s', uid)
                    return user
                logger.error(
                    'Getting wechat user proxy failed, trying loading from db %s',
                    uid,
                )

            user = self.user_cls.query.filter(self.user_cls.openid == uid).first()
            if user is None:
                raise AuthException(
                    errcode=981203,
                    params={
                        'uid': uid,
                        'user_type': user_type,
                    }
                )
            else:
                user.login_type = 'wechat'
                self.redis.login_user(user, user_type)
        elif user_type == 'admin':
            if user_info is not None and isinstance(user_info, dict):
                admin = self.admin_cls.get_proxy(**user_info)
                if admin is not None:
                    admin.login_type = 'admin'
                    logger.debug('Loaded admin proxy for %s', uid)
                    return admin
                logger.error(
                    'Getting admin proxy failed, trying loading from db %s',
                    uid,
                )

            user = self.admin_cls.query.filter(self.admin_cls.id_ == uid).first()
            if user is None:
                raise AuthException(
                    errcode=981305,
                    params={
                        'uid': uid,
                        'user_type': user_type,
                    },
                )
            else:
                user.login_type = 'admin'
                self.redis.login_user(user, user_type)
        else:
            raise AuthException(
                errcode=981105,
                params={
                    'user_type': user_type,
                }
            )

        return user


def _get_user():
    if has_request_context() and hasattr(_request_ctx_stack.top, 'user'):
        return getattr(_request_ctx_stack.top, 'user')

    try:
        try:
            args = current_app.auth.parser.parse_args()
        except:
            logger.error(
                'Parsing headers error, headers(auth): %s Err: %s',
                request.headers.get('authorization'),
                traceback.format_exc(),
            )
            raise AuthException(
                errcode=981106,
            )
        token = args.get('token')
        try:
            _, token = token.split(' ')
        except:
            logger.error(
                'Token format error %s Err: 5s',
                token,
                traceback.format_exc(),
            )
            raise AuthException(
                errcode=981107,
            )
        else:
            logger.debug('Retrieved user token from header: %s', token)

        user = current_app.auth.verify_session_token(token)
    except AuthException:
        raise

    setattr(_request_ctx_stack.top, 'user', user)
    return user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            raise AuthException(
                errcode=981401,
            )
        return func(*args, **kwargs)
    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user._get_current_object()
        return func(*args, **kwargs)
    return wrapper


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
