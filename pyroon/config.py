# -*- coding: utf-8 -*-

"""
pyroon.config
~~~~~~~~~~~~~~~
Loads library configuration e.g. Reddit username/password
"""

import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

def getRedditAuth():
    return dict(Config.items('Reddit'))
