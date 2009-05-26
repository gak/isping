# -*- coding: utf-8 -*-
import re
import urllib

from isping import helpers
from isping.exceptions import InvalidCredentialsException
from providers import *

cls = 'TPG'

PEAK = 0
OFFPEAK = 1

class TPG(Provider):

    name = 'TPG Internet'
    url = 'http://tpg.com.au'

    url = 'https://cyberstore.tpg.com.au/your_account/index.php'
    reo_peak = re.compile(
        'Peak Download used: (?P<peak>[\d\.]+) MB'
        '.*'
        'Off-Peak Download used: (?P<offpeak>[\d\.]+) MB'
    )

    def get_settings(self):
        return [
            UserName(),
            Password(),
        ]

    def get_current_usage(self):

        # Login
        args = {
            'check_username': self.username,
            'password': self.password,
        }
        html = self.post(self.url, args)
        if html.find('Invalid') != -1:
            raise InvalidCredentialsException()

        # Fetch usage page
        html = self.get(self.url + '?function=checkaccountusage')

        # Parse the usage page
        match = self.reo_peak.search(html)
        groups = match.groupdict('peak')

        return {
            PEAK: groups['peak'],
            OFFPEAK: groups['offpeak'],
        }

