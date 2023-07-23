#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui, VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filemoon', 'Filemoon')

    def _getMediaLinkForGuest(self):
        if ('sub.info' in self._url):
            SubTitle = self._url.split('sub.info=')[1]
            oRequest0 = cRequestHandler(SubTitle)
            sHtmlContent0 = oRequest0.request().replace('\\','')
            oParser = cParser()

            sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
            aResult = oParser.parse(sHtmlContent0, sPattern)
            if aResult[0]:
                # initialisation des tableaux
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
        oParser = cParser()
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

        else:
            sPattern = 'file:"([^"]+)",label:"[0-9]+"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                # initialisation des tableaux
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, url)


        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
