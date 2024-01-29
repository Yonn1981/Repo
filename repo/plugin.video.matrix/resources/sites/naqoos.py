# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import requests
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import Unquote
 
SITE_IDENTIFIER = 'naqoos'
SITE_NAME = 'Naqoos'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%86%d9%85%d9%8a/', 'showMovies')

SERIE_EN = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/', 'showSeries')
SERIE_DUBBED = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries')
SERIE_TR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a/', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showSeries')
ANIM_NEWS = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d9%86%d9%85%d9%8a/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN +'?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN +'?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), 'search.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
         
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)  
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
       
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdblg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler) 

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s=فيلم+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s=مسلسل+'+sSearchText
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
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<div class="poster">.+?data-src="([^"]+)" alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            siteUrl = aEntry[2]
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[0])  
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="poster">.+?data-src="([^"]+)" alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace(" والأخيرة","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            siteUrl = aEntry[2]
            sThumb = aEntry[0]
            sDesc = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","").replace("الموسم الحادي عشر","").replace("الموسم الثاني عشر","").replace("الموسم الثالث عشر","").replace("الموسم الرابع عشر","").replace("الموسم الخامس عشر","").replace("الموسم السادس عشر","").replace("الموسم السابع عشر","").replace("الموسم الثامن عشر","").replace("الموسم التاسع عشر","").replace("الموسم العشرون","").replace("الموسم الحادي و العشرون","").replace("الموسم الثاني و العشرون","").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","").replace("الموسم الخامس و العشرون","").replace("الموسم السادس والعشرون","").replace("الموسم السابع والعشرون","").replace("الموسم الثامن والعشرون","").replace("الموسم التاسع والعشرون","").replace("الموسم الثلاثون","").replace("الموسم الحادي و الثلاثون","").replace("الموسم الثاني والثلاثون","").replace("الموسم الاول","").replace("الموسم الثاني","").replace("الموسم الثالث","").replace("الموسم الثالث","").replace("الموسم الرابع","").replace("الموسم الخامس","").replace("الموسم السادس","").replace("الموسم السابع","").replace("الموسم الثامن","").replace("الموسم التاسع","").replace("الموسم","").replace("S ","").replace("الحلقة","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("10","").replace("11","").replace("12","").replace("13","").replace("14","").replace("15","").replace("16","").replace("17","").replace("18","").replace("19","").replace("20","").replace("21","").replace("22","").replace("23","").replace("24","").replace("25","").replace("26","").replace("27","").replace("28","").replace("29","").replace("30","").replace("0","").replace("season","")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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

	sPattern = 'class="numerando">(.+?)</div><div class="episodiotitle"><a href="([^"]+)'
	aResult = oParser.parse(sHtmlContent, sPattern)
	if aResult[0] is True:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
            
			sTitle = re.sub('(\d+) - (\d+)', ' Season \g<1> Episode \g<2>', aEntry[0])
			sTitle = sMovieTitle + sTitle
			siteUrl = aEntry[1]
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()    
    sPattern = 'class="current">.+?<a href="([^"]+)'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

def showLinks(oInputParameterHandler = False):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
          
    sPattern = 'data-type="([^"]+)" data-post="([^"]+)" data-nume="([^"]+).+?class="server">(.+?)</span>' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:  
            if 'short.ink' in aEntry[3]:
                continue
            
            sType = aEntry[0]
            sPost = aEntry[1]
            sNume = aEntry[2]
            sHost = aEntry[3]
            sUrl = f'{URL_MAIN}wp-json/dooplayer/v2/{sPost}/{sType}/{sNume}'
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)
		               
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"embed_url":\s*"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult:
        url = aResult[1][0]
        if URL_MAIN in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult:
                url = Unquote(aResult[1][0])
                url = url.split('source=')[1]

        sHosterUrl = url
        if 'vidtube' in sHosterUrl:
            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
        if 'updown' in sHosterUrl:
            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()