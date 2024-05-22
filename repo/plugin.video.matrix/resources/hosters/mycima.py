#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.util import Unquote
import re

UA = 'Mozilla/5.0 (iPad; CPU OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mycima', 'WeCima', 'gold')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequestHandler.request()

        r2 = re.search(' src="([^<]+)" type="video/mp4">', sHtmlContent)

        if (r2):
            api_call = r2.group(1)

        api_call = Unquote(api_call)
        if api_call:
            return True, api_call.replace(' ', '%20') + "|Referer=" + sReferer + '&User-Agent=' + UA

        return False, False
