#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'linkbox', 'Linkbox')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        url = 'https://www.linkbox.to/api/file/share_out_list/?sortField=utime&sortAsc=0&pageNo=1&pageSize=50&shareToken=' + self._url.rsplit('/', 1)[1]
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        itemId = sHtmlContent['data']['itemId']
        if itemId:
            surl = f'https://www.linkbox.to/api/file/detail?itemId={itemId}'
            oRequestHandler = cRequestHandler(surl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', self._url)
            sHtmlContent = oRequestHandler.request(jsonDecode=True)

            data = sHtmlContent['data']['itemInfo']['resolutionList']
            if data:
                sUrl = []
                sQual = []
                for link in data:
                    sUrl.append(link['url'])
                    sQual.append(link['resolution'])

                api_call = dialog().VSselectqual(sQual, sUrl)

                if api_call:
                    return True, api_call + '|User-Agent=' + UA

        return False, False