#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import sys

ROOT = path.join(path.abspath(path.dirname(__file__)), '..')
sys.path.insert(0, ROOT)

from isping import helpers

def main():
    settings = sys.argv[2::2]
    values = sys.argv[3::2]
    args = dict(zip(settings, values))

    # Load the provider module and populate it with the settings
    provider = helpers.get_provider_instance(sys.argv[1])
    provider.set_config_items(**args)

    print provider.get_current_usage()

if __name__ == '__main__':
    main()

