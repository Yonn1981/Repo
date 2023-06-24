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

SITE_IDENTIFIER = 'sflix'
SITE_NAME = 'sFlix'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/movie', 'showMovies')
KID_MOVIES = (URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=3&country=all', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (URL_MAIN + '/tv-show', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=3&country=all', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

URL_SEARCH_MOVIES = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab2.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انيميشن', 'anime.png', oOutputParameterHandler)  

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
        sUrl = URL_MAIN + '/search/'+sSearchText.replace(' ','-')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText.replace(' ','-')
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=10&country=all'])
    liste.append(['Adventure', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=18&country=all'])
    liste.append(['Animated', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=3&country=all'])
    liste.append(['Biography', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=37&country=all'])
    liste.append(['Comedy', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=7&country=all'])
    liste.append(['Crime', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=2&country=all'])
    liste.append(['Drama', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=4&country=all'])
    liste.append(['Documentary', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=11&country=all'])
    liste.append(['Fantasy', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=13&country=all'])
    liste.append(['History', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=19&country=all'])
    liste.append(['Horror', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=14&country=all'])
    liste.append(['Music', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=15&country=all'])
    liste.append(['Mystery', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=1&country=all'])
    liste.append(['Romance', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=12&country=all'])
    liste.append(['Sci-Fi', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=5&country=all'])
    liste.append(['Thriller', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=16&country=all'])
    liste.append(['War', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=28&country=all'])
    liste.append(['Western', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=6&country=all'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=10&country=all'])
    liste.append(['Adventure', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=18&country=all'])
    liste.append(['Animated', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=3&country=all'])
    liste.append(['Biography', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=37&country=all'])
    liste.append(['Comedy', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=7&country=all'])
    liste.append(['Crime', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=2&country=all'])
    liste.append(['Drama', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=4&country=all'])
    liste.append(['Documentary', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=11&country=all'])
    liste.append(['Fantasy', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=13&country=all'])
    liste.append(['History', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=19&country=all'])
    liste.append(['Horror', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=14&country=all'])
    liste.append(['Music', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=15&country=all'])
    liste.append(['Mystery', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=1&country=all'])
    liste.append(['Romance', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=12&country=all'])
    liste.append(['Sci-Fi', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=5&country=all'])
    liste.append(['Thriller', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=16&country=all'])
    liste.append(['War', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=28&country=all'])
    liste.append(['Western', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=6&country=all'])

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
    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'

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
            if "tv/"  in aEntry[1]:
                continue

            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[1]
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
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
    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'

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
            if "movie/"  in aEntry[1]:
                continue

            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[1]
            sThumb = aEntry[0]
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
	sUrl2 = sUrl
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()
	oParser = cParser()
    # .+? ([^<]+)
	sPattern = 'data-id="(.+?)"'
	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)

	#VSlog(aResult)
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
                    sId = aEntry
 

                    sUrl = URL_MAIN + '/ajax/v2/tv/seasons/' + sId

                    oRequestHandler = cRequestHandler(sUrl)
                    sHtmlContent = oRequestHandler.request()

                    sPattern = '<a data-id="([^"]+)".+?class="dropdown-item ss-item.+?href="([^"]+)">(.+?)</a>'
                    oParser = cParser()
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    #VSlog(aResult)
                    if aResult[0]:
                        for aEntry in aResult[1]:
                            siteUrl = URL_MAIN+'/ajax/v2/season/episodes/'+aEntry[0]
                            sTitle = sMovieTitle+aEntry[2]
                            sThumb = ''
                            sDesc = ''
			
                            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                            oOutputParameterHandler.addParameter('tvUrl',sUrl2)
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


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?

    sPattern = 'data-id="([^"]+)">.+?<a href="([^"]+)" class="film-poster mb-0">.+?<img src="([^"]+)".+?class="film-poster-img".+?title="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(aResult)
    if aResult[0]:
                        for aEntry in aResult[1]:
                            oOutputParameterHandler = cOutputParameterHandler()
                            siteUrl = URL_MAIN + '/ajax/v2/episode/servers/' + aEntry[0]
                            sTitle = aEntry[3]
                            sThumb = URL_MAIN + aEntry[2]
                            sDesc = ''
			
                            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)
                            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)


               
       
    oGui.setEndOfDirectory() 
 
	

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'data-id="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #VSlog(aResult)
    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry
 

            sUrl = URL_MAIN + '/ajax/movie/episodes/' + sId

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            url = sHtmlContent

    sPattern = 'data-id="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(aResult)
    if aResult[0]:
                for aEntry in aResult[1]:
                    sId = aEntry


                    url = URL_MAIN + '/ajax/get_link/' + sId
                    oRequestHandler = cRequestHandler(url)
                    sHtmlContent = oRequestHandler.request()

                    sPattern = '"link":"([^"]+)'
                    oParser = cParser()
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    #VSlog(aResult)
                    if aResult[0]:
                        for aEntry in aResult[1]:
            
                            url = aEntry               		
                            #VSlog(url)
                            sHosterUrl = url 
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = sMovieTitle
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showSeriesLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'data-id="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #VSlog(aResult)
    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry
 

            sUrl = URL_MAIN + '/ajax/sources/' + sId

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            oParser = cParser()

            sPattern = '"link":"([^"]+)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            #VSlog(aResult)
            if aResult[0]:
                        for aEntry in aResult[1]:
                            url = aEntry   
   		
                            #VSlog(url)
                            sHosterUrl = url 
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = sMovieTitle
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'title="Next" class="page-link" href="([^"]+)"'	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False