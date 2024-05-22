# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'cartoonrbi'
SITE_NAME = 'CartoonArbi'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
 
KID_MOVIES = (URL_MAIN + 'films.html', 'showMovies')
KID_CARTOON = (URL_MAIN + 'cats.html', 'showSeries')

MOVIE_PACK = (URL_MAIN , 'showPack')
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'crtoon.png', oOutputParameterHandler)    

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'جميع الكرتون', 'listes.png', oOutputParameterHandler)            
    oGui.setEndOfDirectory()

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<ul id="sidebarmenu1">'
    sEnd = '</ul></li></ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<a href="([^<]+)">([^<]+)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if '#' in aEntry[0]:
                continue 
            sTitle = aEntry[1]
            siteUrl = URL_MAIN + aEntry[0]	

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)			

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, 'crtoon.png', '', '', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<div class="cartoon_cat_pic"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt'
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
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^<]+)">«'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        aResult = URL_MAIN+'/'+aResult[1][0]
        return aResult

    return False	

def showSeries(sSearch = ''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="cartoon_cat_pic"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().ConvertSeasons(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="cartoon_eps_pic"><a href="(.+?)" title="(.+?)"><span class="copy_right"></span><span class="playtime">(.+?)</span><img src="(.+?)" alt'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            siteUrl = aEntry[0]
            sThumb = aEntry[3]
            sTitle = cUtil().ConvertSeasons(aEntry[1]).replace("الحلقة "," E").replace("حلقة "," E")

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, '', oOutputParameterHandler) 
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEps', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
       
def showLink(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = sUrl.replace("cartoon","watch-")

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sname = '0'
    sPage='0'

    sStart = '<div class="servers">'
    sEnd = '<div class="videoshow">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = "server_ch([^<]+),'(.+?)'"
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        for aEntry in aResult[1]:
            sErver = aEntry[0].replace("(","")
            sPage = aEntry[1]
            siteUrl = URL_MAIN + '/plugins/server'+sErver+'/embed.php?url='+sPage+'&id='+sname
			
            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sData = oRequestHandler.request()
   
            sPattern = '<iframe.+?src="(.+?)"'
            oParser = cParser()
            aResult = oParser.parse(sData, sPattern)
	
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = str(aEntry).replace('preview?pli=1#t=1','').replace('https://docs.google.com','https://drive.google.com')  
                   sThumb = sThumb
                   if '.m3u8' in url:
                      url2 = url.split('=') 
                      url = url2[1].replace("&token","")
                   if url.startswith('//'):
                      url = 'http:' + url
                   if 'arteenz' in url:
                      oRequestHandler = cRequestHandler(url)
                      sUrl0 = oRequestHandler.request()

                      sPattern = '<iframe.+?src="(.+?)"'
                      aResult = oParser.parse(sUrl0, sPattern)
                      if aResult[0]:
                        for aEntry in aResult[1]:
                            url = aEntry
                      else:
                          url = ""
								            
                   sHosterUrl = url
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if '.m3u8' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
       
    oGui.setEndOfDirectory()