# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import requests
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, VSlog, addon
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'wecima'
SITE_NAME = 'Wecima'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_TOP = (URL_MAIN + '/movies/best/', 'showMovies')
MOVIE_POP = (URL_MAIN + '/movies/top/', 'showMovies')
MOVIE_CLASSIC = (URL_MAIN + '/movies/old/', 'showMovies')
MOVIE_FAM = (URL_MAIN + '/mpaa/pg/', 'showMovies')
MOVIE_EN = (URL_MAIN + '/category/افلام/10-movies-english-افلام-اجنبي/', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')
MOVIE_AR = (URL_MAIN + '/category/افلام/افلام-عربي-arabic-movies/', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/category/افلام/افلام-تركى-turkish-films/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/افلام/افلام-هندي-indian-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')

RAMADAN_SERIES = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2023-series-ramadan-2023/list/', 'showSeries')

SERIE_AR = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/13-%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d9%87-arabic-series/list/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/مسلسلات/5-series-english-مسلسلات-اجنبي/list/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/مسلسلات/9-series-indian-مسلسلات-هندية/list/', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d8%b1%d8%aa%d9%88%d9%86/list/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/list/', 'showSeries')
SERIE_TR = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/8-%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9-turkish-series/list/', 'showSeries')

DOC_SERIES = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9-documentary-series/list/', 'showSeries')
DOC_NEWS = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9-documentary-films/', 'showMovies')

URL_SEARCH = (URL_MAIN + '/search/', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + '/search/', 'showAnimes')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimesSearch', addons.VSlang(30118), 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/افلام/10-movies-english-افلام-اجنبي/سلاسل-الافلام-الكاملة-full-pack/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'سلاسل افلام كاملة', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/production/netflix/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netfilx', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/production/warner-bros/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Warner Bros', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/production/lionsgate/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Lionsgate', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/production/walt-disney-pictures/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Walt Disney', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def main_function(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="canonical" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        URL_MAIN = aResult[1][0].replace('mycima/','')
    return URL_MAIN

def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showAnimesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showAnimes(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '</i>WECIMA<logotext>'
    sEnd = '</ul><div'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'المزيد' in aEntry[1]:
                continue 

            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace((aEntry[0].split('watch/')[0]), URL_MAIN2)
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            if 'مسلسلات' in sTitle or 'برامج' in sTitle:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', sTitle, 'mslsl.png', '', '', oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'film.png', '', '', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="Thumb--GridItem"><a href="([^<]+)" title="(.+?)">.+?image:url(.+?);"><div.+?class="year">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","")
            siteUrl = aEntry[0].replace((aEntry[0].split('watch/')[0]), URL_MAIN2)
            sDesc = ''
            sThumb = aEntry[2].replace("(","").replace(")","")
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

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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
      sUrl = sSearch+'/list/series/'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="hoverable active">'
    sEnd = '</footer><'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="Thumb--GridItem"><a href="([^<]+)" title="(.+?)">.+?image:url(.+?);">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  in aEntry[1]:
                continue
 
            siteUrl = aEntry[0]
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2].replace("(","").replace(")","")
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
            oOutputParameterHandler.addParameter('URL_MAIN2', URL_MAIN2)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'
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
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showAnimes(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'/list/anime/'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="hoverable active">'
    sEnd = '</footer><'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="Thumb--GridItem"><a href="([^<]+)" title="(.+?)">.+?image:url(.+?);">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  in aEntry[1]:
                continue
 
            siteUrl = aEntry[0]    
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2].replace("(","").replace(")","")
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
            oOutputParameterHandler.addParameter('URL_MAIN2', URL_MAIN2)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'
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
			
            oGui.addTV(SITE_IDENTIFIER, 'showAnimes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showAnimes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a class="next page-numbers" href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:  
        return aResult[1][0]

    return False
  
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    URL_MAIN2 = oInputParameterHandler.getValue('URL_MAIN2')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href="([^<]+)">موسم(.+?)</a>'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult:
 
            sTitle = aEntry[1].replace("موسم","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sTitle =  " S" + sTitle
            sSeason = sTitle.replace("S ","S")
            sTitle1 = sMovieTitle+sSeason
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            

 
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle1, '', sThumb, sDesc, oOutputParameterHandler)
    else: 
        sPattern = '<a class="hoverable activable.+?href="([^"]+)".+?<episodeArea><episodeTitle>([^<]+)</episodeTitle>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
 
                sTitle = aEntry[1].replace("الحلقة","E").replace(" ","")
                sTitle = sMovieTitle+" S01 "+sTitle
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ""
                sHoster = ""
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHoster)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
 
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
    sPattern = '<a title="([^<]+)" href="([^"]+)".+?class="Quality".+?</span></div><span>([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[0]
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sDesc = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sPattern = '<div class="MoreEpisodes.+?" data-term="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            s = requests.Session()            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            data = aEntry
            r1 = s.get(URL_MAIN2+'/AjaxCenter/MoreEpisodes/'+data+'/30/', headers=headers)
            sHtmlContent1 = r1.content.decode('utf8').replace("\\","")
            r2 = s.get(URL_MAIN2+'/AjaxCenter/MoreEpisodes/'+data+'/70/', headers=headers)
            sHtmlContent2 = r2.content.decode('utf8').replace("\\","")
            sHtmlContent = sHtmlContent1+sHtmlContent2
	
            sPattern = 'href=([^<]+)"><div.+?<episodeTitle>([^<]+)<'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
 
                    siteUrl = aEntry[0].replace('"',"")
                    sTitle = " E"+aEntry[1].replace("u0627u0644u062du0644u0642u0629","")
                    sTitle = sTitle+sMovieTitle
                    sThumb = sThumb
                    sDesc = ""

                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
 
    oGui.setEndOfDirectory() 
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<a class="hoverable activable.+?href="([^<]+)"><div class="Thumb"><span><i class="fa fa-play"></i></span></div><episodeArea><episodeTitle>([^<]+)</episodeTitle></episodeArea></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = aEntry[1].replace("الحلقة ","E")
            sTitle = sMovieTitle+sSeason+sTitle
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('sDesc', sDesc)           
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sPattern = '<a title="([^<]+)" href="([^<]+)"><div class="Quality".+?</span></div><span>([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[0]
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sDesc = aEntry[2]
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sPattern = '<div class="MoreEpisodes.+?" data-term="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            s = requests.Session()            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            data = aEntry
            r1 = s.get('https://mycima.biz/AjaxCenter/MoreEpisodes/'+data+'/30/', headers=headers)
            sHtmlContent1 = r1.content.decode('utf8').replace("\\","")
            r2 = s.get('https://mycima.biz/AjaxCenter/MoreEpisodes/'+data+'/70/', headers=headers)
            sHtmlContent2 = r2.content.decode('utf8').replace("\\","")
            r3 = s.get('https://mycima.biz/AjaxCenter/MoreEpisodes/'+data+'/110/', headers=headers)
            sHtmlContent3 = r3.content.decode('utf8').replace("\\","")
            sHtmlContent = sHtmlContent1+sHtmlContent2+sHtmlContent3

            sPattern = 'href=([^<]+)"><div.+?<episodeTitle>([^<]+)<'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
 
                    siteUrl = aEntry[0].replace('"',"")
                    sTitle = " E"+aEntry[1].replace("u0627u0644u062du0644u0642u0629","")
                    sTitle = sMovieTitle+sSeason+sTitle
                    sThumb = sThumb
                    sDesc = ""

                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
 
    oGui.setEndOfDirectory() 
	 
def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sStart = '<singlerelated class="hasdivider">'
    sEnd = '</singlerelated>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)               

    sPattern = '<a href="([^"]+)"><h2>.+?</i>(.+?)</h2>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if '/series/' in aEntry[0]:
                continue
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'film.png', '', '', oOutputParameterHandler)

    sPattern = 'data-url=["\']([^"\']+)["\'].+?<strong>(.+?)</strong>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry[0]
            sServer = aEntry[1].replace('سيرفر ماي سيما','/run/').replace('GoViD','govid.me')

            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().checkHoster(sServer)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
				
    sPattern = 'class="hoverable activable".+?href="([^"]+)"><quality>([^<]+)</quality><resolution><i class=".+?"></i>([^<]+)</resolution>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if '.rar' in aEntry[0]:
                continue
            sHosterUrl = aEntry[0]

            sTitle = sMovieTitle+' ['+aEntry[2]+aEntry[1]+'] '
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().getHoster('lien_direct')
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl , sThumb, oInputParameterHandler=oInputParameterHandler)
                
    oGui.setEndOfDirectory()
