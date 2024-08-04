# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

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

def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<section class="content-type-component">.+?<a href="(.+?)" class="head-title">(.+?)</a>(.+?)</section>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sectionURL = f'{URL_MAIN}{aEntry[0]}'
            sectionTitle = '[COLOR orange]' + u'\u2193' + aEntry[1] + '[/COLOR]'
            sectionHTML = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sectionURL)
            oOutputParameterHandler.addParameter('sMovieTitle', sectionTitle)

            oGui.addMisc(SITE_IDENTIFIER, 'showSection', sectionTitle, 'doc.png', 'https://nowcdn.asharq.com/184x0/14529253851720113239.png', '', oOutputParameterHandler)

            sPattern = '<div class="card.+?<a href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)'
            aResult = oParser.parse(sectionHTML, sPattern)	
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler() 
                for aEntry in aResult[1]:

                    sTitle = aEntry[2]
                    sThumb = aEntry[1]
                    siteUrl = f'{URL_MAIN}{aEntry[0]}'
                    
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)

                    oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler) 

                sNextPage = __checkForNextPage(sHtmlContent)
                if sNextPage:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                    oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
    
def showSection():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    token = oInputParameterHandler.getValue('token')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    if token is False:
        pattern = r'"layout":.*?"(.*?)"'
        match = re.findall(pattern, sHtmlContent)
        token = 'Bearer ' + ' '.join(match)

    nUrl = sUrl
    if 'page=' not in sUrl:
        nUrl = sUrl.replace('content-type','api/v1/content_types').replace('now.', 'nowapi.') + '/data?page=1&limit=12'
    oRequestHandler = cRequestHandler(nUrl)
    oRequestHandler.addHeaderEntry('Authorization', token)
    oRequestHandler.addHeaderEntry('Referer', 'https://now.asharq.com/')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler() 
        for entry in sHtmlContent["data"]["data"]:

            sTitle = entry["title"]
            siteUrl = f'{URL_MAIN}/episode/{entry["episodeSlug"]}'
            try: 
                sThumb = entry["showPoster"]
            except:
                sThumb = entry["episodeImage"]
            sDesc = entry["showLongDescription"]
          
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        sNextPage = __checkForNextjSonPage(nUrl)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oOutputParameterHandler.addParameter('token', token)
            oGui.addDir(SITE_IDENTIFIER, 'showSection', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li >.+?<a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:    
        return f'{URL_MAIN}/{aResult[1][0]}'

    return False

def __checkForNextjSonPage(sUrl):
    from urllib.parse import urlparse, urlunparse

    parsed_url = urlparse(sUrl)
    query_parts = dict(qc.split("=") for qc in parsed_url.query.split("&"))
    if "page" in query_parts:
        page_number = int(query_parts["page"]) + 1
        query_parts["page"] = str(page_number)
        new_query = "&".join(f"{key}={value}" for key, value in query_parts.items())
        return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))

    return sUrl

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
            
            if any(item in aEntry[0] for item in ['High', '1080', '720', '480', '360', '240', 'youtube']):

                url = aEntry[1]
                if url.startswith('//'):
                    url = f'http:{url}'
                sQual = aEntry[0]
                sTitle = f'{sMovieTitle} [COLOR coral]{sQual}[/COLOR]'
                    
                sHosterUrl = url			
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               
    oGui.setEndOfDirectory()