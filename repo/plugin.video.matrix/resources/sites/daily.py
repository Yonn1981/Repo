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

TV_TV = (True, 'showDailyList')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Latest list', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sUrl == 'TV':
        sUrl = URL_WEB


    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "<div class='item-thumbnail'>.+?href='([^']+)'.+?<img alt='([^']+)'.+?data-src='([^']+)' loading="
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'data.title' in aEntry[1]:
                continue
            sUrl2 = aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showAllPlaylist():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  
    sPattern = '<a href="([^"]+)" id="download".+?title="([^"]+)">'
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

            oGui.addMisc(SITE_IDENTIFIER, 'showWeb', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = 'onclick="([^"]+)"><b>(.+?)</b>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0].replace("myDownloadFunction(this,`",'').replace("`)",'')
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addMisc(SITE_IDENTIFIER, 'showWeb', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
