#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/

import re 
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cMegamax
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'halacima'
SITE_NAME = 'Halacima'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/أفلام-أجنبية', 'showMovies')
MOVIE_FAM = (f'{URL_MAIN}genre/أفلام-عائلي', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/أفلام-هندية', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category/أفلام-أنمي', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/أفلام-اسيوية', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category/أفلام-عربية', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}category/أفلام-تركية-مدبلجة', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/أفلام-تركي-مترجمة', 'showMovies')

SERIE_ASIA = (f'{URL_MAIN}category/مسلسلات-أسيوية', 'showSeries')
SERIE_TR_AR = (f'{URL_MAIN}category/مسلسلات-تركية-مدبلجة', 'showSeries')
SERIE_TR = (f'{URL_MAIN}category/مسلسلات-تركية-مترجمة', 'showSeries')
SERIE_EN = (f'{URL_MAIN}category/مسلسلات-أجنبية', 'showSeries')
SERIE_DUBBED = (f'{URL_MAIN}category/مسلسلات-مدبلجة', 'showSeries')
SERIE_KR = (f'{URL_MAIN}category/مسلسلات-كورية-مترجمة', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}category/مسلسلات-انمي', 'showSerie')

REPLAYTV_NEWS = (f'{URL_MAIN}category/برامج-وتلفزة', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search/', 'showSeries')
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
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], 'مسلسلات كورية', 'kr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/%D9%81%D9%8A%D9%84%D9%85-{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '>الرئيسية</a>'
    sEnd = '<div id="search">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'المزيد' in aEntry[1]:
                continue 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sDesc = ''
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            if 'مسلسلات' in sTitle:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', sTitle, 'mslsl.png', '', '', oOutputParameterHandler)
            elif 'برامج' in sTitle:
                oGui.addMisc(SITE_IDENTIFIER, 'showSerie', sTitle, 'mslsl.png', '', '', oOutputParameterHandler)
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

    sPattern = '<article class="post">.+?<a href="([^<]+)" title="([^<]+)">.+?data-original="([^<]+)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
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
            sThumb = aEntry[2]
            siteUrl = aEntry[0].replace("/movies/","/watch_movies/")
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)

    if not sSearch:        
        sPattern = '<li><a href="([^"]+)" data-ci-pagination-page="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle =   f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)
 
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

    sPattern = '<article class="post">.+?<a href="([^<]+)" title="([^<]+)">.+?data-original="([^<]+)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "مسلسل" not  in aEntry[1]:
                continue
            if sSearch:
               if "حلقة" in aEntry[1]:
                   continue
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            sThumb = aEntry[2]
            siteUrl = aEntry[0]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showSeason', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)

    if not sSearch:        
        sPattern = '<li><a href="([^"]+)" data-ci-pagination-page="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<article class="post">.+?<a href="([^<]+)" title="([^<]+)">.+? data-original="([^<]+)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[0].replace("/episodes/","/watch_episodes/")
            sThumb = aEntry[2]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'عرض' in sTitle or 'حفل' in sTitle or 'مبار' in sTitle:
                oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeason', sTitle, 'next.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
        
    sPattern = '<li><a href="([^"]+)" data-ci-pagination-page="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
            siteUrl = aEntry[0]
            sThumb = ""
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeason():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<div id="getSeasonsBySeries" class="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:

        sStart = '<a title="سلسلة مواسم">'
        sEnd = '<div class="container">'
        sHtmlContents = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<div class="seasonNum">(.+?)</div>.+?href="(.+?)" title="(.+?)">.+?src="([^"]+)'
        aResult = oParser.parse(sHtmlContents, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:

                sTitles = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("كامله","").replace("بجودة عالية","").replace("كاملة","").replace("جودة عالية","").replace("كامل","").replace("اونلاين","").replace("اون لاين","").split('الموسم')[0] 
                sTitle =  f'{sTitles.split("الجزء")[0]} {aEntry[0].replace("الموسم","S").replace("مدبلج","").replace("كامل","")}'
                if 'موسم' not in aEntry[0]:
                    sTitle = f'{sTitle} S1'
                siteUrl = aEntry[1]
                sThumb = aEntry[3]
                sDesc = ''
                if sThumb.startswith('//'):
                    sThumb = f'https:{aEntry[1]}'
			
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
        sPattern = '<a class="" href="([^<]+)" title="([^<]+)">.+?<span>([^<]+)</span>.+?<span class="numEp">([^<]+)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = f'{sMovieTitle} E{aEntry[3]}'
                sThumb = sThumb
                siteUrl = aEntry[0].replace("/episodes/","/watch_episodes/")
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<a class="" href="([^<]+)" title="([^<]+)">.+?<span>([^<]+)</span>.+?<span class="numEp">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = f'{sMovieTitle} E{aEntry[3]}'
            sThumb = sThumb
            siteUrl = aEntry[0].replace("/episodes/","/watch_episodes/")
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showServers():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  "baseUrl = '([^']+)" 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        URL_MAIN = aResult[1][0] 

    sPattern =  'postID = "([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        postID = aResult[1][0] 

    sPattern =  'onclick="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sServer = aEntry.replace("getPlayer('","").replace("')","")

            oRequestHandler = cRequestHandler(f'{URL_MAIN}ajax/getPlayer')
            oRequestHandler.addHeaderEntry('Accept', '*/*')
            oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty')
            oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors')
            oRequestHandler.addHeaderEntry('sec-fetch-site', 'same-origin')
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Origin', URL_MAIN)
            oRequestHandler.addParameters('server', sServer)
            oRequestHandler.addParameters('postID', postID)
            oRequestHandler.addParameters('Ajax', '1')
            oRequestHandler.setRequestType(1)
            sHtmlContent1 = oRequestHandler.request()

            sPattern = '<IFRAME.+?SRC=["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent1, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                for aEntry in (aResult[1]):
                    if 'قريبا' in aEntry:
                        continue
                    if 'leech' in aEntry:
                        continue

                    sHosterUrl = aEntry
                    if sHosterUrl.startswith('//'):
                        sHosterUrl = f'http:{sHosterUrl}'

                    if 'megamax' in sHosterUrl:
                        data = cMegamax().GetUrls(sHosterUrl)
                        if data is not False:
                            for item in data:
                                sHosterUrl = item.split(',')[0].split('=')[1]
                                sQual = item.split(',')[1].split('=')[1]
                                sLabel = item.split(',')[2].split('=')[1]

                                sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}][/COLOR][COLOR orange] - {sLabel}[/COLOR]'      
                                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                oOutputParameterHandler.addParameter('sThumb', sThumb)

                                oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<a target="_blank" href=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            if 'megamax' in aEntry:
                continue
            
            url = aEntry
            if url.startswith('//'):
               url = f'http:{url}'
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()