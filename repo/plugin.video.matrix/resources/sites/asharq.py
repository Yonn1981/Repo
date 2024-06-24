# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'asharq'
SITE_NAME = 'Al-Sharq'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

DOC_NEWS = (f'{URL_MAIN}/doc', 'showMovies')
DOC_SERIES = (f'{URL_MAIN}/doc', 'showMovies')
 
def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

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

    sPattern = 'class="imgContainer"><img src="([^<]+)" alt=.+?class="card-description">([^<]+)</p></div>.+?<a href="([^<]+)" class="card-title">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sTitle = aEntry[3]
            sThumb = aEntry[0]
            siteUrl = f'{URL_MAIN}{aEntry[2]}'
            sDesc = aEntry[1]
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMisc(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    oGui.setEndOfDirectory() 
    
def showMoviesLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="d-flex mt-4"><a href="([^<]+)" class="btn btn-main btn-lg">'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = sMovieTitle          
            sThumb = sThumb
            siteUrl = f'{URL_MAIN}{aEntry}'
            sDesc = sDesc
						
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
    sPattern = '<div class="imgContainer"><img src="(.+?)" alt=.+?<a href="(.+?)" class="card-title">(.+?)</a><p class="card-shortdescription">(.+?)</'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2]
            sThumb = aEntry[0]
            siteUrl = f'{URL_MAIN}{aEntry[1]}'
            sDesc = aEntry[3]
				
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesLinks', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li >.+?<a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:    
        return f'{URL_MAIN}/{aResult[1][0]}'

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  ',"Link":.+?},"(.+?)","(.+?)",' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
       for aEntry in aResult[1]:
            if '/Manifest' in aEntry[0]:
                continue
            
            if ('1080' in aEntry[0]) or ('360' in aEntry[0]) or ('720' in aEntry[0]) or ('480' in aEntry[0]) or ('240' in aEntry[0]) or ('High' in aEntry[0]) or ('youtube' in aEntry[0]):

                url = aEntry[1]
                quality = aEntry[0]
                sTitle = f'{sMovieTitle}  [COLOR coral]{quality}[/COLOR]'
                if url.startswith('//'):
                    url = f'http:{url}'
                    
                sHosterUrl = url			
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               
    oGui.setEndOfDirectory()