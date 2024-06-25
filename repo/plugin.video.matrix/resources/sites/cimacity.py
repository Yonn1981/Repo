﻿# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

SITE_IDENTIFIER = 'cimacity'
SITE_NAME = 'CimaCity'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category.php?cat=english-movies', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category.php?cat=arabic-movies', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}category.php?cat=modablaja-movies', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category.php?cat=hindia-movies', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category.php?cat=asian-movies', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category.php?cat=turkey-movies', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category.php?cat=animation-movies', 'showMovies')

DOC_NEWS = (f'{URL_MAIN}category.php?cat=aflam-wthaaeqe', 'showMovies')

SERIE_TR = (f'{URL_MAIN}category.php?cat=moslslat-turkya', 'showSeries')
SERIE_DUBBED = (f'{URL_MAIN}category.php?cat=modablaja-series', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}category.php?cat=asia-series', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}category.php?cat=hindia-series', 'showSeries')
SERIE_EN = (f'{URL_MAIN}category.php?cat=moslslat-agnabya', 'showSeries')
SERIE_AR = (f'{URL_MAIN}category.php?cat=moslslat-arabia', 'showSeries')
RAMADAN_SERIES = (f'{URL_MAIN}category.php?cat=mslslat-rmdtan-2024', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}category.php?cat=animation-series', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}search.php?keywords=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search.php?keywords=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category.php?cat=moslslat-cima-city')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات سيما سيتي', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category.php?cat=cimacity-movies')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام سيما سيتي', 'film.png', oOutputParameterHandler)

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

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdbljt.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'crtoon.png', oOutputParameterHandler)  
     
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?keywords={sSearchText}'
        if 'series' in sUrl:
            showSeries(sUrl)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?keywords={sSearchText}'
        if 'series' in sUrl:
            showSeries(sUrl)
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

    sPattern = '<div class="thumbnail">.+?<a href="([^<]+)" title="(.+?)">.+?img src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'مسلسل' in aEntry[1] or 'موسم' in aEntry[1]:
               continue

            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<div class="thumbnail">.+?<a href="([^<]+)" title="(.+?)">.+?img src="(.+?)" alt='
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
            if 'فيلم' in aEntry[1] :
               continue
             
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            sTitle = re.sub(r"S\d{1,2}", "", sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''

            if sTitle not in itemList:
                itemList.append(sTitle)

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

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

    sPattern = 'onclick=["\']openCity.+?["\'].+?>(.+?)</button>'    
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            sID = aEntry.replace("الموسم ","")
            sTitle = f'{sMovieTitle} {aEntry.replace("الموسم ","S")}'
            siteUrl = sUrl
            sDesc = ''
            sThumb = sThumb
            sYear = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('SeasonID', sID)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        sPattern = '<meta name="title" content="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)    
        if (aResult[0]):
            sDesc = aResult[1][0]
        
        sPattern = '<a class="xtgo" href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sRefer = aResult[1][0]

        oRequestHandler = cRequestHandler(sRefer)
        sHtmlContent = oRequestHandler.request()
        
        sStart = 'class="list_servers'
        sEnd = '</div>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'iframe src=["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
       
                url = aEntry
                url = url.replace("moshahda","ffsff")
                sTitle = sDesc
                sThumb = sThumb
                if url.startswith('//'):
                    url = f'http:{url}'
								            
                sHosterUrl = url
                if 'nowvid' in sHosterUrl or 'userload' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}' 
                 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory() 
    
def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    SeasonID = oInputParameterHandler.getValue('SeasonID')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  'id="Season(.+?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        SID = aResult[1][0] 

    if len(SID) == 1:
        SeasonID = SID
            
    elif len(SID) > 1:
        SeasonID = str(int(SeasonID)-1)

    sStart = f'id="Season{SeasonID}"'
    sEnd = '</div>'
    sHtmlContent2 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href=["\']([^"\']+)["\'].+?<em>(.+?)</em>'
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            
            sTitle = f'{sMovieTitle} E{aEntry[1].replace("الحلقة ","")}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
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

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sRefer = sUrl

    sPattern =  '<a class="xtgo" href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sRefer = aResult[1][0] 

    oRequestHandler = cRequestHandler(sRefer)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request().replace("&#39;","'")

    sStart = '<ul class="list_servers'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'iframe src=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
      
            url = aEntry
            url = url.replace("moshahda","ffsff")
            sThumb = sThumb
            if url.startswith('//'):
                url = f'http:{url}'
								            
            sHosterUrl = url
            if 'nowvid' in sHosterUrl or 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
                 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)     
      
    oGui.setEndOfDirectory()  

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="active"><a href=.+?<a href="(.+?)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return f'{URL_MAIN}{aResult[1][0]}'

    return False