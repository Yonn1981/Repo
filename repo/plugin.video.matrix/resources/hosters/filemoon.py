#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.lib import helpers, random_ua
from resources.lib.util import Unquote
from six.moves import urllib_parse

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filemoon', 'Filemoon')

    def _getMediaLinkForGuest(self, autoPlay = False):
        oParser = cParser()
        self._url = self._url.replace('filemoon.sx','filemoon.in')

        if ('sub.info' in self._url):
            VSlog(self._url)
            SubTitle = self._url.split('sub.info=')[1]
            oRequest0 = cRequestHandler(SubTitle)
            sHtmlContent0 = oRequest0.request().replace('\\','')

            sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
            aResult = oParser.parse(sHtmlContent0, sPattern)
            if aResult[0]:

                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))
                SubTitle = dialog().VSselectsub(qua, url)
        else:
            SubTitle = ''

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        api_call = False

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHtmlContent = cPacker().unpack(aEntry)

        headers = {'User-Agent': UA}
        sPattern = 'sources:\s*\[{\s*file:\s*"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            headers.update({
                    'Referer': self._url,
                    'Origin': urllib_parse.urljoin(self._url, '/')[:-1]})
            api_call = aResult[1][0] + helpers.append_headers(headers)

        else:
            sPattern = 'file:"([^"]+)",label:"[0-9]+"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                headers.update({
                    'Referer': self._url,
                    'Origin': urllib_parse.urljoin(self._url, '/')[:-1]})
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, Unquote(url)) + helpers.append_headers(headers)

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
