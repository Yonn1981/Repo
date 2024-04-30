# -*- coding: utf-8 -*-

import re
import requests
from six.moves import urllib_parse
import six
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, VSlog, addon
from resources.lib.parser import cParser
from resources.lib.multihost import cMegamax
from resources.lib.util import Quote
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

SITE_IDENTIFIER = 'cimalek'
SITE_NAME = 'Cimalek'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_FAM = (URL_MAIN + 'category/aflam-online/aflam-family/', 'showMovies')
MOVIE_EN = (URL_MAIN + 'category/aflam-online/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/asian-aflam/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/indian-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/cartoon-movies/', 'showMovies')
ANIM_MOVIES = (URL_MAIN + 'category/anime-movies/', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + 'category/netflix-movies/', 'showMovies')

SERIE_EN = (URL_MAIN + 'category/english-series/', 'showSeries')
SERIE_NETFLIX = (URL_MAIN + 'category/netflix-series/', 'showSeries')
ANIM_NEWS = (URL_MAIN + 'category/anime-series/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/asian-series/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام نتفليكس', 'netflix.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات نتفليكس', 'netflix.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler)
	
    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return		
		
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
	
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
    
    sPattern = '<div class="film-poster".+?<a href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  not in aEntry[2]:
                continue
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","") 
            siteUrl = aEntry[0]+"/watch/"
            sDesc = ''
            sThumb = aEntry[1]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-id=".+?">.+?<a href="(.+?)">.+?data-src="(.+?)" alt="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  in aEntry[2]:
                continue
 
            siteUrl = aEntry[0]            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[1]
            sDesc = ''
            sTitle = sTitle.split('موسم')[0].split('حلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
    if not sSearch:
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
        oGui.setEndOfDirectory()
  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "class='arrow_pag' href=(.+?)><i id='nextpagination"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:  
        return aResult[1][0].replace('"',"")

    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "href='([^<]+)' title='(.+?)'><span class='serie'>"
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").replace("الحلقة ","E").replace("الحلقة ","E").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            siteUrl = aEntry[0]+"/watch/"
            sThumb = sThumb
            sDesc = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('sDesc', sDesc)           
             
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
	 
def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '"ver":"([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        ver = aResult[1][0] 

    sPattern =  '"site_url":["\']([^"\']+)["\']' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sHost = aResult[1][0].replace('\\','')

    sPattern =  'data-type=["\']([^"\']+)["\'] data-post=["\']([^"\']+)["\'] data-nume=["\']([^"\']+)["\']><ul><li>(.+?)</li>'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
       oOutputParameterHandler = cOutputParameterHandler()
       for aEntry in aResult[1]: 
           
            dtype = aEntry[0]
            dpost = aEntry[1]
            dnume = aEntry[2]
            dHost = aEntry[3]
            drand = getRandomString()
            
            siteUrl = f'{sHost}/wp-json/lalaplayer/v2/?p={dpost}&t={dtype}&n={dnume}&ver={ver}&&rand={drand}'
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, dHost)

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('Referer', Quote(sUrl))

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

    sPattern = 'data-pid="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        pid = aResult[1][0] 
        token = getToken(sHost)
        siteUrl = f'{sHost}/wp-json/direct_download/v1/?p={pid}&rand={drand}&recaptcha_token={token}'
        sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, 'Direct Downloads')

        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sHost', sHost)
        oOutputParameterHandler.addParameter('Referer', Quote(sUrl))

        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

    sStart = '>روابط التحميل</h2>'
    sEnd = '<footer'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?<em>(.+?)</em>'
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry[0]
            sQual = aEntry[1].split('P')[0]

            if 'megamax' in sHosterUrl:
                data = cMegamax().GetUrls(sHosterUrl)
                if data is not False:
                    for item in data:
                        sHosterUrl = item.split(',')[0].split('=')[1]
                        sQual = item.split(',')[1].split('=')[1]
                        sLabel = item.split(',')[2].split('=')[1]

                        sDisplayTitle = ('%s [COLOR coral] [%s][/COLOR][COLOR orange] - %s[/COLOR]') % (sMovieTitle, sQual, sLabel)      
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('sQual', sQual)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'showLinks2', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

            sDisplayTitle = ('%s [COLOR coral] [%s][/COLOR]') % (sMovieTitle, sQual)   
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks2():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sQual = oInputParameterHandler.getValue('sQual')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sDisplayTitle = ('%s [COLOR coral] [%s] [/COLOR]') % (sMovieTitle, sQual)   
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sHost = oInputParameterHandler.getValue('sHost')
    Referer = oInputParameterHandler.getValue('Referer')

    oParser = cParser()
    oRequestHandler = cRequestHandler(siteUrl)
    oRequestHandler.addHeaderEntry('host', sHost.split('//')[1])
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', Referer)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    sData = oRequestHandler.request() 

    sPattern = '"embed_url":\s*"([^"]+)'
    aResult = oParser.parse(sData, sPattern)
    if aResult:
        for aEntry in aResult[1]:
            sUrl = aEntry.replace("\\","")
            sHosting = aEntry.rsplit("/",-1)[2]
            if sUrl.startswith('//'):
                sUrl = 'http:' + sUrl

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', Referer)
            oRequestHandler.addHeaderEntry('Sec-Fetch-Dest', 'iframe')
            sData = oRequestHandler.request() 
            
            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sData, sPattern)
            if aResult[0] is True:
                for aEntry in aResult[1]:
                    url = aEntry.replace("\\","")
                    if url.startswith('//'):
                        url = 'http:' + url
                    sHosterUrl = url                   
                    oHoster = cHosterGui().checkHoster(sHosterUrl) 
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

            else:
                sPattern = '"link":"([^"]+)'
                aResult = oParser.parse(sData, sPattern)
                if aResult[0] is True:
                    for aEntry in aResult[1]:
                        url = aEntry.replace("\\","")                  
                        if url.startswith('/'):
                            url = f'https://{sHosting}' + url

                        hdrs = {
                            "Referer": sUrl,
                            "Sec-Fetch-Dest": "iframe",
                            "Host": sHosting}
                        sData = requests.get(url, headers=hdrs).url
                        sHosterUrl = sData                   
                        oHoster = cHosterGui().checkHoster(sHosterUrl) 
                        if oHoster:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)


                    sHosterUrl = url + f'|Referer=https://{sHosting}/' + f'&Origin=https://{sHosting}'

                    oHoster = cHosterGui().getHoster('febb')
                    sDisplayTitle = sMovieTitle  
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = '"url":"([^"]+)","encrypted":"([^"]+)'
    aResult = oParser.parse(sData, sPattern)
    VSlog(aResult)
    if aResult:
        for aEntry in aResult[1]:
            sUrl = aEntry[0].replace("\\","")
            sCode = aEntry[1].split('=')[0]
            drand = getRandomString()
            sHost = sUrl.split('//')[1].split('/get')[0]

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Host', sHost)
            oRequestHandler.addHeaderEntry('Origin', URL_MAIN.rsplit("/",1)[0])
            oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
            oRequestHandler.addParameters('o', sCode)
            oRequestHandler.addParameters('rand', drand)
            oRequestHandler.setRequestType(1)
            sData2 = oRequestHandler.request(jsonDecode=True)

            sources = sData2["direct_download"]["private_server"]["sources"]
            for source in sources:
                if "file" in source:
                    file_url = source["file"]
                    oRequestHandler = cRequestHandler(file_url)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                    oRequestHandler.addHeaderEntry('Host', sHost)
                    oRequestHandler.request()
                    url = oRequestHandler.getRealUrl()
                    label = source["label"]
            
                    tracks = sData2["direct_download"]["private_server"]["tracks"]
                    sSubtitle = tracks[0]["file"]

                    sHosterUrl = url + '?sub.info=' + sSubtitle               
                    oHoster = cHosterGui().getHoster('lien_direct')   
                    sDisplayTitle = ('%s [COLOR coral] [%s] [/COLOR]') % (sMovieTitle, label)   
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def getRandomString(length=16):
    import random
    allowedChars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return ''.join(random.choice(allowedChars) for _ in range(length))

def b64encode(b):
    return six.ensure_str(base64.b64encode(six.ensure_binary(b)))


def getToken(sHost):
    s = requests.Session()
    rurl = 'https://www.google.com/recaptcha/api.js'
    aurl = 'https://www.google.com/recaptcha/api2'
    hdrs = {'User-Agent': UA,
        'Referer': sHost + '/'}
    url = sHost
    co = None
    sa = ''

    key = '6LfUn7QZAAAAAL2sQ3NMTAbJxlQApCdB06PIFLQs'
    if co is None:
            co = b64encode((url + ':443')).replace('=', '')

    rurl = '{0}?render={1}'.format(rurl, key)

    page_data1 = s.get(rurl, headers=hdrs).text
    v = re.findall('releases/([^/]+)', page_data1)[0]

    rdata = {'ar': 1,
                 'k': key,
                 'co': co,
                 'hl': 'en',
                 'v': v,
                 'size': 'invisible',
                 'cb': '123456789'}
    
    page_data2 = s.get('{0}/anchor?{1}'.format(aurl, urllib_parse.urlencode(rdata)), headers=hdrs).text
    page_data2 = page_data2.replace('\x22', '')
    aresult = re.findall("recaptcha-token.*?=(.*?)>", page_data2)
    if aresult:
                c = aresult[0]

    url3 = f"{aurl}/reload?k=" + key

    post_data = {'v': v, 
                 'reason': 'q', 
                 'k': key, 
                 'c': c, 
                 'sa': sa, 
                 'co': co}

    headers2 = {'user-agent': UA,
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
                'Referer': '{0}/anchor?{1}'.format(aurl, urllib_parse.urlencode(rdata))
                }

    req_url3 = s.post(url3, data=post_data, headers=headers2)
    data = req_url3.text
    aresult = re.findall("resp\",\"(.*?)\"", data)
    if aresult:
        token = aresult[0]
        return token