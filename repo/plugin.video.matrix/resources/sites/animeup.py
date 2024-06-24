# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import requests
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cMegamax
from resources.lib import random_ua

UA = random_ua.get_random_ua()

SITE_IDENTIFIER = 'animeup'
SITE_NAME = 'Anime4up'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_NEWS = (f'{URL_MAIN}episode/', 'showSeries')
ANIM_MOVIES = (f'{URL_MAIN}anime-type/movie-3/', 'showMovies')
ANIM_SUB = (f'{URL_MAIN}anime-category/%d8%a7%d9%84%d8%a7%d9%86%d9%85%d9%8a-%d8%a7%d9%84%d9%85%d8%aa%d8%b1%d8%ac%d9%85/', 'showSeries')
ANIM_DUBBED = (f'{URL_MAIN}anime-category/%d8%a7%d9%84%d8%a7%d9%86%d9%85%d9%8a-%d8%a7%d9%84%d9%85%d8%af%d8%a8%d9%84%d8%ac/', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}?search_param=animes&s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?search_param=animes&s=', 'showMovies')
URL_SEARCH_ANIMS = (f'{URL_MAIN}?search_param=animes&s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أحدث الأفلام', 'anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', ANIM_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'انمي مدبلج', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SUB[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'انمي مترجم', 'anime.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
             
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?search_param=animes&s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?search_param=animes&s={sSearchText}'
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

    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?href="([^<]+)" class="overlay"></a>'
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
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            sTitle = re.sub('[^a-zA-Z0-9]', ' ', sTitle)
            siteUrl = aEntry[2]
            sThumb = aEntry[0]
            sYear = ""
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?href="([^<]+)" class="overlay"></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[2]
            sThumb = aEntry[0]
            sYear = ""
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
    
    sStart = '<h3>حلقات الأنمي</h3>'
    sEnd = '<div class="footer">'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)  

    sPattern = '<h3><a href="([^<]+)">([^<]+)</a></h3>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الحلقة ","").replace("حلقة ","").replace("الأخيرة","")
            sTitle = f'{sMovieTitle} E{sTitle}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)        
		
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    else:
        sStart = '<div class="all-episodes">'
        sEnd = '<div class="form-group">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)    

        sPattern = 'href="([^<]+)">([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = aEntry[1].replace("الحلقة ","").replace("حلقة ","").replace("الأخيرة","")
                sTitle = f'{sMovieTitle} E{sTitle}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ""		

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:      
        return aResult[1][0]

    return False

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'method="post" action="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        rURL = aResult[1][0]

    sPattern = 'name="ur" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sRefer = aResult[1][0]

    sPattern = 'name="wl" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sWatch = aResult[1][0]

    sPattern = 'name="dl" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sDown = aResult[1][0]

    s = requests.Session()  
    headers = {'User-Agent': UA,
				'Referer': URL_MAIN,
                'Origin': URL_MAIN.rsplit('/', 1)[0],
				'Sec-Fetch-Site': 'cross-site',
				'Sec-Fetch-Dest': 'document',
				'Sec-Fetch-Mode': 'navigate',
                'Upgrade-Insecure-Requests':'1'}
    data = {'ur':sRefer,'wl':sWatch,'dl':sDown,'submit':'submit'}
    r = s.post(rURL, headers=headers, data = data)
    sHtmlContent1 = r.content.decode('utf8') 

    sPattern = 'data-ep-url="([^"]+)">(.+?)</a>' 
    aResult = re.findall(sPattern, sHtmlContent1)
    if aResult:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult:
            if 'leech' in aEntry[0]:
                continue
            
            url = aEntry[0].replace('/d/','/f/')
            if url.startswith('//'):
                url = f'http:{url}'
            sLabel = aEntry[1]
            sHosterUrl = url
            if 'megamax' in sHosterUrl:
                data = cMegamax().GetUrls(sHosterUrl)
                if data is not False:
                    for item in data:
                        sHosterUrl = item.split(',')[0].split('=')[1]
                        sQual = item.split(',')[1].split('=')[1]
                        sLabel = item.split(',')[2].split('=')[1]

                        sTitle = f'{sMovieTitle} ({sQual}) [COLOR coral]{sLabel}[/COLOR]'    
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sTitle, oOutputParameterHandler)
            else:
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sLabel}][/COLOR]'   
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sStart = '<div class="tab-content"'
    sEnd = '<div class="container">'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li>(.+?)</li>(.+?)</ul>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :  
        for aEntry in reversed(aResult[1]):
            sQual = aEntry[0].replace("الجودة المتوسطة","").replace("الجودة العالية","").replace("الجودة الخارقة","").strip()
            sHtmlContent = aEntry[1]

            sPattern = 'href="([^"]+)">(.+?)</a>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                for aEntry in aResult[1]:   
                    if 'megamax' in aEntry:
                        continue      
                    url = aEntry[0]
                    if url.startswith('//'):
                        url = f'http:{url}'

                    sHosterUrl = url
                    sDisplayTitle = f'{sMovieTitle} [COLOR coral] {sQual}] [/COLOR]' 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:  
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()	

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()