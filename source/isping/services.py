# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

from isping.helpers import get_opener, view_in_browser

class ServiceExceptionError(Exception):
    pass

class Services(object):

    def __init__(self, services_url):
        self.services_url = services_url
        self.opener = get_opener()

    def request(self, service, rtype, **kw):
        params = urllib.urlencode(kw)
        url = self.services_url + service + '/'
        try:
            if rtype == 'POST':
                data = self.opener.open(url, params).read()
            else:
                data = self.opener.open(url + '?' + params).read()
        except urllib2.HTTPError, e:
            view_in_browser(e.read())
            raise

        response = json.loads(data)
        if not response['status']:
            raise ServiceExceptionError(response)
        return response['data']

    def get(self, service, **kw):
        return self.request(service, 'GET', **kw)

    def post(self, service, **kw):
        return self.request(service, 'POST', **kw)

