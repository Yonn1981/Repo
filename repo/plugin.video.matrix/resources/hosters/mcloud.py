#-*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo
# Thanks https://github.com/Rowdy-Avocado/

import requests
import base64, json
from urllib.parse import unquote
from Cryptodome.Cipher import ARC4
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mcloud', 'mCloud/VizCLoud')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('$')[0]
        self._url0 = str(url)

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''
        VSlog(self._url0)

        if ('sub.info' in self._url0):
            SubTitle = self._url0.split('sub.info=')[1]
            if '&t=' in SubTitle:
                SubTitle = SubTitle.split('&t=')[0]
            else:
                SubTitle = SubTitle
            oRequest0 = cRequestHandler(SubTitle)
            sHtmlContent0 = oRequest0.request().replace('\\','')
            oParser = cParser()

            sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
            aResult = oParser.parse(sHtmlContent0, sPattern)

            if aResult[0]:
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))
                SubTitle = dialog().VSselectsub(qua, url)
        else:
            SubTitle = ''

        my_keys = getKeys()
        domain = self._url.split("/e/")[0]
        id = self._url.rsplit('/e/')[1].split('?', 1)[0]
        encoded_id = encode(id, my_keys[0])
        t = self._url.split("t=")[1].split("&")[0]
        h = encode(id, my_keys[1])
        media_url = f"{domain}/mediainfo/{encoded_id}?t={t}&h={h}"

        response = requests.get(media_url)
        
        encoded_res = response.json().get('result')
        decoded_res = decode(encoded_res, my_keys[2])
        res = json.loads(decoded_res)
        if 'sources' in res:
            sList = json.loads(json.dumps(res))
            api_call = sList['sources'][0]['file']
                    
        api_call = api_call.replace('\\','')

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False

def encode(input_str, key):
        rc4_key = key.encode('utf-8')
        cipher = ARC4.new(rc4_key)
        encrypted_bytes = cipher.encrypt(input_str.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')

def decode(input_str, key):
        decoded_bytes = base64.urlsafe_b64decode(input_str)
        rc4_key = key.encode('utf-8')
        cipher = ARC4.new(rc4_key)
        decrypted_bytes = cipher.decrypt(decoded_bytes)
        decoded_string = decrypted_bytes.decode('utf-8')
        return unquote(decoded_string)

def getKeys():
        oRequestHandler = cRequestHandler("https://raw.githubusercontent.com/Yonn1981/Repo/master/repo/plugin.video.matrix/resources/extra/keys.json")
        res = oRequestHandler.request(jsonDecode=True)
        if res is not None:
             keys = res["Vidplay"]
        return keys