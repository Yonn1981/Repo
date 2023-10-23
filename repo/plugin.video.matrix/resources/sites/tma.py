# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
import requests

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon, VSupdate, isMatrix, VSlog
from resources.lib.tmdb import cTMDb

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

                sId, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'https://prod.omega.themoviearchive.site/v3/movie/sources/%s' % sId)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
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
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    data = requests.get(sUrl).json()

    sPattern = '["\']quality["\']:\s*["\']([^"\']+)["\'], ["\']url["\']:\s*["\']([^"\']+)["\']'
    oParser = cParser()
    aResult = oParser.parse(data, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sQual = aEntry[0]
            url = aEntry[1]
            sThumb = sThumb
            sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sQual)  

            sHosterUrl = url+'?sub.info='+sUrl 
            oHoster = cHosterGui().getHoster('tma') 

            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]No links n\'was found.[/COLOR]')

    oGui.setEndOfDirectory()
