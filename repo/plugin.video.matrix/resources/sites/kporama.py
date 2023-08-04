# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager


SITE_IDENTIFIER = 'kporama'
SITE_NAME = 'Kporama'
SITE_DESC = 'Asian Movies and TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_ASIAN = (URL_MAIN + 'movies/', 'showMovies')

MOVIE_KR = (URL_MAIN + 'app/category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%83%d9%88%d8%b1%d9%8a%d8%a91/', 'showMovies')
MOVIE_CN = (URL_MAIN  +'app/category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%b5%d9%8a%d9%86%d9%8a%d8%a91/', 'showMovies')
MOVIE_JP = (URL_MAIN  +'app/category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%8a%d8%a7%d8%a8%d8%a7%d9%86%d9%8a%d8%a91/', 'showMovies')

SERIE_KR = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d9%88%d8%b1%d9%8a%d8%a91/', 'showSeries')
SERIE_CN = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b5%d9%8a%d9%86%d9%8a%d8%a91/', 'showSeries')
SERIE_JP = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%8a%d8%a7%d8%a8%d8%a7%d9%86%d9%8a%d8%a91/', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a8%d8%b1%d8%a7%d9%85%d8%ac-%d8%aa%d9%84%d9%8a%d9%81%d8%b2%d9%8a%d9%88%d9%86%d9%8a%d8%a91/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeriesResult')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showSeriesResult')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeriesResult')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showSeriesResult')
FUNCTION_SEARCH = 'showSeriesResult'
WhiteList = ('افلام','مسلسلات','برامج','اطفال','رمضان','انمي','كرتون','كارتون')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'Search Series', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', 'Search All', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'أفلام آسيوية', 'asia.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_KR[1], 'أفلام كورية', 'kr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CN[1], 'أفلام صينية', 'cn.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_JP[1], 'أفلام يابانية', 'jp.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], 'مسلسلات كورية', 'kr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CN[1], 'مسلسلات صينية', 'cn.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_JP[1], 'مسلسلات يابانية', 'jp.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_PLAY[1], 'برامج ترفيهية', 'brmg.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeriesResult(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui() 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeriesResult(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeriesResult(sUrl)
        oGui.setEndOfDirectory()
        return  
		
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch 
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 
        
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<li class="TPostMv">.+?href="([^"]+)".+?title="([^"]+)" data-lazy-src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            siteUrl = aEntry[0]
            sTitle = aEntry[1].replace("مترجم","").replace("مدبلج","").replace("فيلم","").split("/")[0]
            sYear = ''
            sThumb = re.sub(r'-\d*x\d*.','.', aEntry[2])
        
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb.replace('"','')

            sDesc = ''

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
        
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)   
    

        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeriesResult(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
            
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<li class="TPostMv">.+?href="([^"]+)".+?src="([^"]+)".+?title="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            siteUrl = aEntry[0]
            sTitle = aEntry[2].replace("مترجم","").replace("مدبلج","").replace("مسلسل","").split("/")[0]
            sYear = ''        
            sThumb = re.sub(r'-\d*x\d*.','.', aEntry[1])        
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
           
            sDesc = ''

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
        
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)   
    
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesResult', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
            
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<li class="TPostMv">.+?href="([^"]+)".+?title="([^"]+)" data-lazy-src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            siteUrl = aEntry[0]
            sTitle = aEntry[1].replace("مترجم","").replace("مدبلج","").replace("مسلسل","").split("/")[0]
            sYear = ''        
            sThumb = re.sub(r'-\d*x\d*.','.', aEntry[2])        
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
           
            sDesc = ''

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
        
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)   
    
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')   
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = 'class="MvTbTtl"><a href="([^"]+)">(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:

            siteUrl = aEntry[0]
            sTitle =  aEntry[1].replace("الحلقة ","E").replace("الحلقة","E").replace("الحلقه ","E").replace("الحلقه","E").replace("END","").replace("والاخيرة","").replace("والأخيرة","").strip()

            sTitle = sMovieTitle + sTitle
            sYear = ''           
            sThumb = sThumb           
            sDesc = ''

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle )
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^"]+)'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    ## Watch Servers
    oParser = cParser()
    sPattern = 'data-tplayernv="(.+?)"><span>(.+?)</span><span>(.+?)</span>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sValue = aEntry[0]
            sQual = aEntry[2].replace('مترجم','').replace('-','').strip()
            sHost = aEntry[1].replace("🌟","").strip()
        
            cook = oRequestHandler.GetCookies()

            sPattern = '<div class="TPlayerTb.+?id="'+sValue+'".+?value="([^"]+)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                for aEntry in aResult[1]:
                    aURL = aEntry
                    sThumb = sThumb
                
                    oRequestHandler = cRequestHandler(aURL)
                    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('authority', 'post.keeparab.com'.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1'.encode('utf-8'))

                    sHtmlContent2 = oRequestHandler.request()
                    sHtmlContent2 = sHtmlContent2.encode("utf-8",errors='ignore').decode("unicode_escape")
                
                    sPattern = '<iframe.+?src="([^"]+)'
                    oParser = cParser()
                    aResult = oParser.parse(sHtmlContent2, sPattern)
                    if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    url = aEntry
                                    sHosterUrl = url

                                    sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sQual)
                                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                                    if oHoster:
                                        sDisplayTitle = sTitle
                                        oHoster.setDisplayName(sDisplayTitle)
                                        oHoster.setFileName(sMovieTitle)
                                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    ## Download Servers
    sPattern = '<a rel="nofollow" target="_blank" href="([^"]+)".+?</noscript>.+?<span>(.+?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry[0]
                        qual = aEntry[1].replace("HD","").replace("SD","").replace("(","").replace(")","").strip()
                        sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, qual)
                        if url.startswith('//'):
                            url = 'http:' + url
				            
                        sHosterUrl = url 
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
        
    oGui.setEndOfDirectory()