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
from resources.sites.sflix import load, showSearch, showSeriesSearch, seriesGenres, moviesGenres, showMovies, showSeries, showSeasons, showEps, showLinks, showSeriesLinks

SITE_IDENTIFIER = 'solar'
SITE_NAME = 'Solar'
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
	
def __checkForNextPage(sHtmlContent):
    sPattern = 'title="Next" class="page-link" href="([^"]+)"'	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False