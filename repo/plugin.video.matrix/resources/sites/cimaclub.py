# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import Unquote, cUtil
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'cimaclub'
SITE_NAME = 'CimaClub'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
 
MOVIE_EN = (URL_MAIN + 'category/أفلام/افلام-اجنبي/', 'showMovies')
MOVIE_AR = (URL_MAIN + 'category/أفلام/افلام-عربى/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/أفلام/افلام-هندى/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/أفلام/افلام-تركى/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/افلام-كرتون/', 'showMovies')
DOC_NEWS = (URL_MAIN + 'category/أفلام/افلام-وثائقية/', 'showMovies')

SERIE_HI = (URL_MAIN + 'category/مسلسلات/مسلسلات-هندية/', 'showSerie')
SERIE_AR = (URL_MAIN + 'category/مسلسلات/مسلسلات-عربية/', 'showSerie')
SERIE_TR = (URL_MAIN + 'category/مسلسلات/مسلسلات-تركية/', 'showSerie')
SERIE_ASIA = (URL_MAIN + 'category/مسلسلات/مسلسلات-اسيوية/', 'showSerie')
SERIE_EN = (URL_MAIN + 'category/مسلسلات-اجنبي/', 'showSerie')
RAMADAN_SERIES = (URL_MAIN + 'category/مسلسلات/مسلسلات-رمضان-2024/', 'showSerie')
KID_CARTOON = (URL_MAIN + 'category/مسلسلات-كرتون/', 'showSerie')

DOC_SERIES = (URL_MAIN + 'category/مسلسلات/مسلسلات-وثائقية/', 'showSerie')
SPORT_WWE = (URL_MAIN + 'category/مصارعة-حرة/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?s=', 'showSerie')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات رمضان', 'rmdn.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
      
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات هندية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات كرتون', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s='+sSearchText
        showSerie(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s='+sSearchText
        showSerie(sUrl)
        oGui.setEndOfDirectory()
        return

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

    sPattern = '<div class="content-box">\s*<a href="([^"]+)" title="([^"]+)".+?img src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0] + 'see/'
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([1-2][0-9]{3})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    sPattern = 'class="page-numbers" href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<div class="content-box">\s*<a href="([^"]+)" title="([^"]+)".+?img src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    itemList = []	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/series' in aEntry[0]:
                continue

            sTitle = cUtil().CleanSeriesName(aEntry[1])  
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle) 
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    sPattern = 'class="page-numbers" href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0]
            sThumb = ""
            sDesc = ""

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', sTitle, 'next.png', oOutputParameterHandler)
         
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<h2>الحلقات</h2>'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    aResult = re.findall('href="([^<]+)">(.+?)</a>', sHtmlContent)
    if aResult:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult:
            siteUrl = aEntry[0] + 'see/'
            sTitle = Unquote(cUtil().CleanMovieName((aEntry[0]).rsplit("/")[3]))
            sTitle = sTitle.replace('موسم-','S').replace('حلقة-','E').replace('-',' ')
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
		
def showServers(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    sHtmlContent = oRequestHandler.request()

    sReferer = sUrl.split('/see')[0]

    sPattern = '"item":"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:      
        sReferer = aResult[1][0]

    sPattern = 'data-embed="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
					            
                    sHosterUrl = aEntry
                    if 'nowvid' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer
                    if 'kvid' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer    
                    if 'darkveed' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer 
                    if 'telvod' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = sMovieTitle
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
       	
    sPattern = 'rel="nofollow" href="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:

            sTitle = f'{sMovieTitle} [{aEntry[1]}]'         
            url = aEntry[0]
            if '?get=' in url:
                import base64
                url_tmp = url.split('?get=')[1].replace('%3D','=')
                url = base64.b64decode(url_tmp).decode('utf8',errors='ignore')

            if url.startswith('//'):
                url = 'http:' + url				
            
            sHosterUrl = url
            if '.shop' in sHosterUrl:
                sHosterUrl = sHosterUrl + '|User-Agent=' + UA + '&Referer=' + siteManager().getUrlMain('wecima')
            oHoster = cHosterGui().getHoster('lien_direct')  
            if oHoster:
               sDisplayTitle = sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    
    oGui.setEndOfDirectory()	
    