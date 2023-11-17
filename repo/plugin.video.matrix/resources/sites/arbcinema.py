# -*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/

import re
import requests
import json 
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, isMatrix, siteManager, addon

 
SITE_IDENTIFIER = 'arbcinema'
SITE_NAME = 'Arbcinema'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
 
MOVIE_EN = (URL_MAIN + 'cat_film/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'type/%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'country/مشاهدة-افلام-اسيوية-مترجمة-21/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0' 

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30330), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (حسب التصنيف)', 'film.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'id="navbarNavDropdown">'
    sEnd = '</ul></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'المزيد' in aEntry[1]:
                continue 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'film.png', '', '', oOutputParameterHandler)
       
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

    sPattern = '<li class="col-md-3"><a href="([^"]+)".+?<img src="([^"]+)".+?<h4 class="move-title">([^<]+)</h4>.+?.+?<div class="mov-typ">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("كامل","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sRes = f'{aEntry[3]}'
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            if sRes:
                sTitle += ' [%s]' % sRes

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
    
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    sNote = ''

    sPattern = '<br>\s*قصة الفيلم:\s*<br>([^<]+)<br>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]

    sPattern = '<input type="hidden" name="([^<]+)" value="1">'   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sDesc = sNote
 		
            if 'download' in aEntry:
                oGui.addLink(SITE_IDENTIFIER, 'showServer', sMovieTitle, sThumb, sDesc, oOutputParameterHandler)
            else:
                s = requests.Session()            
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0' }

                data = {'watch':'1'}
                r = s.post(sUrl,data=data,headers=headers)
                sHtmlContent = r.content.decode('utf8')

                sPattern = 'postid-(.+?)">'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0]):
                    sId = aResult[1][0]

                sPattern = 'url: ["\']([^"\']+)["\']'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0]):
                    serverURL = aResult[1][0]

                sPattern2 = '<li data-name="([^<]+)" data-type="free"'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern2)
                if aResult[0]:
                    for aEntry in aResult[1]:
                        nume = aEntry + sMovieTitle
						            
                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('serverURL', serverURL)
                        oOutputParameterHandler.addParameter('sId', sId)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('nume', nume)

                        oGui.addLink(SITE_IDENTIFIER, 'showHosters', nume, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

    oGui.setEndOfDirectory() 

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    serverURL = oInputParameterHandler.getValue('serverURL')
    sId = oInputParameterHandler.getValue('sId')
    nume = oInputParameterHandler.getValue('nume')

    s = requests.Session()  
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
							'Accept': '*/*',
							'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
							'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
							'X-Requested-With': 'XMLHttpRequest',
							'Connection': 'keep-alive'}
    data = {'id':sId,'name':nume,'type':'free'}
    r = s.post(serverURL, headers=headers, data = data)
    sHtmlContent = r.content.decode('utf8')         

    sPattern3 = '<iframe.+?src="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern3)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
            sHosterUrl = url

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def showServer(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    sId = ''

    sPattern = 'postid-(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if (aResult[0]):
        sId = aResult[1][0]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Connection': 'keep-alive'}
    data = sId
    data = {'id':data,'key':'0','type':'normal'}
    s = requests.Session()
    r = s.post(URL_MAIN+'wp-content/themes/takweed/functions/inc/single/server.php', headers=headers, data = data)
    sHtmlContent = r.content.decode('utf8') 
          	
    sPattern = '<a href="([^<]+)" rel'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
				            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
				
       
    oGui.setEndOfDirectory()	 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<]+)'>&rsaquo;</a>"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        
        return aResult[1][0]

    return False
