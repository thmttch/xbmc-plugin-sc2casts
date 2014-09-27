#!/usr/bin/env python

#from sc2casts_parser import *
from sc2castsclient import *
import json
from pprint import *

parser = Sc2CastsParser()
client = Sc2CastsClient()
TEST_DATA_DIR = 'tests'

# test cases:

def test_titles():
    pass

# test cases:

def test_casts():
    with open(TEST_DATA_DIR + '/all', 'r') as f:
        test_data = f.read()
        #print test_data

    #actual = parser.casts(test_data)
    actual = parser._parse_index(test_data)
    pprint(actual)

    # TODO check each cast

# test cases:
# bo3 in 1 game
# 1 game
# 3 games
# 5 games

def test_games_bo3_in_1_game():
    with open(TEST_DATA_DIR + '/cast14719-Soulkey-vs-Cure-Best-of-3-All-in-1-video-IEM-Cologne-2014-Korean-Qualifier', 'r') as f:
        test_data = f.read()
        #print test_data

    #actual = parser.games(test_data)
    actual = parser._parse_series_page(test_data)

    assert len(actual) == 1

    assert actual[0]['game_id'] == 'Gt4E3rIUhoA'
    assert actual[0]['game_title'] == 'Game 1'

# games 4 and 5 not played
def test_games_5_games():
    with open(TEST_DATA_DIR + '/cast14705-KT-Rolster-vs-Prime-Best-of-5-2014-Proleague-Round-1', 'r') as f:
        test_data = f.read()
        #print test_data

    #actual = parser.games(test_data)
    actual = parser._parse_series_page(test_data)

    print actual
    assert len(actual) == 5

    assert actual[0]['game_id'] == 'QqSRtBVEXDs'
    assert actual[0]['game_title'] == 'Game 1'

    assert actual[1]['game_id'] == '5lFLuOKYTa8'
    assert actual[1]['game_title'] == 'Game 2'

    assert actual[2]['game_id'] == 'wNhcT-NenNs'
    assert actual[2]['game_title'] == 'Game 3'

    assert actual[3]['game_id'] == ''
    assert actual[3]['game_title'] == 'Game 4'

    assert actual[4]['game_id'] == ''
    assert actual[4]['game_title'] == 'Game 5'

# test cases:

def test_events():
    with open(TEST_DATA_DIR + '/browse', 'r') as f:
        test_data = f.read()

    actual = parser.events(test_data)
    pprint(actual)

# test cases:

def test_casters():
    with open(TEST_DATA_DIR + '/browse', 'r') as f:
        test_data = f.read()

    actual = parser.casters(test_data)
    pprint(actual)

# test cases:

def test_matchups():
    with open(TEST_DATA_DIR + '/browse', 'r') as f:
        test_data = f.read()

    actual = parser.matchups(test_data)

    assert len(actual) == 6
    # TODO test that the actual URLs are still valid

# client tests

def test_client_matchups():
    actual = client.matchups()
    assert len(actual) == 6
