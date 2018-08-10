# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json


DEFAULT_PORT = 4281
ENCODING = 'utf-8'


class Endpoints():

    USER_TOKENS = "usertokens"


class Client():

    def __init__(self, host=None, port=None):
        if not host:
            host = 'localhost';

        if not port:
            port = DEFAULT_PORT

        self.url = 'http://{}:{}'.format(host, port)

    def _get(self, endpoint, **kwargs):
        url = self.url + '/' + endpoint

        if kwargs:
            url += '?' + urlencode(kwargs)

        req = urlopen(Request(url))
        data = req.read()
        return json.loads(data.decode(ENCODING))

    def get_user_tokens(self, address):
        return self._get(Endpoints.USER_TOKENS, address=address)

