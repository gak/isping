# -*- coding: utf-8 -*-
import re
import urllib
import urllib2

from isping import helpers
from isping.exceptions import InvalidCredentialsException
from providers import *

cls = 'Optus'

GENERAL = 0

# XXX: This is hardcoded to just phones, I don't know how other services work

class Optus(Provider):

    name = 'Optus'

    url = 'https://my.optus.com.au/'

    re_homepage = re.compile(r'SMAGENTNAME=([^&]*)')
    re_usage = re.compile(
        r'Data - Mobile Internet</td>'
        r'<td class="blue1">([\d\.]+)'
    )

    def get_settings(self):
        return [
            UserName(),
            Password(),
            Setting('phone_number')
        ]

    def get_current_usage(self):
        opener = helpers.get_opener()

        # Home page
        # Loading this page because we need a "SMAGENTNAME" variable which
        # looks to be a cookie that is in the URI.
        html = self.get(self.url)
        match = Optus.re_homepage.search(html)
        smagentname = match.group(1)

        # Login
        url = self.url + 'signon/Optus/login_ext.sec'
        args = {
            'USER': self.username,
            'PASSWORD': self.password,
            'SMENC': 'ISO-8859-1',
            'SMLOCALE': 'US-EN',
            'target': 'HTTPS://my.optus.com.au/web/oscportal.portal?site=personal',
            'smauthreason': '0',
            'smagentname': smagentname,
            'postpreservationdata': '',
        }
        html = self.post(url, args)
        if html.find('Please verify your User Name') != -1:
            raise InvalidCredentialsException()

        # Fetch usage page
        url = self.url + 'web/oscportal.portal?_nfpb=true&' + \
            '_pageLabel=deeplink_myusage_postpaid&site=personal&' + \
            'pageName=unbilledUsage&virAcctNum=' + self.phone_number
        html = self.get(url)
        match = Optus.re_usage.search(html)
        usage = match.group(1)
        helpers.view_in_browser(html)

        # Parse the usage page

        return {
            GENERAL: usage,
        }

