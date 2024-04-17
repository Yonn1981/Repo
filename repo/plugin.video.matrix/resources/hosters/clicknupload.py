import time
from resources.lib import captcha_lib, helpers, random_ua
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re,requests

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'clicknupload', 'Click-n-Upload')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        self._url = oRequest.getRealUrl()
        VSlog(self._url)
        api_call = ''

        headers = {'User-Agent': UA,
                   'Referer': self._url
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        if 'File Not Found' not in sHtmlContent:
            
            data=helpers.get_hidden(sHtmlContent)
            
            html = s.post(self._url, data, headers=headers).text
            headers.update({'Origin': self._url.rsplit('/', 1)[0]})
            html = s.post(self._url, data, headers=headers).text
            data=helpers.get_hidden(html)
            
            data.update(captcha_lib.do_captcha(html))
            time.sleep(16)
            html = s.post(self._url, data, headers=headers).text
            r = re.search(r'''class="downloadbtn"[^>]+onClick\s*=\s*\"window\.open\('(.+?)'\);"''', html)
            if r:
                headers.update({'verifypeer': 'false'})
                api_call= r.group(1).replace(' ', '%20') + helpers.append_headers(headers)
                
        if api_call:
            return True, api_call

        return False, False