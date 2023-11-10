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
from resources.lib.comaddon import progress, VSlog, siteManager, addon

SITE_IDENTIFIER = 'askmovie'
SITE_NAME = 'Ask4Movie'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/recently-added/', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (URL_MAIN + '/channel_cat/tv-series/', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/channel_cat/miniseries/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات سلسلة صغيرة', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/netflix-originals/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام Netfilx', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/channel_cat/netflix/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netfilx', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showSearchSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/channel_cat/action'])
    liste.append(['Adventure', URL_MAIN + '/channel_cat/adventure'])
    liste.append(['Animated', URL_MAIN + '/channel_cat/animated'])
    liste.append(['Biography', URL_MAIN + '/channel_cat/biography'])
    liste.append(['Comedy', URL_MAIN + '/channel_cat/comedy'])
    liste.append(['Crime', URL_MAIN + '/channel_cat/crime'])
    liste.append(['Drama', URL_MAIN + '/channel_cat/drama'])
    liste.append(['Documentary', URL_MAIN + '/channel_cat/documentary'])
    liste.append(['Fantasy', URL_MAIN + '/channel_cat/fantasy'])
    liste.append(['History', URL_MAIN + '/channel_cat/history'])
    liste.append(['Horror', URL_MAIN + '/channel_cat/horror'])
    liste.append(['Music', URL_MAIN + '/channel_cat/music'])
    liste.append(['Mystery', URL_MAIN + '/channel_cat/mystery'])
    liste.append(['Romance', URL_MAIN + '/channel_cat/romance'])
    liste.append(['Sci-Fi', URL_MAIN + '/channel_cat/sci-fi'])
    liste.append(['Sport', URL_MAIN + '/channel_cat/sport'])
    liste.append(['Thriller', URL_MAIN + '/channel_cat/thriller'])
    liste.append(['Western', URL_MAIN + '/channel_cat/western'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/action'])
    liste.append(['Adventure', URL_MAIN + '/adventure'])
    liste.append(['Animated', URL_MAIN + '/animated'])
    liste.append(['Biography', URL_MAIN + '/biography'])
    liste.append(['Comedy', URL_MAIN + '/comedy'])
    liste.append(['Crime', URL_MAIN + '/crime'])
    liste.append(['Drama', URL_MAIN + '/drama'])
    liste.append(['Documentary', URL_MAIN + '/documentary'])
    liste.append(['Fantasy', URL_MAIN + '/fantasy'])
    liste.append(['History', URL_MAIN + '/history'])
    liste.append(['Horror', URL_MAIN + '/horror'])
    liste.append(['Music', URL_MAIN + '/music'])
    liste.append(['Mystery', URL_MAIN + '/mystery'])
    liste.append(['Romance', URL_MAIN + '/romance'])
    liste.append(['Sci-Fi', URL_MAIN + '/sci-fi'])
    liste.append(['Sport', URL_MAIN + '/sport'])
    liste.append(['Thriller', URL_MAIN + '/thriller'])
    liste.append(['Western', URL_MAIN + '/western'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'style="background-image: url((.+?))">.+?href="([^"]+)".+?href=".+?">(.+?)</a></p><p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "Season"  in aEntry[3]:
                continue

            sTitle = aEntry[3]
            siteUrl = aEntry[2]
            sThumb = aEntry[0].replace("'", '').replace('(', '').replace(')', '')
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

def showSearchSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'style="background-image: url((.+?))">.+?href="([^"]+)".+?href=".+?">(.+?)</a></p><p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if not "Season"  in aEntry[3]:
                continue

            sTitle = aEntry[3]
            siteUrl = aEntry[2]
            sThumb = aEntry[0].replace("'", '').replace('(', '').replace(')', '')
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
            oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  
 
def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" title="([^"]+)"><img width="150" height="150" src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  
def showSeasons():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')
 
	oParser = cParser()
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()

	sPattern = '<a class="btn-play-nf btn-play-nf-sm" href="([^"]+)"></a></div><div class="main-item"><div class="description"><p><a href="([^"]+)">(.+?)</a>'
	aResult = oParser.parse(sHtmlContent, sPattern)
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = aEntry[2]
			siteUrl = aEntry[0]
			sThumb = ''
			sDesc = ''
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
    
def showEps():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<ul class="group-links-list">'
    sEnd = '<div class="toolbar-right">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'data-embed-src="([^"]+)">([^<]+)</a></li>' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sEp = "E"+aEntry[1]
            sTitle = sEp
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''

            sHosterUrl = siteUrl 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, sDesc, oInputParameterHandler=oInputParameterHandler)
               
    oGui.setEndOfDirectory() 

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'id="player-embed"><iframe src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = " "
            if url.startswith('//'):
                url = 'http:' + url
				    
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'rel="next" href="([^"]+)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False