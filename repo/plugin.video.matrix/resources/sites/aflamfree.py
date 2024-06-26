﻿# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/
import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon

SITE_IDENTIFIER = 'aflamfree'
SITE_NAME = 'Aflamfree'
SITE_DESC = 'arabic vod'	 
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9', 'showLive')
MOVIE_AR = (f'{URL_MAIN}category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9', 'showLive')
MOVIE_HI = (f'{URL_MAIN}category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9', 'showLive')
MOVIE_ASIAN = (f'{URL_MAIN}category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9', 'showLive')
KID_MOVIES = (f'{URL_MAIN}category/%d9%83%d8%a7%d8%b1%d8%aa%d9%88%d9%86-%d9%88%d8%a7%d9%86%d9%85%d9%8a', 'showLive')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMoviesearch')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMoviesearch')
FUNCTION_SEARCH = 'showMoviesearch'

def load():
	oGui = cGui()
	addons = addon()

	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
	oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

	oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
	oGui.addDir(SITE_IDENTIFIER, 'showLive', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
	oGui.addDir(SITE_IDENTIFIER, 'showLive', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
	oGui.addDir(SITE_IDENTIFIER, 'showLive', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
	oGui.addDir(SITE_IDENTIFIER, 'showLive', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
	oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
	oGui.addDir(SITE_IDENTIFIER, 'showLive', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

	oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}%D8%A7%D9%82%D8%B3%D8%A7%D9%85-%D8%A7%D9%84%D9%85%D9%88%D9%82%D8%B9')
	oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'film.png', oOutputParameterHandler)

	oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'أفلام (بالسنوات)', 'annees.png', oOutputParameterHandler)

	oGui.setEndOfDirectory()

def showYears():
    import datetime
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1921, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}release-year/' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showLive', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
	
def showSearch():
	oGui = cGui()
	 
	sSearchText = oGui.showKeyBoard()
	if sSearchText:
		sUrl = f'{URL_MAIN}?s='+sSearchText
		showMoviesearch(sUrl)
		oGui.setEndOfDirectory()
		return
   
def showMoviesearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<a href="([^<]+)"><div class="image"><img src="([^<]+)" alt="([^<]+)" /><span class="player"></span><span class="imdb"><b><b class="icon-star"></b></b>([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1] 
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
            sDesc = '' 
						
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showLive2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
			
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showPack(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'style="font-size: large;"><a href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            siteUrl = f'{aEntry[0].replace(".top",".one")}/page/1'
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showLive', sTitle, 'film.png', oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "href='([^<]+)'>.+?Next"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        aResult = aResult[1][0]
        return aResult

    return False 
   
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^<]+)"><div class="image"><img src="([^<]+)" alt="([^<]+)" /><span class="player"></span><span class="imdb"><b><b class="icon-star"></b></b>([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]: 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLive2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)        

    sPattern = '<a href="([^<]+)"><div class="image"><img src="([^<]+)" alt="([^<]+)" /><span class="player"></span></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1] 
            sDesc = "" 
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLive2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    page = '1'      
    if 'page' in sUrl:   
        page = sUrl.split('/page/')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('/page/')[0]
    siteUrl = siteUrl +'/page/'+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oGui.addDir(SITE_IDENTIFIER, 'showLive', sTitle,'next.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
  
def showLive2():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  
    sPattern = '<div id="([^<]+)"> <IFRAME SRC="([^<]+)" webkitAllowFullScreen mozallowfullscreen'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        for aEntry in aResult[1]:					
            sTitle = aEntry[0] 
            siteUrl = aEntry[1].replace("r.php?url","r2.php?url") 
    
            oRequestHandler = cRequestHandler(siteUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'source: "([^<]+)", parentId: "#player"'
            aResult1 = re.findall(sPattern, sHtmlContent)
            sPattern = 'content="0; url=([^<]+)" />'
            aResult2 = re.findall(sPattern, sHtmlContent)
            aResult = aResult1 + aResult2
	
            if aResult:
               for aEntry in aResult:       
                   url = aEntry
                   url = url.replace("scrolling=no","")
                   if url.startswith('//'):
                      url = 'http:' + url
								           
                   sHosterUrl = url 
                   if 'userload' in sHosterUrl:
                      sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
                   if 'mystream' in sHosterUrl:
                      sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}' 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       
    oGui.setEndOfDirectory()