#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upstream', 'Upstream')

    def isDownloadable(self):
        return False
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not 'embed-' in self._url:
            self._url = self._url.replace('d/','embed-') + '.html'

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''

        oParser = cParser()
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHtmlContent = cPacker().unpack(aEntry)

        sPattern = r'sources: *\[{file:["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            if 'http' not in api_call:
                api_call = self._url.rsplit('/', 1)[0] + api_call

            return True, api_call + '|Referer=' + self._url

        return False, False
