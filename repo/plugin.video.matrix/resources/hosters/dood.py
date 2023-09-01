# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Do not go through the download version.
# Not all links are downloadable.
# SSL error my region - Temp fixed for my area, might be broken for others
import random
import time
import requests
import urllib.request as urllib

from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.48 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dood', 'Dood')

    def setUrl(self, url):
        sid = str(url).replace('/d/', '/e/')
        sid = sid.split('/e/')[1]
        self._url = 'http://i.doodcdn.co/e/'+sid

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False
        headers = {'User-Agent': UA}

        req = urllib.Request(self._url, None, headers)
        with urllib.urlopen(req, timeout=30) as response:
            sHtmlContent = response.read()
            urlDownload = response.geturl()

        try:
            sHtmlContent = sHtmlContent.decode('utf8')
        except:
            pass

        if '/pass_md5/' not in sHtmlContent:
            return None
        md5 = sHtmlContent.split("'/pass_md5/")[1].split("',")[0]
        token = md5.split("/")[-1]
        randomString = getRandomString()
        expiry = int(time.time() * 1000)
        videoUrlStart = requests.get(
            f"https://i.doodcdn.co/pass_md5/{md5}",
            headers={"referer": urlDownload},
        ).text
        api_call = f"{videoUrlStart}{randomString}?token={token}&expiry={expiry}"

        if api_call:
            api_call = api_call.replace('~','%7E') + '|Referer=' + urlDownload
            return True, api_call

        return False, False


def getRandomString(length=10):
    allowedChars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return ''.join(random.choice(allowedChars) for _ in range(length))
