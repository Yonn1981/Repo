#-*- coding: utf-8 -*-

import json
import re, requests
import base64
import hashlib

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import helpers
from Cryptodome.Cipher import AES
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'chillx', 'Chillx')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        headers = {'User-Agent': UA,
                   'Referer': self._url}
        
        s = requests.Session()  
   
        r = s.get(self._url, headers=headers)
        sHtmlContent = r.text

        key_response = requests.get("https://raw.githubusercontent.com/rushi-chavan/multi-keys/keys/keys.json")
        key_data = key_response.json()
        key = key_data['chillx']
        key = ''.join(key)
        key = bytes(key, 'utf-8')       

        edata = re.search(r"JScript[\w+]?\s*=\s*'([^']+)", sHtmlContent).group(1)
        if edata:
            edata = json.loads(edata)
            ct = base64.b64decode(edata['ct'])
            salt = bytes.fromhex(edata['s'])
            iv = bytes.fromhex(edata['iv'])

            md = hashlib.md5()
            md.update(key)
            md.update(salt)
            cache0 = md.digest()

            md = hashlib.md5()
            md.update(cache0)
            md.update(key)
            md.update(salt)
            cache1 = md.digest()

            key = cache0 + cache1

            cipher = AES.new(key, AES.MODE_CBC, iv)
            ddata = cipher.decrypt(ct)
            ddata = ddata.decode('utf-8').replace("\\", "")
            r = re.search(r'''(?:"file":\s*"([^"]+)")''', ddata) \
                or re.search(r'"video_player".+?file:\s*"([^"]+)', ddata)
            if r:
                headers.update({'Origin': self._url.rsplit("/",3)[0], 'verifypeer': 'false'})
                return True, r.group(1) + helpers.append_headers(headers)

        return False, False

