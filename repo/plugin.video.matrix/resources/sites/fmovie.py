﻿# -*- coding: utf-8 -*-
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

SITE_IDENTIFIER = 'fmovie'
SITE_NAME = 'FMovies'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/movie', 'showMovies')
KID_MOVIES = (URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=10&sort=recently_updated', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (URL_MAIN + '/tv', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=10&sort=recently_updated', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

URL_SEARCH_MOVIES = (URL_MAIN + '/filter?keyword=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/filter?keyword=', 'showSeries')
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
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&sort=trending')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'الأفلام الرائجة', 'film.png', oOutputParameterHandler)	

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انيميشن', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&sort=trending')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'المسلسلات الرائجة', 'mslsl.png', oOutputParameterHandler)	

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
        sUrl = URL_MAIN + '/filter?keyword='+sSearchText + '&type%5B%5D=movie&sort=recently_updated'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/filter?keyword='+sSearchText + '&type%5B%5D=tv&sort=recently_updated'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=25&sort=recently_updated'])
    liste.append(['Adventure', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=17&sort=recently_updated'])
    liste.append(['Animated', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=10&sort=recently_updated'])
    liste.append(['Biography', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=215&sort=recently_updated'])
    liste.append(['Comedy', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=14&sort=recently_updated'])
    liste.append(['Crime', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=26&sort=recently_updated'])
    liste.append(['Drama', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=1&sort=recently_updated'])
    liste.append(['Documentary', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=131&sort=recently_updated'])
    liste.append(['Family', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=43&sort=recently_updated'])
    liste.append(['Fantasy', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=31&sort=recently_updated'])
    liste.append(['History', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=47&sort=recently_updated'])
    liste.append(['Horror', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=74&sort=recently_updated'])
    liste.append(['Music', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=199&sort=recently_updated'])
    liste.append(['Mystery', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=64&sort=recently_updated'])
    liste.append(['Reality TV', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=4&sort=recently_updated'])
    liste.append(['Romance', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=23&sort=recently_updated'])
    liste.append(['Sci-Fi', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=15&sort=recently_updated'])
    liste.append(['Sports', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=44&sort=recently_updated'])
    liste.append(['Thriller', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=7&sort=recently_updated'])
    liste.append(['War', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=58&sort=recently_updated'])
    liste.append(['Western', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=28&sort=recently_updated'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=25&sort=recently_updated'])
    liste.append(['Adventure', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=17&sort=recently_updated'])
    liste.append(['Animated', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=10&sort=recently_updated'])
    liste.append(['Biography', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=215&sort=recently_updated'])
    liste.append(['Comedy', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=14&sort=recently_updated'])
    liste.append(['Crime', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=26&sort=recently_updated'])
    liste.append(['Drama', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=1&sort=recently_updated'])
    liste.append(['Documentary', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=131&sort=recently_updated'])
    liste.append(['Family', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=43&sort=recently_updated'])
    liste.append(['Fantasy', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=31&sort=recently_updated'])
    liste.append(['History', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=47&sort=recently_updated'])
    liste.append(['Horror', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=74&sort=recently_updated'])
    liste.append(['Music', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=199&sort=recently_updated'])
    liste.append(['Mystery', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=64&sort=recently_updated'])
    liste.append(['Reality TV', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=4&sort=recently_updated'])
    liste.append(['Romance', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=23&sort=recently_updated'])
    liste.append(['Sci-Fi', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=15&sort=recently_updated'])
    liste.append(['Sports', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=44&sort=recently_updated'])
    liste.append(['Thriller', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=7&sort=recently_updated'])
    liste.append(['War', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=58&sort=recently_updated'])
    liste.append(['Western', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=28&sort=recently_updated'])

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
    sPattern = '<div class="poster"> <a href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'

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
            if "tv/"  in aEntry[0]:
                continue

            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[0]
            sThumb = aEntry[1]
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
    sPattern = '<div class="poster"> <a href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'

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
            if "movie/"  in aEntry[0]:
                continue

            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[0]
            sThumb = aEntry[1]
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
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sURL2 = sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?

    sPattern = '<div class="watch".+?data-id="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry

            action = "fmovies-vrf"

            vrf = vrf_function(sId, action)

            sUrl = URL_MAIN + '/ajax/episode/list/' + sId + '?vrf=' + vrf

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()


            sPattern = '"display: .+?data-season=([^<]+)>'

            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
	
            #VSlog(aResult)
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
                    sSeason = "Season"+aEntry.replace('\\','').replace('"','')
                    Ss = aEntry.replace('\\','').replace('"','')

                    siteUrl = sURL2 + '/' + Ss + '-1'
                    sTitle = sSeason + ' ' + sMovieTitle 

                    sThumb = sThumb
                    sDesc = ''
			
                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('Ss', Ss)
                    oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    
    oGui.setEndOfDirectory() 
        
def showEps():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Ss = oInputParameterHandler.getValue('Ss')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?

    sPattern = '<div class="watch".+?data-id="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry

            action = "fmovies-vrf"

            vrf = vrf_function(sId, action)

            sUrl = URL_MAIN + '/ajax/episode/list/' + sId + '?vrf=' + vrf

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request().replace('\\','')

            Ss = Ss.replace(' ','')


            oParser = cParser()

            if Ss > '1':
                sStart = ('style="display: none" data-season="'+Ss)
            else:
                sStart = ('style="display: block" data-season="'+Ss)    
            sEnd = '</ul>'
            sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
       
            sPattern = '<a href="([^"]+)" data-id="([^"]+)".+?class="num">(.+?)</span> <span>(.+?)</span>' 
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[1]:
                oOutputParameterHandler = cOutputParameterHandler()   
                for aEntry in aResult[1]:

                    siteUrl = URL_MAIN +aEntry[0].split('\\')[0]
                    sTitle = aEntry[2].replace(':','').replace('Episode','E')
                    if 'Episode' in aEntry[3]:
                        sTitle = sTitle
                    else:
                        sTitle = sTitle + ' ' + aEntry[3]
                    sId =  aEntry[1].split('\\')[0]

                    action = "fmovies-vrf"
                    vrf = vrf_function(sId, action)

                    siteUrl = URL_MAIN + '/ajax/server/list/' + sId +'?vrf='+vrf
                    sThumb = sThumb
                    sDesc = ""
			
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

    sPattern = '<div class="watch".+?data-id="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry

            action = "fmovies-vrf"

            vrf = vrf_function(sId, action)

            sUrl = URL_MAIN + '/ajax/episode/list/' + sId +'?vrf='+vrf

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'data-id.+?"([^"]+)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                for aEntry in aResult[1]:
                    sId = aEntry.split('\\')[0]
                    action = "fmovies-vrf"
                    vrf = vrf_function(sId, action)

                    url = URL_MAIN + '/ajax/server/list/' + sId +'?vrf='+vrf
                    oRequestHandler = cRequestHandler(url)
                    sHtmlContent = oRequestHandler.request()

                    sPattern = 'data-link-id.+?"([^"]+)'
                    oParser = cParser()
                    aResult = oParser.parse(sHtmlContent, sPattern)

                    if aResult[0]:
                        for aEntry in aResult[1]:
            
                            sId = aEntry.split('\\')[0]   

                            action = "fmovies-vrf"
                            vrf = vrf_function(sId, action)
                    
                            url = URL_MAIN + '/ajax/server/' + sId +'?vrf='+vrf
                            oRequestHandler = cRequestHandler(url)
                            sHtmlContent = oRequestHandler.request()

                            sPattern = '"url":"([^"]+)'
                            oParser = cParser()
                            aResult = oParser.parse(sHtmlContent, sPattern)

                            if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    sId = aEntry 
                            
                                    action = "fmovies-decrypt"
                                    url = vrf_function(sId, action)

                            sHosterUrl = url
                            if ('mcloud' in sHosterUrl):
                                sHosterUrl = sHosterUrl.split('e/')[1].split('?')[0]
                                action = "mcloud"
                                sHosterUrl1 = vrf_function2(sHosterUrl, action)
                                oHoster = cHosterGui().checkHoster(sHosterUrl1)
                                if oHoster:
                                    sDisplayTitle = sMovieTitle
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl1, sThumb)

                            if ('vidstream' in sHosterUrl):
                                sHosterUrl = sHosterUrl.split('embed/')[1].split('?')[0]
                                action = "vizcloud"
                                sHosterUrl2 = vrf_function2(sHosterUrl, action)
                                oHoster = cHosterGui().checkHoster(sHosterUrl2)
                                if oHoster:
                                    sDisplayTitle = sMovieTitle
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl2, sThumb)

                            if 'http' not in sHosterUrl:
                                continue
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

    sPattern = 'data-link-id.+?"([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
                        for aEntry in aResult[1]:
            
                            sId = aEntry.split('\\')[0]   

                            action = "fmovies-vrf"
                            vrf = vrf_function(sId, action)
                    
                            url = URL_MAIN + '/ajax/server/' + sId +'?vrf='+vrf
                            oRequestHandler = cRequestHandler(url)
                            sHtmlContent = oRequestHandler.request()

                            sPattern = '"url":"([^"]+)'
                            oParser = cParser()
                            aResult = oParser.parse(sHtmlContent, sPattern)

                            if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    sId = aEntry 
                            
                                    action = "fmovies-decrypt"
                                    url = vrf_function(sId, action)

                            sHosterUrl = url 
                            if ('mcloud' in sHosterUrl):
                                sHosterUrl = sHosterUrl.split('e/')[1].split('?')[0]
                                action = "mcloud"
                                sHosterUrl1 = vrf_function2(sHosterUrl, action)
                                oHoster = cHosterGui().checkHoster(sHosterUrl1)
                                if oHoster:
                                    sDisplayTitle = sMovieTitle
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl1, sThumb)

                            if ('vidstream' in sHosterUrl):
                                sHosterUrl = sHosterUrl.split('embed/')[1].split('?')[0]
                                action = "vizcloud"
                                sHosterUrl2 = vrf_function2(sHosterUrl, action)
                                oHoster = cHosterGui().checkHoster(sHosterUrl2)
                                if oHoster:
                                    sDisplayTitle = sMovieTitle
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl2, sThumb)
                            if 'http' not in sHosterUrl:
                                continue     
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = sMovieTitle
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                                
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page-link" href="([^"]+)" rel="next"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False

def vrf_function(query, action):
# ============== function taken aniyomi-extensions - from 9anime extension ================
    sUrl = 'https://9anime.eltik.net/'+action+'?query='+query+'&apikey=aniyomi'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"url":"(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            vrf = aEntry
            return vrf
        
    return False, False
def vrf_function2(query, action):
# ============== function taken aniyomi-extensions - from 9anime extension ================
    sUrl = 'https://9anime.eltik.net/'+action+'?query='+query+'&apikey=aniyomi'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"file":"([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            url = aEntry

            return url
        
    return False, False