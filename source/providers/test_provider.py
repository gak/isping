#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import sys

ROOT = path.join(path.abspath(path.dirname(__file__)), '..')
sys.path.insert(0, ROOT)

def main():
    module = 'providers.' + sys.argv[1]
    settings = sys.argv[2::2]
    values = sys.argv[3::2]
    args = dict(zip(settings, values))

    # Load the provider module and populate it with the settings
    provider = __import__(module, globals(), locals(), ['get_usage'])
    provider.set_config(args)

    print provider.get_usage()

if __name__ == '__main__':
    main()

