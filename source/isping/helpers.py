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
