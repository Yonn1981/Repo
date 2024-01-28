# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
import re
import requests

SITE_IDENTIFIER = 'hkyturk'
SITE_NAME = 'HkyahTurkiya'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_TR = (URL_MAIN + 'category/مسلسلات-تركية-مترجمة/', 'showSeries')
SERIE_TR_AR = (URL_MAIN + 'category/مسلسلات/مسلسلات-تركية-مدبلجة/', 'showSeries')
MOVIE_TURK = (URL_MAIN + 'movies/', 'showMovies')

URL_SEARCH = (URL_MAIN + '/search/', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'episodes/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries2', 'احدث الحلقات', 'turk.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
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
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request().replace('&rsaquo;', '>').replace('&raquo;', '>>').replace('&lsaquo;', '<')

    sPattern = 'class="block-post">.+?href="([^"]+)" title="([^"]+)".+?style="background-image:url([^<]+);"></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[1]:
                continue
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0] + '?do=watch'
            sThumb = re.sub(r'-\d*x\d*.','.', aEntry[2].replace("(","").replace(")",""))
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
    if not sSearch: 
        sStart = '<div class="pagination">'
        sEnd = '<div class="footer"'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = 'href="([^"]+)" class=".+?">(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)

        sPattern = 'href="([^"]+)">(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler) 

    oGui.setEndOfDirectory()

def showSeries2(sSearch = ''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request().replace('&rsaquo;', '>').replace('&raquo;', '>>').replace('&lsaquo;', '<')

    sPattern = 'class="block-post">.+?href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[1]:
                continue
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثانى","S2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            siteUrl = aEntry[0] + '?do=watch'
            sThumb = aEntry[2]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    sStart = '<div class="pagination">'
    sEnd = '<div class="footer"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+)" class=".+?">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries2', sTitle, '', oOutputParameterHandler)

    sPattern = 'href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries2', sTitle, '', oOutputParameterHandler) 

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
    sHtmlContent = oRequestHandler.request().replace('&rsaquo;', '>').replace('&raquo;', '>>').replace('&lsaquo;', '<')

    itemList = []	
    sPattern = 'class="block-post">.+?href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[1]:
                continue
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sTitle = sTitle.split('الموسم')[0].split('الحلقة')[0].replace('- قصة عشق','')
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace("(","").replace(")","")
            sDesc = ""

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch: 
        sStart = '<div class="pagination">'
        sEnd = '<div class="footer"'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = 'href="([^"]+)" class=".+?">(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

        sPattern = 'href="([^"]+)">(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler) 

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
    
    sPattern = 'data-season="(.+?)">(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sSeason = aEntry[1].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]
            if bool(re.search(r'\d', sSeason)) is False:
                sSeason = "S1"
            siteUrl = URL_MAIN+'wp-content/themes/vo2023/temp/ajax/seasons.php?seriesID='+aEntry[0]
            sTitle = f'{sMovieTitle} {sSeason}' 
            sThumb = sThumb
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('siteUrl0',sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)	

    else:
        sPattern = '<a class="epNum" href="([^"]+)".+?<span>(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
                sTitle =  f'{sMovieTitle} E{aEntry[1]}'
                siteUrl = aEntry[0] + '?do=watch'
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sPattern = '<a class="epNum.+?" href="([^"]+)".+?<span>(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
                sTitle =  f'{sMovieTitle} E{aEntry[1]}'
                siteUrl = aEntry[0] + '?do=watch'
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl0 = oInputParameterHandler.getValue('siteUrl0')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    St=requests.Session()
    oRequestHandler = cRequestHandler(sUrl0)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    siteUrl = str(sUrl).split('?')[0]

    sCode = sUrl.split('seriesID=')[1]
    cook = oRequestHandler.GetCookies()
    hdr = {'x-requested-with' : 'XMLHttpRequest','accept' : '*/*','referer' : sUrl0.encode('utf-8'),'Cookie' : cook}
    params = {'seriesID':sCode}                

    sHtmlContent = St.get(siteUrl,headers=hdr,params=params)
    sHtmlContent = sHtmlContent.content

    sPattern = 'href="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = f'{sMovieTitle} E{aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("الموسم"," S").replace("S ","S").replace("الحلقة "," E").replace("حلقة "," E")}'
            siteUrl = aEntry[0] + '?do=watch'
            sThumb = sThumb
            sDesc = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    oGui.setEndOfDirectory() 

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Referer = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<link rel=["\']shortlink["\'] href=["\']([^"\']+)["\']' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sPage = aResult[1][0].split('?p=')[1]

    sPattern = 'id="s_.+?onClick=".*?getServer2([^"]+)"'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            ServerIDs = aEntry.replace('(this.id,','').replace(');','') 
            sHosterID = ServerIDs.split(',')[0]
            serverId = ServerIDs.split(',')[1]
      
            url = f'{URL_MAIN}wp-content/themes/vo2023/temp/ajax/iframe2.php?id={sPage}&video={sHosterID}&serverId={serverId}'

            oRequestHandler = cRequestHandler(url)
            cook = oRequestHandler.GetCookies()
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
            sHtmlContent2 = oRequestHandler.request()
    
            sPattern = 'iframe.+?src=["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent2.lower(), sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]

                if 'mystream' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    else:
        sPattern = 'id="s_.+?onClick=".*?getServer([^"]+)"'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterID = aEntry.replace('(this.id,','').replace(');','') 

                url = f'{URL_MAIN}wp-content/themes/vo2023/temp/ajax/iframe.php?id={sPage}&video={sHosterID}'

                oRequestHandler = cRequestHandler(url)
                cook = oRequestHandler.GetCookies()
                oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
                oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
                oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
                oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
                oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
                oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
                sHtmlContent2 = oRequestHandler.request()
    
                sPattern = 'iframe.+?src=["\']([^"\']+)["\']'
                aResult = oParser.parse(sHtmlContent2.lower(), sPattern)
                if aResult[0]:
                    sHosterUrl = aResult[1][0]

                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster != False:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()