# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Do not go through the download version.
# Not all links are downloadable.

import random
import time
import requests

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dood', 'Dood')

    def setUrl(self, url):
        sid = str(url).replace('/d/', '/e/')
        sid = sid.split('/e/')[1]
        self._url = url.replace('doods.pro','d0000d.com')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.request()
        surl = oRequestHandler.getRealUrl()

        if surl != self._url:
            self._url = surl
        
        sHost = getHost(self._url)

        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()

        if '/pass_md5/' not in sHtmlContent:
            return None
        md5 = sHtmlContent.split("'/pass_md5/")[1].split("',")[0]

        token = md5.split("/")[-1]
        randomString = getRandomString()
        expiry = int(time.time() * 1000)
        videoUrlStart = requests.get(
            f"{sHost}pass_md5/{md5}",
            headers={"referer": surl},
        ).text

        api_call = f"{videoUrlStart}{randomString}?token={token}&expiry={expiry}"

        if api_call:
            api_call = api_call.replace('~','%7E') + '|Referer=' + surl
            return True, api_call

        return False, False

def getRandomString(length=10):
    allowedChars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return ''.join(random.choice(allowedChars) for _ in range(length))

def getHost(self):
    parts = self.rsplit("/", 2)
    host = parts[0] 
    return f'{host}/'