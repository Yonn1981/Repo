# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.aadecode import decodeAA
import re
import binascii
import base64

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidguard', 'Vidguard')

    def _getMediaLinkForGuest(self, autoPlay = False):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        r = re.search(r'eval\("window\.ADBLOCKER\s*=\s*false;\\n(.+?);"\);</script', sHtmlContent)
        if r:
            r = r.group(1).replace('\\u002b', '+')
            r = r.replace('\\u0027', "'")
            r = r.replace('\\u0022', '"')
            r = r.replace('\\/', '/')
            r = r.replace('\\\\', '\\')
            r = r.replace('\\"', '"')
            sHtmlContent = decodeAA(r, True)

            sPattern = '"Label":"([^"]+)","URL":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url = []
                qua = []
                for i in aResult[1]:
                    url2 = str(i[1])
                    if not  url2 .startswith('https://'):
                        url2 = re.sub(':/*', '://', url2)
                    url2 = url2.encode().decode('unicode-escape')
                    url.append(sig_decode(url2))
                    qua.append(str(i[0]))

                api_call = dialog().VSselectqual(qua, url) + '|Referer=' + self._url
                
            sPattern = '"stream":"(.*?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url = str(aResult[1][0])
                if not url.startswith('https://'):
                    url= re.sub(':/*', '://', url)
                url = url.encode().decode('unicode-escape')
                api_call = sig_decode(url) + '|Referer=' + self._url

        if api_call:
            return True, api_call

        return False, False


# Adapted from PHP code by vb6rocod
# Copyright (c) 2019 vb6rocod
def sig_decode(url):
    sig = url.split('sig=')[1].split('&')[0]
    t = ''
    
    for v in binascii.unhexlify(sig):
        t += chr((v if isinstance(v, int) else ord(v)) ^ 2)
    t = list(base64.b64decode(t + '==')[:-5][::-1])
    
    for i in range(0, len(t) - 1, 2):
        t[i + 1], t[i] = t[i], t[i + 1]
        
    t = ''.join(chr(i) for i in t)
    url = url.replace(sig, ''.join(str(t))[:-5])
    return url
