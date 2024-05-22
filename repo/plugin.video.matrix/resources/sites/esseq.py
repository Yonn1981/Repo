#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Linux; Android 14; SM-A346M Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.108 Mobile Safari/537.36 Instagram 330.0.0.40.92 Android (34/14; 450dpi; 1080x2130; samsung; SM-A346M; a34x; mt6877; pt_BR; 596227443)'

SITE_IDENTIFIER = 'esseq'
SITE_NAME = 'Esseq'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
if addon().getSetting('Use_alternative') == "true":
    URL_MAIN = siteManager().getUrlMain2(SITE_IDENTIFIER)

SERIE_TR = (URL_MAIN + 'all-series/', 'showSeries')
MOVIE_TURK = (URL_MAIN + 'category/الأفلام-التركية/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search/', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'episodes/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries2', 'احدث الحلقات', 'turk.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search/'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="block-post">.+?href="([^"]+)".+?style="background-image:url\((.*?)\).+?class="title">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[2]:
                continue
 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            import base64
            if '?url=' in siteUrl or '?post=' in siteUrl:
                url_tmp = siteUrl.split('?url=')[-1].replace('%3D','=')
                siteUrl = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
               sThumb = 'http:' + sThumb
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="block-post">.+?href="([^"]+)".+?style="background-image:url\((.*?)\).+?class="title">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[2]:
                continue
 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            if 'الموسم' not in aEntry[2]:
                sTitle = sTitle + ' S1'
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "<a href='([^<]+)'>&rsaquo;</a>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:      
        return aResult[1][0]

    return False 

def showSeries2():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="block-post">.+?href="([^"]+)".+?style="background-image:url\((.*?)\).+?class="title">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[2]:
                continue
 
 
            sTitle = (cUtil().CleanMovieName(aEntry[2])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]
            if '?url=' in siteUrl or '?post=' in siteUrl:
                url_tmp = siteUrl.split('?url=')[-1].replace('%3D','=')
                siteUrl = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
            sThumb = aEntry[1]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries2', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sPattern = 'class="story">(.+?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:       
        sDesc = aResult[1][0]

    sPattern = '<article class="postEp">.+?<a href="([^"]+)".+?</span>\s*<span>(.+?)</span>.+?background-image:url\((.*?)\);.+?class="title">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            SerieTitle = aEntry[3].split('الحلقة ')[0].replace(' - ','')
            m = re.search('([0-9]{1})', SerieTitle)
            if m:
               sS = str(m.group(0))
               sTitle = 'S'+sS+' E'+aEntry[1]+' '+SerieTitle.replace(sS,'')
            else:
                sTitle = sMovieTitle+' E'+aEntry[1]
            siteUrl = aEntry[0] 
            if '?url=' in siteUrl or '?post=' in siteUrl:
                url_tmp = siteUrl.split('?url=')[-1].replace('%3D','=')
                siteUrl = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
            sThumb = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sPattern = '<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:       
        sTitle = aResult[1][0]
        oGui.addText(SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' % ('red', sTitle), 'none.png')

    oGui.setEndOfDirectory() 

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<link rel=["\']shortlink["\'] href=["\']([^"\']+)["\']' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        URL_MAIN = aResult[1][0]

    sPattern =  '<div class="skipAd">.+?href="(.+?)">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0].split('?url=')[1]
        oRequestHandler = cRequestHandler(m3url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request() 
      	
    sPattern = 'data-name="(.+?)" data-server="(.+?)">' 
    aResult = re.findall(sPattern, sHtmlContent)
    sPattern = 'href="(.+?)"><img' 
    aResult2 = re.findall(sPattern, sHtmlContent)
    if aResult:
        for aEntry in aResult:
            
            url = aEntry[1]
            host  = aEntry[0].replace('facebook','face')

            if 'ok' in host:
               url =  'https://ok.ru/videoembed/'+ url
            if 'face' in host:
               url =  'https://app.videas.fr/embed/media/'+ url
            if 'tune' in host:
               url =  'https://tune.pk/js/open/embed.js?vid='+url+'&userid=827492&_=1601112672793'
            if 'estream' in host:
               url =  'https://arabveturk.sbs/embed-'+url+'.html'
            if 'now' in host:
               url =  'https://extreamnow.org/embed-'+url+'.html'
            if 'box' in host:
               url =  'https://youdbox.site/embed-'+url+'.html'
            if 'Pro HD' in host:
               url =  'https://segavid.com/embed-'+url+'.html'
            if 'Red HD' in host:
               url =  'https://embedwish.com/e/'+ url
            if 'online' in host:
               url =  'https://player.vimeo.com/video/'+url+'?title=0&byline=0'
            if 'youtube' in host:
               url =  'https://www.youtube.com/watch?v='+url
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'extreamnow' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + m3url
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
	
    if aResult2:
        for aEntry in aResult2:
            
            url = aEntry
            if url.startswith('//'):
               url = 'http:' + url
				            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
              
    oGui.setEndOfDirectory()