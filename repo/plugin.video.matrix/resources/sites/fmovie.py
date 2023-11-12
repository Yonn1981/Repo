# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import base64
import requests
from urllib.parse import unquote, quote
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon


import sys, os, re, json, base64
if sys.version_info >= (3,0,0):
# for Python 3
    to_unicode = str
    from urllib.parse import unquote, parse_qs, parse_qsl, quote, urlencode, quote_plus

else:
    # for Python 2
    to_unicode = unicode
    from urllib import unquote, quote, urlencode, quote_plus
    from urlparse import parse_qsl, parse_qs

SITE_IDENTIFIER = 'fmovie'
SITE_NAME = 'FMovies'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

aniyomi = ''

MOVIE_EN = (URL_MAIN + '/movie', 'showMovies')
KID_MOVIES = (URL_MAIN + '/filter?keyword=&type%5B%5D=movie&genre%5B%5D=10&sort=recently_updated', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (URL_MAIN + '/tv', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/filter?keyword=&type%5B%5D=tv&genre%5B%5D=10&sort=recently_updated', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

DOC_NEWS = (URL_MAIN + '/filter?keyword=&type=movie&genre=131&sort=recently_added', 'showMovies')
DOC_SERIES = (URL_MAIN + '/filter?keyword=&type=tv&genre=131&sort=recently_added', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + '/filter?keyword=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/filter?keyword=', 'showSeries')
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

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/filter?keyword=&type%5B%5D=movie&sort=trending')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'الأفلام الرائجة', 'film.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انيميشن', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/filter?keyword=&type%5B%5D=tv&sort=trending')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'المسلسلات الرائجة', 'mslsl.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/filter?keyword='+sSearchText + '&type%5B%5D=movie&sort=most_relevance'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/filter?keyword='+sSearchText + '&type%5B%5D=tv&sort=most_relevance'
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

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="poster"> <a href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
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

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="poster"> <a href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
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
    sSeriesTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sURL2 = sUrl

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="watch".+?data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry

            action = "fmovies-vrf"
            vrf = getVerid(sId)
            sUrl = URL_MAIN + '/ajax/episode/list/' + sId + '?vrf=' + vrf

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '"display: .+?data-season=([^<]+)>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:

                    sSeason = aEntry.replace('\\','').replace('"','')                  
                    Ss = aEntry.replace('\\','').replace('"','')
                    sDisplaySeason = sSeriesTitle+ ' S{:02d}'.format(int(sSeason))
                    siteUrl = sURL2 + '/' + Ss + '-1'
                    sThumb = sThumb
                    sDesc = ''
			
                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('SeasonTitle', sDisplaySeason)
                    oOutputParameterHandler.addParameter('sSeriesTitle', sSeriesTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('Ss', Ss)
                    oGui.addSeason(SITE_IDENTIFIER, 'showEps', sDisplaySeason, '', sThumb, sDesc, oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
        
def showEps():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    SeasonTitle = oInputParameterHandler.getValue('SeasonTitle')
    Ss = oInputParameterHandler.getValue('Ss')
    sSeriesTitle = oInputParameterHandler.getValue('sSeriesTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    if Ss is False:
        Ss = sUrl.split("/")[5].split("+")[0]
        SeasonTitle = ""

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="watch".+?data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sId = aEntry
            action = "fmovies-vrf"
            vrf = getVerid(sId)
            sUrl = URL_MAIN + '/ajax/episode/list/' + sId + '?vrf=' + vrf

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request().replace('\\','')

            Ss = Ss.replace(' ','')
            if Ss > '1':
                sStart = ('style="display: none" data-season="'+Ss)
            else:
                sStart = ('style="display: block" data-season="'+Ss)    
            sEnd = '</ul>'
            sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
       
            sPattern = '<a href="([^"]+)" data-id="([^"]+)".+?class="num">(.+?)</span> <span>(.+?)</span>' 
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[1]:
                oOutputParameterHandler = cOutputParameterHandler()   
                for aEntry in aResult[1]:

                    siteUrl = URL_MAIN +aEntry[0].split('\\')[0]
                    sEpisode = aEntry[2].replace('Episode ','').replace(':','')
                    episode = '{}E{:02d}'.format(SeasonTitle, int(sEpisode))

                    sTitle = aEntry[3].replace(':','')                      
                    sDisplayTitle = SeasonTitle + ' - ' + episode + ' - ' + sTitle

                    sId =  aEntry[1].split('\\')[0]

                    action = "fmovies-vrf"
                    from urllib.parse import quote
                    vrf = quote(getVerid(sId))

                    siteUrl = URL_MAIN + '/ajax/server/list/' + sId +'?vrf='+vrf
                    sThumb = sThumb
                    sDesc = ""
			
                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
   
    oGui.setEndOfDirectory() 
 
def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    from urllib.parse import unquote
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()  
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="watch".+?data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry

            action = "fmovies-vrf"
            vrf = getVerid(sId)
            sUrl = URL_MAIN + '/ajax/episode/list/' + sId +'?vrf='+vrf

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request().replace('\\','')

            sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
            aResult = oParser.parse(sHtmlContent, sPattern)        
            if aResult[0]:
                for aEntry in aResult[1]:

                    sId = aEntry[0]
                    nTitle = aEntry[1]
                    action = "fmovies-vrf"
                    vrf = getVerid(sId)
                    url = URL_MAIN + '/ajax/server/list/' + sId +'?vrf='+vrf

                    oRequestHandler = cRequestHandler(url)
                    sHtmlContent = oRequestHandler.request().replace('\\','')

                    sPattern = 'data-link-id="([^"]+)".+?<span>(.+?)</span>'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        oOutputParameterHandler = cOutputParameterHandler()
                        for aEntry in aResult[1]:
            
                            sId = aEntry[0].split('\\')[0] 
                            sHost = aEntry[1]
                            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

                            oOutputParameterHandler.addParameter('sId', sId)
                            oOutputParameterHandler.addParameter('nTitle', nTitle)
                            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)
                            oOutputParameterHandler.addParameter('sHost', sHost)

                            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request().replace('\\','')

    sPattern = 'data-link-id="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            
            sId = aEntry[0].split('\\')[0] 
            sHost = aEntry[1]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)
                                
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sId = oInputParameterHandler.getValue('sId')
    nTitle = oInputParameterHandler.getValue('nTitle')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    action = "fmovies-vrf"
    vrf = getVerid(sId)

    url = URL_MAIN + '/ajax/server/' + sId +'?vrf='+vrf
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"url":"([^"]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:

        sId = aResult[0]                             
        action = "fmovies-decrypt"
        url = DecodeLink(sId)

        sHosterUrl = unquote(url)
        SubTitle = ""
        if ('mcloud' in sHosterUrl) or ('vidstream' in sHosterUrl) or ('vidplay' in sHosterUrl):
            if ('sub.info' in sHosterUrl):
                SubTitle = sHosterUrl.split('sub.info=')[1]
                sHosterUrl = sHosterUrl.split('&sub.info')[0]
            else:
                SubTitle = ""
                sHosterUrl = sHosterUrl
                                    
            if ('vidstream' in sHosterUrl) or ('vidplay' in sHosterUrl):
                action = "rawVizcloud"
            else:
                action = "rawMcloud"
            sHosterUrl1 = vrf_function2(sHosterUrl, action)

            if 'm3u8' in sHosterUrl1:
                oHoster = cHosterGui().getHoster('mcloud') 
            else:
                oHoster = cHosterGui().checkHoster(sHosterUrl1)
            if oHoster:
                sDisplayTitle = sMovieTitle
                if ('http' in SubTitle):
                    sHosterUrl1 = sHosterUrl1+'?sub.info='+SubTitle
                else:
                    sHosterUrl1 = sHosterUrl1
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl1, sThumb, oInputParameterHandler=oInputParameterHandler)

        else:
            if ('sub.info' in sHosterUrl):
                SubTitle = sHosterUrl.split('sub.info=')[1]
                sHosterUrl = sHosterUrl.split('&sub.info')[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                if ('http' in SubTitle):
                    sHosterUrl = sHosterUrl+'?sub.info='+SubTitle
                else:
                    sHosterUrl = sHosterUrl
                if nTitle:
                    sDisplayTitle = nTitle+' '+sMovieTitle
                else:
                    sDisplayTitle = sMovieTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)


    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="page-link" href="([^"]+)" rel="next"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False

def DecodeLink(mainurl):
	mainurl = mainurl.replace('_', '/').replace('-', '+')
	#
	ab=mainurl[0:6]   #23.09.21
	ac2 = mainurl[6:]	#23.09.21
	ac2 = mainurl#[6:]	#23.09.21
	
	
	
	#ab = 'DZmuZuXqa9O0z3b7'
	ab= 'hlPeNwkncH0fq9so'
	ab = '8z5Ag5wgagfsOuhz'
	
	ac= decode2(mainurl)
	
	link = dekoduj(ab,ac)
	link = unquote(link)
	return link

def dekoduj(r,o):

    t = []
    e = []
    n = 0
    a = ""
    for f in range(256): 
        e.append(f)

    for f in range(256):

        n = (n + e[f] + ord(r[f % len(r)])) % 256
        t = e[f]
        e[f] = e[n]
        e[n] = t

    f = 0
    n = 0
    for h in range(len(o)):
        f = f + 1
        n = (n + e[f % 256]) % 256
        if not f in e:
            f = 0
            t = e[f]
            e[f] = e[n]
            e[n] = t

            a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])
        else:
            t = e[f]
            e[f] = e[n]
            e[n] = t
            if sys.version_info >= (3,0,0):
                a += chr((o[h]) ^ e[(e[f] + e[n]) % 256])
            else:
                a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])

    return a

def vrf_function(query, action):
    sUrl = 'https://9anime.eltik.net/'+action+'?query='+query+'&apikey='+aniyomi

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"url":"(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        vrf = quote(aResult[0])
        return vrf
        
    return False, False

def vrf_function2(query, action):
    if '?' in query:
        SubTitle = query.split('?')[1]
        query = query.split('/e/')[1].split('?')[0]

    else:
        SubTitle = ''
        query = query.split('e/')[1]

    reqURL = 'https://9anime.eltik.net/'+action+'?query='+query+'&apikey='+aniyomi

    futoken = requests.get("https://vidplay.site/futoken")
    futoken = futoken.text

    rawSource = requests.post(reqURL, headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"query": query, "futoken": futoken})
    sHtmlContent = rawSource.content

    sPattern = '"rawURL":"([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)  

    if aResult[0]:
        url = aResult[1][0].replace('mcloud.to','mcloud.bz')
        if 'vidstream' in url or 'vidplay' in url:
                referer = 'https://vidplay.site/'
        else:
                referer = "https://mcloud.bz/"
        headers2 = {'Referer': referer
                    }

        url = url+'?'+SubTitle
        req = requests.get(url ,headers=headers2)
        response = str(req.content)

        sPattern = '"file":"([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(response, sPattern)
        if aResult[0]:
            url = aResult[1][0]
            url = url.replace('\\','').replace('+','%2B')

        return url
        
    return False, False

try:
	import string
	STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	#CUSTOM_ALPHABET =   "5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"   #23/05/22
	CUSTOM_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'#'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='

	ENCODE_TRANS = string.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
	DECODE_TRANS = string.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)
except:
	STANDARD_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	#CUSTOM_ALPHABET =   b"5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"  #23/05/22
	CUSTOM_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'#'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='
	
	
	ENCODE_TRANS = bytes.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
	DECODE_TRANS = bytes.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)

def encode2(input):
	return base64.b64encode(input).translate(ENCODE_TRANS)
def decode2(input):
	try:	
		xx= input.translate(DECODE_TRANS)
	except:
		xx= str(input).translate(DECODE_TRANS)
	return base64.b64decode(xx)

	
def endEN(t, n) :
    return t + n;

def rLMxL(t, n):
    return t < n;

def VHtgA (t, n) :
    return t % n;

def DxlFU(t, n) :
    return rLMxL(t, n);

def dec2(t, n) :
    o=[]
    s=[]
    u=0
    h=''
    for e in range(256):
        s.append(e)

    for e in range(256):
        u = endEN(u + s[e],ord(t[e % len(t)])) % 256
        o = s[e];
        s[e] = s[u];
        s[u] = o;
    e=0
    u=0
    c=0
    for c in range(len(n)):
        e = (e + 1) % 256
        o = s[e]
        u = VHtgA(u + s[e], 256)
        s[e] = s[u];
        s[u] = o;
        try:
            h += chr((n[c]) ^ s[(s[e] + s[u]) % 256]);
        except:
            h += chr(ord(n[c]) ^ s[(s[e] + s[u]) % 256]);
    return h

def getVerid(id):
    def convert_func(matchobj):
        m =  matchobj.group(0)

        if m <= 'Z':
            mx = 90
        else:
            mx = 122
        mx2 = ord( m)+ 13  
        if mx>=mx2:
            mx = mx2
        else:
            mx = mx2-26
        gg = chr(mx)
        return gg

    def but(t):
        o=''
        for s in range(len(t)):
            u = ord(t[s]) 
            if u==0:
                u=0
            else:
                if (s % 5 == 1 or s % 5 == 4):
                    u -= 2
                else:
                    if (s % 5 == 3):
                        u += 5;
                    else:
                        if s % 5 == 0 :
                            u -= 4;
                        else:
                            if s % 5 == 2 :
                                u -= 6
            o += chr(u) 
			
			
			
        if sys.version_info >= (3,0,0):
            o=o.encode('Latin_1')

        if sys.version_info >= (3,0,0):
            o=(o.decode('utf-8'))

        return o
    ab = 'DZmuZuXqa9O0z3b7' #####stare
    ab = 'MPPBJLgFwShfqIBx'
    ab = 'rzyKmquwICPaYFkU'
    ab = 'FWsfu0KQd9vxYGNB'
    ac = id
    hj = dec2(ab,ac) #

    if sys.version_info >= (3,0,0):
        hj=hj.encode('Latin_1')

    hj2 = encode2(hj)   

    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
    hj2 = re.sub("[a-zA-Z]", convert_func, hj2) 
    if sys.version_info >= (3,0,0):
        hj2=hj2.encode('Latin_1')
	
	

	
	
    hj2 = encode2(hj2)   
    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
		

    xc= but(hj2) 

    return xc
		
	