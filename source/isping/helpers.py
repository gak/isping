# -*- coding: utf-8 -*-

import cookielib
import urllib2

def get_opener():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    return opener

def view_in_browser(html):
    import webbrowser
    open('tmp.html', 'wb').write(html)
    webbrowser.open('tmp.html')

def get_provider_module(provider):
    module = 'providers.' + provider
    provider = __import__(module, globals(), locals(), ['get_usage'])
    return provider

