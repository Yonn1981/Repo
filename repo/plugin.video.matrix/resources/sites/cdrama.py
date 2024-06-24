#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re
 
SITE_IDENTIFIER = 'cdrama'
SITE_NAME = 'Cdrama'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_ASIAN = (f'{URL_MAIN}category/الأفلام-الاسيوية-asian-movies/', 'showMovies')

SERIE_KR = (f'{URL_MAIN}category/الدراما-الكورية-kdrama/', 'showSeries')
SERIE_CN = (f'{URL_MAIN}category/دراما-الصينية-chinese-drama/', 'showSeries')
SERIE_JP = (f'{URL_MAIN}category/الدراما-اليابانية-japanese-drama/', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}category/الدراما-الكورية-kdrama/', 'showSeries')

FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30330), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'الدراما الكورية', 'asia.png', oOutputParameterHandler)   

    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], 'مسلسلات كورية', 'kr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CN[1], 'مسلسلات صينية', 'cn.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_JP[1], 'مسلسلات يابانية', 'jp.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/درامات-آخرى-other-dramas/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'درامات آخرى', 'asia.png', oOutputParameterHandler)   

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/ترجماتنا-الحصرية-our-exclusive-translation/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'ترجماتنا الحصرية', 'asia.png', oOutputParameterHandler)    

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/البرامج-الأسيوية-asian-program/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'البرامج الأسيوية', 'brmg.png', oOutputParameterHandler)         
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}/movies-categories/{sSearchText}'
        showMovies(sUrl)
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

    sPattern = '<div class=["\']img["\']>.+?<img src=["\']([^"\']+)["\'].+?alt=["\']([^"\']+)["\'].+?<a href=["\']([^"\']+)["\']'
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
            siteUrl = aEntry[2]
            sThumbnail = aEntry[0]
            sInfo = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

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

    sPattern = '<div class=["\']img["\']>.+?<img src=["\']([^"\']+)["\'].+?alt=["\']([^"\']+)["\'].+?<a href=["\']([^"\']+)["\']'
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
            siteUrl = aEntry[2]
            sThumbnail = aEntry[0]
            sInfo = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '</div><h4.+?href="([^<]+)">([^<]+)</a> </h4>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("والاخيرة","").replace("الاخيرة","")
            siteUrl = aEntry[0]
            sInfo = ""
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
               
    oGui.setEndOfDirectory()
	  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = ''
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
              
    sPattern = "data-url='([^<]+)'>"
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
        
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = f'https:{url}'
				           
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)				
                
    oGui.setEndOfDirectory()