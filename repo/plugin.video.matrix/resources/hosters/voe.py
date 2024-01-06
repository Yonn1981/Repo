# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import re
import base64

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', 'Voe')

    def _getMediaLinkForGuest(self, autoPlay = False):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        r = re.search(r"let\s*wc0\s*=\s*'([^']+)", sHtmlContent)
        if r:
            import json
            r = json.loads(base64.b64decode(r.group(1)).decode('utf8',errors='ignore'))
            url = r.get('file')
            return True, url

        oParser = cParser()
        sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
