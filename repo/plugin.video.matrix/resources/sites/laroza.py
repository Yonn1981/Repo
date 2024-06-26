﻿# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re	
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

SITE_IDENTIFIER = 'laroza'
SITE_NAME = 'Laroza'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_AR = (f'{URL_MAIN}category.php?cat=arabic-movies18', 'showMovies')
MOVIE_EN = (f'{URL_MAIN}category.php?cat=all_movies', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category.php?cat=indian-movies3', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category.php?cat=asian-movies', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}category.php?cat=aflammdblgh', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category.php?cat=anime-movies', 'showMovies')

RAMADAN_SERIES = (f'{URL_MAIN}category.php?cat=17-ramadan-2024', 'showSeries')
SERIE_EN = (f'{URL_MAIN}category.php?cat=english-series3', 'showSeries')
SERIE_AR = (f'{URL_MAIN}category.php?cat=arabic-series31', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}category.php?cat=4indian-series', 'showSeries')
SERIE_TR = (f'{URL_MAIN}category.php?cat=turkish-3isk-seriess30', 'showSeries')

REPLAYTV_PLAY = (f'{URL_MAIN}category.php?cat=masrh1', 'showMovies')
REPLAYTV_NEWS = (f'{URL_MAIN}category.php?cat=tv-programs5', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}search.php?keywords=', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search.php?keywords=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search.php?keywords=', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', 'rmdn.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
      
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام مدبلجة', 'mdblg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category.php?cat=ramadan-2023')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان 2023', 'rmdn.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?keywords={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?keywords=فيلم+{sSearchText}'
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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="thumbnail">.+?<i class="fa fa-clock-o">.+?<a href="(.+?)".+?title="(.+?)".+?<img src=.+?data-echo="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "مسلسل"  in aEntry[1]:
                continue
            if "حلقة"  in aEntry[1]:
                continue
             
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0].replace("watch.php","play.php").replace("video.php","play.php")
            sDesc = ""
            sThumb = aEntry[2]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

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

        progress_.VSclose(progress_)
 
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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
  
    sPattern = '<div class="thumbnail">.+?<i class="fa fa-clock-o">.+?<a href="(.+?)"\s*title="(.+?)".+?<img src=.+?data-echo="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    itemList = []		
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            siteUrl = aEntry[0]
            if 'حلقة' not in aEntry[1]: 
                siteUrl = aEntry[0].replace("watch.php","play.php").replace("video.php","play.php")      
            sTitle = cUtil().CleanMovieName(aEntry[1])
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.split('الموسم')[0].split('موسم')[0].split('الحلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
			
            if sTitle not in itemList:
                itemList.append(sTitle)				
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                if 'حلقة' not in aEntry[1]:
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)        

    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="active">\s*<a href="#".+?<li class.+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :     
        return f'{URL_MAIN}{aResult[1][0]}'

    return False
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="SeasonsEpisodes" style="display:none;" data-serie="(.+?)">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sSeason = f'S{aEntry[0]}'
            sHtmlContent = aEntry[1]

            sPattern = 'href="(.+?)" title.+?<em>(.+?)</em><span>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
 
                    siteUrl = URL_MAIN +aEntry[0]
                    siteUrl = siteUrl.replace("video.php","play.php").replace("video.php","play.php")
                    sTitle = f'{sMovieTitle} {sSeason}'
                    sTitle = f'{sTitle} E{aEntry[1]}'
                    sThumb = sThumb
                    sDesc = ""
			
                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
              
    oGui.setEndOfDirectory() 
	 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
               
    sPattern = 'data-embed-url=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry
            if sHosterUrl.startswith('//'):
                sHosterUrl = f'http:{sHosterUrl}'
 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        sPattern = '<iframe src=["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0] :
            for aEntry in aResult[1]:
            
                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = f'http:{sHosterUrl}'

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
                                   
    oGui.setEndOfDirectory()