#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

class SC2CastsParser:

    # out: [
    # {
    #   game_title:
    #   game_id:
    # },
    # ...
    # ]
    def games(self, html_content):
        result = [ ]

        soup = BeautifulSoup(html_content)
        #log('link = ' + link)
        # find divs with id='g1', id='g2', etc
        #matchCount = re.compile('<div id="g(.+?)"(.+?)</div></div>').findall(link)
        #matchLinks = [ e['src'] for e in soup.find_all('iframe') ]
        matchLinks = [ e['src'] for e in soup.find_all('iframe') ]
        #log('matchCount = ' + str(matchCount))

        #youtubeLinksRe = re.compile('src="https?://www.youtube.com/embed/(.+?)"')

        #gameDivs = soup.find_all(name='div', id=re.compile('g*'))
        #gameDivs = soup.find_all(name='div', id=re.compile('^g*$'))
        gameDivs = soup.find_all(name='div', id=re.compile('g.*'))
        self.log('# gameDivs = ' + str(len(gameDivs)))

        # if it's only 1 game
        if len(gameDivs) == 0:
            iframe = soup.find(id='ytplayer')
            game_title = 'Game 1'
            game_url = iframe['src']
            game_id = game_url.rsplit('/', 1)[-1]

            #self.addVideo(game_title, game_id)
            result.append({ 'game_title': game_title, 'game_id': game_id })

        # if there's more than 1 game
        for i, g in enumerate(gameDivs):
            self.log('game div tag: ' + str(g))
            #log(g.contents)

            # if it doesn't have an iframe, game not played or casted
            game_title = 'Game ' + str(i + 1)
            if g.iframe:
                self.log(g.iframe['src'])

                game_url = g.iframe['src']
                game_id = game_url.rsplit('/', 1)[-1]
                self.log(game_id)

                self.log('title, url, id = ' + game_title + ', ' + game_url + ', ' + game_id)
                #break

                #self.addVideo(game_title, game_id)
                result.append({ 'game_title': game_title, 'game_id': game_id })
            else:
                # TODO how to send an ui alert of something
                self.log('Game not played or casted yet.')
                game_id = ''
                #self.addVideo(game_title, game_id)
                result.append({ 'game_title': game_title, 'game_id': game_id })

        return result

    def log(self, msg):
        print msg
