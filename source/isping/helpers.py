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

def get_provider_module(provider):
    module = 'providers.' + provider

    # This is done so that variables in the scope of the provider module are
    # cleared. This is a paranoid safety precaution so that variables from
    # previous uses of the module are not left over.
    if module in sys.modules:
        del(sys.modules[module])

    provider = __import__(module, None, None, ['*'])
    return provider

