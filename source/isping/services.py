# -*- coding: utf-8 -*-
import urllib
import json

from isping.helpers import get_opener

class ServiceExceptionError(Exception):
    pass

class Services(object):

    URL = 'http://localhost:8000/services/'

    def __init__(self):
        self.opener = get_opener()

    def request(self, service, rtype, **kw):
        params = urllib.urlencode(kw)
        url = Services.URL + service + '/'
        if rtype == 'POST':
            data = self.opener.open(url, params).read()
        else:
            data = self.opener.open(url + '?' + params).read()
        response = json.loads(data)
        if not response['status']:
            raise ServiceExceptionError(response)
        return response['data']

    def get(self, service, **kw):
        return self.request(service, 'GET', **kw)

    def post(self, service, **kw):
        return self.request(service, 'POST', **kw)

