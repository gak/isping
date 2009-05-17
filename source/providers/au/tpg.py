# -*- coding: utf-8 -*-

import urllib

from isping import helpers
from isping.exceptions import InvalidCredentialsException

name = 'TPG Internet'
url = 'http://tpg.com.au'
account_url = 'https://cyberstore.tpg.com.au/your_account/index.php'

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
#        'Submit': 'GO!',
    })
    html = opener.open(account_url, args).read()
    if html.find('Invalid') != -1:
        raise InvalidCredentialsException()

    # Fetch usage page
    html = opener.open(account_url + '?function=checkaccountusage').read()
    helpers.view_in_browser(html)

