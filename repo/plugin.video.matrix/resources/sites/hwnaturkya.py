# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.multihost import cMegamax
import re
import requests

SITE_IDENTIFIER = 'hwnaturkya'
SITE_NAME = 'HwnaTurkya'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_TR = (URL_MAIN + 'category/مسلسلات-تركية-مترجمة', 'showSeries')
SERIE_TR_AR = (URL_MAIN + 'category/مسلسلات-تركية-مدبلجة', 'showSeries')
MOVIE_TURK = (URL_MAIN + 'category/افلام-تركية-مترجمة', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + 'category/افلام-تركية-مدبلجة', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search/', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showSeries')
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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية مدبلجة', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', 'turk.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search/'+sSearchText
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

    sPattern = '<article class="post">.+?<a href="([^"]+)" title="([^"]+)".+?data-original="([^"]+)'
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
            siteUrl = aEntry[0] .replace("/movies/","/watch_movies/")
            sThumb = aEntry[2]
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch: 
        sPattern = '<li><a href="([^"]+)" data-ci-pagination-page="([^"]+)'
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
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)

            progress_.VSclose(progress_)
 
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
    sPattern = '<article class="post">.+?<a href="([^"]+)" title="([^"]+)".+?data-original="([^"]+)'
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
            sDesc = ''
            sYear = ''
            sThumb = aEntry[2]
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            if 'موسم' not in aEntry[1]:
                sTitle = f'{sTitle} S1'
            sThumb = aEntry[2]
            siteUrl = aEntry[0]
            sDesc = ""
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace(" الأول","1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("الموسم","S").replace("S ","S")


            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch: 
        sPattern = '<li><a href="([^"]+)" data-ci-pagination-page="([^"]+)'
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
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

            progress_.VSclose(progress_)

        oGui.setEndOfDirectory()
 
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<div id="getSeasonsBySeries" class="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:

        sStart = '<a title="سلسلة مواسم">'
        sEnd = '<div class="container">'
        sHtmlContents = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<div class="seasonNum">(.+?)</div>.+?href="(.+?)" title="(.+?)">.+?src="([^"]+)'
        aResult = oParser.parse(sHtmlContents, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:

                sTitle =  aEntry[0].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace(" الأول","1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("الموسم","S").replace("S ","S")
                siteUrl = aEntry[1]
                sThumb = aEntry[3]
                sDesc = ''
                if sThumb.startswith('//'):
                    sThumb = "https:"+aEntry[1]
			
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
        sPattern = '<a class href="([^"]+)" title="([^"]+)".+?class="numEp">([^<]+)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = sMovieTitle + ' E'+ aEntry[2]
                sThumb = sThumb
                siteUrl = aEntry[0].replace("/episodes/","/watch_episodes/")
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<a class href="([^"]+)" title="([^"]+)".+?class="numEp">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = sMovieTitle + ' E'+ aEntry[2]
            sThumb = sThumb
            siteUrl = aEntry[0].replace("/episodes/","/watch_episodes/")
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    oGui.setEndOfDirectory() 

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  "baseUrl = '([^']+)" 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        URL_MAIN = aResult[1][0] 

    sPattern =  'postID = "([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        postID = aResult[1][0] 

    sPattern =  'onclick="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
                    sServer = aEntry.replace("getPlayer('","").replace("')","")

                    s = requests.Session()            
                    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.188',
                        'origin': URL_MAIN,
                        'referer': URL_MAIN,
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'Accept': '*/*'}

                    data = {'server':sServer,'postID':postID,'Ajax':'1'}
                    r = s.post(f'{URL_MAIN}ajax/getPlayer', headers=headers,data = data)
                    sHtmlContent1 = r.content.decode('utf8')

                    sPattern = '<IFRAME.+?SRC=["\']([^"\']+)["\']'
                    aResult = oParser.parse(sHtmlContent1, sPattern)
                    if aResult[0]:
                        oOutputParameterHandler = cOutputParameterHandler()
                        for aEntry in (aResult[1]):
                            if 'قريبا' in aEntry:
                                continue
                            if 'leech' in aEntry:
                                continue

                            sHosterUrl = aEntry
                            if sHosterUrl.startswith('//'):
                                sHosterUrl = 'http:' + sHosterUrl

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

                                        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster != False:
                                oHoster.setDisplayName(sMovieTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = '<a target="_blank" href=["\']([^"\']+)["\'].+?<i class="icon-download">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            if 'megamax' in aEntry:
                continue
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks():
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