#!/usr/bin/env python

import re
from bs4 import BeautifulSoup
import requests

# ONLY does parsing; use something else to get the URL and pass it in as an html string
class SC2CastsParser:

    # out: [
    # {
    #   game_title:
    #   game_id:
    # },
    # ...
    # ]
    def TODO_titles(self, html_content):
        results = [ ]

        soup = BeautifulSoup(html_content)
        self.log('soup = ' + str(soup))

        # Get settings
        #boolMatchup = self.__settings__.getSetting( "matchup" )
        #boolNr_games = self.__settings__.getSetting( "nr_games" )
        #boolEvent = self.__settings__.getSetting( "event" )
        #boolRound = self.__settings__.getSetting( "round" )
        #boolCaster = self.__settings__.getSetting( "caster" )

        # Get info to show
        caster = re.compile('<a href="/.+?"><span class="caster_name">(.*?)</span></a>').findall(link)
        matchup = re.compile('<span style="color:#cccccc">(.*?)</span>').findall(link)
        roundname = re.compile('<span class="round_name">(.*?)</span>').findall(link)
        #checkSource = re.compile('<span class="source_name">(.*?)</span>').findall(link)
        # this span no longer exists, use the img icon as a proxy
        #checkSource = re.compile('<span class="source_name">(.*?)</span>').findall(link)
        checkSource = [ div.img['alt'] for div in soup.find_all('div', class_='latest_series') ]
        event = re.compile('<span class="event_name".*?>(.*?)</span>').findall(link)
        self.log('checkSource = ' + str(len(checkSource)))
        self.log('event = ' + str(len(event)))

        #Different source if URL is .../top
        if get("action") == 'showTitlesTop':
            title = re.compile('<h3><a href="(.+?)"><b >(.+?)</b> vs <b >(.+?)</b>&nbsp;\((.*?)\)</a></h3>').findall(link)
        else:
            title = re.compile('<h2><a href="(.+?)"><b >(.+?)</b> vs <b >(.+?)</b> \((.*?)\)</a>').findall(link)

        for i in range(len(event)):
            log('event = ' + str(event[i]))
            log('checkSource = ' + str(checkSource[i]))
            #if checkSource[i] != '@ YouTube':
            if 'YouTube' not in checkSource[i]:
                continue

            url = ''
            if boolMatchup == 'true':
                url += matchup[i] + ' | '

            url += title[i][1] + ' vs ' + title[i][2] + ' | '

            if boolNr_games == 'true':
                url += title[i][3] + ' | '
            if boolEvent == 'true':
                url += event[i] + ' | '
            if boolRound == 'true':
                url += roundname[i] + ' | '
            if boolCaster == 'true':
                url += 'cast by: ' + caster[i]

            #self.addCategory(url,title[i][0],'showGames')
            results.append(url, title[i][0], 'showGames')

        return results

    # out: [
    # {
    #   name: string,
    #   source: { youtube, },
    #   event: { name: string, path: string, },
    #   round: string <e.g. Semi-finals>,
    #   players: [
    #       {
    #           names: [ ],
    #           path: string,
    #       },
    #   ],
    #   casters: [
    #       {
    #           name: string,
    #           names: [ ],
    #           path: string,
    #       },
    #       ...
    #   ],
    #   series: {
    #     num_videos: int,
    #     best_of: int,
    #     desc: string <human readable, e.g. Bof3 in 1 Video>,
    #   },
    #   matchup: string <can be none, e.g. for team matches>,
    #   path: string,
    # },
    # ...
    # ]
    def casts(self, html):
        results = [ ]

        soup = BeautifulSoup(html)

        # TODO there's no deeper structure, so we have to parse in order to get "today", "yesterday", etc
        content_div = soup.select('div .content')[0]
        #self.log('content_div: ' + str(content_div))
        for div in content_div.find_all('div', recursive=False):
            #self.log('\t' + 'div: ' + str(div))

            def is_section_header(div):
                if not div.has_attr('class'):
                    return True
                return 'latest_series' not in div['class']
            if is_section_header(div):
                self.log('\t' + 'is section header; skipping')
                continue

            def name(div):
                return div.h2.a.get_text()
            def source(div):
                return div.img['alt']
            def event(div):
                return {
                    'name': div.select('.event_name')[0].string,
                    'path': div.select('.event_name')[0].parent['href']
                }
            def round_name(div):
                return div.select('.round_name')[0].string
            def players(div):
                return {
                    'names': [ t.string for t in div.find_all('b') ],
                    'path': div.h2.a['href'],
                }
            def casters(div):
                name_tag = div.select('.caster_name')[0]
                return {
                    'name': name_tag.string,
                    'names': [ f.strip() for f in name_tag.string.split('&') ],
                    'path': name_tag.parent['href'],
                }
            def series(div):
                # extract it from the name
                best_of_string = re.search('\((.*)\)', name(div)).group(1)
                #print best_of_string

                # case by case
                if '1 game' in best_of_string.lower():
                    num_videos = 1
                    best_of = 1
                elif 'in 1 video' in best_of_string.lower():
                    num_videos = 1
                    best_of = int(re.search('BO(\d+) in 1 Video', best_of_string).group(1))
                elif 'best of ' in best_of_string.lower():
                    num_videos = int(re.search('Best of (\d+)', best_of_string).group(1))
                    best_of = num_videos
                else:
                    print 'unknown:', best_of_string
                    num_videos = -1
                    best_of = -1

                return {
                    'num_videos': num_videos,
                    'best_of': best_of,
                    'desc': best_of_string,
                }
            def matchup(div):
                # team matches don't have the matchup tag
                if not div.span.string:
                    return ''
                return div.span.string.replace('[', '').replace(']', '')
            def path(div):
                return div.h2.a['href']

            cast = {
                'name': name(div),
                'source': source(div),
                'event': event(div),
                'round': round_name(div),
                'players': players(div),
                'casters': casters(div),
                'series': series(div),
                'matchup': matchup(div),
                'path': path(div),
            }
            self.log('\t' + 'adding: ' + str(cast))
            results.append(cast)

        return results

    # out: [
    # {
    #   game_title: Game 1, Game 2, etc
    #   game_id: YouTube video id, like 'Gt4E3rIUhoA'
    # },
    # ...
    # ]
    def games(self, game_page_html):
        results = [ ]

        soup = BeautifulSoup(game_page_html)
        matchLinks = [ e['src'] for e in soup.find_all('iframe') ]
        self.log('matchLinks: ' + str(len(matchLinks)))
        gameDivs = soup.find_all(name='div', id=re.compile('g.*'))
        self.log('gameDivs: ' + str(len(gameDivs)))

        # if it's only 1 game
        if len(gameDivs) == 0:
            iframe = soup.find(id='ytplayer')
            game_title = 'Game 1'
            game_url = iframe['src']
            game_id = game_url.rsplit('/', 1)[-1]

            #self.addVideo(game_title, game_id)
            results.append({ 'game_title': game_title, 'game_id': game_id })

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
                results.append({ 'game_title': game_title, 'game_id': game_id })
            else:
                # TODO how to send an ui alert of something
                self.log('Game not played or casted yet.')
                game_id = ''
                #self.addVideo(game_title, game_id)
                results.append({ 'game_title': game_title, 'game_id': game_id })

        return results

    # out: [
    # {
    #   desc: string,
    #   path: string,
    # },
    # ...
    # ]
    # TODO split into prominent and all?
    def casters(self, html):
        results = [ ]

        soup = BeautifulSoup(html)

        # there are 4 'valign=top' fields:
        # 0: prominent and all events
        # 1: notable and all events
        # 2: prominent and all casters
        # 3: matchup
        content_div = soup.find_all('td', attrs={ 'valign': 'top' })[2]
        #print content_div

        for anchor in content_div.find_all('a'):
            #print anchor
            results.append({
                'desc': anchor.string,
                'path': anchor['href'],
            })

        return results

    # out: [
    # {
    #   desc: string,
    #   path: string,
    # },
    # ...
    # ]
    # TODO split into prominent and all?
    def events(self, html):
        results = [ ]

        for anchor in self._browse_page_sections(html, 'events').find_all('a'):
            #print anchor
            results.append({
                'desc': anchor.string,
                'path': anchor['href'],
            })

        return results

    # out: [
    # {
    #   desc: string,
    #   path: string,
    # },
    # ...
    # ]
    # TODO split into prominent and all?
    def casters(self, html):
        results = [ ]

        for anchor in self._browse_page_sections(html, 'casters').find_all('a'):
            #print anchor
            results.append({
                'desc': anchor.string,
                'path': anchor['href'],
            })

        return results

    # list of sub-categories, meant to be used like <HOST> + "/" + result
    #
    # out: [
    # {
    #   desc: PvZ, ZvT, etc
    #   path: path to append to HOST
    # },
    # ...
    # ]
    def matchups(self, html):
        #return [
            #{ 'description': 'PvZ', 'path': 'matchups-PvZ' },
            #{ 'description': 'PvT', 'path': 'matchups-PvT' },
            #{ 'description': 'TvZ', 'path': 'matchups-TvZ' },
            #{ 'description': 'PvP', 'path': 'matchups-PvP' },
            #{ 'description': 'TvT', 'path': 'matchups-TvT' },
            #{ 'description': 'ZvZ', 'path': 'matchups-ZvZ' },
        #]
        results = [ ]

        for anchor in self._browse_page_sections(html, 'matchups').find_all('a'):
            #print anchor
            results.append({
                'desc': anchor.string,
                'path': anchor['href'],
            })

        return results


    # in: a section name; there are 4 'valign=top' fields:
    # events: prominent and all events
    # players: notable and all players
    # casters: prominent and all casters
    # matchups: matchups
    #
    # out: the `td` tag containing the given section
    def _browse_page_sections(self, browse_page_html, section_name):
        soup = BeautifulSoup(browse_page_html)

        section_id = {
            'events': 0,
            'players': 1,
            'casters': 2,
            'matchups': 3,
        }[section_name]

        content_div = soup.find_all('td', attrs={ 'valign': 'top' })[section_id]
        return content_div


    def log(self, msg):
        print msg

class SC2CastsClient:

    HOST = 'http://sc2casts.com'

    PATH_INDEX = '/index.php'
    PATH_BROWSE = '/browse'
    PATH_ALL = '/all'

    parser = SC2CastsParser()

    @classmethod
    def cast(cls, cast_path):
        url = cls.HOST + cast_path
        print(url)
        html = requests.get(url).text
        #print(html)
        return cls.parser.games(html)

    @classmethod
    def casts(cls):
        html = requests.get(cls.HOST + cls.PATH_INDEX).text
        #print(html)
        return cls.parser.casts(html)

    @classmethod
    def events(cls):
        html = requests.get(cls.HOST + cls.PATH_BROWSE).text
        return cls.parser.events(html)

    @classmethod
    def matchups(cls):
        html = requests.get(cls.HOST + cls.PATH_BROWSE).text
        return cls.parser.matchups(html)

    @classmethod
    def casters(cls):
        html = requests.get(cls.HOST + cls.PATH_BROWSE).text
        return cls.parser.casters(html)

