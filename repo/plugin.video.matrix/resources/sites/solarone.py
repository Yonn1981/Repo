# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.util import cUtil, Unquote

SITE_IDENTIFIER = 'solarone'
SITE_NAME = 'SolarOne'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/movie/', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (URL_MAIN + '/tv/', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

URL_SEARCH_MOVIES = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH SERIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab2.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/featured/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام السينما', 'agnab2.png', oOutputParameterHandler)   

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/tv/action'])
    liste.append(['Adventure', URL_MAIN + '/tv/adventure'])
    liste.append(['Animated', URL_MAIN + '/tv/animation'])
    liste.append(['Biography', URL_MAIN + '/tv/biography'])
    liste.append(['Comedy', URL_MAIN + '/tv/comedy'])
    liste.append(['Crime', URL_MAIN + '/tv/crime'])
    liste.append(['Drama', URL_MAIN + '/tv/drama'])
    liste.append(['Documentary', URL_MAIN + '/tv/documentary'])
    liste.append(['Fantasy', URL_MAIN + '/tv/fantasy'])
    liste.append(['History', URL_MAIN + '/tv/history'])
    liste.append(['Horror', URL_MAIN + '/tv/horror'])
    liste.append(['Music', URL_MAIN + '/tv/music'])
    liste.append(['Mystery', URL_MAIN + '/tv/mystery'])
    liste.append(['Romance', URL_MAIN + '/tv/romance'])
    liste.append(['Sci-Fi', URL_MAIN + '/tv/sci-fi'])
    liste.append(['Sport', URL_MAIN + '/tv/sport'])
    liste.append(['Thriller', URL_MAIN + '/tv/thriller'])
    liste.append(['Western', URL_MAIN + '/tv/western'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/movie/action'])
    liste.append(['Adventure', URL_MAIN + '/movie/adventure'])
    liste.append(['Animated', URL_MAIN + '/movie/animation'])
    liste.append(['Biography', URL_MAIN + '/movie/biography'])
    liste.append(['Comedy', URL_MAIN + '/movie/comedy'])
    liste.append(['Crime', URL_MAIN + '/movie/crime'])
    liste.append(['Drama', URL_MAIN + '/movie/drama'])
    liste.append(['Documentary', URL_MAIN + '/movie/documentary'])
    liste.append(['Fantasy', URL_MAIN + '/movie/fantasy'])
    liste.append(['History', URL_MAIN + '/movie/history'])
    liste.append(['Horror', URL_MAIN + '/movie/horror'])
    liste.append(['Music', URL_MAIN + '/movie/music'])
    liste.append(['Mystery', URL_MAIN + '/movie/mystery'])
    liste.append(['Romance', URL_MAIN + '/movie/romance'])
    liste.append(['Sci-Fi', URL_MAIN + '/movie/sci-fi'])
    liste.append(['Sport', URL_MAIN + '/movie/sport'])
    liste.append(['Thriller', URL_MAIN + '/movie/thriller'])
    liste.append(['Western', URL_MAIN + '/movie/western'])

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



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # ([^<]+) .+? (.+?)
    sPattern = '<div class="ml-item"><a href="([^"]+)".+?title="([^"]+)">.+?src="([^"]+)'

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
            if "/tv/" in aEntry[0]:
                continue

            sTitle = aEntry[1]
            siteUrl = URL_MAIN + aEntry[0] + 'watching'
            sThumb = URL_MAIN + aEntry[2]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


        progress_.VSclose(progress_)
 
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  

 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # ([^<]+) .+?
    sPattern = '<div class="ml-item"><a href="([^"]+)".+?title="([^"]+)">.+?src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(aResult)

	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "/movie/" in aEntry[0]:
                continue
            sTitle = aEntry[1]
            siteUrl = URL_MAIN + aEntry[0] + 'watching'
            sThumb = URL_MAIN + aEntry[2]
            sDesc = ''
            sYear = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  

    
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sStart = '<div class="les-content">'
    sEnd = '<div id="mv-info">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a title="([^"]+)".+?data-file="([^"]+)' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(aResult)

	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sName = aEntry[0].split(':')[-1]
            sTitle = aEntry[0] + sName
            siteUrl = aEntry[1]
            sThumb = " "
            sDesc = ''

			
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)


    oGui.setEndOfDirectory() 
 
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent1 = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'id="iframe-embed".+?src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)
    #VSlog(aResult)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
            if ('membed' in url):
                oRequestHandler = cRequestHandler(url)
                sHtmlContent = oRequestHandler.request()
                oParser = cParser()

                sPattern = 'data-video="([^"]+)'

                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                #VSlog(aResult)
                if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry

                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                sPattern = 'id="embedvideo" src="([^"]+)'

                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                #VSlog(aResult)
                if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry

                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            else:
                sTitle = sMovieTitle
                sHosterUrl = url
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    sDisplayTitle = sTitle
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'data-file="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)
    #VSlog(aResult)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            if ('membed' in url):
                oRequestHandler = cRequestHandler(url)
                sHtmlContent = oRequestHandler.request()
                oParser = cParser()

                sPattern = 'data-video="([^"]+)'

                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                #VSlog(aResult)
                if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry

                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                sPattern = 'id="embedvideo" src="([^"]+)'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                VSlog(aResult)
                if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry

                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            else:
                sTitle = sMovieTitle
                sHosterUrl = url
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    sDisplayTitle = sTitle
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'data-video="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)

    if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry
                        sTitle = sMovieTitle
                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<iframe id="embedvideo" src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)

    if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry
                        sTitle = sMovieTitle
                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="active">.+?<a href="([^"]+)'	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False