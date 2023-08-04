# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser
import resolveurl
from urllib.parse import unquote

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'resolver', 'ResolveURL')
        self.__sRealHost = ''

    def setRealHost(self, host):
        self.__sRealHost = "/" + host

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR violet]'+ self._defaultDisplayName + self.__sRealHost + '[/COLOR]'


    def _getMediaLinkForGuest(self, autoPlay = False):
        self._url0 = str(self._url)

        if ('sub.info' in self._url0):
            SubTitle = self._url0.split('sub.info=')[1]
            oRequest0 = cRequestHandler(unquote(SubTitle))
            sHtmlContent0 = oRequest0.request().replace('\\','')
            oParser = cParser()

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

        hmf = resolveurl.HostedMediaFile(url = self._url)
        if hmf.valid_url():
            stream_url = hmf.resolve()
            if stream_url:
                if ('http' in SubTitle):
                    return True, stream_url, SubTitle
                else:
                    return True, stream_url

        return False, False
