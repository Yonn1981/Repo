#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import progress, VSlog
import re
import base64

UA = 'Mozilla/5.0 (iPad; CPU OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'faselhd', 'FaselHD', 'gold')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = self._url
        VSlog(self._url)
        oParser = cParser()   

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        sHtmlContent = oRequest.request()

        sPattern = ',RESOLUTION=(.+?),.+?(http.+?m3u8)'
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            sLink = []
            sQual = []
            for Stream in aResult[1]:
                sLink.append(str(Stream[1]))
                sQual.append(str(Stream[0]))
            api_call = dialog().VSselectqual(sQual, sLink)

        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False
