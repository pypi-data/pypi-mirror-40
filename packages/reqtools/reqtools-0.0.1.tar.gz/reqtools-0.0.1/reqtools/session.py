# -*- coding: utf-8 -*-

import os
import json
import logging
from urllib.parse import urljoin

from requests import Session


logger = logging.getLogger(__name__)


class RemoteApiSession(Session):

    def __init__(self, base_url: str = None, prefix: str = None):
        super(RemoteApiSession, self).__init__()

        self._base_url = base_url
        self._prefix = prefix

    def __repr__(self):
        if self._prefix:
            url = urljoin(self._base_url, self._prefix)
        else:
            url = self._base_url

        return f'{self.__class__.__name__}({url})'

    def _build_url(self, url_path: str):
        if self._prefix:
            url_path = os.path.join(self._prefix, url_path)

        return urljoin(self._base_url, url_path)

    def request(self, method, url_path, **kwargs):
        url = self._build_url(url_path)
        logger.info(f'Performing "{method}" request to "{url}"')

        if kwargs:
            for k, v in kwargs.items():
                if v is not None:
                    message = json.dumps(v, ensure_ascii=False, indent=4)
                    logger.info(f'Request param "{k}": {message}')

        resp = super(RemoteApiSession, self).request(method, url, **kwargs)
        logger.info(f'Response status code is "{resp.status_code}"')

        try:
            message = json.dumps(resp.json(), ensure_ascii=False, indent=4)
            logger.info('\n' + message)
        except ValueError:
            logger.info("\n" + resp.text)

        headers = json.dumps({k: v for k, v in resp.headers.items()})
        logger.info(f'Headers: {headers}')

        total_seconds = resp.elapsed.total_seconds()
        logger.info(f'Response time is "{total_seconds}" seconds')

        return resp
