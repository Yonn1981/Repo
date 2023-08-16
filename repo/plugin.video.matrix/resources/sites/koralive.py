# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote
from resources.lib.util import Quote
 
SITE_IDENTIFIER = 'koralive'
SITE_NAME = 'Koralive'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = (URL_MAIN, 'showMovies')

 
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
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
	# (.+?) .+? 
    sPattern = '<a title="(.+?)" id="match-live" href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[0]
            sThumb = ""
            siteUrl =  aEntry[1]
            sDesc = ''
			
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
 
    oGui.setEndOfDirectory()
  
def showLive(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    URLMAIN = sUrl.split('/')[2]
    URLMAIN = 'https://' + URLMAIN
    if "?src=" in sUrl:
       slink = sUrl.split('?src=')[1]

    sHtmlContent2 =""
    sHtmlContent1 =""
    sHtmlContent3 =""
      # (.+?) ([^<]+) .+?
    sPattern = 'iframe.src = ["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if (aResult[0]):
        sUrl = aResult[1][0]

        sUrl = sUrl+slink

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent3 = oRequestHandler.request()
      # (.+?) ([^<]+) .+?
    sPattern = 'iframe" src="(.+?)" width'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if (aResult[0]):
        sUrl = aResult[1][0]
        if sUrl.startswith('/'):
           sUrl = URLMAIN + sUrl

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    # (.+?) # ([^<]+) .+? 
    if 'no_mobile_iframe' in sHtmlContent:
       sPattern = 'no_mobile_iframe = "(.+?)";'
       aResult = oParser.parse(sHtmlContent, sPattern)
       if (aResult[0]):
           siteUrl = aResult[1][0]
           if siteUrl.startswith('/'):
               siteUrl = URLMAIN + siteUrl
           import requests    
           oRequestHandler = cRequestHandler(siteUrl)
           hdr = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1','referer' : URL_MAIN}
           St=requests.Session()
           sHtmlContent2 = St.get(siteUrl,headers=hdr)
           sHtmlContent2 = sHtmlContent2.content.decode('utf-8')
    if 'mobile' in sHtmlContent:
       sPattern = '_iframe = "(.+?)";'
       aResult = oParser.parse(sHtmlContent, sPattern)
       if (aResult[0]):
           siteUrl = aResult[1][0]
           if siteUrl.startswith('/'):
               siteUrl = URL_MAIN + siteUrl
           import requests    
           oRequestHandler = cRequestHandler(siteUrl)
           hdr = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1','referer' : URL_MAIN}
           St=requests.Session()
           sHtmlContent1 = St.get(siteUrl,headers=hdr)
           sHtmlContent1 = sHtmlContent1.content.decode('utf-8')
    sHtmlContent = sHtmlContent3+sHtmlContent2+sHtmlContent1

    sPattern = 'href="(.+?)">(.+?)</a>'   
    aResult = oParser.parse(sHtmlContent, sPattern) 
   

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace("('","").replace("')","")
            if siteUrl.startswith('/'):
               siteUrl = URL_MAIN + siteUrl
            sDesc = ""
            import requests    
            oRequestHandler = cRequestHandler(siteUrl)
            hdr = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1','referer' : URL_MAIN}
            St=requests.Session()
            sHtmlContent = St.get(siteUrl,headers=hdr)
            sHtmlContent = sHtmlContent.content.decode('utf-8')
            oParser = cParser()
    # (.+?) # ([^<]+) .+? 		


            sPattern = "<script>AlbaPlayerControl([^<]+)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]: 
               import base64
               for aEntry in aResult[1]:
                   url_tmp = aEntry
                   url = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)	


            sPattern = "source: '(.+?)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"+'&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = "hls.loadSource(.+?);"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry.replace("('","").replace("')","")
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = "<source src='(.+?)' type='application/x-mpegURL'"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry.replace("('","").replace("')","")
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ siteUrl 
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
            sPattern = 'source:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    # (.+?) # ([^<]+) .+? 
            sPattern = 'src="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    # (.+?) # ([^<]+) .+? 
            sPattern = 'file:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'onclick="([^<]+)" >.+?>([^<]+)</strong>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry[0].replace("('",'').replace("')","").replace("update_frame","")
                   url = url.split('?link=', 1)[1]
                   if url.startswith('//'):
                      url = 'http:' + url
                   if '/embed/' in url:
                      oRequestHandler = cRequestHandler(url)
                      oParser = cParser()
                      sPattern =  'src="(.+?)" scrolling="no">'
                      aResult = oParser.parse(url,sPattern)
                      if aResult[0]:
                          url = aResult[1][0]
                          sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                          sMovieTitle = str(aEntry[1])
                          if 'vimeo' in sHosterUrl:
                              sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                          oHoster = cHosterGui().checkHoster(sHosterUrl)
                          if oHoster:
                              oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                              oHoster.setFileName(sMovieTitle)
                              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'src="(.+?)" width="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry[0]
                   if url.startswith('//'):
                      url = 'http:' + url
                   if 'xyz' in url:
                       oRequestHandler = cRequestHandler(url)
                       oRequestHandler.setRequestType(1)
                       oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0')
                       oRequestHandler.addHeaderEntry('referer', 'https://msdee.xyz/')
                       data = oRequestHandler.request();
                       sPattern =  '(http[^<]+m3u8)'
                       aResult = oParser.parse(data,sPattern)
                       if aResult[0]:
                           url = aResult[1][0]+ '|User-Agent=' + 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0' +'&Referer=' + "https://memotec.xyz/"
 
                           sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","") 
                           sMovieTitle = sMovieTitle
                           if 'vimeo' in sHosterUrl:
                               sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                           oHoster = cHosterGui().checkHoster(sHosterUrl)
                           if oHoster:
                               oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                               oHoster.setFileName(sMovieTitle)
                               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    
    if 'streamable' in sUrl:
        sHosterUrl = sUrl.split('?src=')[1]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
           oHoster.setDisplayName(sMovieTitle)
           oHoster.setFileName(sMovieTitle)
           cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                
    oGui.setEndOfDirectory()			

  	
def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    oParser = cParser()
    sPattern =  "'homepageUrl': '([^']+)" 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        mSite = aResult[1][0] 

    oParser = cParser()
    sPattern = '; setURL(.+?)">(.+?)</button>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sQual = aEntry[1]
            url = mSite + aEntry[0].replace("('","").replace("')","")
            headers2 = {'Referer': sUrl,
                        'authority': 'medo.360koralive.com',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
                        'Cookie': cook,
                        'Sec-Fetch-Dest':'iframe',
                        'Sec-Fetch-Mode':'navigate',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
                        }
            req = requests.get(url ,headers=headers2)
            sHtmlContent = str(req.text)
            oParser = cParser()
            sPattern = 'source:\s*["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry
                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sQual)
                    if url.startswith('//'):
                        url = 'https:' + url
            
                
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false'
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = 'loadSource(.+?);'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry.replace("('","").replace("')","")
                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sQual)
                    if url.startswith('//'):
                        url = 'https:' + url
            
                
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false'
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry
                    sHosterUrl = url
                    sDisplayTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sQual)

                    if sHosterUrl.startswith('//'):
                        sHosterUrl = 'http:' + sHosterUrl            
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    else:
        sPattern = 'iframe.src = ["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry

                    if 'albaplayer' in url:
                        url = url + sUrl.split('src=')[1]
                        oRequestHandler = cRequestHandler(url)
                        data = oRequestHandler.request()

                        oParser = cParser()
                        sStart = 'class="albaplayer_name">'
                        sEnd = 'class="albaplayer_site_name">'
                        data = oParser.abParse(data, sStart, sEnd)
                        sPattern =  'href=["\']([^"\']+)["\']'
                        aResult = oParser.parse(data,sPattern)
                        if aResult[0]:
                            for aEntry in aResult[1]:
                                url = aEntry
                                oRequestHandler = cRequestHandler(url)
                                data2 = oRequestHandler.request()
                            
                                sPattern =  '<iframe.+?src="([^"]+)'
                                aResult = oParser.parse(data2,sPattern)
                                if aResult[0]:
                                    url = aResult[1][0]
                                    if 'sharecast' in url:
                                        Referer =  "https://sharecast.ws/"
                                        oRequestHandler = cRequestHandler(url)
                                        oRequestHandler.addHeaderEntry('Referer', Referer)
                                        data3 = oRequestHandler.request()

                                        sPattern2 = '"player","([^"]+)",{\'([^\']+)'

                                        aResult = re.findall(sPattern2, data3)
                                        if aResult:
                                            sHosterUrl = 'https://%s/hls/%s/live.m3u8' % (aResult[0][1], aResult[0][0])
                                            sHosterUrl += '|referer=https://sharecast.ws/'

                                    if 'live7' in url:
                                        oRequestHandler = cRequestHandler(url)
                                        oRequestHandler.addHeaderEntry('Referer', Referer)
                                        data3 = oRequestHandler.request()

                                        sPatternUrl = 'hlsUrl = "https:\/\/" \+ ea \+ "([^"]+)"'
                                        sPatternPK = 'var pk = "([^"]+)"'
                                        sPatternEA = 'ea = "([^"]+)";'
                                        aResultUrl = re.findall(sPatternUrl, data3)
                                        aResultEA = re.findall(sPatternEA, data3)
                                        aResultPK = re.findall(sPatternPK, data3)
                                        if aResultUrl and aResultPK and aResultEA:
                                            aResultPK = aResultPK[0][:53] + aResultPK[0][54:] 
                                            url3 = aResultEA[0] + aResultUrl[0] + aResultPK
                                            sHosterUrl = 'https://' + url3

                                    sHosterUrl = url
                                    sMovieTitle = sMovieTitle           

                                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                                    if oHoster:
                                        oHoster.setDisplayName(sMovieTitle)
                                        oHoster.setFileName(sMovieTitle)
                                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
                    else:
                        url = url + sUrl.split('src=')[1]                        
                        sHosterUrl = url
                    
                    sDisplayTitle = sMovieTitle

                    if sHosterUrl.startswith('//'):
                        sHosterUrl = 'http:' + sHosterUrl            
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

                
    oGui.setEndOfDirectory()    
