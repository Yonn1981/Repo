# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.multihost import cVidNet, cVidPro, cVidVip
from urllib.parse import urlparse


UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
SITE_IDENTIFIER = 'vidplay'
SITE_NAME = 'VidPlay'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}/movies/year', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}/genres/watch-animation-movies-online-free-release/1', 'showMovies')
MOVIE_TOP = (f'{URL_MAIN}/movies/star-rating/', 'showMovies')
MOVIE_POP = (f'{URL_MAIN}/movies/popular/', 'showMovies')
MOVIE_GENRES = (f'{URL_MAIN}/movies', 'moviesGenres')
SERIE_EN = (f'{URL_MAIN}/tv-shows', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}/tv-tags/animation', 'showSeries')
SERIE_GENRES = (f'{URL_MAIN}/tv-shows', 'seriesGenres')

DOC_NEWS = (f'{URL_MAIN}/genres/watch-documentary-movies-online-free-release/1', 'showMovies')
DOC_SERIES = (f'{URL_MAIN}/tv-tags/documentary', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}/index.php?menu=search&query=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}/index.php?menu=search&query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POP[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'الأفلام الرائجة', 'film.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انيميشن', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/tv-shows/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'المسلسلات الرائجة', 'mslsl.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}/index.php?menu=search&query={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}/index.php?menu=search&query={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<option value="([^<]+)">([^<]+)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = aEntry[1]
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showSeries', sTitle, 'film.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<option value="([^<]+)">([^<]+)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = aEntry[1]
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'film.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      sPattern = '<figure class="figured">\s*<a href="([^"]+)".+?src="([^"]+)".+?<div class="title">(.+?)</div>.+?<div class="year".+?>(.+?)</div>'
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = '<figure class="figured">\s*<a href="([^"]+)".+?data-src="([^"]+)".+?<div class="title">(.+?)</div>.+?<div class="year".+?>(.+?)</div>'

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "watchseries/"  in aEntry[0]:
                continue

            sTitle = f'{aEntry[2]} ({aEntry[3]})'
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = aEntry[1]
            sDesc = ''
            sYear = aEntry[3]

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
      sPattern = '<figure class="figured">\s*<a href="([^"]+)".+?src="([^"]+)".+?<div class="title">(.+?)</div>.+?<div class="year".+?>(.+?)</div>'
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = '<figure class="figured">\s*<a href="([^"]+)".+?data-src="([^"]+)".+?<div class="title">(.+?)</div>.+?<div class="year".+?>(.+?)</div>'

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "movie/"  in aEntry[0]:
                continue

            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = aEntry[1]
            sDesc = ''
            sYear = aEntry[3]

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

    sPattern = '<div class="seasonHeader".+?>Season(.+?)</b>.+?<div class="episodeList"(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sId = aEntry[0]
            sHtml = aEntry[1]

            sTitle = f"{sMovieTitle} S{sId}"
            sThumb = sThumb
            sDesc = ''
    
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sHtml', sHtml)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
        
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sHtmlContent = oInputParameterHandler.getValue('sHtml')

    oParser = cParser()
    sPattern = 'href="([^"]+)">(.+?)<span' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()   
        for aEntry in aResult[1]:
            
            sEp = aEntry[1].replace('Episode ','').strip()
            siteUrl = f'{URL_MAIN}/{aEntry[0]}'
            sTitle = f"{sMovieTitle} E{sEp}"
            sThumb = sThumb
            sDesc = ""
    
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
   
    oGui.setEndOfDirectory() 
 
def showLinks(oInputParameterHandler = False):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()  
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    url_pattern = r"\$.get\('(.+?)',"
    embed_pattern = r'"embed":\s*"(.+?)"'

    url_matches = re.findall(url_pattern, sHtmlContent)
    embed_matches = re.findall(embed_pattern, sHtmlContent)

    url_embed_pairs = zip(url_matches, embed_matches)
    sLinks = list(url_embed_pairs)
    
    for aEntry in sLinks:
        nUrl = f'{URL_MAIN}{aEntry[0]}?embed={aEntry[1]}'

        oRequestHandler = cRequestHandler(nUrl)
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<iframe src="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            iFrame = aResult[1][0]
            sHost = urlparse(iFrame).netloc

            sTitle = f'{sMovieTitle} ({sHost})'  
            oOutputParameterHandler.addParameter('sHosterUrl', iFrame)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesLinks(oInputParameterHandler = False):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()  
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    url_pattern = r"\$.get\('(.+?)',"
    embed_pattern = r'"embed":\s*"(.+?)"'
    season_pattern = r'"season":\s*"(.+?)"'
    episode_pattern = r'"episode":\s*"(.+?)"'

    url_matches = re.findall(url_pattern, sHtmlContent)
    embed_matches = re.findall(embed_pattern, sHtmlContent)
    season_matches = re.findall(season_pattern, sHtmlContent)
    episode_matches = re.findall(episode_pattern, sHtmlContent)

    url_embed_pairs = zip(url_matches, embed_matches, season_matches, episode_matches)
    sLinks = list(url_embed_pairs)
    
    for aEntry in sLinks:
        import requests
        nUrl = f'{URL_MAIN}{aEntry[0]}?embed={aEntry[1]}&season={season_matches}&episode={episode_matches}'

        oRequestHandler = cRequestHandler(nUrl)
        oRequestHandler = cRequestHandler(nUrl)
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = '<iframe src="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            iFrame = aResult[1][0]
            if '[' in iFrame:
                parts = iFrame.replace('[', '').replace(']', '').split('/')
                base_url = '/'.join(parts[:-2])
                season = parts[-2][1]
                episode = parts[-1][1]
                iFrame = f"{base_url}/{season}/{episode}"
                if '.vip' in iFrame:
                    iFrame = f'{iFrame}&server=1&switch=off&autoplay=true'

            sHost = urlparse(iFrame).netloc

            sTitle = f'{sMovieTitle} ({sHost})'  
            oOutputParameterHandler.addParameter('sHosterUrl', iFrame)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('sHosterUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if '.net' in sUrl:
        data = cVidNet().extract(sUrl)

        sHosterUrl = data['source']
        subtitles = data['subtitles']
        referer = data['referer']

        sHosterUrl = f'{sHosterUrl}|Referer={referer}?sub.info={subtitles}'
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:  
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    if '.xyz' in sUrl or '.vip' in sUrl:
        sLink = cVidVip().extract(sUrl)
        for item in sLink:
            sHosterUrl = item.split(',')[0].split('url=')[1]
            sQual = item.split(',')[1].split('qual=')[1]

            sDisplayTitle = f'{sMovieTitle} ({sQual})' 
            oHoster = cHosterGui().getHoster('lien_direct')
            if oHoster:  
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    if '.pro' in sUrl:
        sHosterUrl = cVidPro().extract(sUrl)

        sDisplayTitle = sMovieTitle
        oHoster = cHosterGui().getHoster('vidsrcstream')
        if oHoster:
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a href="([^"]+)">Next'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False
