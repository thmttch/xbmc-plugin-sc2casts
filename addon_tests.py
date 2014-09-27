#!/usr/bin/env python

#from sc2casts_parser import *
from sc2castsclient import *
import json
from pprint import *
from xbmcswift2 import Plugin

parser = Sc2CastsParser()
client = Sc2CastsClient()
TEST_DATA_DIR = 'tests'

# test cases:

def test_recent_casts():
    actual = client.series()

    pprint(actual)

    assert len(actual) > 0

'''
def test_show_casts():
    actual = client.series()

    assert len(actual) > 0
'''
