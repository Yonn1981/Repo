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
from resources.lib.util import Quote
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'shoffree'
SITE_NAME = 'Shoffree'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'movies?lang=الإنجليزية', 'showMovies')
MOVIE_AR = (URL_MAIN + 'movies?lang=العربية', 'showMovies')
MOVIE_HI = (URL_MAIN + 'movies?lang=الهندية', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'movies?lang=الكورية', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'movies?lang=التركية', 'showMovies')
KID_MOVIES = (URL_MAIN + 'movies?genre=14', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
MOVIE_ANNEES = (URL_MAIN + 'movies', 'showYears')

RAMADAN_SERIES = (URL_MAIN + 'ramadan', 'showSeries')
SERIE_EN = (URL_MAIN + 'series?lang=الإنجليزية', 'showSeries')
SERIE_AR = (URL_MAIN + 'series?lang=العربية', 'showSeries')
SERIE_TR = (URL_MAIN + 'series?lang=التركية', 'showSeries')
SERIE_HEND = (URL_MAIN + 'series?lang=الهندية', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'series?lang=الكورية', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')
SERIE_ANNEES = (URL_MAIN + 'series', 'showSerieYears')

ANIM_NEWS = (URL_MAIN + 'series?genre=40', 'showSeries')
ANIM_MOVIES = (URL_MAIN + 'movies?genre=40', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search?query=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?query=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', 'rmdn.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler) 
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'resent')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'الأفلام المضاف حديثاً', 'film.png', oOutputParameterHandler)	

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

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام انمي', 'anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies')
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'أفلام (بالسنوات)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series')
    oGui.addDir(SITE_IDENTIFIER, 'showSerieYears', 'مسلسلات (بالسنوات)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies')
    oGui.addDir(SITE_IDENTIFIER, 'showLang', 'أفلام (حسب اللغة)', 'film.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series')
    oGui.addDir(SITE_IDENTIFIER, 'showSerieLang', 'مسلسلات (حسب اللغة)', 'mslsl.png', oOutputParameterHandler)	

    oGui.setEndOfDirectory()

def main_function(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="naked" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        sMain = aResult[1][0]+'/'
    return sMain
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/search?query='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/search?query='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> السنة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies?year=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> السنة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series?year=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> اللغة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies?lang=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> اللغة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series?lang=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'series?genre=8'])
    liste.append(['انيميشن', URL_MAIN + 'series?genre=14'])
    liste.append(['مغامرات', URL_MAIN + 'series?genre=12'])
    liste.append(['غموض', URL_MAIN + 'series?genre=7'])
    liste.append(['تاريخي', URL_MAIN + 'series?genre=28'])
    liste.append(['كوميديا', URL_MAIN + 'series?genre=16'])
    liste.append(['موسيقى', URL_MAIN + 'series?genre=20'])
    liste.append(['رياضي', URL_MAIN + 'series?genre=25'])
    liste.append(['دراما', URL_MAIN + 'series?genre=6'])
    liste.append(['رعب', URL_MAIN + 'series?genre=9'])
    liste.append(['عائلى', URL_MAIN + 'series?genre=15'])
    liste.append(['فانتازيا', URL_MAIN + 'series?genre=38'])
    liste.append(['حروب', URL_MAIN + 'series?genre=36'])
    liste.append(['الجريمة', URL_MAIN + 'series?genre=17'])
    liste.append(['رومانسى', URL_MAIN + 'series?genre=5'])
    liste.append(['خيال علمى', URL_MAIN + 'series?genre=13'])
    liste.append(['اثارة', URL_MAIN + 'series?genre=11'])
    liste.append(['وثائقى', URL_MAIN + 'series?genre=19'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'movies?genre=8'])
    liste.append(['انيميشن', URL_MAIN + 'movies?genre=14'])
    liste.append(['مغامرات', URL_MAIN + 'movies?genre=12'])
    liste.append(['غموض', URL_MAIN + 'movies?genre=7'])
    liste.append(['تاريخي', URL_MAIN + 'movies?genre=28'])
    liste.append(['كوميديا', URL_MAIN + 'movies?genre=16'])
    liste.append(['موسيقى', URL_MAIN + 'movies?genre=20'])
    liste.append(['رياضي', URL_MAIN + 'movies?genre=25'])
    liste.append(['دراما', URL_MAIN + 'movies?genre=6'])
    liste.append(['رعب', URL_MAIN + 'movies?genre=9'])
    liste.append(['عائلى', URL_MAIN + 'movies?genre=15'])
    liste.append(['فانتازيا', URL_MAIN + 'movies?genre=38'])
    liste.append(['حروب', URL_MAIN + 'movies?genre=36'])
    liste.append(['الجريمة', URL_MAIN + 'movies?genre=17'])
    liste.append(['رومانسى', URL_MAIN + 'movies?genre=5'])
    liste.append(['خيال علمى', URL_MAIN + 'movies?genre=13'])
    liste.append(['اثارة', URL_MAIN + 'movies?genre=11'])
    liste.append(['وثائقى', URL_MAIN + 'movies?genre=19'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

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

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'serie/' in aEntry[0] or 'episode/' in aEntry[0]:
                continue 

            sTitle = aEntry[1].replace("مشاهدة","").replace("برنامج","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","").replace("مدبلج","").replace("عرض","").replace("الرو","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
            sDesc = ''
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
 
        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
        if sNextPage != False:
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
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    itemList = []		
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'movie/' in aEntry[0]:
                continue 
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مدبلج للعربية","مدبلج")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثانى","S2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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

    sStart = '>المواسم</div>'
    sEnd = '<section class="text-center"'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent1, sPattern) 
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("-"," ").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("كامل","").replace("برنامج","").replace("فيلم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        sPattern = '<a class="sku" href="(.+?)" title=.+?data-src="(.+?)" alt.+?class="episode" style="display: inline;">.+?<i>(.+?)</i></span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:

                sEp =  "E"+aEntry[2].replace(" ","")
                sTitle = sMovieTitle+sEp
                siteUrl = aEntry[0]
                sThumb = aEntry[1].replace('/w342','/w500')
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
 
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory() 
 
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="sku" href="(.+?)" title=.+?data-src="(.+?)" alt.+?class="episode" style="display: inline;">.+?<i>(.+?)</i></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sEp =  "E"+aEntry[2].replace(" ","")
            sTitle = sMovieTitle+sEp
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace('/w342','/w500')
            sDesc = ''
            sHost = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def __checkForNextPage(sHtmlContent, sUrl):
    oParser = cParser()
    sPattern = '<a class="page-link" href="([^"]+)">التالي</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return sUrl+'&'+aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'movie' in sUrl:
        sUrl = sUrl.rsplit("/",1)[0] + '/single-movie?watch=1'
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sMain = main_function(sHtmlContent)
    if sMain:
        URL_MAIN = sMain

    sPattern =  '<form action="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        maction = aResult[1][0] 

    sPattern =  'name="url" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            murl = aEntry

            oRequestHandler = cRequestHandler(maction)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('Host', "shoffree.net")
            oRequestHandler.addParameters('url', murl)
            oRequestHandler.setRequestType(1)
            sHtmlContent = oRequestHandler.request()

            sPattern =  "window.open\('(.*?)'" 
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0]:
                url = aResult[1][0] 
                if 'shoffree' in url:
                    oRequestHandler = cRequestHandler(url)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', maction)
                    oRequestHandler.addHeaderEntry('Host', "shoffree.net")
                    sHtmlContent = oRequestHandler.request()  
                    
                    sPattern =  '<iframe.+?src="([^"]+)"></iframe>'
                    aResult = oParser.parse(sHtmlContent,sPattern)
                    if aResult[0]:
                        url = aResult[1][0].split('&role')[0]
                        url = aResult[1][0].split('?key=')[0] + '?key=' + Quote(url.split('?key=')[1])

                sHosterUrl = url
                if 'userload' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                if 'shoffree' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                if 'mystream' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()
