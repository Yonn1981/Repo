# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_random_ua()

SITE_IDENTIFIER = 'bahyfilm'
SITE_NAME = 'BahyFilm'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'section.php?sidebarID=11', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'section.php?sidebarID=15', 'showMovies')
MOVIE_HI = (URL_MAIN + 'section.php?sidebarID=12', 'showMovies')
KID_MOVIES = (URL_MAIN + 'section.php?sidebarID=8', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'section.php?sidebarID=11', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')
MOVIE_ANNEES = (URL_MAIN , 'showYears')

SERIE_EN = (URL_MAIN + 'series/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/', 'showSeries')
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'أفلام بالسنة', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<ul class="menu"'
    sEnd = '<button class'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?<li>(.+?)</li>'
    aResult = oParser.parse(sHtmlContent1, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'soon' in aEntry[0] or 'alt=' in aEntry[1]:
                continue 
            sTitle = aEntry[1]
            siteUrl = URL_MAIN + aEntry[0]
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', '', '', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<ul class="menu">'
    sEnd = '<button class='
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent1, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'soon' in aEntry[0]:
                continue 
            sTitle = aEntry[2]
            siteUrl = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]

			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'film.png', sThumb, '', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
			
def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser() 

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch or '?s=' in sUrl:
        sUrl = sSearch
        squery = sUrl.split('?s=')[1]

        oRequestHandler = cRequestHandler(URL_MAIN + 'search_suggestion.php')
        oRequestHandler.addHeaderEntry('Accept', '*/*')
        oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        oRequestHandler.addHeaderEntry('Origin', getHost(sUrl))
        oRequestHandler.addParameters('query', squery)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<a href="([^"]+)".+?<img src="([^"]+)".+?class="suggestion-name">(.+?)</span>'

    else:

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
        oRequestHandler.addHeaderEntry('Origin', getHost(sUrl))
        sHtmlContent = oRequestHandler.request()

        sPattern = '<div class="card">\s*<a href="([^"]+)".+?src="([^"]+)".+?alt="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)
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

            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = URL_MAIN + aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sDesc = sYear

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
    
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sStart = '<a class="current-page"'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    page_links = re.findall(r'class="page-link" href=["\']([^"\']+)', sHtmlContent)

    for link in (page_links[:2] + page_links[-2:]):
        oOutputParameterHandler = cOutputParameterHandler()  
        sTitle = "PAGE " + link.split('page=')[1]
        sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
        siteUrl = URL_MAIN + 'section.php' + link

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    oParser = cParser() 

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch or '?s=' in sUrl:
        sUrl = sSearch
        squery = sUrl.split('?s=')[1]

        oRequestHandler = cRequestHandler(URL_MAIN + 'search_suggestion.php')
        oRequestHandler.addHeaderEntry('Accept', '*/*')
        oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        oRequestHandler.addHeaderEntry('Origin', getHost(sUrl))
        oRequestHandler.addParameters('query', squery)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<a href="([^"]+)".+?<img src="([^"]+)".+?class="suggestion-name">(.+?)</span>'

    else:

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
        oRequestHandler.addHeaderEntry('Origin', getHost(sUrl))
        sHtmlContent = oRequestHandler.request()

        sPattern = '<div class="card">\s*<a href="([^"]+)".+?data-src="([^"]+)".+?alt="([^"]+)'

    itemList = []	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/watch' in aEntry[0]:
                continue

            sTitle = cUtil().CleanSeriesName(aEntry[2])
            siteUrl = aEntry[0]
            if 'http' not in siteUrl:
                siteUrl = f'{URL_MAIN}series/{aEntry[0]}'
            sThumb = aEntry[1].replace("(","").replace(")","")
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sDesc = sYear

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
    
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sStart = '<a class="current-page"'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    page_links = re.findall(r'class="page-link" href=["\']([^"\']+)', sHtmlContent)

    for link in (page_links[:2] + page_links[-2:]):
        oOutputParameterHandler = cOutputParameterHandler()  
        sTitle = "PAGE " + link.split('page=')[1]
        sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
        siteUrl = URL_MAIN + 'section.php' + link

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sDesc = ""
    sPattern = '<p>(.+?</p>)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]

    sPattern = '<div class="episode-section">.+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        nUrl = f'{URL_MAIN}series/{aResult[1][0]}'

    else:
        sPattern = 'data-dropdown.+?href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            nUrl = f'{URL_MAIN}series/{aResult[1][0]}'

    oRequestHandler = cRequestHandler(nUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="seasons-episodes">'
    sEnd = '<div class="footer">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'data-dropdown=".+?">(.+?)<i class(.+?)</ul>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            sSeason = aEntry[0].replace('الموسم ','S')
            sHtmlContent = aEntry[1]

            sPattern = 'href="([^"]+)">(.+?)</li>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
 
                    siteUrl = URL_MAIN +aEntry[0]
                    sEp = aEntry[1].replace('الحلقة ','')
                    sTitle = f'{sMovieTitle} {sSeason} E{sEp}'
                    sThumb = sThumb
			
                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'episode' not in sUrl:
        movie_id = base64.b64decode(sUrl.split('?id=')[1]).decode('utf8',errors='ignore')
        slink = URL_MAIN + 'getlinks.php'
    else:
        episode_id = base64.b64decode(sUrl.split('&episode=')[1]).decode('utf8',errors='ignore')
        slink = f'{URL_MAIN}series/getepisodelink.php'

    oRequestHandler = cRequestHandler(slink)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addHeaderEntry('Origin', getHost(sUrl))
    if 'episode' not in sUrl:
        oRequestHandler.addParameters('movie_id', movie_id)
    else:
        oRequestHandler.addParameters('episode_id', episode_id)
    oRequestHandler.addParameters('bypasscf', '1')
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    for sResolution, sLink in sHtmlContent.items():
        sQual = sResolution
        sHosterUrl = sLink

        sDisplayTitle = ('%s [COLOR coral] (%sp) [/COLOR]') % (sMovieTitle, sQual) 

        if 'mp4' in sHosterUrl:
            sHosterUrl = sLink + '|User-Agent=' + UA + '&Referer=' + sUrl
            oHoster = cHosterGui().getHoster('lien_direct')
        else:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()  

def getHost(url):
    parts = url.split('//', 1)
    host = parts[0] + '//' + parts[1].split('/', 1)[0]
    return host