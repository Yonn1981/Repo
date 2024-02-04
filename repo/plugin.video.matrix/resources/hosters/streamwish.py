from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import unicodedata

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamwish', 'Streamwish')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        self._url = self._url.replace('/f/','/e/').replace('/d/','/v/')
        api_call = ''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
       
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent = cPacker().unpack(data)

        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        sPattern = 'MDCore.wurl=["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 
            if api_call.startswith('//'):
                api_call = 'http:' + api_call

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False