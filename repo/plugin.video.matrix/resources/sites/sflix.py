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

SITE_IDENTIFIER = 'sflix'
SITE_NAME = 'sFlix'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/movie', 'showMovies')
KID_MOVIES = (URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=3&country=all', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (URL_MAIN + '/tv-show', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=3&country=all', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

URL_SEARCH_MOVIES = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/home')
    oGui.addDir(SITE_IDENTIFIER, 'showHome', 'محتوى الصفحة الرئيسية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انيميشن', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText.replace(' ','-')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText.replace(' ','-')
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=10&country=all'])
    liste.append(['Adventure', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=18&country=all'])
    liste.append(['Animated', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=3&country=all'])
    liste.append(['Biography', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=37&country=all'])
    liste.append(['Comedy', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=7&country=all'])
    liste.append(['Crime', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=2&country=all'])
    liste.append(['Drama', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=4&country=all'])
    liste.append(['Documentary', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=11&country=all'])
    liste.append(['Fantasy', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=13&country=all'])
    liste.append(['History', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=19&country=all'])
    liste.append(['Horror', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=14&country=all'])
    liste.append(['Music', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=15&country=all'])
    liste.append(['Mystery', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=1&country=all'])
    liste.append(['Romance', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=12&country=all'])
    liste.append(['Sci-Fi', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=5&country=all'])
    liste.append(['Thriller', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=16&country=all'])
    liste.append(['War', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=28&country=all'])
    liste.append(['Western', URL_MAIN + '/filter?type=tv&quality=all&release_year=all&genre=6&country=all'])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=10&country=all'])
    liste.append(['Adventure', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=18&country=all'])
    liste.append(['Animated', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=3&country=all'])
    liste.append(['Biography', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=37&country=all'])
    liste.append(['Comedy', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=7&country=all'])
    liste.append(['Crime', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=2&country=all'])
    liste.append(['Drama', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=4&country=all'])
    liste.append(['Documentary', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=11&country=all'])
    liste.append(['Fantasy', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=13&country=all'])
    liste.append(['History', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=19&country=all'])
    liste.append(['Horror', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=14&country=all'])
    liste.append(['Music', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=15&country=all'])
    liste.append(['Mystery', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=1&country=all'])
    liste.append(['Romance', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=12&country=all'])
    liste.append(['Sci-Fi', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=5&country=all'])
    liste.append(['Thriller', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=16&country=all'])
    liste.append(['War', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=28&country=all'])
    liste.append(['Western', URL_MAIN + '/filter?type=movie&quality=all&release_year=all&genre=6&country=all'])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHome():
    oGui = cGui()
      
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '>Trending</h2>'
    sEnd = '</section>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    oGui.addText(SITE_IDENTIFIER, u'\u2193' + 'Trending', 'pop.png')

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[1]
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if "tv/"  in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sStart = '>Latest Movies</h2>'
    sEnd = '</section>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    oGui.addText(SITE_IDENTIFIER, u'\u2193' + 'Latest Movies', 'film.png')

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[1]
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sStart = '>Latest TV Shows</h2>'
    sEnd = '</section>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    oGui.addText(SITE_IDENTIFIER, u'\u2193' + 'Latest TV Shows', 'mslsl.png')

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[1]
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

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

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "tv/"  in aEntry[1]:
                continue

            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[1]
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

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

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "movie/"  in aEntry[1]:
                continue

            sTitle = aEntry[2]
            siteUrl = URL_MAIN+aEntry[1]
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

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
    sUrl2 = sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:

            sId = aEntry
            sUrl = URL_MAIN + '/ajax/v2/tv/seasons/' + sId

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<a data-id="([^"]+)".+?class="dropdown-item ss-item.+?href="([^"]+)">(.+?)</a>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()    
                for aEntry in aResult[1]:
                    sSeason = aEntry[2].replace('Season ','S')
                    sTitle = f'{sMovieTitle} {sSeason}'
                    siteUrl = URL_MAIN+'/ajax/v2/season/episodes/'+aEntry[0]
                    sThumb = sThumb
                    sDesc = ''

                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('tvUrl',sUrl2)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)

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

    sPattern = 'data-id="([^"]+)">.+?<a href="([^"]+)" class="film-poster mb-0">.+?<img src="([^"]+)".+?class="film-poster-img".+?title="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            siteUrl = URL_MAIN + '/ajax/v2/episode/servers/' + aEntry[0]
            sEpisode = aEntry[3].split(':')[0].replace('Episode ','').replace(':','')
            sEpisode = '{}E{:02d}'.format(sMovieTitle, int(sEpisode))
            sTitle = aEntry[3].split(':')[1].replace('Episode','')
            sDisplayTitle = '{} [COLOR coral]{}[/COLOR]'.format(sEpisode, str(sTitle)) 
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
       
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
    oParser = cParser()

    sPattern = 'data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sId = aEntry
            sUrl = URL_MAIN + '/ajax/movie/episodes/' + sId
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

    sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sId = aEntry[0]
            sHost = aEntry[1]
            sUrl2 = URL_MAIN + '/ajax/get_link/' + sId

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

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

    sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sId = aEntry[0]
            sHost = aEntry[1]
            sUrl2 = URL_MAIN + '/ajax/sources/' + sId

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"link":"([^"]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'title="Next" class="page-link" href="([^"]+)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False