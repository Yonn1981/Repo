# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import json
import base64
import requests, time
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon, isMatrix, VSlog
from resources.lib.tmdb import cTMDb

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

SITE_IDENTIFIER = 'tma'
SITE_NAME = 'The Movie Archive'
SITE_DESC = 'english vod'

URL_MAIN = 'https://www.themoviedb.org/'

API_VERS = '3'
API_URL = URL_MAIN + API_VERS

tmdb_session = ''
tmdb_account = ''

MOVIE_EN = ('movie/now_playing', 'showMovies')
MOVIE_TOP = ('movie/top_rated', 'showMovies')
MOVIE_POP = ('movie/popular', 'showMovies')
#MOVIE_4k = ('movie/popular', 'showMovies')
MOVIE_GENRES = ('genre/movie/list', 'showGenreMovie')

URL_SEARCH_MOVIES = ('https://api.themoviedb.org/3/search/movie?include_adult=false&query=', 'showMoviesSearch')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', addons.VSlang(30330), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POP[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30425), 'pop.png', oOutputParameterHandler)

    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_4k[0])
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' 4k أفلام', 'pop.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30426), 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30427), 'top.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', addons.VSlang(30428), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText.replace(' ', '+'))
        return  

def showGenreMovie():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")
            sUrl = 'genre/' + str(sId) + '/movies'
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(sTitle), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showFolderList():
    oGui = cGui()

    liste = []
    liste.append(['Top 50 Greatest Movies', '10'])
    liste.append(['Oscar winners', '31670'])
    liste.append(['Fascinating movies ', '43'])
    liste.append(['Science-Fiction', '3945'])
    liste.append(['Adaptations', '9883'])
    liste.append(['Disney Classic', '338'])
    liste.append(['Pixar', '3700'])
    liste.append(['Marvel', '1'])
    liste.append(['DC Comics Universe', '3'])
    liste.append(['Top Manga', '31665'])
    liste.append(['Top Manga 2', '31695'])
    liste.append(['Best Series', '36788'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showLists', sTitle, 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesSearch(sSearch=''):
    oGui = cGui()
    addons = addon()
    API_Key = addons.getSetting('api_tmdb')

    sUrl = sSearch + '&api_key='+API_Key
        
    data = requests.get(sUrl)
    sHtmlContent = data.text

    sPattern = '"id":(.+?),.+?"original_title":"([^"]+)".+?"overview":"([^"]+)".+?"poster_path":(.+?),'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'null' in aEntry[3] or 'none' in aEntry[3]:
                continue
                
            sId = aEntry[0]
            siteUrl = f'https://prod.omega.themoviearchive.site/v3/movie/sources/{sId}'
            sTitle = aEntry[1]
            sThumb = "https://image.tmdb.org/t/p/w500" + aEntry[3].replace('"','')
            sDesc = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)
    if not sSearch:
        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    try:
        total = len(result)
        if total > 0:
            total = len(result['results'])
            progress_ = progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                i = grab._format(i, '', "movie")

                sId, sTitle, simdb_id, sThumb, sDesc, sYear = i['tmdb_id'], i['title'], i['imdb_id'], i['poster_path'], i['plot'], i['year']

                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")
                sDisplayTitle = sTitle.replace(' ','%2520').replace('%20','%2520')
                siteUrl = base64.b64decode('aHR0cHM6Ly9hcGkuYnJhZmxpeC52aWRlby9mZWJib3gvc291cmNlcy13aXRoLXRpdGxlPw==').decode('utf8',errors='ignore')
                siteUrl = f'{siteUrl}title={sDisplayTitle}&year={sYear}&mediaType=movie&episodeId=1&seasonId=1&tmdbId={sId}&imdbId={simdb_id}'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sId', sId)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError as e:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]No result n\'was found.[/COLOR]')

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sId = oInputParameterHandler.getValue('sId')

    simdb_id = sUrl.split('imdbId=')[1]
    if simdb_id == '':
        addons = addon()
        API_Key = addons.getSetting('api_tmdb')
        sApi = f'https://api.themoviedb.org/3/movie/{sId}?api_key={API_Key}'
        sResponse = requests.request("GET", sApi, headers=None, data=None)
        data = json.loads(sResponse.text)
        simdb_id = data["imdb_id"]
        sUrl = sUrl + simdb_id

    from resources.lib.multihost import cVidsrcto
    try:
        sHosterUrl = f'https://vidsrc.to/embed/movie/{simdb_id}'
        aResult = cVidsrcto().GetUrls(sHosterUrl)
        if (aResult):
            for aEntry in aResult:
                sHosterUrl = aEntry
                VSlog(sHosterUrl)

                sDisplayTitle = sMovieTitle
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler) 

    except:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]فشل الاتصال بالموقع ، حاول مرة أخرى[/COLOR]')
        time.sleep(5)

    oGui.setEndOfDirectory()
