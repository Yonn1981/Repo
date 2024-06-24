# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, VSlog
from resources.lib.parser import cParser
from resources.lib.util import cUtil
 
SITE_IDENTIFIER = 'detectiveconanar'
SITE_NAME = 'Detectiveconanar'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
ANIM_NEWS = (f'{URL_MAIN}episodes/', 'showSeries')
ANIM_MOVIES = (f'{URL_MAIN}movies/', 'showMovies')
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()   
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', 'anime.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
   
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="film-poster">\s*<img data-src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)'
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
            sDesc = '' 
            siteUrl = aEntry[2]
            sThumb = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="film-poster">.+?data-src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            siteUrl = aEntry[2]
            sThumb = aEntry[0]
            sDesc = ''
            sTitle = cUtil().CleanMovieName(aEntry[1])

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a title="التالي" class="page-link" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    
    else:
        sPattern = '<span class="current">.+?href=(.+?) class='
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return aResult[1][0].replace("'","")

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

    sPattern = 'data-embed="([^"]+)".+?class="btn">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'Blog' in aEntry[1]:
                continue

            sLink = aEntry[0]
            if sLink.startswith('//'):
               sLink = f'http:{sLink}'
            
            try:
                sQual = re.search(r"\(([^)]+)\)", aEntry[1]).group(1)
            except:
                sQual = aEntry[1]

            sDisplayTitle = f'{sMovieTitle} [{sQual}]'
            sHosterUrl = f'{sLink}|Referer={URL_MAIN}'
            oHoster = cHosterGui().getHoster('jimmy') 
            if oHoster:
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               
    oGui.setEndOfDirectory()