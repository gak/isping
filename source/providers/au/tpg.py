# -*- coding: utf-8 -*-
import re
import urllib

from isping import helpers
from isping.exceptions import InvalidCredentialsException

name = 'TPG Internet'
url = 'http://tpg.com.au'

account_url = 'https://cyberstore.tpg.com.au/your_account/index.php'

reo_peak = re.compile(
    'Peak Download used: (?P<peak>[\d\.]+) MB'
    '.*'
    'Off-Peak Download used: (?P<offpeak>[\d\.]+) MB'
)

def periods():
    return [
        'Peak',
        'Off-peak'
    ]

def settings():
    return [
        'username',
        'password',
        ]

def get_usage():
    opener = helpers.get_opener()

    # Login
    args = urllib.urlencode({
        'check_username': username,
        'password': password,
    })
    html = opener.open(account_url, args).read()
    if html.find('Invalid') != -1:
        raise InvalidCredentialsException()

    # Fetch usage page
    html = opener.open(account_url + '?function=checkaccountusage').read()
#    helpers.view_in_browser(html)

    # Parse the usage page
    match = reo_peak.search(html)
    groups = match.groupdict('peak')

    return [
        groups['peak'],
        groups['offpeak']
    ]
