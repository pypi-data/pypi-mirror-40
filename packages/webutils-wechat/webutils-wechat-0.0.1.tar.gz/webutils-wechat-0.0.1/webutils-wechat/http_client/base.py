# -*- coding: utf-8 -*-

import logging
import traceback

import requests

from ..exceptions import UtilsException

logger = logging.getLogger(__name__)


class BaseHttpClient(object):
    def __init__(self):
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def get(self, url, params=None, jsonify=True, binary=False):
        try:
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            if jsonify:
                resp = resp.json()
            elif binary:
                resp = resp.content
            else:
                resp = resp.text
        except:
            logger.error(
                'Error while request(get) url: %s params: %s Err: %s',
                url,
                params,
                traceback.format_exc(),
            )
            raise UtilsException(
                errcode=983050,
                params={
                    'url': url,
                    'params': params,
                }
            )
        return resp

    def post(self, url, data=None, json_payload=None, params=None, headers=None, jsonify=True, raw=False):
        try:
            if headers is None:
                headers = {}
            headers.update(self.session.headers)
            resp = self.session.post(url, data=data, json=json_payload, headers=headers, params=params)
            resp.raise_for_status()
            if raw:
                pass
            elif jsonify:
                resp = resp.json()
            else:
                resp = resp.text
        except:
            logger.error(
                'Error while request(post) url: %s data: %s json: %s params: %s Err: %s',
                url,
                data,
                json_payload,
                params,
                traceback.format_exc()
            )
            raise UtilsException(
                errcode=991150,
                params={
                    'url': url,
                    'data': data,
                    'json': json_payload,
                    'params': params,
                }
            )
        return resp
