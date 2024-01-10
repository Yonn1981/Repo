#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog, VSlog
import re
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'rubystream', 'Rubystream')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        
        if '/d/' in self._url:
            self._url = self._url.replace('/d/','/embed-') + '.html'

        headers = {'User-Agent': UA,
                   'Origin': self._url.rsplit('/', 1)[0],
                   'Referer': self._url,
                   'Accept-Language': 'en-US,en;q=0.5'
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        api_call = ''

        aResult = re.search(r'(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>', sHtmlContent)
        if aResult:
            sHtmlContent = cPacker().unpack(aResult.group(1))
        
        aResult = re.search(r'''sources:\s*\[(?:{src:|{file:)?\s*['"]([^'"]+)''', sHtmlContent)
        if aResult:
            api_call = aResult.group(1)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url + '&Origin=' + self._url.rsplit('/', 1)[0]

        return False, False
