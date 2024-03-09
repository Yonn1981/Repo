#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import base64
import json
import requests

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'shortlink', 'Short.ink')

    def __getHost(self, url):
        parts = url.split('//', 1)
        host = parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        response = requests.get(self._url)
        sUrl = response.url
        host = self.__getHost(sUrl)
        sHost = f'https://{host}/'

        api_call = ''
        s = requests.session()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": host,
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UA
            }

        response = s.get(sUrl, headers=headers).text
        start_pos = response.index("atob(") + 6
        end_pos = response.rindex(")")
        base64_encoded_string = response[start_pos:end_pos]
        decoded_string = base64.b64decode(base64_encoded_string).decode('utf-8')

        json_data = json.loads(decoded_string)
        id = json_data["id"]
        domain = json_data["domain"]

        # add www for hd
        api_call = f'https://{domain}/www{id}'

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + sHost + '&Host=' + domain

        return False, False
