#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voodc', 'Voodc')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
        url = self._url

        oRequestHandler = cRequestHandler(url)
        sHtmlContent2 = oRequestHandler.request()
        sPattern2 = '<script type="text/javascript" src="([^"]+)'
        aResult = re.findall(sPattern2, sHtmlContent2)
        if aResult:
                url2 = 'https:' + aResult[0]
                Referer = url
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('Referer', Referer)
                sHtmlContent2 = oRequestHandler.request()
                
                sPattern2 = 'var r = "player="\+embedded\+"&e=([^"]+)'
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    url2 = 'https://voodc.com/player.php?player=d&e=' + aResult[0]
                    Referer = url
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('Referer', Referer)
                    sHtmlContent2 = oRequestHandler.request()
                    sPattern2 = '"file": \'([^\']+)'
                    aResult = re.findall(sPattern2, sHtmlContent2)
                    if aResult:
                        api_call = aResult[0]

        if api_call:
                return True, api_call

        return False, False
