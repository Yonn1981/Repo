#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'lulustream', 'Lulustream')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.addHeaderEntry('origin', self._url.rsplit('/', 1)[0])
        sHtmlContent = oRequestHandler.request()

        api_call = ''

        aResult = re.search(r'(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>', sHtmlContent)
        if aResult:
            sHtmlContent = cPacker().unpack(aResult.group(1))
        
        aResult = re.search(r'sources:\s*\[{file:\s*["\']([^"\']+)', sHtmlContent)
        if aResult:
            api_call = aResult.group(1)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url + '&Origin=' + self._url.rsplit('/', 1)[0]

        return False, False
