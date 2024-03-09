# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'tvfun'
SITE_NAME = 'Tvfun'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

RAMADAN_SERIES = (URL_MAIN + '/ts/mosalsalat-ramadan-2024/', 'showSeries')
SERIE_TR = (URL_MAIN + '/cat/mosalsalat-torkia,3/', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/ts/mosalsalat-modablaja/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/cat/mosalsalat-hindia/', 'showSeries')
SERIE_AR = (URL_MAIN + '/cat/mosalsalat-3arabia,3/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/cat/mosalsalat-korea/', 'showSeries')
SERIE_LATIN = (URL_MAIN + '/cat/mosalsalat-latinia/', 'showSeries')
REPLAYTV_NEWS = (URL_MAIN + '/cat/programme-tv/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/q/', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeriesSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتنية', 'latin.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdblg.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', 'rmdn.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/ts/mosalsalat-motarjama/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مترجمة', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/ts/zee-alwan/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'زي الوان', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/q/'+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
  
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="serie-thumb">\s*<a href="(.+?)" title="(.+?)">\s*<img loading=".+?" src="(.+?)" alt'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مترجمة","").replace("مترجم","")
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + siteUrl

            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<ul class="pagination">(.+?)class="headline">'  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent = aResult[1][0]

    sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'موقع' in aEntry[1]:
                continue

            sTitle = aEntry[1]     
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0]
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + siteUrl
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            sThumb = ""
            sDesc = ""

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+"/"
      sUrl = sUrl.replace(' ','')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="headline">(.+?)<div id="footer">'  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent2 = aResult[1][0]

    sPattern = '<a href="(.+?)" title="(.+?)">.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent2, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("والاخيرة","")
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + siteUrl

            sThumb = aEntry[2]
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)

    sPattern = 'class="videocontainer">\s*<iframe src="([^<]+)" id="([^<]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "playlist"
            siteUrl = 'https:'+aEntry[0]
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + siteUrl
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<ul class="pagination">(.+?)class="headline">'  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent3 = aResult[1][0]

        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
        aResult = oParser.parse(sHtmlContent3, sPattern)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
                if 'موقع' in aEntry[1]:
                    continue 
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="headline">(.+?)class="head-title"> أخر الحلقات </h3>'  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent = aResult[1][0]

    sPattern = '<div class="video-thumb">\s*<a href="(.+?)" title="(.+?)">\s*<img loading="lazy" src="(.+?)" alt'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("مدبلج للعربية","مدبلج").replace("مشاهدة وتحميل","").replace("اون لاين","")
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + siteUrl

            sThumb = sThumb
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = 'class="videocontainer">\s*<iframe src="([^<]+)" id="([^<]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "playlist"
            siteUrl = 'https:'+aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = sThumb
            sDesc = ""
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<ul class="pagination">(.+?)div id="footer">'  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent3 = aResult[1][0]

        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
        aResult = oParser.parse(sHtmlContent3, sPattern)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
                if 'موقع' in aEntry[1]:
                    continue
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                if siteUrl.startswith('/'):
                    siteUrl = URL_MAIN + siteUrl
                if siteUrl.startswith('//'):
                    siteUrl = 'http:' + siteUrl
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
  
    oGui.setEndOfDirectory()

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern =  "PGlmcmFt(.+?)'"
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            m3url = "PGlmcmFt" + aEntry
            sHtmlContent2 = base64.b64decode(m3url)
   
            sPattern = 'src="(.+?)".+?allowfullscreen'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
        
                   url = aEntry.replace("https://dai.ly/","https://www.dailymotion.com/video/")
                   sTitle = " " 
                   if url.startswith('//'):
                       url = 'http:' + url
            
                   sHosterUrl = url 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       sDisplayTitle = sMovieTitle+sTitle
                       oHoster.setDisplayName(sDisplayTitle)
                       oHoster.setFileName(sDisplayTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
                
    oGui.setEndOfDirectory()