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
    }, {
        'label': 'Browse casts', 'path': plugin.url_for('recent_casts')
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

    def build_label(cast):
        description_fields = [ cast['name'] ]
        # before
        if boolMatchup and cast['matchup'] != '':
            description_fields.insert(0, cast['matchup'])
        # after
        #if boolNr_games:
            #description_fields.append(cast['series']['desc'])
        if boolEvent:
            description_fields.append(cast['event']['name'])
        if boolRound:
            description_fields.append(cast['round'])
        if boolCaster:
            description_fields.append(', '.join(cast['casters']['names']))

        return {
            'label': ' | '.join(description_fields),
            'path': plugin.url_for('show_cast', cast_path=cast['path']),
        }

    #items = [ build_label(cast) for cast in SC2CastsClient.casts() if cast['source'] == 'YouTube' ]
    items = [ build_label(cast) for cast in client.series() if cast['source'] == 'YouTube' ]
    plugin.log.info('Found ' + str(len(items)) + ' casts')
    return items

@plugin.route('/cast/<cast_path>')
def show_cast(cast_path):
    def build_label(game):
        return {
            'label': game['game_title'],
            'path': plugin.url_for('show_youtube', youtube_id=game['game_id']),
            # this means this link is a video rather than another entry in the heirarchy
            'is_playable': True,
        }

    return [
        #build_label(game) for game in Sc2CastsClient.cast(cast_path)
        build_label(game) for game in client.cast(cast_path)
    ]

@plugin.route('/show_youtube/<youtube_id>')
def show_youtube(youtube_id):
    url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtube_id
    plugin.log.info('Playing url: %s' % url)
    plugin.set_resolved_url(url)

if __name__ == '__main__':
    plugin.run()
