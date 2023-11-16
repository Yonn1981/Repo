#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.lib.util import Unquote

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filemoon', 'Filemoon')

    def _getMediaLinkForGuest(self, autoPlay = False):
        oParser = cParser()

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
        sHtmlContent = oRequest.request()

        api_call = False

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                url = aEntry
                sHtmlContent = cPacker().unpack(url)

                sPattern = 'file:"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)

                if aResult[0]:
                    api_call = aResult[1][0]

                    oRequestHandler = cRequestHandler(api_call)
                    sHtmlContent2 = oRequestHandler.request()
                    list_url = []
                    list_q = []

                    sPattern = 'PROGRAM.*?BANDWIDTH.*?RESOLUTION=(\d+x\d+).*?(http.+?)(#|$)'
                    aResult = oParser.parse(sHtmlContent2, sPattern)
                    if aResult[0]:
                        for aEntry in aResult[1]:
                            list_url.append(aEntry[1])
                            list_q.append(aEntry[0])
                        if list_url:
                            api_call = dialog().VSselectqual(list_q, list_url)

        else:
            sPattern = 'file:"([^"]+)",label:"[0-9]+"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:

                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                url = dialog().VSselectqual(qua, Unquote(url))


        if api_call:
            if ('http' in SubTitle):
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url, SubTitle
            else:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
