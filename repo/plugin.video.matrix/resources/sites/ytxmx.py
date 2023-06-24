# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.util import cUtil, Unquote

	
SITE_IDENTIFIER = 'ytxmx'
SITE_NAME = 'YTX.MX'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'


MOVIE_4k = (URL_MAIN + '/browse-movies/0/2160p/all/0/latest/0/all', 'showMovies')
MOVIE_EN = (URL_MAIN + '/browse-movies/0/all/all/0/year/0/all', 'showMovies')
KID_MOVIES = (URL_MAIN + '/browse-movies/0/all/animation/0/year/0/all', 'showMovies')

MOVIE_GENRES = (True, 'moviesGenres')

URL_SEARCH = (URL_MAIN + '/ajax/search?query=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/ajax/search?query=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4k[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' 4k أفلام', '4k.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab2.png', oOutputParameterHandler)
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'ajax/search?query='+sSearchText
        showSearchMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showSearchMovies(sSearch = ''):
    import requests
    oGui = cGui()
    sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '{"url":"([^"]+)","img":"([^"]+)","title":"([^"]+)","year":"(.+?)"}'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    #VSlog(aResult)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace('download','').replace('télécharger','')
            siteUrl = aEntry[0].replace('\/','/')
            sThumb = aEntry[1]
            sDesc = ''
            sYear = aEntry[3]


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

        progress_.VSclose(progress_)
 
    if not sSearch:

        oGui.setEndOfDirectory()  

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'browse-movies/0/all/action/0/year/0/all'])
    liste.append(['Adventure', URL_MAIN + 'browse-movies/0/all/adventure/0/year/0/all'])
    liste.append(['Animated', URL_MAIN + 'browse-movies/0/all/animation/0/year/0/all'])
    liste.append(['Biography', URL_MAIN + 'browse-movies/0/all/biography/0/year/0/all'])
    liste.append(['Comedy', URL_MAIN + 'browse-movies/0/all/comedy/0/year/0/all'])
    liste.append(['Crime', URL_MAIN + 'browse-movies/0/all/crime/0/year/0/all'])
    liste.append(['Drama', URL_MAIN + 'browse-movies/0/all/drama/0/year/0/all'])
    liste.append(['Documentary', URL_MAIN + 'browse-movies/0/all/documentary/0/year/0/all'])
    liste.append(['Family', URL_MAIN + 'browse-movies/0/all/family/0/year/0/all'])
    liste.append(['Fantasy', URL_MAIN + 'browse-movies/0/all/fantasy/0/year/0/all'])
    liste.append(['History', URL_MAIN + 'browse-movies/0/all/history/0/year/0/all'])
    liste.append(['Horror', URL_MAIN + 'browse-movies/0/all/horror/0/year/0/all'])
    liste.append(['Music', URL_MAIN + 'browse-movies/0/all/music/0/year/0/all'])
    liste.append(['Mystery', URL_MAIN + 'browse-movies/0/all/mystery/0/year/0/all'])
    liste.append(['Romance', URL_MAIN + 'browse-movies/0/all/romance/0/year/0/all'])
    liste.append(['Sci-Fi', URL_MAIN + 'browse-movies/0/all/sci-fi/0/year/0/all'])
    liste.append(['Thriller', URL_MAIN + 'yts.mx/browse-movies/0/all/thriller/0/year/0/all'])
    liste.append(['War', URL_MAIN + 'browse-movies/0/all/war/0/year/0/all'])
    liste.append(['Western', URL_MAIN + 'browse-movies/0/all/western/0/year/0/all'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4"><a href="([^"]+)".+?src="([^"]+)" alt="([^"]+)' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    #VSlog(aResult)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace('download','').replace('télécharger','')
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''


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

        progress_.VSclose(progress_)
 
    if not sSearch:

        oGui.setEndOfDirectory()  

 

def showServer():
    import xbmc
    oGui = cGui()
    import requests

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<div class="modal-torrent">.+?<span>(.+?)</span>.+?class="quality-size">(.+?)</p>.+?href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    if aResult[0]:
        for aEntry in aResult[1]:
            m = re.search('([0-9]{4})', sMovieTitle)
            if m:
               sYear = str(m.group(0))
               sMovieTitle = sMovieTitle.replace(sYear,'')
            

            url = aEntry[2]+'ttmxtt'
            qual = aEntry[0].replace('p','')
            sSize = aEntry[1].replace(' ','')
            sTitle = ('%s  [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, qual)	
					
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()  



def __checkForNextPage(sHtmlContent):
    sPattern = 'li class="pagination-bordered">.+?</li><li><a href="([^"]+)'	 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        return URL_MAIN + aResult[1][0]

    return False

    return False