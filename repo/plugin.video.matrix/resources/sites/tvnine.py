﻿# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, isMatrix
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib import random_ua

UA = random_ua.get_random_ua()
 
SITE_IDENTIFIER = 'tvnine'
SITE_NAME = 'Tv96'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = ('https://go.radar2.com/p/footyy.html?m=1', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'sport.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

   
def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<div class="containerMatch"><a href="([^"]+)".+?<div style="font-weight: bold">(.+?)</div>.+?<div class="matchTime">(.+?)</div>.+?<div style="font-weight: bold">(.+?)</div>'
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
 
            sTitle =  aEntry[1]+' vs '+aEntry[3]
            sYear = ""
            sThumb = ""
            siteUrl = aEntry[0]
            sDesc = aEntry[2]+' GMT+1'
			
			
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    oGui.setEndOfDirectory()

def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()                   

    if 'data-embed=' in sHtmlContent :
        sPattern = 'data-embed="(.+?)">(.+?)</li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
    else :
        sPattern = 'onclick="location.href=(.+?);">(.+?)</li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
   
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace("'","")
            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            data = oRequestHandler.request()

            sPattern = 'source: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if '.png' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url 
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
 
            sPattern = 'hls.loadSource(.+?);'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if '.png' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url 
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   sHosterUrl = url.replace('("',"").replace('")',"")
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

            sPattern = 'hls: "(.+?)"'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url 
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

            sPattern = "source: '(.+?)',"
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url 
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = 'src="(.+?)"'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if 'jsdelivr' in url:
                       continue
                   if 'sotchoum' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   if 'href.li' in url:
                      url = url.replace("https://href.li/?","") 
                   if 'realbit' in url:
                      url = getHosterIframe(url,sUrl)
                   if 'sportsonline' in url:
                      url = getHosterIframe(url,sUrl) 
                   if 'linecrystal' in url:
                      url = getHosterIframe(url,sUrl) 
                   if ".php" or ".html" in url:
                       oRequestHandler = cRequestHandler(url)
                       data2 = oRequestHandler.request() 
                       sPattern = "source: '(.+?)',"
                       aResult = oParser.parse(data2, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

                       sPattern = '<iframe src=["\']([^"\']+)["\']'
                       aResult = oParser.parse(data2, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url2 = aEntry
                              if url2.startswith('//'):
                                 url2 = 'https:' + url2
                              if '?src=' in url:
                                 url2 = url2.split('?src=')[1] 
                              sHosterUrl = url2
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                              else:
                                  sHosterUrl = getHosterIframe(url2,url) 
                                  sHosterUrl = sHosterUrl + "|Referer=" + url2
            
                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

                       sPattern = 'source: "(.+?)",'
                       aResult = oParser.parse(data2, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

                   if '1stream' in url:
                       continue
                   sHosterUrl = url
                   sMovieTitle = sTitle         
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)  

            sPattern = 'hls: "(.+?)"'		
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl        

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)

            sPattern = "hls: '(.+?)'"
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url 
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

            sPattern = 'file: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)   

            sPattern = '<iframe src=".+?stream_url=(.+?)" height'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

                   if 'href.li' in url:
                      url = url.replace("https://href.li/?","") 
                   if ".php" or ".html" in url:
                       oRequestHandler = cRequestHandler(url)
                       data = oRequestHandler.request() 
                       sPattern = "source: '(.+?)',"
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                       sPattern = '<iframe src=["\']([^"\']+)["\']'
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:                  
                              url2 = aEntry.replace("https://href.li/?","") 
                              if url2.startswith('//'):
                                 url2 = 'https:' + url2
                              if '?src=' in url2:
                                 url2 = url2.split('?src=')[1] 
                              sHosterUrl = url2
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                              if 'sportsonline' in sHosterUrl:
                                sHosterUrl = getHosterIframe(url2,url) 
                                if 'planet' in sHosterUrl:
                                    sHosterUrl = getHosterIframe(sHosterUrl,url2)
                                sHosterUrl = sHosterUrl + "|Referer=" + url  
                              if 'dynamic' in url2:
                                sHosterUrl = url2 + "|Referer=" + url 
                              if 'mangomolo' in sHosterUrl:
                                oRequestHandler = cRequestHandler(sHosterUrl)
                                data = oRequestHandler.request() 
                                sPattern = 'src: ["\']([^"\']+)["\']'
                                aResult = oParser.parse(data, sPattern)
                                if aResult[0]:
                                    for aEntry in aResult[1]:           
                                        sHosterUrl = aEntry
                              if 'live7' in sHosterUrl:
                                oRequestHandler = cRequestHandler(sHosterUrl)
                                data = oRequestHandler.request() 
                                sPattern = '<iframe src=["\']([^"\']+)["\']'
                                aResult = oParser.parse(data, sPattern)
                                if aResult[0]:
                                    for aEntry in aResult[1]:           
                                        sHosterUrl = aEntry  + "|Referer=https://www.live7.pro/"          

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                       sPattern = 'source: "(.+?)",'
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                                  
                   sHosterUrl = url.replace("https://tv.hd44.net/p/phone.html?src=","") 
                   if 'sportsonline' in sHosterUrl:
                        continue                   
                   sHosterUrl = sHosterUrl   
                   sMovieTitle = sTitle
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'				
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                      
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = 'hls:\s*["\']([^"\']+)["\']'				
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url or '.webp' in url or '.jpg' in url:
                       continue
                   if '.' not in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                      
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = 'file: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

            sPattern = '<iframe src=".+?stream_url=(.+?)" height'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = "document.write(.+?)</script>"
            aResult = oParser.parse(data, sPattern)
            
            if aResult[0]:
               for aEntry in aResult[1]:
                   sContent = aEntry.replace("(unescape('","").replace("'))","")
                   import urllib
                   sHtmlContent = urllib.parse.unquote(sContent)

                   sPattern = '<video src=["\']([^"\']+)["\']'
                   aResult = re.findall(sPattern, sHtmlContent)

                   if aResult:
                        url = aResult[0]
                        sMovieTitle = sTitle
                        if '.m3u8' in url:
                            sHosterUrl = url
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
             
    oGui.setEndOfDirectory() 

def getHosterIframe(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False

    if 'channel' in url:
         referer = url.split('channel')[0]

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        for code in aResult:
            try:
                if isMatrix():
                    code = base64.b64decode(code).decode('ascii')
                else:
                    code = base64.b64decode(code)
                if '.m3u8' in code:
                    return True, code + '|Referer=' + url
            except Exception as e:
                pass

    sPattern = "mimeType: *\"application\/x-mpegURL\",\r\nsource:'([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return sHosterUrl + '|referer=' + referer

    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//'+referer.split('/')[2] + url  
                url = "https:" + url
            referer2 = url.split('embed')[0]
            url = getHosterIframe(url, referer)
            if url:
                return url + "|Referer=" + referer2 

    sPattern = 'src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return url + '|referer=' + referer

    sPattern = 'player.load\({source: (.+?)\('
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        func = aResult[0]
        sPattern = 'function %s\(\) +{\n + return\(\[([^\]]+)' % func
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            referer = url
            sHosterUrl = aResult[0].replace('"', '').replace(',', '').replace('\\', '').replace('////', '//')
            return True, sHosterUrl + '|referer=' + referer

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]
        if '.m3u8' in sHosterUrl:
            return True, sHosterUrl 

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for sHosterUrl in aResult:
            if '.m3u8' in sHosterUrl:
                if 'fls/cdn/' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('/playlist.', '/tracks-v1a1/mono.')
                else:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', referer)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()
                    return sHosterUrl + '|referer=' + referer

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return True, sHosterUrl + '|referer=' + referer

    sPattern = "onload=\"ThePlayerJS\('.+?','([^\']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = 'https://sharecast.ws/player/' + aResult[0]
        b, url = Hoster_ShareCast(url, referer)
        if b:
            return True, url

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return True, aResult[0] + '|referer=' + url

    sPattern = 'source\s*["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    return False
	