# -*- coding: utf-8 -*-

import re, requests
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'cimaclub'
SITE_NAME = 'CimaClub'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
 
MOVIE_FAM = (URL_MAIN + 'getposts?genre=14&category=2', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'getposts?category=2&data=rating', 'showMovies')
MOVIE_EN = (URL_MAIN + 'category/افلام-اجنبى-aflam-onilne20', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/افلام-هندي', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/افلام-اسيوية-اونلاين', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/أفلام-انيميشن-اونلاين-انمي', 'showMovies')

SERIE_HI = (URL_MAIN + 'category/مسلسلات-هندية', 'showSerie')
SERIE_KR = (URL_MAIN + 'category/مسلسلات-كوري4', 'showSerie')
SERIE_TR = (URL_MAIN + 'category/مسلسلات-تركية', 'showSerie')
SERIE_EN = (URL_MAIN + 'category/مسلسلات-اجنبية5', 'showSerie')

ANIM_NEWS = (URL_MAIN + 'category/مسلسلات-أنمي', 'showSerie')

URL_SEARCH = (URL_MAIN + 'search?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?s=', 'showSerie')
URL_SEARCH_MISC = (URL_MAIN + 'search?s=', 'showSerie')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', addons.VSlang(30330), 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
      
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)
      
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات هندية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], 'مسلسلات كورية', 'kr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات انمي', 'crtoon.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s='+sSearchText
        showSerie(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s='+sSearchText
        showSerie(sUrl)
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
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="content-box">.+?<a href="([^"]+)".+?data-src="([^"]+)".+?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("اونلاين","").replace("برنامج","").replace("بجودة","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج").replace("انيمي","")
            siteUrl = URL_MAIN + aEntry[0].replace('/film/','/watch/').replace('/post/','/watch/').replace('/movie/','/watch/')
            sThumb = aEntry[1].replace('(','').replace(')','')
            sDesc = ''
            sYear = ''
            m = re.search('([1-2][0-9]{3})', sTitle)
            if m:
                sYear = str(m.group(0))
                if 'عرض' in sTitle:
                    sTitle = sTitle.replace('عرض','')
                else:
                    sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    sPattern = 'class="page-link" href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = URL_MAIN + aEntry[0].replace('---','-–-')
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<div class="content-box">.+?<a href="([^"]+)".+?data-src="([^"]+)".+?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    itemList = []	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/series' in aEntry[0]:
                continue

            sTitle = aEntry[2].split('الحلقه')[0].split('الحلقة')[0].split('حلقة')[0].split('الموسم')[0].split('موسم')[0].replace("مشاهدة","").replace("مشاهده","").replace("مسلسل","").replace("انيمي","").replace("انمي","").replace("انمى","").replace("مترجمة","").replace("برنامج","").replace("مترجم","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مدبلج للعربية","مدبلج").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("انيمي","").replace("كامل","")  
            siteUrl = URL_MAIN + aEntry[0].replace("/episode/","/watch/").replace("/post/","/watch/").replace("/anime/","/watch/").replace('---','-–-')
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثانى","S2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").split('الحلقة')[0].replace("الاخيرة","").replace("مترجم","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10").replace("موسم"," S")

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle) 
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    sPattern = 'class="page-link" href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = URL_MAIN + aEntry[0].replace('---','-–-')
            sThumb = ""
            sDesc = ""

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', sTitle, '', oOutputParameterHandler)
         
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sStart = '<ul class="Seasons">'
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'data-season="([^"]+)" data-S="([^"]+)" data-B="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sSeason = aEntry[0]
            sTitle = f'{sMovieTitle} S{sSeason}'
            siteUrl = sUrl
            dataS = aEntry[1]
            dataB = aEntry[2]
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sSeason',sSeason)
            oOutputParameterHandler.addParameter('dataS',dataS)
            oOutputParameterHandler.addParameter('dataB',dataB)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
        sStart = '<ul class="Episodes'
        sEnd = '</div>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        aResult = re.findall('href="([^<]+)" title.+?<em>(.+?)</em>', sHtmlContent)
        if aResult:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult:
                sEp = aEntry[1]
                siteUrl = URL_MAIN + aEntry[0].replace("/episode/","/watch/").replace("/anime/","/watch/").replace("/post/","/watch/").replace('---','-–-')
                sTitle = f'{sMovieTitle} E{sEp}'
                sThumb = sThumb
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, '', oOutputParameterHandler)
        
            sNextPage = __checkForNextPage(sHtmlContent)
            if sNextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSeason = oInputParameterHandler.getValue('sSeason')
    dataS = oInputParameterHandler.getValue('dataS')
    dataB = oInputParameterHandler.getValue('dataB')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    s = requests.Session()            
    headers = {'user-agent': UA,
                        'referer': URL_MAIN,
                        'Accept': '*/*'}

    data = {'_action':'GetSeasonEp','_season':sSeason,'_S':dataS,'_B':dataB}
    r = s.get(f'{URL_MAIN}ajaxCenter?_action=GetSeasonEp&_season={sSeason}&_S={dataS}&_B={dataB}', headers=headers,data = data)
    sHtmlContent = r.text

    aResult = re.findall('href="([^<]+)" title.+?<em>(.+?)</em>', sHtmlContent)
    if aResult:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult:
            sEp = aEntry[1]
            siteUrl = URL_MAIN + aEntry[0].replace("/episode/","/watch/").replace("/anime/","/watch/").replace("/post/","/watch/").replace('---','-–-')
            sTitle = f'{sMovieTitle} E{sEp}'
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
		
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="page-link" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:       
        return URL_MAIN + aResult[1][0]

    return False
  
def showServers(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    sHtmlContent = oRequestHandler.request()

    sReferer = sUrl.split('/watch')[0]
    
    sPattern = 'data-embedd="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
					            
                    sHosterUrl = aEntry
                    if 'nowvid' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer
                    if 'kvid' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer    
                    if 'darkveed' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer 
                    if 'telvod' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + sReferer 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = sMovieTitle
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
       	
    sPattern = 'rel="nofollow" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url				
            
            sHosterUrl = url 
            if 'nowvid' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sReferer
            if 't7meel' in sHosterUrl:
                continue
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sReferer
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sReferer
            if 'darkveed' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sReferer 
            if 'telvod' in sHosterUrl or 'downvol' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sReferer  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    
    oGui.setEndOfDirectory()	