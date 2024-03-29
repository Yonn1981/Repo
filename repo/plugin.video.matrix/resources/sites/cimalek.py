﻿# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, VSlog, addon
from resources.lib.parser import cParser
from resources.lib.multihost import cMegamax
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'cimalek'
SITE_NAME = 'Cimalek'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_FAM = (URL_MAIN + 'category/aflam-online/aflam-family/', 'showMovies')
MOVIE_EN = (URL_MAIN + 'category/aflam-online/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/asian-aflam/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/hindi-movie/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/indian-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/cartoon-movies/', 'showMovies')
ANIM_MOVIES = (URL_MAIN + 'category/anime-movies/', 'showMovies')

SERIE_EN = (URL_MAIN + 'category/english-series/', 'showSeries')
SERIE_NETFLIX = (URL_MAIN + 'category/netflix-series/', 'showSeries')
ANIM_NEWS = (URL_MAIN + 'category/anime-series/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/asian-series/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
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
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات نتفليكس', 'netflix.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler)
	
    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return		
		
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
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
    
    sPattern = '<div class="title">(.+?)</div>.+?<a href="(.+?)">.+?data-src="(.+?)" alt'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  not in aEntry[0]:
                continue
            
            sTitle = aEntry[0].replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","") 
            siteUrl = aEntry[1]+"/watch/"
            sDesc = ''
            sThumb = aEntry[2]
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

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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

    sPattern = 'data-id=".+?">.+?<a href="(.+?)">.+?data-src="(.+?)" alt="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  in aEntry[2]:
                continue
 
            siteUrl = aEntry[0]            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[1]
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

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
    if not sSearch:
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
        oGui.setEndOfDirectory()
  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "class='arrow_pag' href=(.+?)><i id='nextpagination"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:  
        return aResult[1][0].replace('"',"")

    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "href='([^<]+)' title='(.+?)'><span class='serie'>"
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").replace("الحلقة ","E").replace("الحلقة ","E").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('sDesc', sDesc)           
             
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
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

    sPattern =  '"ver":"([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        ver = aResult[1][0] 

    sPattern =  'data-postid=["\']([^"\']+)["\']' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        dPost = aResult[1][0] 

    sPattern = 'data-nume=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            
            sHost = f'Server {aEntry}'
            siteUrl = f'{URL_MAIN}wp-json/lalaplayer/v2/?p={dPost}&t=movie&n={aEntry}&ver={ver}'
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

    sPattern = 'class="cat-heading">روابط التحميل</h2>.+?href="([^<]+)" target='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry

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

                        oGui.addLink(SITE_IDENTIFIER, 'showLinks2', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
				              
    oGui.setEndOfDirectory()

def showLinks2():
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

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(siteUrl)
    sData = oRequestHandler.request()

    sPattern = '"embed_url":\s*"([^"]+)'
    aResult = oParser.parse(sData, sPattern)
    if aResult:
        for aEntry in aResult[1]:
            url = aEntry.replace("\\","")
            if url.startswith('//'):
                url = 'http:' + url

            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            sData = oRequestHandler.request()              

            sPattern = '"file":"(.+?)","label":'
            aResult = oParser.parse(sData, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:        
                    url = aEntry.replace("\\","")
                    if url.startswith('//'):
                        url = 'http:' + url

                    sHosterUrl = url 
                    if 'streamtape' in sHosterUrl:
                        sHosterUrl = sHosterUrl
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl                         
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl+"|verifypeer=false", sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()