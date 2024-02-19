# -*- coding: utf-8 -*-
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
from resources.lib.util import Quote
 
SITE_IDENTIFIER = 'koralive'
SITE_NAME = 'Koralive'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_MAIN2 = siteManager().getUrlMain2(SITE_IDENTIFIER)

SPORT_LIVE = (URL_MAIN, 'showMovies')
SPORT_FOOT = (URL_MAIN + 'p/videos.html', 'showVideos')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'foot.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showVideos', 'أهداف و ملخصات ', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
	
    
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN2)
    if URL_MAIN2 not in sUrl:
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' بث مباشر اخر من كورة لايف', 'sites/kooralive.png', oOutputParameterHandler)

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="match-container">\s*<a href="([^"]+)" title="([^"]+)".+?id="result">(.+?)</div>.+?data-start=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "#" in aEntry[0]:
                sCondition = "لا توجد روابط للمباراة \n \n"
            else:
                sCondition = "الروابط متاحة \n \n"
 
            sTitle =  aEntry[1].replace('بث مباشر اليوم','')
            if 'مباراة' in sTitle:
                sTitle = sTitle.split('مباراة')[1]
                if 'كورة' in sTitle:
                    sTitle = sTitle.split('كورة')[0]
            sThumb = ''
            siteUrl =  aEntry[0]
            sDesc = sCondition + f'وقت المباراة \n {aEntry[3].split("T")[1]}GMT \n \n النتيجة \n {aEntry[2]}'
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'foot.png', '', sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
 
    oGui.setEndOfDirectory()

def showVideos():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="match-container">\s*<a href="([^"]+)" target="_blank" title="([^"]+)".+?id="result">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[1].replace('بث مباشر اليوم','')
            if 'مباراة' in sTitle:
                sTitle = sTitle.split('مباراة')[1]
                if 'كورة' in sTitle:
                    sTitle = sTitle.split('كورة')[0]
            sThumb = ''
            siteUrl =  aEntry[0]
            sDesc = f'النتيجة \n {aEntry[2]}'
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, 'foot.png', '', sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)

    sStart = "<ul class='goals-tabs'>"
    sEnd = '</ul></div>'
    sHtmlContent2 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = "href='([^']+)'.+?<strong>(.+?)</strong>"
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = URL_MAIN + aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showVideos', sTitle, 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oOutputParameterHandler = cOutputParameterHandler()


    sHosterUrl = sUrl.split('?src=')[1]

    if '.mp4' in sHosterUrl:
        sHosterUrl = sHosterUrl
    else:
        sHosterUrl = 'https://www.youtube.com/watch?v=' +  sHosterUrl

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    sHosterUrl = sHosterUrl 
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

    oGui.setEndOfDirectory()    

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if '.mp4' in sUrl:
        oOutputParameterHandler = cOutputParameterHandler()
        sTitle = ' نتيجة مباراة ' + sMovieTitle
        url = sUrl.split('src=')[1]

        sHosterUrl = url
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        sHosterUrl = sHosterUrl 
        if oHoster:
           oHoster.setDisplayName(sTitle)
           oHoster.setFileName(sTitle)
           cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

    murl = ''
    sTitle = ''
    sHosterUrl = ''

    sPattern = 'iframe.src = ["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            murl = aEntry + sUrl.split('src=')[1]
            if 'youtube' in murl or 'ok' in murl:
                sHosterUrl = murl
                sDisplayTitle = sMovieTitle

                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'http:' + sHosterUrl            

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
            else:
                oRequestHandler = cRequestHandler(murl)
                sHtmlContent = oRequestHandler.request()

    else:
        sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                murl = aEntry

                oRequestHandler = cRequestHandler(murl)
                sHtmlContent = oRequestHandler.request()

    if 'class="albaplayer_name' not in sHtmlContent:
        if 'youtube' in murl or 'ok' in murl:
            sHosterUrl = murl
            sDisplayTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)

            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

        sPattern = '<iframe src=["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                murl = aEntry       

                oRequestHandler = cRequestHandler(murl)
                sHtmlContent = oRequestHandler.request()

    sStart = 'class="albaplayer_name">'
    sEnd = 'class="albaplayer_server-body'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            murl = aEntry[0]

            oRequestHandler = cRequestHandler(murl)
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
            sPattern = 'source:\s*["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry
                    if 'm3u8' not in url:
                        try:
                            sPatternUrl = "source: 'https:\/\/'\s*\+\s*serv\s*\+\s*'([^']+)'"
                            sPatternPK = 'var servs = .+?,\s*"([^"]+)"'
                            aResultUrl = re.findall(sPatternUrl, sHtmlContent)
                            aResultPK = re.findall(sPatternPK, sHtmlContent)
                            if aResultUrl and aResultPK:
                                url3 = 'http://'+aResultPK[0]+aResultUrl[0]
                                url1 = url3 + "|Referer=" + url
                        except:
                            VSlog('no link detected')

                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                    if url.startswith('//'):
                        url = 'https:' + url
            
                
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if 'm3u8' in sHosterUrl:
                        oHoster = cHosterGui().getHoster('lien_direct')
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
                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                    if url.startswith('//'):
                        url = 'https:' + url


                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false'
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)   	

            sPattern = 'embeds =(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry.replace(' ["',"")
                    if 'm3u8' in url:           
                        sHosterUrl = url.split('=')[1]
                    if '.php' in url:
                        import requests    
                        oRequestHandler = cRequestHandler(url)
                        St=requests.Session()
                        oRequestHandler = cRequestHandler(url)
                        sHtmlContent2 = St.get(url).content.decode('utf-8') 
                        oParser = cParser()
                        sPattern =  "src='(.+?)' type="
                        aResult = oParser.parse(sHtmlContent2,sPattern)
                        if aResult[0]:
                           for aEntry in aResult[1]:
                               url = aEntry
                               sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                               if url.startswith('//'):
                                   url = 'https:' + url
                               sHosterUrl = url
                               oHoster = cHosterGui().checkHoster(sHosterUrl)
                               if oHoster:
                                   oHoster.setDisplayName(sTitle)
                                   oHoster.setFileName(sMovieTitle)
                                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = '<iframe src="(.+?)" allowfullscreen'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry.replace("('","").replace("')","")
                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                    if url.startswith('//'):
                        url = 'https:' + url
            
                
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false'
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = '<video.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry.replace("('","").replace("')","")
                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                    if url.startswith('//'):
                        url = 'https:' + url
            
                
                    sHosterUrl = url
                    oHoster = cHosterGui().getHoster('lien_direct') 
                    sHosterUrl = sHosterUrl + "|Referer=" + murl
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = 'var file = ["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry.replace("('","").replace("')","")
                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                    if url.startswith('//'):
                        url = 'https:' + url
            
                
                    sHosterUrl = url 
                    oHoster = cHosterGui().getHoster('lien_direct') 
                    sHosterUrl = sHosterUrl + "|Referer=" + murl
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = "<script>AlbaPlayerControl([^<]+)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]: 
               import base64
               for aEntry in aResult[1]:
                   url_tmp = aEntry
                   url = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
                   sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer='+ murl

                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + murl
                   if 'm3u8' in sHosterUrl:
                       oHoster = cHosterGui().getHoster('lien_direct') 
                   else:
                       oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sTitle)
                       oHoster.setFileName(sTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)	

            sPattern = "<source src='(.+?)' type='application/x-mpegURL'"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry.replace("('","").replace("')","")
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ murl 
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + url
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    if 'http' not in aEntry:
                        continue
                    if 'javascript' in aEntry:
                        continue
                    url = aEntry
                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                    if 'sharecast' in url:
                            Referer =  "https://sharecast.ws/"
                            url = Hoster_ShareCast(url, Referer)

                    if 'live7' in url:
                            oRequestHandler = cRequestHandler(url)
                            oRequestHandler.addHeaderEntry('Referer', url)
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
                                url = 'https://' + url3

                    if 'sportsonline' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2   

                    if 'abolishstand' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2 + "|Referer=" + url

                    if 'realbitsport' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2   

                    if 'youtube' in url:
                            url = url  

                    if 'ok.ru' in aEntry:
                            url = aEntry 

                    if 'javascript' in url:
                            url = ''
                    if '/albaplayer/ch' in url:
                            if 'ch2cdn/' in url:
                                url = 'https://ninecdn.online/albaplayer/ch2cdn/'
                            if 'ch3cdn/' in url:
                                url = 'https://ninecdn.online/albaplayer/ch3cdn/'
                            if 'ch4cdn/' in url:
                                url = 'https://ninecdn.online/albaplayer/ch4cdn/'
                            oRequestHandler = cRequestHandler(url)
                            oRequestHandler.addHeaderEntry('Referer', url)
                            data3 = oRequestHandler.request()                        

                            sPattern = "AlbaPlayerControl.+?'([^\']+)"
                            aResult = re.findall(sPattern, data3)
                            if aResult:
                                url = f'{base64.b64decode(aResult[1]).decode("utf8",errors="ignore")}|Referer={url}'
                                sHosterUrl = url
                                oHoster = cHosterGui().checkHoster(sHosterUrl)
                                sHosterUrl = sHosterUrl
                                if oHoster:
                                    oHoster.setDisplayName(sTitle)
                                    oHoster.setFileName(sTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
                    
                    elif '.php' in url or 'stream' in url:
                        url2 = getHosterIframe(url,url) 
                        url = url2   

                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sHosterUrl = sHosterUrl
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()    

def Hoster_ShareCast(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60')
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()
    sPattern = "new Player\(.+?player\",\"([^\"]+)\",{'([^\']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        site = 'https://' + aResult[0][1]
        url = (site + '/hls/' + aResult[0][0]  + '/live.m3u8') + '|Referer=' + Quote(site)
        return url 

    return False, False

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
            return url

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
        return aResult[0] + '|referer=' + referer

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

    sPatternUrl = "source: 'https:\/\/' \+ serv \+ '([^']+)'"
    sPatternPK = 'var servs = .+?, "([^"]+)"'
    aResultUrl = re.findall(sPatternUrl, sHtmlContent)
    aResultPK = re.findall(sPatternPK, sHtmlContent)

    if aResultUrl and aResultPK:
        url3 = 'http://'+aResultPK[0]+aResultUrl[0]
        return url3 + "|Referer=" + referer

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return True, aResult[0] + '|referer=' + url

    sPattern = 'source\s*["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    return False
	