#!/usr/bin/env python

#from sc2casts_parser import *
#from sc2castsclient import *
#import json

from xbmcswift2 import Plugin
from addon import *

from pprint import *

#parser = Sc2CastsParser()
#client = Sc2CastsClient()
#TEST_DATA_DIR = 'tests'

# test cases:

def test_menu():
    actual = len(main_menu())
    expected = 5
    assert actual == expected, 'Expected {} items, but got {}'.format(expected, actual)

def test_recent_casts():
    actual = len(recent_casts())
    assert actual > 0, 'Expected > 0 items, but got {}'.format(actual)

def test_show_casts():
    actual = len(show_cast('cast16700-WelMu-vs-Ryung-Best-of-3-DreamHack-Stockholm-2014-Group-Stage-3'))
    expected = 3
    assert actual == expected, 'Expected {} games, but got {}'.format(expected, actual)
