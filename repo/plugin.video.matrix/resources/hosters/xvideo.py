from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import unicodedata
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'xvideo', 'xVideoSharing')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        sReferer = f'https://{self._url.split("/")[2]}'

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
       
        api_call = ''
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent = cPacker().unpack(data)

        else:
            self._url = self._url.replace('embed-','')
            oRequest = cRequestHandler(self._url)
            sHtmlContent = oRequest.request()

            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                data = aResult[1][0]
                data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
                sHtmlContent = cPacker().unpack(data)


        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            api_call = aResult[1][0] 

        sPattern = 'sources:\["([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer 

        return False, False