#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://sama-share.com/embed-shsaa6s49l55-750x455.html

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib.util import Unquote
import re,xbmc
import requests

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uppom', 'Uppom')

    def setUrl(self, sUrl):
        self._url2 = sUrl
        self._url = str(sUrl).replace(".html","")

        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")

    def _getMediaLinkForGuest(self, autoPlay = False):
         oParser = cParser() 

         if 'https' in self._url:
            d = re.findall('https://(.*?)/([^<]+)',self._url)

         else:
            d = re.findall('http://(.*?)/([^<]+)',self._url)

         for aEntry in d:
            sHost= aEntry[0]
            sID= aEntry[1]
            if '/' in sID:
               sID = sID.split('/')[0]
         sLink= 'http://'+sHost+'/'+sID     
  
         api_call = Unquote(self._url2)  

         Sgn=requests.Session()
         UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
         headers = {
            'Origin': 'http://{0}'.format(sHost),
            'Referer': sLink,
            'User-Agent': UA
         }
         payload = {
            'op': 'download2',
            'id2': sID,
            'rand': '',
            'referer': sLink
         }
         _r = Sgn.post(sLink,headers=headers,data=payload)
         sHtmlContent = _r.content.decode('utf8',errors='ignore')

         sPattern = 'id="direct_link".+?href="([^"]+)'
         aResult = oParser.parse(sHtmlContent,sPattern)
         if aResult[0]:
             api_call = aResult[1][0].replace(' ', '%20')
         
         if api_call:
             return True, api_call

         return False, False