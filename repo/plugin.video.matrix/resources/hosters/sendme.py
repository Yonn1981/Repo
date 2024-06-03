#-*- coding: utf-8 -*-

import requests
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sendme', 'Send.Me')

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        headers = {
        "Referer":self._url,
        "User-Agent": UA
        }

        sHtmlContent = requests.get(self._url, headers=headers, verify=False).text
        oParser = cParser()

        api_call = False
        sPattern = '<source src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
           
        if api_call:
            return True, f'{api_call}|User-Agent={UA}&Referer={self._url}'

        return False, False
        
