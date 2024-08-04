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
from Cryptodome.Cipher import ARC4
from urllib.parse import unquote, quote, urlparse

SITE_IDENTIFIER = 'cinezone'
SITE_NAME = 'CineZone'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

key = "VmSazcydpguRBnhG"

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

    sPattern = '<div class="item">.+?<a href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'
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

    sPattern = '<div class="item">.+?<a href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'
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

    sPattern = 'data-id="(.+?)" data-season='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry

            vrf = vrf_encrypt(sId)
            sUrl = f'{URL_MAIN}/ajax/episode/list/{sId}?vrf={vrf}'

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '"display: .+?data-season=([^<]+)>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:

                    sSeason = int(aEntry.replace('\\','').replace('"',''))           
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

    sPattern = 'data-id="(.+?)" data-season='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sId = aEntry
            vrf = vrf_encrypt(sId)
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
       
            sPattern = '<a href="([^"]+)" data-id="([^"]+)".+?data-num="([^"]+)".+?<span>(.+?)</span>' 
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[1]:
                oOutputParameterHandler = cOutputParameterHandler()   
                for aEntry in aResult[1]:
                    
                    nLink = aEntry[0].split("\\")[0]
                    siteUrl = f'{URL_MAIN}{nLink}'
                    sEpisode = int(aEntry[2].replace('Episode ','').replace(':',''))
                    episode = f"{SeasonTitle} E{sEpisode:02d}"

                    sTitle = aEntry[3].replace(':','')                      
                    sDisplayTitle = SeasonTitle + ' - ' + episode + ' - ' + sTitle

                    sId =  aEntry[1].split('\\')[0]
                    vrf = quote(vrf_encrypt(sId))

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

    sPattern = 'data-id="(.+?)" data-season='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sId = aEntry
            vrf = vrf_encrypt(sId)
            nUrl = f'{URL_MAIN}/ajax/episode/list/{sId}?vrf={vrf}'

            oRequestHandler = cRequestHandler(nUrl)
            sHtmlContent = oRequestHandler.request().replace('\\','')

            sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
            aResult = oParser.parse(sHtmlContent, sPattern)        
            if aResult[0]:
                for aEntry in aResult[1]:

                    sId = aEntry[0]
                    nTitle = aEntry[1]
                    vrf = vrf_encrypt(sId)
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

    vrf = vrf_encrypt(sId)

    url = f'{URL_MAIN}/ajax/server/{sId}?vrf={vrf}'
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"url":"([^"]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:

        sId = aResult[0]                             
        url = vrf_decrypt(sId)

        sHosterUrl = unquote(url)
        SubTitle = ""

        if ('sub.info' in sHosterUrl):
            SubTitle = sHosterUrl.split('sub.info=')[1]
            sHosterUrl = sHosterUrl.split('&sub.info')[0]
        if 'F2Cloud' in sHost or 'MegaCloud' in sHost:
            oHoster = cHosterGui().getHoster('mcloud')  
        elif '.xyz' in sHosterUrl:
            oHoster = cHosterGui().getHoster('filemoon')    
        else:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            if ('http' in SubTitle):
                sHosterUrl = f'{sHosterUrl}$sub.info={SubTitle}'
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

def getKeys():
    oRequestHandler = cRequestHandler("https://raw.githubusercontent.com/Yonn1981/Repo/master/repo/plugin.video.matrix/resources/extra/keys.json")
    res = oRequestHandler.request(jsonDecode=True)
    if res is not None:
        keys = (res["Cinezone"][0], res["Cinezone"][1])
    else:
        raise Exception("Unable to fetch keys")
    return keys

def vrf_encrypt(input: str) -> str:
        key = getKeys()
        cipher = ARC4.new(key[0].encode())
        vrf = cipher.encrypt(input.encode())
        vrf_base64 = base64.urlsafe_b64encode(vrf).decode('utf-8')
        string_vrf = quote(vrf_base64)
        return string_vrf

def vrf_decrypt(input: str) -> str:
        key = getKeys()
        vrf_base64 = unquote(input)
        vrf = base64.urlsafe_b64decode(vrf_base64.encode('utf-8'))

        cipher = ARC4.new(key[1].encode())
        decrypted_vrf = cipher.decrypt(vrf)
        return decrypted_vrf.decode('utf-8')

def rot13(vrf: bytes) -> bytes:
        transformed = bytearray(vrf)
        for i in range(len(transformed)):
            byte = transformed[i]
            if b'A' <= byte <= b'Z':
                transformed[i] = ((byte - b'A' + 13) % 26 + b'A')[0]
            elif b'a' <= byte <= b'z':
                transformed[i] = ((byte - b'a' + 13) % 26 + b'a')[0]
        return bytes(transformed)

def vrf_shift(vrf: bytes) -> bytes:
        transformed = bytearray(vrf)
        shifts = [4, 3, -2, 5, 2, -4, -4, 2]
        for i in range(len(transformed)):
            shift = shifts[i % 8]
            transformed[i] = (transformed[i] + shift) % 256
        return bytes(transformed)

def get_base_url(url: str) -> str:
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"