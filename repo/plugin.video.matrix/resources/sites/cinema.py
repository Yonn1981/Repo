# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

SITE_IDENTIFIER = 'cinema'
SITE_NAME = 'CinemaAllYear'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

sHost = base64.b64decode(URL_MAIN)
dHost = sHost.decode("utf-8")

URL_MAIN = dHost[::-1]
MOVIE_EN = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=10&isMovie=true&pageNumber=1', 'showMovies')
MOVIE_AR = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=7&isMovie=true&pageNumber=1', 'showMovies')
MOVIE_HI = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=3&isMovie=true&pageNumber=1', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=6&isMovie=true&pageNumber=1', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=12&isMovie=true&pageNumber=1', 'showMovies')
KID_MOVIES = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=14&isMovie=true&pageNumber=1', 'showMovies')

SERIE_TR = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=13&sortType=8&pageNumber=1', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=5&sortType=8&pageNumber=1', 'showSeries')
SERIE_HEND = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=8&sortType=8&pageNumber=1', 'showSeries')
SERIE_EN = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=1&sortType=8&pageNumber=1', 'showSeries')
SERIE_AR = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=4&sortType=8&pageNumber=1', 'showSeries')
RAMADAN_SERIES = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=28&sortType=8&pageNumber=1', 'showSeries')
KID_CARTOON = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=15&sortType=8&pageNumber=1', 'showSeries')

DOC_SERIES = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=23&sortType=8&pageNumber=1', 'showSeries')

ANIM_NEWS = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=2&sortType=8&pageNumber=1', 'showSeries')
ANIM_MOVIES = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=9&isMovie=true&pageNumber=1', 'showMovies')
REPLAYTV_PLAY = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=11&sortType=8&pageNumber=1', 'showSeries')
REPLAYTV_NEWS = (URL_MAIN + 'api/MobileV3/Show/GetShows?sortType=2&categoryId=19&sortType=8&pageNumber=1', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + 'api/MobileV3/Show/SearchShows?showName=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'api/MobileV3/Show/SearchShows?showName=', 'showSeries')
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
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية','brmg.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسرحيات', 'msrh.png', oOutputParameterHandler)
   
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = URL_MAIN + 'api/MobileV3/Show/SearchShows?showName='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = URL_MAIN + 'api/MobileV3/Show/SearchShows?showName='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', getHost() +'/')
    oRequestHandler.addHeaderEntry('Origin', getHost())
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
    
    oOutputParameterHandler = cOutputParameterHandler() 
    for aEntry in sHtmlContent["data"]:
        if aEntry["isMovie"] == "false":
            continue
        movie_id = aEntry["id"]
        siteUrl = f'{URL_MAIN}api/MobileV3/Show/GetShow?id={movie_id}'
        sTitle = aEntry["title"]
        sThumb = aEntry["photoUrl"]
        sDesc = aEntry["description"]

        m = re.search('([0-9]{4})', sTitle)
        if m:
            sYear = str(m.group(0))
            if 'عرض' in sTitle:
                sTitle = sTitle.replace('عرض','')
            else:
                sTitle = sTitle.replace(sYear,'')

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
            			
        oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:       
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            nPage = int(sUrl.split('pageNumber=')[1]) + 1
            tPages = sNextPage
            nUrl = sUrl.split('pageNumber=')[0] + 'pageNumber=' + str(nPage)
            sTitle = f'Page {nPage}/{tPages}'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', nUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', f'[COLOR teal]{sTitle} >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', getHost() +'/')
    oRequestHandler.addHeaderEntry('Origin', getHost())
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
    
    oOutputParameterHandler = cOutputParameterHandler() 
    for aEntry in sHtmlContent["data"]:
        if aEntry["isMovie"] == "true":
            continue
        serie_id = aEntry["id"]
        siteUrl = f'{URL_MAIN}api/MobileV3/Show/GetShow?id={serie_id}'
        sTitle = aEntry["title"]
        sThumb = aEntry["photoUrl"]
        sDesc = aEntry["description"]

        m = re.search('([0-9]{4})', sTitle)
        if m:
            sYear = str(m.group(0))
            if 'عرض' in sTitle:
                sTitle = sTitle.replace('عرض','')
            else:
                sTitle = sTitle.replace(sYear,'')

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
                
        oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:       
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            nPage = int(sUrl.split('pageNumber=')[1]) + 1
            tPages = sNextPage
            nUrl = sUrl.split('pageNumber=')[0] + 'pageNumber=' + str(nPage)
            sTitle = f'Page {nPage}/{tPages}'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', nUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', f'[COLOR teal]{sTitle} >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
			
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
  
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', getHost() +'/')
    oRequestHandler.addHeaderEntry('Origin', getHost())
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler() 
    for aEntry in sHtmlContent["data"]["seasons"]:
        season_id = aEntry["id"]
        siteUrl = f'{URL_MAIN}api/MobileV3/Series/GetEpisodes?pageNumber=1&sessionId={season_id}'
        sTitle = f'{sMovieTitle} S{aEntry["seasonNumber"]}'
        sThumb = sThumb
        sDesc = sDesc

        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
            
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', getHost() +'/')
    oRequestHandler.addHeaderEntry('Origin', getHost())
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler() 
    for aEntry in sHtmlContent["data"]:
        siteUrl = sUrl
        sTitle = f'{sMovieTitle} E{aEntry["episodeNumber"]}'
        sThumb = sThumb
        sDesc = sDesc

        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sEpi', aEntry["episodeNumber"])
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
			    
        oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    if sHtmlContent["pagesCount"]:
        return sHtmlContent["pagesCount"]
    
    return False

def showSeriesLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sEpi = oInputParameterHandler.getValue('sEpi')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', getHost() +'/')
    oRequestHandler.addHeaderEntry('Origin', getHost())
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sSub = ''
    for item in sHtmlContent["data"]:
        if item["episodeNumber"] == int(sEpi):
            episode_files = item["episodeFiles"]
            if item["subtitles"]:
                subtitle_files = item["subtitles"]
                for file in subtitle_files:
                    sSub = file['path']

            for file in episode_files:
                sHosterUrl = file['path'] + '?sub.info=' + sSub
                sQual = file['resolution']

                oHoster = cHosterGui().getHoster('cinemayear') 
                if oHoster:
                    sDisplayTitle = ('%s [COLOR coral] [%s] [/COLOR]') % (sMovieTitle, sQual)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', getHost() +'/')
    oRequestHandler.addHeaderEntry('Origin', getHost())
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sSub = ''
    if sHtmlContent["data"]["subtitles"]:
        for aEntry in sHtmlContent["data"]["subtitles"]:
            sSub = aEntry["path"]

    for aEntry in sHtmlContent["data"]["files"]:
        sQual = aEntry["resolution"]
        sHosterUrl = aEntry["path"] + '?sub.info=' + sSub

        oHoster = cHosterGui().getHoster('cinemayear') 
        if oHoster:
            sDisplayTitle = ('%s [COLOR coral] [%s] [/COLOR]') % (sMovieTitle, sQual)
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def getHost():
    decoded_bytes = base64.b64decode('d29ocy5yYTU2My5hbWVuaWMvLzpzcHR0aA==')
    decoded_string = decoded_bytes.decode("utf-8")
    decoded_string = decoded_string[::-1]
    return decoded_string
