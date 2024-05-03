#-*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cinemayear', 'Cinema', 'gold')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''
        if ('sub.info' in self._url):
            SubTitle = self._url.split('sub.info=')[1]
            api_call = self._url.split('?sub.info=')[0] 

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
