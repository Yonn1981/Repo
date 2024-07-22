# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog
from Cryptodome.Cipher import ARC4
from urllib.parse import unquote, quote, urlparse
import re
import requests, base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):
        sHtmlContent = GetHtml(url)
        sPattern = '<form action="([^"]+)'
        result = re.findall(sPattern, sHtmlContent)
        if result:
           NewUrl = f'https://multiup.io{result[0]}'.replace('/fr/download', '/en/mirror').replace('/en/download', '/en/mirror').replace('/download', '/en/mirror')

        sHtmlContent = GetHtml(NewUrl)

        sPattern = 'nameHost="([^"]+)"\s*link="([^"]+)'
        r = re.findall(sPattern, sHtmlContent)
        if not r:
            return False

        for aEntry in r:
            if 'UseNext' in aEntry[0] or 'doodrive' in aEntry[0] or 'fikper' in aEntry[0] or 'ddownload' in aEntry[0] or 'rapidgator' in aEntry[0] or '1fichier' in aEntry[0]:
                  continue
            sHosterUrl = aEntry[1]
            sLabel = 'Multiup - ' + aEntry[0]
            self.list.append(f'url={sHosterUrl}, label={sLabel}')

        return self.list

class cJheberg:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):

        if url.endswith('/'):
            url = url[:-1]

        idFile = url.rsplit('/', 1)[-1]
        NewUrl = 'https://api.jheberg.net/file/' + idFile
        sHtmlContent = GetHtml(NewUrl)

        sPattern = '"hosterId":([^"]+),"hosterName":"([^"]+)",".+?status":"([^"]+)"'
        r = re.findall(sPattern, sHtmlContent, re.DOTALL)
        if not r:
            return False

        for item in r:
            if not 'ERROR' in item[2]:
                urllink = 'https://download.jheberg.net/redirect/' + idFile + '-' + item[0]
                try:
                    url = GetHtml(urllink)
                    self.list.append(url)
                except:
                    pass

        return self.list
    
# modif cloudflare
def GetHtml(url, postdata=None):

    if 'download.jheberg.net/redirect' in url:
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()
        url = oRequest.getRealUrl()
        return url
    else:
        sHtmlContent = ''
        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)

        if postdata != None:
            oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            oRequest.addHeaderEntry('Referer', 'https://download.jheberg.net/redirect/xxxxxx/yyyyyy/')

        elif 'download.jheberg.net' in url:
            oRequest.addHeaderEntry('Host', 'download.jheberg.net')
            oRequest.addHeaderEntry('Referer', url)

        oRequest.addParametersLine(postdata)

        sHtmlContent = oRequest.request()

        return sHtmlContent
        
class cMegamax:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        sHosterUrl = url.replace('download','iframe').replace(' ','')
        if 'leech' in sHosterUrl or '/e/' in sHosterUrl:
            return False
        oRequestHandler = cRequestHandler(sHosterUrl)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = sHtmlContent.replace('&quot;','"')
        oParser = cParser()
        
        sVer = ''
        sPattern = '"version":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in (aResult[1]):
                sVer = aEntry

        s = requests.Session()            
        headers = {'Referer':sHosterUrl,
                                'Sec-Fetch-Mode':'cors',
                                'X-Inertia':'true',
                                'X-Inertia-Partial-Component':'files/mirror/video',
                                'X-Inertia-Partial-Data':'streams',
                                'X-Inertia-Version':sVer}

        r = s.get(sHosterUrl, headers=headers).json()
        
        for key in r['props']['streams']['data']:
            sQual = key['label'].replace(' (source)','')
            for sLink in key['mirrors']:
                sHosterUrl = sLink['link']
                sLabel = sLink['driver'].capitalize()
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'https:' + sHosterUrl
        
                self.list.append(f'url={sHosterUrl}, qual={sQual}, label={sLabel}')
                                 
        return self.list 

class cVidsrcto:
    oRequestHandler = cRequestHandler("https://raw.githubusercontent.com/Ciarands/vidsrc-keys/main/keys.json")
    res = oRequestHandler.request(jsonDecode=True)
    if res is not None:
        keys = (res["encrypt"][0], res["decrypt"][0])

    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        oParser = cParser()
        
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()
        
        sPattern = 'data-id="(.*?)"'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if (aResult[0]):
          sources_code = aResult[1][0]
          sources = self.get_sources(sources_code)

          sPattern = "'.*?': '(.*?)'"
          aResult = oParser.parse(sources, sPattern)
          if aResult[0]:
            for aEntry in aResult[1]:
                source = aEntry
                source_url = self.get_source_url(source)
                self.list.append(source_url)
        return self.list 

    def get_sources(self, data_id) -> dict:
        encoded_id = cVidsrcto.vrf_encrypt(self.keys[0], data_id)
        req = requests.get(f"https://vidsrc.to/ajax/embed/episode/{data_id}/sources?token={encoded_id}")
        data = req.json()

        return {video.get("title"): video.get("id") for video in data.get("result")}    

    def get_source_url(self, source_id) -> str:
        encoded_source = cVidsrcto.vrf_encrypt(self.keys[0], source_id)
        req = requests.get(f"https://vidsrc.to/ajax/embed/source/{source_id}?token={encoded_source}")
        data = req.json()

        encrypted_source_url = data.get("result", {}).get("url")
        return self.decrypt_source_url(encrypted_source_url)

    def decrypt_source_url(self, source_url) -> str:
        encoded = self.decode_base64_url_safe(source_url)
        decoded = cVidsrcto.vrf_decrypt(self.keys[1], encoded)

        return unquote(decoded)       
    
    def decode_base64_url_safe(self, s) -> str:
        standardized_input = s.replace('_', '/').replace('-', '+')
        return standardized_input

    def vrf_encrypt(key: str, input: str) -> str:
        cipher = ARC4.new(key.encode())
        vrf = cipher.encrypt(input.encode())
        vrf_base64 = base64.urlsafe_b64encode(vrf).decode('utf-8')
        string_vrf = quote(vrf_base64)
        return string_vrf

    def vrf_decrypt(key: str, input: str) -> str:
        vrf_base64 = unquote(input)
        vrf = base64.urlsafe_b64decode(vrf_base64.encode('utf-8'))

        cipher = ARC4.new(key.encode())
        decrypted_vrf = cipher.decrypt(vrf)
        return decrypted_vrf.decode('utf-8')

class cVidsrcnet:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        oParser = cParser()
        req = requests.get(url)
        sources = re.findall(r'<div class="server" data-hash="(.*?)">(.+?)</div>', req.text)

        sPattern = "'(.*?)', '.*?'"
        aResult = oParser.parse(sources, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                source = aEntry
                req_1 = requests.get(f"https://rcp.vidsrc.me/rcp/{source}", headers={"Referer": url})

                encoded = re.search(r'data-h="(.*?)"', req_1.text).group(1)
                seed = re.search(r'<body data-i="(.*?)">', req_1.text).group(1)

                decoded_url = self.decode_src(encoded, seed)
                if decoded_url.startswith("//"):
                   decoded_url = f"https:{decoded_url}"

                req_2 = requests.get(decoded_url, allow_redirects=False, headers={"Referer": f"https://rcp.vidsrc.me/rcp/{source}"})
                location = req_2.headers.get("Location")
        
                if "vidsrc.stream" in location:
                  location= location + f"?Referer=https://rcp.vidsrc.me/rcp/{source}"
                  self.list.append(location)
                if "2embed.cc" in location:
                  location = ''
                  self.list.append(location)
                if "multiembed.mov" in location:
                  location= location + f"?Referer=https://rcp.vidsrc.me/rcp/{source}"
                  self.list.append(location)

        return self.list
       
    def decode_src(self, encoded, seed) -> str:
        '''decodes hash found @ vidsrc.me embed page'''
        encoded_buffer = bytes.fromhex(encoded)
        decoded = ""
        for i in range(len(encoded_buffer)):
            decoded += chr(encoded_buffer[i] ^ ord(seed[i % len(seed)]))
        return decoded
    
