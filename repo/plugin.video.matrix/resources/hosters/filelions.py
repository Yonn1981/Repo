# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker
from six.moves import urllib_parse

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filelions', 'FileLions')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        referer = self._url
        if '|Referer=' in self._url:
            self._url, referer = self._url.split('|Referer=')
            referer = urllib_parse.urljoin(referer, '/')
        else:
            referer = self._url

        self._url = self._url.replace('/d/','/v/').replace('/f/','/v/').replace('/file/','/v/').replace('/download/','/v/')
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', referer)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        if api_call:
            return True, api_call

        return False, False
