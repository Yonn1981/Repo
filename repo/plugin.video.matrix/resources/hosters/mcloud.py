#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser
from resources.lib.util import urlEncode, Quote
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mcloud', 'mCloud/VizCLoud')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('#')[0]
        self._url0 = str(url)
    def _getMediaLinkForGuest(self):
        api_call = self._url

        if ('sub.info' in self._url0):
            SubTitle = self._url0.split('sub.info=')[1]
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

        oParser = cParser()

        sUrl = self._url
        sUrlf = self._url.split('list.m3u8')[0]

        url = []
        qua = []

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        sPattern = 'RESOLUTION=(\d+x\d+)(.+?.m3u8)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            for aEntry in aResult[1]:
                url.append(aEntry[1])
                qua.append(aEntry[0])

            if url:
                api_call = sUrlf + dialog().VSselectqual(qua, url)

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
