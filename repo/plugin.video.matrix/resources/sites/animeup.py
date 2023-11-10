# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'animeup'
SITE_NAME = 'Anime4up'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_NEWS = (URL_MAIN + '/anime-season/صيف-2023/', 'showSeries')
ANIM_MOVIES = (URL_MAIN + '/anime-type/movie-3/', 'showMovies')

URL_SEARCH = (URL_MAIN + '/?search_param=animes&s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?search_param=animes&s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + '/?search_param=animes&s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أحدث الأفلام', 'anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)
            
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/episode/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'يعرض الان', 'anime.png', oOutputParameterHandler)    

    oGui.setEndOfDirectory()
             
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?search_param=animes&s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?search_param=animes&s='+sSearchText
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
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?href="([^<]+)" class="overlay"></a>'
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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[2]
            sThumb = aEntry[0]
            sYear = ""
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?href="([^<]+)" class="overlay"></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("الجزء","الموسم").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            
            siteUrl = aEntry[2]
            sThumb = aEntry[0]
            sYear = ""
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sStart = '<h3>حلقات الأنمي</h3>'
    sEnd = '<div class="footer">'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)  

    sPattern = '<h3><a href="([^<]+)">([^<]+)</a></h3>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("الأخيرة","")
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)        
		
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    else:
        sStart = '<div class="all-episodes">'
        sEnd = '<div class="form-group">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)    

        sPattern = 'href="([^<]+)">([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("الأخيرة","")
                sTitle = sMovieTitle+sTitle
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ""		

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:      
        return aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     
    sPattern = '<a href="(.+?)" target="_blank"><i class="fa fa-star"></i><span>(.+?)</span><span>(.+?)</span></a>' 
    aResult1 = re.findall(sPattern, sHtmlContent)
    aResult = aResult1 	
    if aResult:
        for aEntry in aResult:
            
            url = aEntry[0].replace('/d','/f')
            sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, aEntry[1])

            sHosterUrl = url
            if '?download_' in sHosterUrl:
                sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sStart = '<div class="tab-content"'
    sEnd = '<div class="container">'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li>(.+?)</li>(.+?)</ul>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :  
        for aEntry in reversed(aResult[1]):
            sQual = aEntry[0].replace("الجودة المتوسطة","").replace("الجودة العالية","").replace("الجودة الخارقة","").strip()
            sHtmlContent = aEntry[1]

            sPattern = 'href="(.+?)">(.+?)</a>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                for aEntry in aResult[1]:            
                    url = aEntry[0]
                    sTitle = aEntry[1]
                    if url.startswith('//'):
                        url = 'http:' + url

                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = ('[COLOR coral](%s)[/COLOR]') % (sQual)
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()	