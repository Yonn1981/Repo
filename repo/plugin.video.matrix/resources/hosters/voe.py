# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import random_ua
import re
import base64

UA = random_ua.get_random_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', 'Voe')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        r = re.search(r"let\s*(?:wc0|[0-9a-f]+)\s*=\s*'([^']+)", sHtmlContent)
        if r:
            import json
            r = json.loads(base64.b64decode(r.group(1))[::-1].decode('utf8',errors='ignore'))
            url = r.get('file') 
            return True, url + '|Referer=' + self._url + '&Origin=' + self._url.rsplit('/', 2)[0]

        oParser = cParser()
        sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        aResult1 = base64.b64decode(aResult[1][0])
        if aResult[0]:
            api_call = aResult1.decode("utf-8")

        if api_call:
            return True, api_call

        return False, False