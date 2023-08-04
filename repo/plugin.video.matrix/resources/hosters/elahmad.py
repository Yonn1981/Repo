# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://gounlimited.to/embed-xxx.html
# top_replay robin des droits
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'elahmad', 'elahmad')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False


        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '(eval\(function\(p,a,c,k,e,r(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = '<iframe src=.+?"([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            if aResult[0]:
                api_call = aResult[1][0].replace('\\', '')
                api_call = base64.b64decode(api_call)
     
                oRequest = cRequestHandler(api_call)
                oRequest.addHeaderEntry('Referer', self._url)
                sHtmlContent = oRequest.request()
                api_call = oRequest.getRealUrl()

        if api_call:
            return False, api_call  # redirection

        return False, False
