# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
import re
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):
        sHtmlContent = GetHtml(url)
        sPattern = '<form action="(.+?)" method="post"'
        result = re.findall(sPattern, sHtmlContent)
        if result:
           url = 'https://multiup.org' + ''.join(result[0])

        NewUrl = url.replace('https://www.multiup.org/fr/download', 'https://www.multiup.org/fr/mirror')\
                    .replace('https://www.multiup.eu/fr/download', 'https://www.multiup.org/fr/mirror')\
                    .replace('https://www.multiup.org/download', 'https://www.multiup.org/fr/mirror')

        sHtmlContent = GetHtml(NewUrl)

        sPattern = 'nameHost="([^"]+)".+?link="([^"]+)".+?class="([^"]+)"'
        r = re.findall(sPattern, sHtmlContent, re.DOTALL)

        if not r:
            return False

        for item in r:

            if 'bounce-to-right' in str(item[2]) and not 'download-fast' in item[1]:
                self.list.append(item[1])

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

class cMegamax:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        sHosterUrl = url.replace('download','iframe')
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
                                'X-Inertia-Partial-Component':'web/files/mirror/video',
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
