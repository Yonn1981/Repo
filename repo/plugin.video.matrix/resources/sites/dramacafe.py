# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib import random_ua

UA = random_ua.get_ua()
	
SITE_IDENTIFIER = 'dramacafe'
SITE_NAME = 'Dramacafe'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_AR = (URL_MAIN + 'category.php?cat=aflam-araby1', 'showMovies')
MOVIE_EN = (URL_MAIN + 'category.php?cat=aflam-agnaby', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category.php?cat=aflam-hindi', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category.php?cat=asian-movies', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category.php?cat=Turkish-Movies', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + 'category.php?cat=Dubbed-Movies', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category.php?cat=aflam-cartoon', 'showMovies')

RAMADAN_SERIES = (URL_MAIN + 'category.php?cat=ramadan-2024', 'showSeries')
SERIE_EN = (URL_MAIN + 'category.php?cat=moslslat-agnaby', 'showSeries')
SERIE_AR = (URL_MAIN + 'category.php?cat=moslslat-arabia', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category.php?cat=moslslat-hindia', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category.php?cat=moslslat-asia', 'showSeries')
SERIE_TR = (URL_MAIN + 'category.php?cat=moslslat-turkya', 'showSeries')
SERIE_DUBBED = (URL_MAIN + 'category.php?cat=moslslat-modablaja', 'showSeries')
KID_CARTOON = (URL_MAIN + 'category.php?cat=anime-arabic', 'showSeries')

REPLAYTV_PLAY = (URL_MAIN + 'category.php?cat=masr7eyat', 'showMovies')
REPLAYTV_NEWS = (URL_MAIN + 'category.php?cat=tv-programs', 'showSeries')

URL_SEARCH = (URL_MAIN + 'search.php?keywords=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?keywords=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search.php?keywords=', 'showSeries')

FUNCTION_SEARCH = 'showSeries'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', 'rmdn.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام مدبلجة', 'mdblg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdblg.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)
	  
    oGui.setEndOfDirectory()

 
def showSearch():
    oGui = cGui() 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search.php?keywords=فيلم+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search.php?keywords=مسلسل+'+sSearchText
        showSeries(sUrl)
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

    sPattern = '<div class="thumbnail">.+?<a href="([^"]+)" title="([^"]+)".+?data-echo="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'مسلسل' in aEntry[1] or 'موسم' in aEntry[1]:
               continue

            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<div class="thumbnail">.+?<a href="([^"]+)" title="([^"]+)".+?data-echo="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    itemList = []
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'فيلم' in aEntry[1] or 'فلم' in aEntry[1]:
               continue 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]           
            sTitle = sTitle.split('الحلقة')[0]
            sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch: 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

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

    sPattern = '<h1 class="title">(.+?)</h1>' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        sTitleSeries = aResult[1][0]

    sPattern = 'onclick=["\']openCity.+?["\'].+?>(.+?)</button>'    
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:

            sID = aEntry.replace("الموسم ","")
            sTitle = f'{sTitleSeries} {aEntry.replace("الموسم ","S")}'
            siteUrl = sUrl
            sDesc = ''
            sThumb = sThumb
            sYear = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('SeasonID', sID)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    SeasonID = oInputParameterHandler.getValue('SeasonID')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = f'id="Season{SeasonID}"'
    sEnd = '</div>'
    sHtmlContent2 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href=["\']([^"\']+)["\']><li><em>(.+?)</em>'
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            
            sTitle = sMovieTitle+' E'+aEntry[1]
            siteUrl = URL_MAIN+aEntry[0]
            if '?post=' in siteUrl:
                url_tmp = siteUrl.split('?post=')[-1].replace('%3D','=')
                siteUrl = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="active">.+?href="#".+?href="([^"]+)'	
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
    sHtmlContent = oRequestHandler.request()
            
    sPattern = '<a id="play-video" class="video-play-button" href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        m3url = aResult[1][0]
        oRequestHandler = cRequestHandler(m3url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request() 

    sPattern = 'name="isFormServs" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        m3url = aResult[1][0]
        sHtmlContent = base64.b64decode(m3url).decode('utf8',errors='ignore').replace('\\','')

    sPattern = '"([^"]+)":"([^"]+)' 
    aResult = re.findall(sPattern, sHtmlContent)	
    if aResult:
        for aEntry in aResult:
            if 'home' in aEntry[0] or 'back' in aEntry[0]:
                continue        
            url = aEntry[1]
            if url.startswith('//'):
               url = 'http:' + url
			           
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = 'data-embed-url=["\']([^"\']+)["\']' 
    aResult = re.findall(sPattern, sHtmlContent)	
    if aResult:
        for aEntry in aResult:            
            url = aEntry
            if url.startswith('//'):
               url = 'http:' + url
			           
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = '<iframe src=["\']([^"\']+)["\']' 
    aResult = re.findall(sPattern, sHtmlContent)	
    if aResult:
        for aEntry in aResult:            
            url = aEntry
            if url.startswith('//'):
               url = 'http:' + url
			           
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()
                
   
