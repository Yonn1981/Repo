# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import requests
from resources.lib import recaptcha_v2
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'akwam'
SITE_NAME = 'Akwam'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_FAM = (URL_MAIN + '/movies?section=0&category=33&rating=0&year=0&language=0&formats=0&quality=0', 'showMovies')
MOVIE_AR = (URL_MAIN + '/movies?section=29', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + '/movies?section=0&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showMovies')
MOVIE_EN = (URL_MAIN + '/movies?section=30', 'showMovies')
MOVIE_HI = (URL_MAIN + '/movies?section=31', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/movies?section=33', 'showMovies')
KID_MOVIES = (URL_MAIN + '/movies?category=30', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/movies?section=32', 'showMovies')
MOVIE_TOP = (URL_MAIN + '/movies?section=30&category=0&rating=8&year=0&language=0&formats=0&quality=0', 'showMovies')
RAMADAN_SERIES = (URL_MAIN + '/series?section=0&category=87&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
SERIE_EN = (URL_MAIN + '/series?section=30', 'showSeries')
SERIE_AR = (URL_MAIN + '/series?section=29', 'showSeries')
SERIE_HEND = (URL_MAIN + '/series?section=31', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/series?section=33', 'showSeries')
SERIE_TR = (URL_MAIN + '/series?section=32', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/series?section=30&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')

SERIE_TR_AR = (URL_MAIN + '/series?section=32&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
SERIE_HEND_AR = (URL_MAIN + '/series?section=31&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/series?category=30', 'showSeries')

DOC_NEWS = (URL_MAIN + '/movies?category=28', 'showMovies')
DOC_SERIES = (URL_MAIN + '/shows?section=46&category=0&rating=0&year=0&formats=0&quality=0', 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + '/shows?section=42', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + '/shows?section=45', 'showMovies')
SPORT_WWE = (URL_MAIN + 'shows?section=43&category=0&rating=0&year=0&formats=0&quality=0', 'showMovies')

MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '/search?q=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search?q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search?q=', 'showSeriesSearch')
URL_SEARCH_MISC = (URL_MAIN + '/search?q=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', 'Search All', 'search.png', oOutputParameterHandler)
    
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

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
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdblg.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية مدبلجة', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    import datetime
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1925, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/movies?section=0&category=0&rating=0&language=0&formats=0&quality=0&year=' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?q='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui() 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?q='+sSearchText+'&section=movie&year=0&rating=0&formats=0&quality=0'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?q=+'+sSearchText+'&section=series&year=0&rating=0&formats=0&quality=0'
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
		
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&section=movie&year=0&rating=0&formats=0&quality=0'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<span class="label quality">([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[3])
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = aEntry[4]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&section=series&year=0&rating=0&formats=0&quality=0'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class="label quality">(.+?)</span>.+?<a href="(.+?)" class="box">.+?data-src="(.+?)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[3])
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sYear = aEntry[4]
            sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                if '/movie/' in siteUrl:
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
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

    sDesc = ""
    sPattern = '<h2><div class=.+?style=".*?">.*?<p>(.+?)<'	 
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sDesc =  aResult[1][0]

    sPattern = '<meta property="og:title" content="([^"]+)".+?<meta property="og:image" content="([^"]+)".+?<meta property="og:url" content="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            sTitle = aEntry[0].replace(" | اكوام","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S01").replace("الموسم الاول","S01").replace("الموسم الثاني","S02").replace("الموسم الثالث","S03").replace("الموسم الثالث","S03").replace("الموسم الرابع","S04").replace("الموسم الخامس","S05").replace("الموسم السادس","S06").replace("الموسم السابع","S07").replace("الموسم الثامن","S08").replace("الموسم التاسع","S09")
            siteUrl = aEntry[2]
            sThumb = aEntry[1]

            if'موسم' not in aEntry[0]:
                sTitle =sTitle+' S01'

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('SeasonTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)  

    sPattern = '<a href="([^<]+)" class="text-white- ml-2 btn btn-light mb-2">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S01").replace("الموسم الاول","S01").replace("الموسم الثاني","S02").replace("الموسم الثالث","S03").replace("الموسم الثالث","S03").replace("الموسم الرابع","S04").replace("الموسم الخامس","S05").replace("الموسم السادس","S06").replace("الموسم السابع","S07").replace("الموسم الثامن","S08").replace("الموسم التاسع","S09")
            if'موسم' not in aEntry[1]:
                sTitle =sTitle+' S01'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('SeasonTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)        
       
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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class="label quality">([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[3])
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sYear = aEntry[4]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sStart = 'id="series-episodes">'
    sEnd = '<div class="widget-4 widget widget-style-1 more mb-4">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
  
    sPattern = 'class="text-white">([^<]+)</a>.+?href="([^"]+)".+?img src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sEp = aEntry[0].split(':')[0]
            sEp = sEp.replace("الحلقة ","").replace("حلقة ","")
            sTitle =  '{}E{:02d}'.format(sMovieTitle, int(sEp))
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    sPattern = '<a href="http([^<]+)/watch/(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]: 
            sTitle = sMovieTitle
            siteUrl = sUrl
            sThumb = sThumb
            sDesc = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser() 
    sPattern = 'href="([^<]+)" rel="next"'	 
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()

    if not oInputParameterHandler:
        oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  'href="(http[^<]+/watch/.+?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        murl =  aResult[1][0]
        oRequest = cRequestHandler(murl)
        sHtmlContent = oRequest.request()

    sPattern =  'href="(http[^<]+/watch/.+?)"'  
    aResult = oParser.parse(sHtmlContent,sPattern)  
    if aResult[0]:
        murl =  aResult[1][0]

        oRequest = cRequestHandler(murl)
        sHtmlContent = oRequest.request()

        sPattern =  "site_url = '([^']+)" 
        aResult = oParser.parse(sHtmlContent,sPattern)    
        if aResult[0]:
            URL_MAIN =  aResult[1][0]

        sPattern =  'data\-sitekey="(.+?)"' 
        aResult = oParser.parse(sHtmlContent,sPattern)    
        if aResult[0]:
            sitek =  aResult[1][0]

            s = requests.Session() 
            token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitek, lang='en', Referer=URL_MAIN)
            data = {'g-recaptcha-response':token}
            url = URL_MAIN+'verify'
            headers = {'User-Agent': UA,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': murl,
                    'Content-Type': 'application/x-www-form-urlencoded'}
            r = s.post(url,data=data,headers=headers)
            rt = s.get(murl)
            sHtmlContent = rt.text
            s.close()

    sPattern =  '>Click here</span>.+?<a href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)    
    if aResult[0]:
        murl =  aResult[1][0]

        oRequest = cRequestHandler(murl)
        oRequest.disableSSL()
        sHtmlContent = oRequest.request()
      
    sPattern =  '<source\s*src="([^"]+)"\s*type="video/mp4"\s*size="([^"]+)'                                                                      
    aResult = oParser.parse(sHtmlContent,sPattern)       
    if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry1 in aResult[1]:
                sHosterUrl = aEntry1[0] 
                sHost = aEntry1[1]  

                sTitle = ('%s  [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, sHost)  

                oOutputParameterHandler.addParameter('sTitle', sTitle)
                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sHost', sHost)

                oGui.addLink(SITE_IDENTIFIER, 'showLinks', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

            oGui.setEndOfDirectory()


def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    oHosterGui = cHosterGui()
    if not oInputParameterHandler:
        oInputParameterHandler = cInputParameterHandler()
        
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sTitle = oInputParameterHandler.getValue('sTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    sHosterUrl = sHosterUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
           
    if oHoster:
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sMovieTitle)
        oHosterGui.showHoster(oGui, oHoster, sHosterUrl + "|verifypeer=false", sThumb, oInputParameterHandler=oInputParameterHandler)
                
    oGui.setEndOfDirectory()
