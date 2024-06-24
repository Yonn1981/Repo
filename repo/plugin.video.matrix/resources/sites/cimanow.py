# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/
# Yonn1981 https://github.com/Yonn1981/Repo
# big thx to Rgysoft

import re
import base64	
import requests
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

SITE_IDENTIFIER = 'cimanow'
SITE_NAME = 'CimaNow'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}/category/افلام-اجنبية/', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}/category/%d8%a7%d9%84%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}/category/%d8%a7%d9%84%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}/category/افلام-انيميشن/', 'showMovies')

SERIE_TR = (f'{URL_MAIN}/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showSeries')
RAMADAN_SERIES = (f'{URL_MAIN}/category/رمضان-2024/', 'showSeries')
SERIE_EN = (f'{URL_MAIN}/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showSeries')
SERIE_AR = (f'{URL_MAIN}/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}/category/مسلسلات-انيميشن/', 'showSeries')

DOC_NEWS = (f'{URL_MAIN}/?s=%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A', 'showMovies')
REPLAYTV_NEWS = (f'{URL_MAIN}/category/%d8%a7%d9%84%d8%a8%d8%b1%d8%a7%d9%85%d8%ac-%d8%a7%d9%84%d8%aa%d9%84%d9%81%d8%b2%d9%8a%d9%88%d9%86%d9%8a%d8%a9/', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}/?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
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
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/category/رمضان-2023/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان 2023', 'rmdn.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s=%D9%81%D9%8A%D9%84%D9%85+{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+{sSearchText}'
        showSeries(sUrl)
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
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    page = oRequest.request()

    if 'adilbo' in page:
        page = decode_page(page)

    sPattern = '<article aria-label="post"><a href="([^"]+).+?<li aria-label="year">(.+?)</li>.+?<li aria-label="title">([^<]+)<em>.+?data-src="(.+?)" width'
    aResult = oParser.parse(page, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            try:
                sTitle = str(sTitle.encode('latin-1'),'utf-8')
                sThumb = str(aEntry[3].encode('latin-1'),'utf-8')
            except:
                sTitle = str(sTitle)
                sThumb = str(aEntry[3])
            siteUrl = aEntry[0] + '/watching/'
            if sThumb.startswith('//'):
                sThumb = f'http:{sThumb}'
            sYear = aEntry[1]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sStart = '</section>'
        sEnd = '</ul>'
        page = oParser.abParse(page, sStart, sEnd)

        sPattern = '<li><a href="(.+?)">(.+?)</a>'
        aResult = oParser.parse(page, sPattern)	
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
 
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)
 
        oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    page = oRequest.request()

    if 'adilbo' in page:
        page = decode_page(page)

    sPattern = '<article aria-label="post"><a href="([^<]+)">.+?<li aria-label="year">(.+?)</li>.+?<li aria-label="title">([^<]+)<em>.+?data-src="(.+?)" width'
    aResult = oParser.parse(page, sPattern)
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[2]:
                continue
 
            sTitle = aEntry[2]
            try:
                sTitle = str(sTitle.encode('latin-1'),'utf-8')
                sThumb = str(aEntry[3].encode('latin-1'),'utf-8')
            except:
                sTitle = str(sTitle)
                sThumb = str(aEntry[3])
            siteUrl = aEntry[0]
            if sThumb.startswith('//'):
                sThumb = f'http:{sThumb}'
            sDesc = ''
            sYear = aEntry[1]
                    
            if sTitle not in itemList:
                itemList.append(sTitle)                
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sStart = '</section>'
        sEnd = '</ul>'
        page = oParser.abParse(page, sStart, sEnd)

        sPattern = '<li><a href="(.+?)">(.+?)</a>'
        aResult = oParser.parse(page, sPattern)	
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
 
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
 
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<section aria-label="seasons">'
    sEnd = '<ul class="tabcontent" id="related">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    page = oRequest.request()

    if 'adilbo' in page:
        page = decode_page(page)

    sPattern = '<a href="([^<]+)">([^<]+)<em>'
    aResult = oParser.parse(page, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            
            try:
                sSeason = str(aEntry[1].encode('latin-1'),'utf-8')
            except:
                sSeason = str(aEntry[1])
            sTitle = f'{sMovieTitle} {sSeason.replace("الموسم"," S").replace("S ","S")}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
    else:
        sMovieTitle = f'{sMovieTitle} S1'
        oOutputParameterHandler = cOutputParameterHandler() 
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addSeason(SITE_IDENTIFIER, 'showEps', sMovieTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
 
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()  
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    page = oRequest.request()

    if 'adilbo' in page:
        page = decode_page(page)

    sStart = '<section aria-label="seasons">'
    sEnd = '<ul class="tabcontent" id="related">'
    page = oParser.abParse(page, sStart, sEnd)

    sPattern = '<li><a href="([^"]+)".+?src="([^"]+)" alt="logo" />.+?<em>(.+?)</em>'
    aResult = oParser.parse(page, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            sTitle = f'{sMovieTitle} E{aEntry[2]}'
            siteUrl = f'{aEntry[0]}watching/'
            try:
                sThumb = str(aEntry[1].encode('latin-1'),'utf-8')
            except:
                sThumb = str(aEntry[1])
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showServer():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    host = sUrl.split('/')[2]
    URL_MAIN = f'https://{host}'

    oParser = cParser() 
    oRequest = cRequestHandler(sUrl)
    cook = oRequest.GetCookies()
    hdr = {'User-Agent' : UA,'Accept-Encoding' : 'gzip','cookie' : cook,'host' : host,'referer' : URL_MAIN}
    St=requests.Session()
    data = St.get(sUrl,headers=hdr)
    data = data.content.decode('utf8')  

    if 'adilbo' in data:
        data = decode_page(data)

    sStart = '<li aria-label="quality">'
    sEnd = '<li aria-label="download">'
    page0 = oParser.abParse(data, sStart, sEnd)
     	
    sPattern = '<a href="(.+?)".+?class="fas fa-cloud-download-alt"></i>(.+?)<p'
    aResult = oParser.parse(page0, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[0]
            sTitle = aEntry[1].replace('</i>',"")
            sTitle = f'{sMovieTitle} ([COLOR coral]{sTitle}[/COLOR])'
            url = url.replace("cimanow","rrsrr")
            if url.startswith('//'):
                url = f'http:{url}'
				           
            sHosterUrl = f'{url}|Referer={URL_MAIN}'
            oHoster = cHosterGui().getHoster('lien_direct')
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<iframe src="([^"]+)" scrolling'
    aResult = oParser.parse(data, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = f'http:{url}'
				
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'data-index="([^"]+)".+?data-id="([^"]+)"' 
    aResult = oParser.parse(data, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sIndex = aEntry[0]
            sId = aEntry[1]

            sTitle = 'server '
            siteUrl = f'{URL_MAIN}/wp-content/themes/Cima%20Now%20New/core.php?action=switch&index={sIndex}&id={sId}'
            hdr = {'User-Agent' : UA,'referer' : URL_MAIN}
            params = {'action':'switch','index':sIndex,'id':sId}                
            St=requests.Session()
            sHtmlContent = St.get(siteUrl,headers=hdr,params=params)
            sHtmlContent = sHtmlContent.content

            sPattern =  '<iframe.+?src="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry.replace("cimanow","rrsrrs").replace("newcima","rrsrrsn")
                    sTitle = sMovieTitle
                    if url.startswith('//'):
                        url = f'http:{url}'
            
                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                        sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<a href="([^"]+)"><i class="fa fa-download">'
    aResult = oParser.parse(data, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            url = aEntry
            if url.startswith('//'):
                url = f'http:{url}'
				
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def decode_page(data):
    t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
    t_int = re.findall('/g.....(.*?)\)', data, re.S)
    if t_script and t_int:
        script = t_script[0].replace("'",'')
        script = script.replace("+",'')
        script = script.replace("\n",'')
        sc = script.split('.')
        page = ''
        for elm in sc:
            c_elm = base64.b64decode(elm+'==').decode()
            t_ch = re.findall('\d+', c_elm, re.S)
            if t_ch:
                nb = int(t_ch[0])+int(t_int[0])
                page = page + chr(nb)

    return page