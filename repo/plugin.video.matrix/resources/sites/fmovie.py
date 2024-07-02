# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from urllib.parse import unquote, quote
import sys, re, base64
to_unicode = str

SITE_IDENTIFIER = 'fmovie'
SITE_NAME = 'FMovies'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

aniyomi = ''

MOVIE_EN = (f'{URL_MAIN}/movie', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=10&sort=recently_updated', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (f'{URL_MAIN}/tv', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=10&sort=recently_updated', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

DOC_NEWS = (f'{URL_MAIN}/filter?keyword=&type=movie&genre=131&sort=recently_added', 'showMovies')
DOC_SERIES = (f'{URL_MAIN}/filter?keyword=&type=tv&genre=131&sort=recently_added', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}/filter?keyword=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}/filter?keyword=', 'showSeries')
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

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&sort=trending')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'الأفلام الرائجة', 'film.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انيميشن', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&sort=trending')
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
        sUrl = f'{URL_MAIN}/filter?keyword={sSearchText}&type%5B%5D=movie&sort=most_relevance'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}/filter?keyword={sSearchText}&type%5B%5D=tv&sort=most_relevance'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=25&sort=recently_updated'])
    liste.append(['Adventure', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=17&sort=recently_updated'])
    liste.append(['Animated', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=10&sort=recently_updated'])
    liste.append(['Biography', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=215&sort=recently_updated'])
    liste.append(['Comedy', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=14&sort=recently_updated'])
    liste.append(['Crime', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=26&sort=recently_updated'])
    liste.append(['Drama', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=1&sort=recently_updated'])
    liste.append(['Documentary', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=131&sort=recently_updated'])
    liste.append(['Family', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=43&sort=recently_updated'])
    liste.append(['Fantasy', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=31&sort=recently_updated'])
    liste.append(['History', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=47&sort=recently_updated'])
    liste.append(['Horror', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=74&sort=recently_updated'])
    liste.append(['Music', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=199&sort=recently_updated'])
    liste.append(['Mystery', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=64&sort=recently_updated'])
    liste.append(['Reality TV', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=4&sort=recently_updated'])
    liste.append(['Romance', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=23&sort=recently_updated'])
    liste.append(['Sci-Fi', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=15&sort=recently_updated'])
    liste.append(['Sports', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=44&sort=recently_updated'])
    liste.append(['Thriller', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=7&sort=recently_updated'])
    liste.append(['War', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=58&sort=recently_updated'])
    liste.append(['Western', f'{URL_MAIN}/filter?keyword=&type%5B%5D=tv&genre%5B%5D=28&sort=recently_updated'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=25&sort=recently_updated'])
    liste.append(['Adventure', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=17&sort=recently_updated'])
    liste.append(['Animated', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=10&sort=recently_updated'])
    liste.append(['Biography', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=215&sort=recently_updated'])
    liste.append(['Comedy', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=14&sort=recently_updated'])
    liste.append(['Crime', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=26&sort=recently_updated'])
    liste.append(['Drama', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=1&sort=recently_updated'])
    liste.append(['Documentary', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=131&sort=recently_updated'])
    liste.append(['Family', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=43&sort=recently_updated'])
    liste.append(['Fantasy', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=31&sort=recently_updated'])
    liste.append(['History', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=47&sort=recently_updated'])
    liste.append(['Horror', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=74&sort=recently_updated'])
    liste.append(['Music', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=199&sort=recently_updated'])
    liste.append(['Mystery', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=64&sort=recently_updated'])
    liste.append(['Reality TV', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=4&sort=recently_updated'])
    liste.append(['Romance', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=23&sort=recently_updated'])
    liste.append(['Sci-Fi', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=15&sort=recently_updated'])
    liste.append(['Sports', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=44&sort=recently_updated'])
    liste.append(['Thriller', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=7&sort=recently_updated'])
    liste.append(['War', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=58&sort=recently_updated'])
    liste.append(['Western', f'{URL_MAIN}/filter?keyword=&type%5B%5D=movie&genre%5B%5D=28&sort=recently_updated'])

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

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
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

            vrf = getVerid(sId)
            sUrl = f'{URL_MAIN}/ajax/episode/list/{sId}?vrf={vrf}'

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '"display: .+?data-season=([^<]+)>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:

                    sSeason = aEntry.replace('\\','').replace('"','')                  
                    Ss = aEntry.replace('\\','').replace('"','')
                    sDisplaySeason = f"{sSeriesTitle} S{sSeason:02d}"
                    siteUrl = f'{sURL2}/{Ss}-1'
                    sThumb = sThumb
                    sDesc = ''
			
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('SeasonTitle', sDisplaySeason)
                    oOutputParameterHandler.addParameter('sSeriesTitle', sSeriesTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('Ss', Ss)
                    oGui.addSeason(SITE_IDENTIFIER, 'showEps', sDisplaySeason, '', sThumb, sDesc, oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
        
def showEps():
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
            vrf = getVerid(sId)
            sUrl = f'{URL_MAIN}/ajax/episode/list/{sId}?vrf={vrf}'

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
                    
                    nLink = aEntry[0].split("\\")[0]
                    siteUrl = f'{URL_MAIN}{nLink}'
                    sEpisode = aEntry[2].replace('Episode ','').replace(':','')
                    episode = f"{SeasonTitle} E{sEpisode:02d}"

                    sTitle = aEntry[3].replace(':','')                      
                    sDisplayTitle = SeasonTitle + ' - ' + episode + ' - ' + sTitle

                    sId =  aEntry[1].split('\\')[0]
                    vrf = quote(getVerid(sId))

                    siteUrl = f'{URL_MAIN}/ajax/server/list/{sId}?vrf={vrf}'
                    sThumb = sThumb
                    sDesc = ""
			
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
   
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

    sPattern = '<div class="watch".+?data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry
            vrf = getVerid(sId)
            nUrl = f'{URL_MAIN}/ajax/episode/list/{sId}?vrf={vrf}'

            oRequestHandler = cRequestHandler(nUrl)
            sHtmlContent = oRequestHandler.request().replace('\\','')

            sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
            aResult = oParser.parse(sHtmlContent, sPattern)        
            if aResult[0]:
                for aEntry in aResult[1]:

                    sId = aEntry[0]
                    nTitle = aEntry[1]
                    vrf = getVerid(sId)
                    url = f'{URL_MAIN}/ajax/server/list/{sId}?vrf={vrf}'

                    oRequestHandler = cRequestHandler(url)
                    sHtmlContent = oRequestHandler.request().replace('\\','')

                    sPattern = 'data-link-id="([^"]+)".+?<span>(.+?)</span>'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        oOutputParameterHandler = cOutputParameterHandler()
                        for aEntry in aResult[1]:
            
                            sId = aEntry[0].split('\\')[0] 
                            sHost = aEntry[1]
                            sTitle = f'{sMovieTitle} [COLOR coral]{sHost}[/COLOR]'

                            oOutputParameterHandler.addParameter('sId', sId)
                            oOutputParameterHandler.addParameter('nTitle', nTitle)
                            oOutputParameterHandler.addParameter('siteUrl', sUrl)
                            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)
                            oOutputParameterHandler.addParameter('sHost', sHost)

                            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sTitle, oOutputParameterHandler)

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
            sTitle = f'{sMovieTitle} [COLOR coral]{sHost}[/COLOR]'

            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sTitle, oOutputParameterHandler)
                                
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sId = oInputParameterHandler.getValue('sId')
    nTitle = oInputParameterHandler.getValue('nTitle')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sHost = oInputParameterHandler.getValue('sHost')

    vrf = getVerid(sId)

    url = f'{URL_MAIN}/ajax/server/{sId}?vrf={vrf}'
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"url":"([^"]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:

        sId = aResult[0]                             
        url = DecodeLink(sId)

        sHosterUrl = unquote(url)
        SubTitle = ""

        if ('sub.info' in sHosterUrl):
            SubTitle = sHosterUrl.split('sub.info=')[1]
            sHosterUrl = sHosterUrl.split('&sub.info')[0]
        if 'Vidplay' in sHost:
            oHoster = cHosterGui().getHoster('mcloud')     
        else:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            if ('http' in SubTitle):
                sHosterUrl = f'{sHosterUrl}?sub.info={SubTitle}'
            else:
                sHosterUrl = sHosterUrl
            if nTitle:
                sDisplayTitle = f'{nTitle} {sMovieTitle}'
            else:
                sDisplayTitle = sMovieTitle
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

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
###### 12.07.23     
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
    
    
    def butxx(t):
        o=''
        for s in range(len(t)):
            u = ord(t[s]) 
            if u==0:
                u=0
            else:
                if (s % 6 == 1):
                    u += 5
                else:
                    if (s % 6 == 5):
                        u -= 6
                    else:
                        if (s % 6 == 0 or s % 6 == 4):
                            u += 6
                        else:
                            if not (s % 6 != 3 and s % 6 != 2):
                                u -= 5
            o += chr(u) 
            
    def but(t):
    
        o=''
        for s in range(len(t)):
            u = ord(t[s]) 
            if u==0:
                u=0
            else:
                if s%8 ==2:
                    u -= 2
                else:
                    if (s % 8 == 4 or s % 8 == 7):
                        u += 2;
                    else:
                        if s % 8 == 0 :
                            u += 4;
                        else:
                            if (s % 8 == 5 or s % 8 == 6):
                                u -= 4
                            else:
                                if (s % 8 == 1):
                                    u += 3
                                else:
                                    if (s % 8 == 3):
                                        u += 5
    
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
    
    ab = 'Ij4aiaQXgluXQRs6'

    hj = dec2(ab,id) 
    if sys.version_info >= (3,0,0):
        hj=hj.encode('Latin_1')  
    id = encode2(hj)
    
    if sys.version_info >= (3,0,0):
        id = id.decode('utf-8')
    id = id.replace('/','_').replace('+','-')
    
    if sys.version_info >= (3,0,0):
        id = id.encode('Latin_1')  
        
    id = encode2(id)    
    if sys.version_info >= (3,0,0):
        id = id.decode('utf-8')
    id = id.replace('/','_').replace('+','-')   

    if sys.version_info >= (3,0,0):
        id=(''.join(reversed(id)))
        id = id.encode('Latin_1') 
    else:
        id=(''.join((id)[::-1]))
    id = encode2(id)
    if sys.version_info >= (3,0,0):
        id = id.decode('utf-8')
    id = id.replace('/','_').replace('+','-')
    
    
    xc= but(id) 
    
    return xc