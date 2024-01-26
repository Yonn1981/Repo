#-*- coding: utf-8 -*-
import re
import requests
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upstream', 'Upstream')

    def isDownloadable(self):
        return False
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not 'embed-' in self._url:
            self._url = self._url.replace('d/','embed-') + '.html'

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''

        headers = {'User-Agent': UA,
                   'Origin': self._url.rsplit('/', 1)[0],
                   'Referer': self._url
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        api_call = ''

        aResult = re.search(r'(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>', sHtmlContent)
        if aResult:
            sHtmlContent = cPacker().unpack(aResult.group(1))

        aResult = re.search(r'sources: *\[{file:["\']([^"\']+)', sHtmlContent)
        if aResult:
            api_call = aResult.group(1)
            

        if api_call:
            if 'http' not in api_call:
                api_call = self._url.rsplit('/', 1)[0] + api_call

            return True, api_call + '|Referer=' + self._url

        return False, False
