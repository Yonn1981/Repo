#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
import requests

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser
from resources.lib.util import urlEncode, Quote
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tma', 'TheMovieArchive')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('#')[0]

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = self._url
        SubTitle = ''
        if ('sub.info' in self._url):
            SubTitle = self._url.split('sub.info=')[1]
            api_call = self._url.split('?sub.info=')[0]
            
            oRequest = cRequestHandler(SubTitle)
            data = oRequest.request().replace('\\','')
            SubTitle = ''
            oParser = cParser()
            sPattern = '["\']language["\']:\s*["\']([^"\']+)["\'],\s*["\']url["\']:\s*["\']([^"\']+)["\']'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
                url = []
                slang = []
                for i in aResult[1]:
                    url.append(str(i[1]))
                    slang.append(str(i[0]))
                SubTitle = dialog().VSselectsub(slang, url)

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
