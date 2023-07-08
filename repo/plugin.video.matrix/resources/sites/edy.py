# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
import base64	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager

SITE_IDENTIFIER = 'edy'
SITE_NAME = 'Edy [COLOR orange]- Server -[/COLOR]'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_MAIN = base64.b64decode(URL_MAIN).decode('utf8',errors='ignore')

MOVIE_EN = (URL_MAIN + 'movies/', 'showMovies')
SERIE_EN = (URL_MAIN + 'tvs/', 'showSeries')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<span class="name"><a href="([^"]+)">(.+?)/</a></span>'

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

            sTitle = aEntry[1]
            siteUrl = URL_MAIN + 'movies/' + aEntry[0]
            sThumb = ''
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
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?
    sPattern = '<span class="name"><a href="([^"]+)">(.+?)/</a></span>'

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


            sTitle = aEntry[1]
            siteUrl = URL_MAIN + 'tvs/' + aEntry[0]
            sThumb = ''
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
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
	sThumb = oInputParameterHandler.getValue('sThumb')

	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()
    # .+? ([^<]+)
	sPattern = '<span class="name"><a href="(.+?)">(.+?)/</a></span>'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = aEntry[1].replace('/','') + ' ' + sMovieTitle
			siteUrl = sUrl + aEntry[0]
			sThumb = ''
			sDesc = ''
            
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
    
def showEps():

    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

     # (.+?) ([^<]+) .+?
    sPattern = '<span class="name"><a href="([^"]+)">(.+?)</a></span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = sUrl + aEntry[0]
            sThumb = sThumb
            sDesc = ''

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            sHosterUrl = siteUrl 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, sDesc)


               
       
    oGui.setEndOfDirectory() 
 
	

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<span class="name"><a href="([^"]+)">(.+?)</a></span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            sTitle = aEntry[1]
            url = sUrl + aEntry[0]
            sThumb = sThumb
            sDesc = ''
				
					
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'rel="next" href="([^"]+)"'	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False