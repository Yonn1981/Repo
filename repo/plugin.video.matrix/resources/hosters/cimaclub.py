#-*- coding: utf-8 -*-
# Temp ??
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
import re, base64
import requests

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cimaclub', 'CimaClub', 'gold')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        referer = self._url

        headers = {'User-Agent': UA,
                   'Referer': self._url
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text
     
        aResult = re.search(r'file:["\']([^"\']+)["\']', sHtmlContent)
        if aResult:
            sSource = aResult.group(1)

        aResult = re.search(r'name="Xtoken" content=["\']([^"\']+)["\']', sHtmlContent)
        if aResult:
            sSource = aResult.group(1)
            sSource = base64.b64decode(sSource).decode('utf8',errors='ignore')
            sSource = re.findall('(https://master.+?.m3u8)', sSource)
            sSource = str(sSource).replace('[', '').replace(']', '').replace("'", '')

        sHtmlContent = s.get(sSource, headers=headers).text
        sources = re.findall(',RESOLUTION=(.+?)\n(.+?.m3u8)', sHtmlContent)
        if len(sources) == 1:
            api_call = sources[0][1]
            
        elif len(sources) > 1:
            url=[]
            qua=[]
            for aEntry in sources:
                url.append(str(aEntry[1]))
                qua.append(str(aEntry[0].split(',FRAME-RATE')[0]))
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' +referer

        return False, False
