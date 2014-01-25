#!/usr/bin/env python

from sc2casts_parser import *
import json

# test cases:
# bo3 in 1 game
# 1 game
# 3 games
# 5 games

TEST_DATA_DIR = 'tests'

def test_games_bo3_in_1_game():
    with open(TEST_DATA_DIR + '/cast14719-Soulkey-vs-Cure-Best-of-3-All-in-1-video-IEM-Cologne-2014-Korean-Qualifier', 'r') as f:
        test_data = f.read()
        #print test_data

    parser = SC2CastsParser()
    actual = parser.games(test_data)

    assert len(actual) == 1

    assert actual[0]['game_id'] == 'Gt4E3rIUhoA'
    assert actual[0]['game_title'] == 'Game 1'

# games 4 and 5 not played
def test_games_5_games():
    with open(TEST_DATA_DIR + '/cast14705-KT-Rolster-vs-Prime-Best-of-5-2014-Proleague-Round-1', 'r') as f:
        test_data = f.read()
        #print test_data

    parser = SC2CastsParser()
    actual = parser.games(test_data)

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
