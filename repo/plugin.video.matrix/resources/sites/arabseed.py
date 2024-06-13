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
from resources.lib.util import Quote, cUtil
from resources.lib.comaddon import progress, siteManager
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'arabseed'
SITE_NAME = 'Arabseed'
SITE_DESC = 'arabic vod'
 
MAIN_URL = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_MAIN = random_ua.get_arabseedUrl(MAIN_URL)

MOVIE_CLASSIC = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%83%d9%84%d8%a7%d8%b3%d9%8a%d9%83%d9%8a%d9%87/', 'showMovies')
MOVIE_EN = (URL_MAIN + '/category/foreign-movies/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/arabic-movies-5/', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/indian-movies/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/asian-movies/', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/category/turkish-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%86%d9%8a%d9%85%d9%8a%d8%b4%d9%86/', 'showMovies')

SERIE_TR = (URL_MAIN + '/category/turkish-series-1/', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d9%88%d8%b1%d9%8a%d9%87/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/foreign-series/', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/arabic-series/', 'showSeries')
RAMADAN_SERIES = (URL_MAIN + '/category/ramadan-series-2024/', 'showSeries')

SPORT_WWE = (URL_MAIN + '/category/wwe-shows/', 'showMovies')
ANIM_NEWS = (URL_MAIN + '/category/cartoon-series/', 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + '/category/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/find/?find=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/find/?find=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'


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
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', 'class.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

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
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdblg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/netfilx/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-netfilz/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netfilx', 'agnab.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/netfilx/%d8%a7%d9%81%d9%84%d8%a7%d9%85-netfilx/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام Netfilx', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2023/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان 2023', 'rmdn.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2022/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان 2022', 'rmdn.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()    
    if sSearchText is not False:
        sUrl = URL_MAIN + '/find/?find='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/find/?find='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
			
def showMovies(sSearch = ''):
    oGui = cGui()

    oParser = cParser()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', Quote(sUrl))
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()
  
    if sSearch:
        psearch = sUrl.split('?find=')[1]
        oRequestHandler = cRequestHandler(URL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', Quote(sUrl))
        oRequestHandler.addParameters('search', psearch)
        oRequestHandler.addParameters('type', 'movies')
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

    sPattern = '</div><a href="(.+?)">.+?data-src="([^"]+)".+?alt="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
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

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch: 
        oGui.setEndOfDirectory()
 
def showPacks(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^"]+)".+?class.+?<div class="BlockTitle">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            siteUrl = aEntry[0]
            sTitle = cUtil().CleanMovieName(aEntry[2])
            sThumb = aEntry[1]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showPack', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPacks', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch: 
        oGui.setEndOfDirectory()

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^"]+)".+?class.+?<div class="BlockTitle">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = (cUtil().CleanMovieName(aEntry[2])).replace("</em>","").replace("<em>","").replace("</span>","").replace("<span>","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ""
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
        
       
    oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', Quote(sUrl))
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()
  
    if sSearch:
        psearch = sUrl.split('?find=')[1]
        oRequestHandler = cRequestHandler(URL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', Quote(sUrl))
        oRequestHandler.addParameters('search', psearch)
        oRequestHandler.addParameters('type', 'series')
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<div class="Movie.+?">.+?<a href="([^<]+)">.+?data-image="([^<]+)" alt="([^<]+)">'
    else:
        sPattern = '</div><a href="(.+?)">.+?data-src="([^"]+)".+?alt="(.+?)">'

    itemList = []
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
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

    sPattern = 'data-id="(.+?)" data-season="(.+?)"><i class="fa fa-folder"></i>الموسم <span>(.+?)</span></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sSeason =cUtil().ConvertSeasons(aEntry[2])
            sSeason = f'{sMovieTitle} S{sSeason}'
            pseason = aEntry[1]
            post = aEntry[0]

            oRequestHandler = cRequestHandler(URL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/Single/Episodes.php')
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addParameters('post_id', post)
            oRequestHandler.addParameters('season', pseason)
            oRequestHandler.setRequestType(1)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'href="([^<]+)">([^<]+)<em>([^<]+)</em>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                oOutputParameterHandler = cOutputParameterHandler() 
                for aEntry in aResult[1]:
                    siteUrl = aEntry[0]
                    sEp = "E"+aEntry[2]
                    sTitle = sSeason+sEp
                    sThumb = sThumb
                    sDesc = ''

                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
    
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:

        sPattern = '<link rel="canonical" href="([^"]+)".+?<meta property="og:title" content="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:

                sTitle = (cUtil().CleanMovieName(aEntry[1])).replace("‎عرب سيد - Arabseed","")
                sTitle = (cUtil().ConvertSeasons(sTitle)).split('الحلقة')[0]
                sSeason = sTitle.replace(sMovieTitle,'').replace(' - ','')
                if 'موسم' not in aEntry[1]:
                    sTitle = sTitle+' '+'S1'
                else:
                 sTitle = sMovieTitle +' '+ sSeason
                
                siteUrl = aEntry[0]
                
                sThumb = sThumb
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
 
                oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
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

    sStart = '<div class="ContainerEpisodesList"'
    sEnd = '<div style="clear: both;"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^<]+)">([^<]+)<em>([^<]+)</em>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:

                sEp = "E"+aEntry[2].replace(" ","")
                if "مدبلج" in sMovieTitle:
                    sMovieTitle = sMovieTitle.replace("مدبلج","")
                    sMovieTitle = "مدبلج"+sMovieTitle
                sTitle = sMovieTitle+' '+sEp
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
             
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                      
    oGui.setEndOfDirectory() 

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="next page-numbers" href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        return URL_MAIN+aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb') 

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<a href="([^<]+)" class="watchBTn">'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0].replace(' ','')
        oRequestHandler = cRequestHandler(m3url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request() 

    sStart = '<div class="containerServers">'
    sEnd = '<div class="containerIframe">'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)
    	
    sPattern = '<h3>(.+?)</h3>(.+?)</i>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :
       
        for aEntry in aResult[1]:
            sQual = aEntry[0].replace("مشاهدة","").replace(' ','')
            sHtmlContent = aEntry[1]

            sHosterUrl = url_function(sHtmlContent)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = ('%s [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sDisplayTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = '<h3>(.+?)</h3>(.+?)</i>(.+?)</i>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :
       
        for aEntry in aResult[1]:
            sQual = aEntry[0].replace("مشاهدة","").replace(' ','')
            sHtmlContent = aEntry[2]
		         
            sHosterUrl = url_function(sHtmlContent)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = ('%s [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sDisplayTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = '<h3>(.+?)</h3>(.+?)</i>(.+?)</i>(.+?)</i>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :
       
        for aEntry in aResult[1]:
            sQual = aEntry[0].replace("مشاهدة","").replace(' ','')
            sHtmlContent = aEntry[3]
		         
            sHosterUrl = url_function(sHtmlContent)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = ('%s [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sDisplayTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = '<h3>(.+?)</h3>(.+?)</i>(.+?)</i>(.+?)</i>(.+?)</i>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :
       
        for aEntry in aResult[1]:
            sQual = aEntry[0].replace("مشاهدة","").replace(' ','')
            sHtmlContent = aEntry[4]
		         
            sHosterUrl = url_function(sHtmlContent)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = ('%s [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sDisplayTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = '<h3>(.+?)</h3>(.+?)</i>(.+?)</i>(.+?)</i>(.+?)</i>(.+?)</i>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :
       
        for aEntry in aResult[1]:
            sQual = aEntry[0].replace("مشاهدة","").replace(' ','')
            sHtmlContent = aEntry[5]
		         
            sHosterUrl = url_function(sHtmlContent)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = ('%s [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sDisplayTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    
    else:
        sPattern = 'data-link="(.+?)" class'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
            
                url = aEntry
                if 'vtbe' in url:
                    url = url +'|Referer='+URL_MAIN
                if url.startswith('//'):
                    url = 'http:' + url
				           
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    sDisplayTitle = sMovieTitle
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sDisplayTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def url_function(sHtmlContent):
    oParser = cParser()
    sPattern = 'data-link="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0] :
        for aEntry in aResult[1]:            
            url = aEntry
            if 'vtbe' in url:
                url = url +'|Referer='+URL_MAIN
            if url.startswith('//'):
                url = 'http:' + url
    return url
