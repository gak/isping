# -*- coding: utf-8 -*-
import sys
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

def get_provider_instance(provider):
    module = 'providers.' + provider
    provider_mod = __import__(module, None, None, ['*'])
    provider_cls = getattr(provider_mod, provider_mod.cls)
    return provider_cls(debug=True, debug_view_in_browser=True)

