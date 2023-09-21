# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
import requests
import xbmcgui

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager


SITE_IDENTIFIER = 'netflixmirror'
SITE_NAME = 'Netflix'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'movies', 'showMovies')
SERIE_EN = (URL_MAIN + 'series', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search.php?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH SERIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search.php?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search.php?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def showMovies(sSearch = ''):
    oGui = cGui()
    import requests
    oParser = cParser()
    if sSearch:
        sUrl = sSearch

        oOutputParameterHandler = cOutputParameterHandler()
        data = requests.get(sUrl, cookies={"hd": "on"}).json()
        for key in data['searchResult']:
            siteUrl = f'{URL_MAIN}playlist.php?id={key["id"]}'
            sThumb = "https://i0.wp.com/img.netflixmirror.com/poster/v/"+key['id']+".jpg"
            sTitle = key['t']
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        cookies = {"hd": "on"}
        response = requests.get(sUrl, cookies=cookies)
        sHtmlContent = response.text

        sPattern =  'data-time="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sTime = aResult[1][0] 

        Yes = xbmcgui.Dialog().yesno(
            'Get Title Name',
            'Do you want to try getting title name? Might be slow..',
            'Cancel'
            )

        listitems =[]
        sPattern =  'class="tray-link">(.+?)</a>' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sCat = aEntry
                listitems.append(sCat)
      
        index = xbmcgui.Dialog().contextmenu(listitems)
        if index>=0:
            entry = listitems[index] 

        oParser = cParser()
        sStart = f'>{entry}</a>'
        sEnd = '<div class="tray-container">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent1, sPattern)	
        if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                siteUrl = f'{URL_MAIN}playlist.php?id={aEntry[0]}&tm={sTime}'
                sThumb = aEntry[1]
                sTitle = aEntry[0]
                if Yes:
                    sMovie = f'{URL_MAIN}post.php?id={aEntry[0]}'
                    data = requests.get(sMovie, cookies={"hd": "on"}).json()
                    sTitle = data['title']
                    siteUrl = f'{URL_MAIN}playlist.php?id={aEntry[0]}&t={sTitle}&tm={sTime}'
                sDesc = ''
                sCode = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sCode', sCode)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeries(sSearch = ''):
    oGui = cGui()
    import requests
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
        oOutputParameterHandler = cOutputParameterHandler()
        data = requests.get(sUrl, cookies={"hd": "on"}).json()
        for key in data['searchResult']:
            siteUrl = URL_MAIN+'post.php?id='+key['id']
            sThumb = "https://i0.wp.com/img.netflixmirror.com/poster/v/"+key['id']+".jpg"
            sTitle = key['t']
            sDesc = ''
            sCode = key['id']

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sCode', sCode)
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        cookies = {"hd": "on"}
        response = requests.get(sUrl, cookies=cookies)
        sHtmlContent = response.text

        sPattern =  'data-time="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sTime = aResult[1][0] 

        Yes = xbmcgui.Dialog().yesno(
            'Get Title Name',
            'Do you want to try getting title name? Might be slow..',
            'Cancel'
            )

        listitems =[]
        sPattern =  'class="tray-link">(.+?)</a>' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sCat = aEntry
                listitems.append(sCat)
      
        index = xbmcgui.Dialog().contextmenu(listitems)
        if index>=0:
            entry = listitems[index] 

        oParser = cParser()
        sStart = f'>{entry}</a>'
        sEnd = '<div class="tray-container">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent1, sPattern)	
        if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                siteUrl = f'{URL_MAIN}post.php?id={aEntry[0]}'
                sThumb = aEntry[1]
                sTitle = aEntry[0]
                if Yes:
                    data = requests.get(siteUrl, cookies={"hd": "on"}).json()
                    sTitle = data['title']
                sDesc = ''
                sCode = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sCode', sCode)
                oOutputParameterHandler.addParameter('sTime', sTime)
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeasons():
    import requests
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sCode = oInputParameterHandler.getValue('sCode')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTime = oInputParameterHandler.getValue('sTime')
    
    data = requests.get(sUrl, cookies={"hd": "on"}).json()
    for key in data['season']:
        sSeason = ' S'+ key['s']
        siteUrl = URL_MAIN+'episodes.php?s='+key['id']+'&series='+sCode
        sThumb = "https://i0.wp.com/img.netflixmirror.com/poster/v/"+key['id']+".jpg"
        sTitle = data['title']
        sTitle = sTitle + sSeason
        sDesc = data['desc']
			
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sCode', sCode)
        oOutputParameterHandler.addParameter('sTime', sTime)
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    
    oGui.setEndOfDirectory() 
        
def showEpisodes():
    import requests
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sCode = oInputParameterHandler.getValue('sCode')
    sTime = oInputParameterHandler.getValue('sTime')


    data = requests.get(sUrl, cookies={"hd": "on"}).json()
    for key in data['episodes']:
        sEpisode = key['ep']
        siteUrl = f'{URL_MAIN}playlist.php?id={key["id"]}&tm={sTime}'
        sThumb = "https://i0.wp.com/img.netflixmirror.com/poster/v/"+key['id']+".jpg"
        sTitle = sMovieTitle + sEpisode
        sDesc = sDesc

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    sPage = int(data['nextPageShow'])
    if sPage > 0: 
            siteUrl = f'{URL_MAIN}episodes.php?s={data["nextPageSeason"]}&series={sCode}&page={data["nextPage"]}'
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
 

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    data = requests.get(sUrl, cookies={"hd": "on"}).json()
    for key in data:
        for data in key['sources']:
            sQual = data['label']
            if 'Full' in sQual:
                sQual = '1080p'
            if 'Mid' in sQual:
                sQual = '720p Default'
            if 'Low' in sQual:
                sQual = '480p'
            sUrl = f'{URL_MAIN}{data["file"]}'
            sThumb = ''
            sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sQual)  

            sHosterUrl = sUrl +'|Referer='+URL_MAIN
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()
