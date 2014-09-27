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
    actual = main_menu()

    pprint(actual)

    assert len(actual) == 2


def test_recent_casts():
    actual = recent_casts()

    pprint(actual)

    assert len(actual) > 0

'''
def test_show_casts():
    actual = client.series()

    assert len(actual) > 0
'''
