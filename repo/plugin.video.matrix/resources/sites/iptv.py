# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import string

from resources.lib.comaddon import progress, addon, dialog, siteManager
from resources.lib.enregistrement import cEnregistremement
from resources.lib.epg import cePg
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote

SITE_IDENTIFIER = 'iptv'
SITE_NAME = '[COLOR orange]Premium IPTV[/COLOR]'
SITE_DESC = 'Watch Live television'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_WEB = 'https://raw.githubusercontent.com/Yonn1981/Repo/master/repo/zips/Resources/iptv.m3u'


TV_TV = (True, 'showMenuTV')

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

icon = 'tv.png'
sRootArt = ''
ADDON = addon()


class track:
    def __init__(self, length, title, path, icon, data=''):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon
        self.data = data


def load():
    addons = addon()

    if (addons.getSetting('hoster_iptv_username') == '') and (addons.getSetting('hoster_iptv_password') == ''):
        oGui = cGui()
        oGui.addText(SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' % ('red', 'Requires an IPTV Premium or Free Account'))

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addons.VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:
        oGui = cGui()
        addons = addon()

        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', addons.VSlang(30115), 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def opensetting():
    addon().openSettings()

def showMenuTV():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_WEB)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30332), 'tv.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def parseM3U(sUrl=None):  # Traite les m3u local
    
    if not sUrl:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    inf = oRequestHandler.request().split('\n')

    playlist = []
    song = track(None, None, None, None)
    ValidEntry = False

    for line in inf:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            length, title = line.split('#EXTINF:')[1].split(',', 1)
            try:
                licon = line.split('#EXTINF:')[1].partition('tvg-logo=')[2]
                icon = licon.split('"')[1]
            except:
                icon = 'tv.png'
            ValidEntry = True
            song = track(length, title, None, icon)

        elif len(line) != 0:
            if ValidEntry and (not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path = line
                playlist.append(song)
                song = track(None, None, None, None)

    return playlist


def showWeb():  # Code qui s'occupe de liens TV du Web
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sUrl == 'TV':
        sUrl = URL_WEB


    playlist = parseM3U(sUrl=sUrl)



    if not playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Error getting playlist[/COLOR]')

    else:
        total = len(playlist)
        progress_ = progress().VScreate(SITE_NAME)
        for track in playlist:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sThumb = track.icon
            if not sThumb:
                sThumb = 'https://raw.githubusercontent.com/Yonn1981/Repo/master/repo/plugin.video.matrix/resources/art/tv.png'


            # les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')

            thumb = ''.join([sRootArt, sThumb])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', thumb)

            oHoster = cHosterGui().getHoster('lien_direct')
        
            if oHoster:
                oHoster.setDisplayName(track.title)
                oHoster.setFileName(track.title)
                cHosterGui().showHoster(oGui, oHoster, url2, sThumb)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()




def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for i in string.digits:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    for i in string.ascii_uppercase:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<title>(.+?)</title><link>(.+?)</link>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        progress_ = progress().VScreate(SITE_NAME)

        # affiche par
        if oInputParameterHandler.exist('AZ'):
            sAZ = oInputParameterHandler.getValue('AZ')
            string = filter(lambda t: t[0].strip().capitalize().startswith(sAZ), aResult[1])
            string = sorted(string, key=lambda t: t[0].strip().capitalize())
        else:
            string = sorted(aResult[1], key=lambda t: t[0].strip().capitalize())

        total = len(string)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[0])
            oOutputParameterHandler.addParameter('sThumbnail', 'tv.png')

            oHoster = cHosterGui().getHoster('lien_direct')
        
            if oHoster:
                oHoster.setDisplayName(track.title)
                oHoster.setFileName(track.title)
                cHosterGui().showHoster(oGui, oHoster, aEntry[1], 'tv.png')

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def play__():  # Lancer les liens
    addons = addon()
    oGui = cGui()

    Iuser = addons.getSetting('hoster_iptv_username')
    Ipass = addons.getSetting('hoster_iptv_password')
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+').replace('username', Iuser).replace('password', Ipass)
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sDesc = oInputParameterHandler.getValue('sDesc')

    # Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = getRealUrl(sUrl)

    # Bug specifique au flux france TV
    # eof detectedL
    if 'youtube' in sUrl:
        oHoster = cHosterGui().checkHoster(sUrl)

        if oHoster:
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)

    else:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sTitle)
        sUrl = sUrl.replace(' ', '%20')
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)

        from resources.lib.player import cPlayer
        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        
        return False, False

    oGui.setEndOfDirectory()


"""
Fonction diverse:
#   - getRealUrl = Regex pour Iptv(Officiel)
#   - showDailymotionStream = Lis les liens de streaming de Daylimotion qui sont speciaux
#   - getBrightcoveKey = Recupere le token pour les liens proteger par Brightcove (RMC Decouvert par exemple)
"""


def getRealUrl(chain):
    oParser = cParser()

    UA2 = UA
    url = chain
    regex = ''
    param = ""
    head = None

    r = re.search('\[[DECODENRJ]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = decodeNrj(r.group(1))

    r = re.search('\[[BRIGHTCOVEKEY]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = getBrightcoveKey(r.group(1))

    r = re.search('\[[REGEX]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        regex = r.group(1)

    r = re.search('\[[UA]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        UA2 = r.group(1)

    r = re.search('\[[URL]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = r.group(1)

    r = re.search('\[[HEAD]+\](.+?)(?:(?:\[[A-Z]+\])|$)',chain)
    if r:
        head = r.group(1)

    # post metehod ?
    r = re.search('\[[POSTFORM]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        param = r.group(1)

    oRequestHandler = cRequestHandler(url)
    if param:
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
    if head:
        import json
        head = json.loads(head)
        for a in head:
            oRequestHandler.addHeaderEntry(a,head[a])
    sHtmlContent = oRequestHandler.request()

    if regex:
        aResult2 = oParser.parse(sHtmlContent, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url


def decodeNrj(d):
    oRequestHandler = cRequestHandler(d)
    sHtmlContent = oRequestHandler.request()

    title = re.search('data-program_title="([^"]+)"', sHtmlContent).group(1)
    ids = re.search('data-ref="([^"]+)"', sHtmlContent).group(1)

    url = 'https://www.nrj-play.fr/compte/live?channel=' + d.split('/')[3] + '&channel=' + d.split('/')[3] + '&title='
    url += title + '&channel=' + d.split('/')[3] + '&ref=' + ids + '&formId=formDirect'

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    dataUrl = re.search('"contentUrl" content="([^"]+)"', sHtmlContent).group(1)

    return dataUrl


def getBrightcoveKey(sUrl):
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "rmcdecouverte" in sUrl:
        url = re.search('<script type="application/javascript" src="([^"]+)"></script>', sHtmlContent).group(1)

        oRequestHandler = cRequestHandler("https://" + sUrl.split('/')[2] + url)
        sHtmlContent = oRequestHandler.request()
        result = re.search('N="([^"]+)",y="([^"]+)"\)', sHtmlContent)
        player = result.group(1)
        video = result.group(2)

        oRequestHandler = cRequestHandler("https://static.bfmtv.com/ressources/next-player/cleo-player/playerBridge.js")
        sHtmlContent = oRequestHandler.request().lower()

        ID = sUrl.split('/')[2].split('.')[0]
        account = re.search("\n(.+?): '" + ID + "'", sHtmlContent).group(1).replace('            ', '')

    else:
        result = re.search('<div class="video_block" id="video_player_.+?" accountid="([^"]+)" playerid="([^"]+)" videoid="([^"]+)"', sHtmlContent)

        account = result.group(1)
        player = result.group(2)
        video = result.group(3)

    url = 'http://players.brightcove.net/%s/%s_default/index.min.js' % (account, player)
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    policyKey = re.search('policyKey:"(.+?)"', sHtmlContent).group(1)

    url = "https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s" % (account, video)
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Accept', "application/json;pk=" + policyKey)
    sHtmlContent = oRequestHandler.request()
    url = re.search('"sources":.+?src":"([^"]+)"', sHtmlContent).group(1)

    return url
