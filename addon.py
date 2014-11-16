#activate_this = '/home/pvg/.xbmc/addons/plugin.video.sc2casts/venv/bin/activate_this.py'
#activate_this = './venv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

from xbmcswift2 import Plugin
from sc2castsclient import *

'''
__version__ = "0.4.4"
__plugin__ = "SC2Casts-" + __version__
__author__ = "Kristoffer Petersson"
__settings__ = xbmcaddon.Addon(id='plugin.video.sc2casts')
__language__ = __settings__.getLocalizedString

SC2Casts = sc2casts.SC2Casts()

if not sys.argv[2]:
    SC2Casts.root()
else:
    print __plugin__

    params = SC2Casts.getParams(sys.argv[2])
    get = params.get
    if get("action"):
        SC2Casts.action(params)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
'''

plugin = Plugin()
client = Sc2CastsClient()

@plugin.route('/')
def main_menu():
    return [ {
        'label': 'Recent casts', 'path': plugin.url_for('recent_casts')
    }, {
        'label': 'Top casts (Today)', 'path': plugin.url_for('top_today_casts')
    }, {
        'label': 'Top casts (Week)', 'path': plugin.url_for('top_week_casts')
    }, {
        'label': 'Top casts (Month)', 'path': plugin.url_for('top_month_casts')
    }, {
        'label': 'All casts', 'path': plugin.url_for('all_casts')
    } ]

def build_series_label(cast):
    boolMatchup     = True
    boolNr_games    = True
    boolEvent       = True
    boolRound       = True
    boolCaster      = True

    description_fields = [ cast.name ]
    # before cast.name
    if boolMatchup and cast.matchup != '':
        description_fields.insert(0, cast.matchup.name)
    # after cast.name
    if boolEvent:
        description_fields.append(cast.event.name)
    if boolRound:
        description_fields.append(cast.event_round)
    if boolCaster:
        description_fields.append(', '.join([ caster.name for caster in cast.casters ]))

    plugin.log.info('description_fields = {}'.format(description_fields))

    return {
        'label': ' | '.join(description_fields),
        # note: strip off the leading slash; it'll get url-encoded
        'path': plugin.url_for('show_cast', cast_path=cast.path[1:]),
    }

@plugin.route('/casts/recent')
def recent_casts():
    items = [ build_series_label(series) for series in client.series('recent') if series.source == 'YouTube' ]
    plugin.log.info('Found {} casts'.format(len(items)))
    return items

@plugin.route('/casts/top_today')
def top_today_casts():
    items = [ build_series_label(series) for series in client.series('top_24h') if series.source == 'YouTube' ]
    plugin.log.info('Found {} casts'.format(len(items)))
    return items

@plugin.route('/casts/top_week')
def top_week_casts():
    items = [ build_series_label(series) for series in client.series('top_week') if series.source == 'YouTube' ]
    plugin.log.info('Found {} casts'.format(len(items)))
    return items

@plugin.route('/casts/top_month')
def top_month_casts():
    items = [ build_series_label(series) for series in client.series('top_month') if series.source == 'YouTube' ]
    plugin.log.info('Found {} casts'.format(len(items)))
    return items

@plugin.route('/casts/all')
def all_casts():
    items = [ build_series_label(series) for series in client.series('all') if series.source == 'YouTube' ]
    plugin.log.info('Found {} casts'.format(len(items)))
    return items

@plugin.route('/cast/<cast_path>')
def show_cast(cast_path):
    def build_single_game_label(game):
        return {
            'label': game.name,
            'path': plugin.url_for('show_youtube', youtube_id=game.video_id),
            # this means this link is a video rather than another entry in the heirarchy
            'is_playable': True,
        }

    series = client.series_by_path('/' + cast_path)
    played_games = [
        build_single_game_label(game) for game in series.casts
    ]

    dummy_game = Sc2CastsCast()
    dummy_game.video_id = 'dummy_game'
    dummy_label = build_single_game_label(dummy_game)
    # pad out the remaining count with dummy games, to avoid spoilers
    for i in xrange(series.best_of - len(played_games)):
        played_games.append(dummy_label)

    return played_games

@plugin.route('/show_youtube/<youtube_id>')
def show_youtube(youtube_id):
    url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtube_id
    plugin.log.info('Playing url: %s' % url)
    plugin.set_resolved_url(url)

if __name__ == '__main__':
    plugin.run()
