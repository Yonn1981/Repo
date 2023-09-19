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

    sPattern = '<a class="tray-link">(.+?)</a>(.+?)</article></div></div></div></div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sCat = aEntry[0]

            oOutputParameterHandler.addParameter('sCat',sCat)
            oOutputParameterHandler.addParameter('sUrl',sUrl)
            oOutputParameterHandler.addParameter('sTime', sTime)
            oOutputParameterHandler.addParameter('cookies', cookies)
            oOutputParameterHandler.addParameter('sHtmlContent', sHtmlContent)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesContent', sCat, 'agnab.png', oOutputParameterHandler)

    if sSearch:
        oOutputParameterHandler = cOutputParameterHandler()
        data = requests.get(sUrl, cookies={"hd": "on"}).json()
        for key in data['searchResult']:
            siteUrl = URL_MAIN+'hls/'+key['id']+'.m3u8'
            sThumb = "https://i0.wp.com/img.netflixmirror.com/poster/v/"+key['id']+".jpg"
            sTitle = key['t']
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  

def showMoviesContent():
    oGui = cGui()
    import requests
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sTime = oInputParameterHandler.getValue('sTime')
    cookies = oInputParameterHandler.getValue('cookies')
    sCat = oInputParameterHandler.getValue('sCat')
    sHtmlContent = oInputParameterHandler.getValue('sHtmlContent')

    cookies = {"hd": "on"}
    sHtmlContent1 = sHtmlContent

    Yes = xbmcgui.Dialog().yesno(
        'Get Title Name',
        'Do you want to try getting title name? Might be slow..',
        'Cancel'
        )

    sPattern = '<a class="tray-link">'+sCat+'</a>(.+?)</article></div></div></div></div></div>'    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sHtmlContent2 = aEntry          

            sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()    
                for aEntry in aResult[1]:
                    
                    siteUrl = URL_MAIN+'hls/'+aEntry[0]+'.m3u8'
                    sTitle = aEntry[0]
                    if Yes:
                        data = requests.get(siteUrl, cookies={"hd": "on"}).json()
                        sTitle = data['title']
                    sThumb = aEntry[1]
                    sDesc = ''
                    sYear = ''

                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        oGui.setEndOfDirectory()  


def showSeries(sSearch = ''):
    oGui = cGui()
    import requests
    oParser = cParser()
    if sSearch:
      sUrl = sSearch
      
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

    sPattern = '<a class="tray-link">(.+?)</a>(.+?)</article></div></div></div></div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sCat = aEntry[0]

            oOutputParameterHandler.addParameter('sCat',sCat)
            oOutputParameterHandler.addParameter('sUrl',sUrl)
            oOutputParameterHandler.addParameter('sTime', sTime)
            oOutputParameterHandler.addParameter('cookies', cookies)
            oOutputParameterHandler.addParameter('sHtmlContent', sHtmlContent)
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesContent', sCat, 'agnab.png', oOutputParameterHandler)

    if sSearch:
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

    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeriesContent():
    oGui = cGui()
    import requests
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sTime = oInputParameterHandler.getValue('sTime')
    sCat = oInputParameterHandler.getValue('sCat')
    sHtmlContent = oInputParameterHandler.getValue('sHtmlContent')

    sHtmlContent1 = sHtmlContent
    
    sPattern = '<a class="tray-link">'+sCat+'</a>(.+?)</article></div></div></div></div></div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)

    Yes = xbmcgui.Dialog().yesno(
        'Get Title Name',
        'Do you want to try getting title name? Might be slow..',
        'Cancel'
        )

    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sHtmlContent2 = aEntry          

            sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'

            oParser = cParser()
            aResult = oParser.parse(sHtmlContent2, sPattern)

            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()    
                for aEntry in aResult[1]:
                    
                    siteUrl = URL_MAIN+'post.php?id='+aEntry[0]+'&t='+sTime
                    sTitle = aEntry[0]
                    if Yes:
                        data = requests.get(siteUrl, cookies={"hd": "on"}).json()
                        sTitle = data['title']
                    sCode = aEntry[0]
                    sThumb = "https://i0.wp.com/img.netflixmirror.com/poster/v/"+aEntry[0]+".jpg"
                    sDesc = ''
                    sYear = ''

                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sTime', sTime)
                    oOutputParameterHandler.addParameter('sCode', sCode)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sYear', sYear)
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        oGui.setEndOfDirectory()  

def showSeasons():
    import requests
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sCode = oInputParameterHandler.getValue('sCode')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
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


    data = requests.get(sUrl, cookies={"hd": "on"}).json()
    for key in data['episodes']:
        sEpisode = key['ep']
        siteUrl = URL_MAIN+'hls/'+key['id']+'.m3u8'
        sThumb = "https://i0.wp.com/img.netflixmirror.com/poster/v/"+key['id']+".jpg"
        sTitle = sMovieTitle + sEpisode
        sDesc = sDesc

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    sPage = int(data['nextPageShow'])
    if sPage > 0: 
            siteUrl = URL_MAIN+'episodes.php?s='+key['id']+'&series='+sCode
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
 

def showHosters():
    oGui = cGui()
    from resources.lib.comaddon import dialog
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    cookies = {"hd": "on"}
    data = requests.get(sUrl, cookies=cookies).text

    sPattern = 'RESOLUTION=(\w+).+?(https.+?m3u8)'
    aResult = oParser.parse(data, sPattern)
    if aResult[0]:            
        url=[]
        qua=[]
        for i in aResult[1]:
            url.append(str(i[1]))
            qua.append(str(i[0]))
        sUrl = dialog().VSselectqual(qua, url)

    sHosterUrl = sUrl +'|Referer='+URL_MAIN
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
                sDisplayTitle = sMovieTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()
