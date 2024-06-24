# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
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

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'bazplay'
SITE_NAME = 'BazPlay'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_TR = (f'{URL_MAIN}category/مسلسلات-تركية/', 'showSeries')
MOVIE_TURK = (f'{URL_MAIN}movies', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}search/', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search/', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}episodes/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries2', 'احدث الحلقات', 'turk.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
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

    sPattern = '<article class="post">.+?href="([^"]+)" title=.+?style="([^"]+)".+?<div class="title">(.+?)</div>' 
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[2]:
                continue
 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = re.sub(r'-\d*x\d*.','.', aEntry[1]).replace('background-image:url(','').replace(');','')
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_) 

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

    itemList = []	
    sPattern = '<div class="block-post">.+?<a href="([^<]+)" title="([^<]+)">.+?data-img="([^<]+)" title='
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[2]:
                continue
 
            sTitle = (cUtil().CleanSeriesName(aEntry[1])).replace('- قصة عشق','')
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace("(","").replace(")","")
            sDesc = ""

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries2(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="block-post">.+?<a href="([^<]+)" title="([^<]+)">.+?data-img="([^<]+)" title='
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[2]:
                continue
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace("(","").replace(")","")
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries2', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

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
    
    sPattern = 'data-season="(.+?)">(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            siteUrl = f'{URL_MAIN}wp-content/themes/vo2023/temp/ajax/seasons.php?seriesID={aEntry[0]}'
            sTitle = f'{sMovieTitle} {cUtil().ConvertSeasons(aEntry[1]).split("الحلقة")[0]}'
            sThumb = sThumb
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('siteUrl0',sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)	

    else:
        sPattern = '<a class="epNum" href="([^"]+)" title="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
                sTitle =  f'{sMovieTitle} {aEntry[1].replace("الحلقة","E").replace("الموسم","S")}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sPattern = '<a class="epNum.+?" href="([^"]+)" title="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
                sTitle =  f'{sMovieTitle} {aEntry[1].replace("الحلقة","E").replace("الموسم","S")}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:       
        return aResult[1][0]

    else:
        sPattern = "<span class='current'>.+?<a href='([^']+)"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:       
            return aResult[1][0]

    return False 

def showEps():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl0 = oInputParameterHandler.getValue('siteUrl0')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl0)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sCode = sUrl.split('seriesID=')[1]

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl0.encode('utf8'))
    oRequestHandler.addParameters('seriesID', sCode)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = f'{sMovieTitle} E{aEntry[1]}'
            siteUrl = aEntry[0] 
            sThumb = sThumb
            sDesc = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    oGui.setEndOfDirectory() 

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern =  '<form method="post" action="([^"]+)".+?name="watch" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            wcode = aEntry[1]
            sLink = aEntry[0]

            oRequestHandler = cRequestHandler(sLink)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
            oRequestHandler.addParameters('watch', wcode)
            oRequestHandler.addParameters('submit', '')
            oRequestHandler.setRequestType(1)
            sHtmlContent = oRequestHandler.request()

    sPattern =  '<form method="post" action="([^"]+)".+?name="watch" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            wcode = aEntry[1]
            sLink = aEntry[0]

            oRequestHandler = cRequestHandler(sLink)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
            oRequestHandler.addParameters('watch', wcode)
            oRequestHandler.addParameters('submit', '')
            oRequestHandler.setRequestType(1)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'data-src=["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent, sPattern)
            itemList = []
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                for aEntry in (aResult[1]):
     
                    sHosterUrl = aEntry
                    if sHosterUrl not in itemList:
                        itemList.append(sHosterUrl)

                        if 'leech' in aEntry:
                            continue
                        if sHosterUrl.startswith('//'):
                            sHosterUrl = 'http:' + sHosterUrl
                        if 'megamax' in sHosterUrl:
                            data = cMegamax().GetUrls(sHosterUrl)
                            if data is not False:
                                for item in data:
                                    sHosterUrl = item.split(',')[0].split('=')[1]
                                    sQual = item.split(',')[1].split('=')[1]
                                    sLabel = item.split(',')[2].split('=')[1]

                                    sDisplayTitle = f'{sMovieTitle} ({sQual}) [COLOR coral]{sLabel}[/COLOR]'     
                                    oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                                    oOutputParameterHandler.addParameter('sQual', sQual)
                                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                    oOutputParameterHandler.addParameter('sThumb', sThumb)

                                    oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
 
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster != False:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showLinks():
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