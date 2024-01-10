# -*- coding: utf-8 -*-
# Adopted from ResolveURL https://github.com/Gujal00/ResolveURL
from six.moves import urllib_parse
from resources.lib.comaddon import dialog, VSlog 
from resources.hosters.hoster import iHoster
import re, requests, json

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vk', 'Vk')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        headers = {'User-Agent': UA,
                   'Referer': 'https://vk.com/',
                   'Origin': 'https://vk.com'}
        
        media_id = self._url.rsplit('/', 1)[1]
        if 'video_ext.php?' in media_id:
            media_id = media_id.split('video_ext.php?')[1]

        query = urllib_parse.parse_qs(media_id)

        try:
            oid, video_id = query['oid'][0], query['id'][0]

        except:
            oid, video_id = re.findall('video(.*)_(.*)', media_id)[0]
        

        sources = self.__get_sources(oid, video_id, headers)
        if sources:
            sources.sort(key=lambda x: int(x[0]), reverse=True)
        
        if len(sources) == 1:
            api_call = sources[0][1]
            
        elif len(sources) > 1:
            url=[]
            qua=[]
            for aEntry in sources:
                url.append(str(aEntry[1]))
                qua.append(str(aEntry[0]))
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False

    def __get_sources(self, oid, video_id, headers={}):
        sources_url = 'https://vk.com/al_video.php?act=show'
        data = {
            'act': 'show',
            'al': 1,
            'video': '{0}_{1}'.format(oid, video_id)
        }
        headers.update({'X-Requested-With': 'XMLHttpRequest'})
        html = requests.post(sources_url, data=data, headers=headers).text

        if html.startswith('<!--'):
            html = html[4:]
        js_data = json.loads(html)
        payload = []
        sources = []
        for item in js_data.get('payload'):
            if isinstance(item, list):
                payload = item
        if payload:
            for item in payload:
                if isinstance(item, dict):
                    js_data = item.get('player').get('params')[0]
            for item in list(js_data.keys()):
                if item.startswith('url'):
                    sources.append((item[3:], js_data.get(item)))
            if not sources:
                sources = [('360', js_data.get('hls'))]
            return sources