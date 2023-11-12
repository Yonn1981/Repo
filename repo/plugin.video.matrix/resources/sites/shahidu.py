# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'shahidu'
SITE_NAME = 'Shahid4U'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'category/افلام-اجنبي', 'showMovies')
MOVIE_AR = (URL_MAIN + 'category/افلام-عربي', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/افلام-هندي', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/افلام-اسيوية', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/افلام-تركية', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')

RAMADAN_SERIES = (URL_MAIN + 'category/مسلسلات-رمضان-2023', 'showSeries')
SERIE_EN = (URL_MAIN + 'category/مسلسلات-اجنبي', 'showSeries')
SERIE_AR = (URL_MAIN + 'category/مسلسلات-عربي', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category/مسلسلات-هندية', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/مسلسلات-اسيوية', 'showSeries')
SERIE_TR = (URL_MAIN + 'category/مسلسلات-تركية', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

ANIM_MOVIES = (URL_MAIN + 'category/افلام-انمي', 'showMovies')
ANIM_NEWS = (URL_MAIN+'category/مسلسلات-انمي' , 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + 'category/برامج-تلفزيونية', 'showSeries')

DOC_NEWS = (URL_MAIN + 'genre/وثائقي', 'showMovies')
DOC_SERIES = (URL_MAIN + 'genre/وثائقي', 'showSeries')

SPORT_WWE = (URL_MAIN + 'category/عروض-مصارعة', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?s=فيلم+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?s=مسلسل+', 'showSeries')
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
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler) 
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler) 
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)
     
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', 'anime.png', oOutputParameterHandler)
     
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
   
def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'genre/اكشن'])
    liste.append(['انيميشن', URL_MAIN + 'genre/كرتون'])
    liste.append(['مغامرات', URL_MAIN + 'genre/مغامرات'])
    liste.append(['حركة', URL_MAIN + 'genre/حركة'])
    liste.append(['تاريخي', URL_MAIN + 'genre/تاريخي'])
    liste.append(['كوميديا', URL_MAIN + 'genre/كوميدي'])
    liste.append(['موسيقى', URL_MAIN + 'genre/موسيقي'])
    liste.append(['رياضي', URL_MAIN + 'genre/رياضي'])
    liste.append(['دراما', URL_MAIN + 'genre/دراما'])
    liste.append(['رعب', URL_MAIN + 'genre/رعب'])
    liste.append(['عائلى', URL_MAIN + 'genre/عائلي'])
    liste.append(['فانتازيا', URL_MAIN + 'genre/فانتازيا'])
    liste.append(['حروب', URL_MAIN + 'genre/حروب'])
    liste.append(['الجريمة', URL_MAIN + 'genre/جريمة'])
    liste.append(['رومانسى', URL_MAIN + 'genre/رومانسي'])
    liste.append(['خيال علمى', URL_MAIN + 'genre/خيال%20علمي'])
    liste.append(['اثارة', URL_MAIN + 'genre/ﺗﺸﻮﻳﻖ%20ﻭﺇﺛﺎﺭﺓ'])
    liste.append(['وثائقى', URL_MAIN + 'genre/وثائقي'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'genre/اكشن'])
    liste.append(['انيميشن', URL_MAIN + 'genre/كرتون'])
    liste.append(['مغامرات', URL_MAIN + 'genre/مغامرات'])
    liste.append(['حركة', URL_MAIN + 'genre/حركة'])
    liste.append(['تاريخي', URL_MAIN + 'genre/تاريخي'])
    liste.append(['كوميديا', URL_MAIN + 'genre/كوميدي'])
    liste.append(['موسيقى', URL_MAIN + 'genre/موسيقي'])
    liste.append(['رياضي', URL_MAIN + 'genre/رياضي'])
    liste.append(['دراما', URL_MAIN + 'genre/دراما'])
    liste.append(['رعب', URL_MAIN + 'genre/رعب'])
    liste.append(['عائلى', URL_MAIN + 'genre/عائلي'])
    liste.append(['فانتازيا', URL_MAIN + 'genre/فانتازيا'])
    liste.append(['حروب', URL_MAIN + 'genre/حروب'])
    liste.append(['الجريمة', URL_MAIN + 'genre/جريمة'])
    liste.append(['رومانسى', URL_MAIN + 'genre/رومانسي'])
    liste.append(['خيال علمى', URL_MAIN + 'genre/خيال%20علمي'])
    liste.append(['اثارة', URL_MAIN + 'genre/ﺗﺸﻮﻳﻖ%20ﻭﺇﺛﺎﺭﺓ'])
    liste.append(['وثائقى', URL_MAIN + 'genre/وثائقي'])

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
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="container">'
    sEnd = '<div class="footer">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?style="background-image: url\((.+?)\);.+?class="title">(.+?)</h4>'
    sPattern += '.+?<h5 class="description">(.+?)</h5>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "episode" in aEntry[0] or "season" in aEntry[0]or "series" in aEntry[0]:
                continue
            if "مسلسل" in aEntry[2]:
                continue

            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("يلم","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("HD","").replace("كامل","")
            if 'http' not in aEntry[1]:
                sThumb = URL_MAIN+aEntry[1]
            else:
                sThumb = aEntry[1]
            if 'http' not in aEntry[0]:
                siteUrl = URL_MAIN+aEntry[0].replace('film/','download/').replace('post/','download/')
            else:
                siteUrl = aEntry[0].replace('film/','download/').replace('post/','download/')
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                if 'عرض' in sTitle:
                    sTitle = sTitle.replace('عرض','')
                else:
                    sTitle = sTitle.replace(sYear,'')
            sDesc = ''
            if aEntry[3]:
                sDesc = str(aEntry[3])

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
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

    sStart = '<div class="container">'
    sEnd = '<div class="footer">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?style="background-image: url\((.+?)\);.+?class="title">(.+?)</h4>'
    sPattern += '.+?<h5 class="description">(.+?)</h5>'    
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
 
            if "film/" in aEntry[0]:
                continue
            if "post/" in aEntry[0]:
                continue
            if "فيلم" in aEntry[2]:
                continue
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("كامل","")
            if 'http' not in aEntry[1]:
                sThumb = URL_MAIN+aEntry[1]
            else:
                sThumb = aEntry[1]
            if 'http' not in aEntry[0]:
                siteUrl = URL_MAIN+aEntry[0].replace('film/','download/')
            else:
                siteUrl = aEntry[0].replace('film/','download/')
            sDesc = ''
            if aEntry[3]:
                sDesc = str(aEntry[3])
            sYear = ''
            sTitle = sTitle.split('الحلقة')[0].split('الموسم')[0]

            if sTitle not in itemList:
                itemList.append(sTitle)			
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
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

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'جميع المواسم'
    sEnd = '<hr class'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="(.+?)".+?>الموسم</span>.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle =  " S" + aEntry[1]
            sTitle =  sMovieTitle+sTitle
            if 'http' not in aEntry[0]:
                siteUrl = URL_MAIN+aEntry[0]
            else:
                siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)

    else:
        sStart = '</i>\s*جميع الحلقات\s*</div>'
        sEnd = '<i class'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'href="([^"]+)" class="epss.+?</span>.+?>(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
 
                sTitle = " E"+aEntry[1]
                sTitle = sMovieTitle+sTitle
                if 'http' not in aEntry[0]:
                    siteUrl = URL_MAIN+aEntry[0].replace('episode/','download/')
                else:
                    siteUrl = aEntry[0].replace('episode/','download/')
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            progress_.VSclose(progress_)
       
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

    sStart = '</i>\s*جميع الحلقات\s*</div>'
    sEnd = '<i class'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)" class="epss.+?</span>.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if "season/" in aEntry[0]:
                continue 
            sTitle = " E"+aEntry[1]
            sTitle = sMovieTitle+sTitle
            if 'http' not in aEntry[0]:
                siteUrl = URL_MAIN+aEntry[0].replace('episode/','download/')
            else:
                siteUrl = aEntry[0].replace('episode/','download/')
            sThumb = sThumb
            sDesc = ''			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()		
 
def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    sUrl2 = sUrl.replace('/download/','/watch/')
    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent1 = oRequestHandler.request()

    sPattern = '"url":"([^"]+)",'
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:            
            url = aEntry

            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
           
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="down-container">'
    sEnd = '<button style='
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="qual">.+?</i>(.+?)</h1>(.+?)<hr/>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :    
        for aEntry in aResult[1]:
            sQual = aEntry[0].replace("سيرفرات تحميل","")
            sHtmlContent1 = aEntry[1]

            sPattern = 'href="([^"]+)'
            aResult = oParser.parse(sHtmlContent1, sPattern)	
            if aResult[0] :
                for aEntry in aResult[1]:            
                    url = aEntry
                    sTitle = " "
                    if url.startswith('//'):
                        url = 'http:' + url		   

                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = sMovieTitle + ('[COLOR coral](%sp)[/COLOR]') % (sQual)
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent, sUrl):
    oParser = cParser()
    sPattern = 'class="page-link cursor-normal".+?style="background-color.+?onclick="(.+?)">.+?class="fa-solid fa-backward"></i>' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if '?page=' in sUrl:
                sUrl = sUrl.split('?page=')[0]
                aResult = sUrl+'?page='+aEntry.replace(')','').replace("updateQuery('page', ","")
            else:
                aResult = sUrl+'?page='+aEntry.replace(')','').replace("updateQuery('page', ","")
            
            return aResult

    return False 