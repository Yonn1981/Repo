# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_phone_ua()
 
SITE_IDENTIFIER = 'qfilm'
SITE_NAME = 'Q-Film'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'category.php?cat=english-movies', 'showMovies')
MOVIE_AR = (URL_MAIN + 'category.php?cat=arabic', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category.php?cat=turkish-movies', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category.php?cat=indian-movies', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category.php?cat=asian-movies', 'showMovies')
ANIM_MOVIES = (URL_MAIN + 'category.php?cat=anime-movies', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + 'category.php?cat=dubbed-movies', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')

URL_SEARCH = (URL_MAIN + 'search.php?keywords=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?keywords=', 'showMovies')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'افلام آسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category.php?cat=adult-movies')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'للكبار فقط +18', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search.php?keywords='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'category.php?cat=action-movies'])
    liste.append(['انيميشن', URL_MAIN + 'category.php?cat=anime-movies'])
    liste.append(['مغامرات', URL_MAIN + 'category.php?cat=adventure-movies'])
    liste.append(['غموض', URL_MAIN + 'category.php?cat=mystery-movies'])
    liste.append(['تاريخي', URL_MAIN + 'category.php?cat=historical-movies'])
    liste.append(['كوميديا', URL_MAIN + 'category.php?cat=comedy-movies'])
    liste.append(['موسيقى', URL_MAIN + 'category.php?cat=musical-movies'])
    liste.append(['سيرة ذاتية', URL_MAIN + 'category.php?cat=biography-movies'])
    liste.append(['دراما', URL_MAIN + 'category.php?cat=drama-movies'])
    liste.append(['رعب', URL_MAIN + 'category.php?cat=horror-movies'])
    liste.append(['عائلى', URL_MAIN + 'category.php?cat=family-movies'])
    liste.append(['فانتازيا', URL_MAIN + 'category.php?cat=fantasy-movies'])
    liste.append(['حروب', URL_MAIN + 'category.php?cat=war-movies'])
    liste.append(['الجريمة', URL_MAIN + 'category.php?cat=crime-movies'])
    liste.append(['رومانسى', URL_MAIN + 'category.php?cat=romance-movies'])
    liste.append(['خيال علمى', URL_MAIN + 'category.php?cat=sci-fi-movies'])
    liste.append(['اثارة', URL_MAIN + 'category.php?cat=thriller-movies'])
    liste.append(['وثائقى', URL_MAIN + 'category.php?cat=documentary-movies'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()	

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="thumbnail">.+?<a href=["\']([^"\']+)["\']\s*title=["\']([^"\']+)["\'].+?data-echo=["\']([^"\']+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break 
            
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0].replace("watch.php","view.php")
            sDesc = ""
            sThumb = aEntry[2]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="active"><a href="#".+?<li class><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :      
        return URL_MAIN+aResult[1][0]

    return False
	 
def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()     

    sPattern = '<iframe src=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
				               
    oGui.setEndOfDirectory()