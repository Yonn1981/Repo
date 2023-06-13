# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
from resources.lib.util import Quote
from resources.lib.comaddon import progress, siteManager
from resources.sites.iptv import showWeb, play__


SITE_IDENTIFIER = 'daily'
SITE_NAME = '[COLOR orange]Daily IPTV List[/COLOR]'
SITE_DESC = 'Watch IPTV Channels'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_WEB = URL_MAIN
URL_EUROPE = URL_MAIN + 'iptv-uk-2023/'
URL_AMERICA = URL_MAIN + 'iptv-usa/'
URL_ARAB = URL_MAIN + 'iptv-arabic-2023-3/'
URL_SPORT = URL_MAIN + 'iptv-sports-2023-7/'

TV_TV = (True, 'showDailyList')

def load():
    oGui = cGui()


    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Latest list', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_EUROPE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'UK IPTV List', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_AMERICA)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'US IPTV List', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_ARAB)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Arabic IPTV List', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SPORT)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Sports IPTV List', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sUrl == 'TV':
        sUrl = URL_WEB


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?
    sPattern = '<h2 class="entry-title".+?href="([^"]+)" rel="bookmark">(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'tv.png', oOutputParameterHandler)

        progress_.VSclose(progress_)


    oGui.setEndOfDirectory()


def showAllPlaylist():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<ul class="da-attachments-list">'
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<a href="([^"]+)" title="([^"]+)" class='
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
