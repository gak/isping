# -*- coding: utf-8 -*-

import urllib
import urllib2

from isping import helpers

# -----------------------------------------------------------------------------
# Provider base class
# -----------------------------------------------------------------------------

class Provider(object):

    def __init__(self, debug=False, debug_view_in_browser=False):
        self.debug = debug
        self.debug_view_in_browser = debug_view_in_browser
        self.opener = helpers.get_opener()

    def set_config_items(self, **d):
        for key, value in d.items():
            self.set_config_item(key, value)

    def set_config_item(self, key, value):
        setattr(self, key, value)

    def get(self, url):
        if self.debug:
            print('-> GET ' + url)
        try:
            return self.opener.open(url).read()
        except urllib2.HTTPError, e:
            if self.debug_view_in_browser:
                helpers.view_in_browser(e.read())
            raise

    def post(self, url, params):
        encoded = urllib.urlencode(params)
        if self.debug:
            print('-> POST ' + url + ' data:' + encoded)
        try:
            return self.opener.open(url, encoded).read()
        except urllib2.HTTPError, e:
            if self.debug_view_in_browser:
                helpers.view_in_browser(e.read())
            raise


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

class Setting(object):

    def __init__(self, name, is_required=False, is_password=False):
        self.name = name
        self.is_required = is_required
        self.is_password = is_password
   
    def __str__(self):
        return self.name


class UserName(Setting):

    def __init__(self):
        Setting.__init__(self, 'username', is_required=True)


class Password(Setting):

    def __init__(self):
        Setting.__init__(self, 'password', is_required=True, is_password=True)
    
    
