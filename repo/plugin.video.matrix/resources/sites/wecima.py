# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, VSlog, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_ua()
 
SITE_IDENTIFIER = 'wecima'
SITE_NAME = 'Wecima'
SITE_DESC = 'arabic vod'
 
MAIN_URL = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_MAIN = random_ua.get_wecimaUrl(MAIN_URL)
if addon().getSetting('Use_alternative') == "true":
    URL_MAIN = siteManager().getUrlMain2(SITE_IDENTIFIER)

MOVIE_TOP = (f'{URL_MAIN}movies/best/', 'showMovies')
MOVIE_POP = (f'{URL_MAIN}movies/top/', 'showMovies')
MOVIE_CLASSIC = (f'{URL_MAIN}movies/old/', 'showMovies')
MOVIE_FAM = (f'{URL_MAIN}mpaa/pg/', 'showMovies')
MOVIE_EN = (f'{URL_MAIN}category/أفلام/10-movies-english-افلام-اجنبي/list/recent/', 'showMovies')
MOVIE_PACK = (f'{URL_MAIN}category/افلام/10-movies-english-افلام-اجنبي/سلاسل-الافلام-الكاملة-full-pack/', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category/أفلام/افلام-عربي-arabic-movies/', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/أفلام/افلام-تركى-turkish-films/list/recent/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/أفلام/افلام-هندي-indian-movies/list/recent/', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category/افلام-كرتون/', 'showMovies')

RAMADAN_SERIES = (f'{URL_MAIN}category/مسلسلات/مسلسلات-رمضان-2024/', 'showSeries')

SERIE_AR = (f'{URL_MAIN}category/مسلسلات/13-مسلسلات-عربيه-arabic-series/list/', 'showSeries')
SERIE_EN = (f'{URL_MAIN}category/مسلسلات/5-series-english-مسلسلات-اجنبي/list/', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}category/مسلسلات/9-series-indian-مسلسلات-هندية/list/', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}category/مسلسلات-كرتون/list/', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}category/مسلسلات/مسلسلات-اسيوية/list/', 'showSeries')
SERIE_TR = (f'{URL_MAIN}category/مسلسلات/8-مسلسلات-تركية-turkish-series/list/', 'showSeries')

DOC_SERIES = (f'{URL_MAIN}category/مسلسلات/مسلسلات-وثائقية-documentary-series/list/', 'showSeries')
DOC_NEWS = (f'{URL_MAIN}category/أفلام/افلام-وثائقية-documentary-films/list/recent/', 'showMovies')
SPORT_WWE = (f'{URL_MAIN}category/مصارعة-حرة/', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}search/', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search/', 'showSeries')
URL_SEARCH_ANIMS = (f'{URL_MAIN}search/', 'showAnimes')
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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'سلاسل افلام كاملة', 'pack.png', oOutputParameterHandler)

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
  
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}production/netflix/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netfilx', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}production/warner-bros/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Warner Bros', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}production/lionsgate/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Lionsgate', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}production/walt-disney-pictures/list/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Walt Disney', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showAnimesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showAnimes(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
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
            siteUrl = aEntry[0].replace((aEntry[0].split('watch/')[0]), URL_MAIN)
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
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
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="Grid--WecimaPosts">'
    sEnd = '<wecima'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

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
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0].replace((aEntry[0].split('watch/')[0]), URL_MAIN)
            sDesc = ''
            sThumb = aEntry[2].replace("(","").replace(")","")
            sThumb = sThumb.replace(sThumb.split('wp-content/')[0], URL_MAIN)
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
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
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="hoverable active">'
    sEnd = '</footer><'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="Thumb--GridItem"><a href="([^<]+)" title="(.+?)">.+?image:url(.+?);">'
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
 
            if "فيلم"  in aEntry[1]:
                continue
 
            siteUrl = aEntry[0]
            if 'gocimago.shop' in siteUrl:
                siteUrl = siteUrl.replace("https://gocimago.shop/", URL_MAIN)
            sTitle = cUtil().CleanMovieName(aEntry[1])
            sThumb = aEntry[2].replace("(","").replace(")","")
            sThumb = sThumb.replace(sThumb.split('wp-content/')[0], URL_MAIN)
            sDesc = ''
            sTitle = sTitle.split('موسم')[0].split('حلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
            siteUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)
 
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
            sTitle = cUtil().CleanMovieName(aEntry[1])
            sThumb = aEntry[2].replace("(","").replace(")","")
            sThumb = sThumb.replace(sThumb.split('wp-content/')[0], URL_MAIN)
            sDesc = ''
            sTitle = sTitle.split('موسم')[0].split('حلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
	
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
            siteUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addDir(SITE_IDENTIFIER, 'showAnimes', sTitle, 'next.png', oOutputParameterHandler)
 
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
    sSeason = oInputParameterHandler.getValue('sSeason')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sData = oInputParameterHandler.getValue('sData')
    total_episodes = oInputParameterHandler.getValue('total_episodes')

    if sSeason is False:
        sSeason = 'S1'

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href="([^<]+)">موسم(.+?)</a>'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult:
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            sSeason = sTitle.replace("S ","S")
            sTitle1 = f'{sMovieTitle} S{sSeason}'
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

        sPattern = 'href=([^<]+)"><div.+?<episodeTitle>([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
    
                siteUrl = aEntry[0].replace('"',"").replace('\\','')
                sTitle = aEntry[1].replace("\\","")
                sTitle = f'{sTitle.replace("u0627u0644u062du0644u0642u0629","").replace("الحلقة","").strip()}'
                sTitle = f'{sMovieTitle} S{sSeason} E{sTitle}'
                sThumb = sThumb
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        sPattern = '<div class="MoreEpisodes.+?" data-term="([^<]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                sData = aEntry

                match = re.search('episodeTitle>(.+?)</episodeTitle>', sHtmlContent)
                if match:
                    total_episodes = (match.group(1)).replace('الحلقة','').strip()

                base_link = f'{URL_MAIN}AjaxCenter/MoreEpisodes/{sData}/'
                links = generate_links(total_episodes, base_link)
                for aEntry in links:
                    match = re.search(r'/(\d+)/$', aEntry)
                    if match:
                        pages = int(match.group(1))
                    else:
                        pages = 'Next'
                    pTitle = f'[COLOR red]More Episodes: {pages}[/COLOR]'
                    siteUrl = aEntry
                    sThumb = sThumb

                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sSeason', sSeason)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sData', sData)
                    oOutputParameterHandler.addParameter('total_episodes', total_episodes)
                        
                    oGui.addDir(SITE_IDENTIFIER, 'showEps', pTitle, sThumb, oOutputParameterHandler)
 
    oGui.setEndOfDirectory() 
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sData = oInputParameterHandler.getValue('sData')
    total_episodes = oInputParameterHandler.getValue('total_episodes')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    sHtmlContent = oRequestHandler.request()
    
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

    sPattern = 'href=([^<]+)"><div.+?<episodeTitle>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            siteUrl = aEntry[0].replace('"',"").replace('\\','')
            sTitle = aEntry[1].replace("\\","")
            sTitle = f'{sTitle.replace("u0627u0644u062du0644u0642u0629","").replace("الحلقة","").strip()}'
            sTitle = f'{sMovieTitle} S{sSeason} E{sTitle}'
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
    
    sPattern = '<div class="MoreEpisodes.+?" data-term="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sData = aEntry

            match = re.search('episodeTitle>(.+?)</episodeTitle>', sHtmlContent)
            if match:
                total_episodes = (match.group(1)).replace('الحلقة','').strip()

            base_link = f'{URL_MAIN}AjaxCenter/MoreEpisodes/{sData}/'
            links = generate_links(total_episodes, base_link)
            for aEntry in links:
                match = re.search(r'/(\d+)/$', aEntry)
                if match:
                    pages = int(match.group(1))
                else:
                    pages = 'Next'
                pTitle = f'[COLOR red]More Episodes: {pages}[/COLOR]'
                siteUrl = aEntry
                sThumb = sThumb

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sSeason', sSeason)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sData', sData)
                oOutputParameterHandler.addParameter('total_episodes', total_episodes)
                    
                oGui.addDir(SITE_IDENTIFIER, 'showEps', pTitle, sThumb, oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def generate_links(total_episodes, base_link):
    initial_episodes = 60
    increment = 40
    links = []
    episodes = initial_episodes
    while int(episodes) <= int(total_episodes):
        link = f"{base_link}{episodes}/"
        links.append(link)
        episodes += increment

    if links and int(links[-1].split('/')[-2]) > int(total_episodes):
        links[-1] = f"{base_link}{total_episodes}/"

    return links

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
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
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
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
            if 'userload' in sHosterUrl or '.shop' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sServer)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
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

            if 'userload' in sHosterUrl or '.shop' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().getHoster('lien_direct')
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl , sThumb)
                
    oGui.setEndOfDirectory()
