activate_this = '/home/pvg/.xbmc/addons/plugin.video.sc2casts/venv/bin/activate_this.py'
#activate_this = './venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

#import sys, xbmc, xbmcplugin, xbmcaddon, sc2casts
from xbmcswift2 import Plugin
#from sc2casts_parser import *
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
        'label': 'Top casts', 'path': plugin.url_for('recent_casts')
    #}, {
        #'label': 'Browse casts', 'path': plugin.url_for('recent_casts')
    #}, {
        #'label': 'Search casts', 'path': plugin.url_for('recent_casts')
    } ]

@plugin.route('/casts/recent')
def recent_casts():
    boolMatchup     = True
    boolNr_games    = True
    boolEvent       = True
    boolRound       = True
    boolCaster      = True

    def build_label(series):
        description_fields = [ series.name ]
        # before
        if boolMatchup:
            description_fields.insert(0, series.matchup.name)
        # after
        #if boolNr_games:
            #description_fields.append(series['series']['desc'])
        if boolEvent:
            description_fields.append(series.event.name)
        if boolRound:
            description_fields.append(series.event_round)
        if boolCaster:
            description_fields.append(', '.join([ caster.name for caster in series.casters ]))

        return {
            'label': ' | '.join(description_fields),
            'path': plugin.url_for('show_cast', cast_path=series.path),
        }

    items = [ build_label(series) for series in client.series() ]
    plugin.log.info('Found ' + str(len(items)) + ' casts')
    return items

@plugin.route('/cast/<cast_path>')
def show_cast(cast_path):
    plugin.log.info('cast_path = ' + cast_path)

    def build_label(game):
        return {
            #'label': game['game_title'],
            'label': game.name,
            #'path': plugin.url_for('show_youtube', youtube_id=game['game_id']),
            'path': plugin.url_for('show_youtube', youtube_id=game.video_id),
            # means this link is a video rather than another entry in the heirarchy
            'is_playable': True,
        }

    series = client.series_by_path(cast_path)
    plugin.log.info('series = ' + repr(series))
    result = [ build_label(game) for game in series.casts ]
    plugin.log.info('result = ' + repr(result))

    # add placeholders for unplayed games
    for i in xrange(series.num_videos + 1, series.best_of + 1):
        plugin.log.info(i)
        result.append({
            'label': 'Game ' + str(i),
            'path': plugin.url_for('show_nogame')
        })

    return result

@plugin.route('/show_youtube/<youtube_id>')
def show_youtube(youtube_id):
    url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtube_id
    plugin.log.info('Playing url: %s' % url)
    plugin.set_resolved_url(url)

@plugin.route('/show_nogame')
def show_nogame():
    plugin.notify('Game not played!')

if __name__ == '__main__':
    plugin.run()
