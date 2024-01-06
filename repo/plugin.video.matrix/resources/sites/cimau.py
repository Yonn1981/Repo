# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import base64
import requests
from requests.compat import urlparse
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.multihost import cVidsrcto, cVidsrcnet
 
SITE_IDENTIFIER = 'cimau'
SITE_NAME = 'Cima4u'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


MOVIE_EN = (URL_MAIN + '/category/افلام-اجنبي-movies7-english/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/arabic-movies/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/indian-movies/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/افلام-اجنبي-movies7-english/asian-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/movies-anime/', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + '/category/افلام-اجنبي-movies7-english/netflix-movie/', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')

RAMADAN_SERIES = (URL_MAIN + '/category/series/مسلسلات-رمضان-2023/', 'showSeries')
SERIE_TR = (URL_MAIN + '/category/series/مسلسلات-تركية-series1-turkish/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/series/مسلسلات-اجنبي-english/', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/series/مسلسلات-عربية-arabic-series/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/series/مسلسلات-اسيوية-series1-asian/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/series/مسلسلات-هندية-series-indian/', 'showSeries')
SERIE_LATIN = (URL_MAIN + '/category/series/latino-mexico/', 'showSeries')
SERIE_NETFLIX = (URL_MAIN + '/category/series/series-netflix/', 'showSeries')

WWE = (URL_MAIN + '/category/اخرى-1other/wwe/', 'showSeries')
PROGRAMS = (URL_MAIN + '/category/series/برامج-تليفزيونية-tv1-shows/', 'showSeries')

SERIE_ANIME = (URL_MAIN + '/category/series/مسلسلات-كرتون-anime-series/', 'showSeries')
URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'anim.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler) 
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مكسيكي', 'latin.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', PROGRAMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيون', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام Netflix', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netflix', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '>الرئيسية</a>'
    sEnd = '</ul></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'اخري' in aEntry[1]:
                continue 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sDesc = ''
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            if 'series' in siteUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', sTitle, 'mslsl.png', '', '', oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'film.png', '', '', oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
			
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

    sStart = 'class="PageContent">'
    sEnd = '<script'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd) 

    sPattern = '<li class="MovieBlock"><a href="([^<]+)"><div.+?image:url([^<]+);"></div>.+?</div></div>([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("ومترجمه","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if "سلسلة"  in sTitle or "جميع"  in sTitle:
                oGui.addDir(SITE_IDENTIFIER, 'showTag', sTitle, '', oOutputParameterHandler)
            else:         
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = 'page-numbers" href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]           
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()


def showTag():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
            
    sPattern =  '<a href="([^<]+)"><div class="WatchingArea Hoverable">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    sPattern = '<li class="MovieBlock"><a href="([^<]+)"><div.+?image:url([^<]+);"></div>.+?</div></div>([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if "سلسلة"  in sTitle or "جميع"  in sTitle:
                oGui.addDir(SITE_IDENTIFIER, 'showTag', sTitle, '', oOutputParameterHandler)
            else:         
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<title>([^<]+)</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        sDisplay = aResult[1][0]

    oParser = cParser()
    sStart = 'class="SeasonsSections"'
    sEnd = 'class="WatchSectionContainer"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = "href='(.+?)'>(.+?)</a>"
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("الجزء الأول","Part 1").replace("الجزء الاول","Part 1").replace("الجزء الثانى","Part 2").replace("الجزء الثاني","Part 2").replace("الجزء الثالث","Part 3").replace("الجزء الثالث","Part 3").replace("الجزء الرابع","Part 4").replace("الجزء الخامس","Part 5").replace("الجزء السادس","Part 6").replace("الجزء السابع","Part 7").replace("الجزء الثامن","Part 8").replace("الجزء التاسع","Part 9").replace("الجزء","Part ").replace('مترجم','').replace('ومدبلجة','مدبلجة')
            sTitle = sTitle + ' ' + sDisplay.replace('سلسلة','').replace('افلام','').replace('أفلام','').replace('مترجم','')
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = 'page-numbers" href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0].replace('"',"")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showTag', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
		
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
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<li class="MovieBlock"><a href="([^<]+)"><div.+?image:url([^<]+);"></div>.+?</div></div>([^<]+)</div>'
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
 
            sTitle = aEntry[2].replace("&#8217;","'").replace("مشاهدة","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("أنمي","").replace("كاملة","").replace("كامل","").replace("مترجم","").replace("فيلم","").replace("برنامج","").replace("برنامج","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ""
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("موسم","S").replace("S ","S").split('حلقة')[0].split('حلقه')[0]

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                if "حفلات"  in sTitle or "جلسات"  in sTitle:
                    oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:         
                    oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = 'page-numbers" href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]           
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0].replace('"',"")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

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
    
    sDesc = ''

    sPattern = '<h2>القصة</h2><p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sDesc = aResult[1][0]
            
    sPattern =  '<a href="([^<]+)"><div class="WatchingArea Hoverable">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0] 
        if 'Episode'  in m3url: 
            m3url = aResult[1][0] 
            oRequest = cRequestHandler(m3url)
            sHtmlContent = oRequest.request()

            sPattern = '<a href="([^<]+)"><em>([^<]+)</em><span>([^<]+)</span></a></li>'
            aResult = oParser.parse(sHtmlContent, sPattern)	
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               for aEntry in aResult[1]:
 
                  if "مدبلج" in sMovieTitle:
                     sMovieTitle = sMovieTitle.replace("مدبلج","")
                     sMovieTitle = "مدبلج"+sMovieTitle
                  sTitle = sMovieTitle+' E'+ aEntry[2]
                  sUrl = aEntry[0]
                  sThumb = sThumb
                  sDesc = sDesc
			
                  oOutputParameterHandler.addParameter('siteUrl',sUrl)
                  oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                  oOutputParameterHandler.addParameter('sThumb', sThumb)
                  oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        else:
            oRequest = cRequestHandler(m3url)
            sHtmlContent = oRequest.request()

    sPattern = '<a href="" data-link="([^<]+)" class="sever_link"><img src="http://.+?/template/logo_server/1593281223_333.jpg" width="40" height="40" alt="" />([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]: 
        oOutputParameterHandler = cOutputParameterHandler()             
        for aEntry in aResult[1]: 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
         
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = ''

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<h2>القصة</h2><p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sDesc = aResult[1][0]
    
    sPattern = '<a href="([^<]+)"><div class="WatchingArea Hoverable">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        m3url = aResult[1][0]
        if '/tag/'  in m3url: 
            m3url = aResult[1][0] 
            oRequest = cRequestHandler(m3url)
            sData = oRequest.request()

            sPattern = '<li class="MovieBlock"><a href="([^<]+)">.+?style="background-image:url([^<]+);"></div>.+?</div></div>([^<]+)</div>'
            aResult = oParser.parse(sData, sPattern)
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()    
               for aEntry in aResult[1]:
 
                   sTitle = aEntry[2]
                   siteUrl = aEntry[0]
                   sThumb = aEntry[1].replace("(","").replace(")","")
                   sDesc = sDesc

                   sYear = ''
                   m = re.search('([0-9]{4})', sTitle)
                   if m:
                      sYear = str(m.group(0))
                      sTitle = sTitle.replace(sYear,'')
			
                   oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                   oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                   oOutputParameterHandler.addParameter('sThumb', sThumb)
                   oOutputParameterHandler.addParameter('sYear', sYear)
                   oOutputParameterHandler.addParameter('sDesc', sDesc)
                   oGui.addLink(SITE_IDENTIFIER, 'showLinks', sTitle, sThumb, sDesc, oOutputParameterHandler, oInputParameterHandler)
         
               sNextPage = __checkForNextPage(sHtmlContent)
               if sNextPage:
                  oOutputParameterHandler = cOutputParameterHandler()
                  oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                  oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
        else:
               oRequest = cRequestHandler(m3url)
               sHtmlContent = oRequest.request()
				           
    sPattern =  '<meta itemprop="embedURL" content="(.+?)" />' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
    
    sPattern =  'type="text/css" href="([^"]+)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m4url = aResult[1][0].split('styles')[0]

    sPattern = 'data-link="([^<]+)" class=".+?"><img.+?/>(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sPage = aEntry[0]
            sServer = aEntry[1].replace(' OK ','ok.ru').replace(' Goovid ','govid.me')
            serverUrl = m4url + 'structure/server.php?id='+sPage
            sDesc = sDesc

            oRequest = cRequestHandler(serverUrl)
            sDomain = oRequest.request()          

            sPattern2 = '<iframe.+?src="([^"]+)"'
            aResult = oParser.parse(sDomain, sPattern2)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                for aEntry in aResult[1]:
        
                    sHosterUrl = aEntry

                    if sHosterUrl.startswith('//'):
                       sHosterUrl = 'http:' + sHosterUrl

                    if 'vidsrc.to' in sHosterUrl:
                        sLabel = 'Vidsrc.to'
                        sDisplayTitle = ('%s [COLOR orange] [%s] [/COLOR]') % (sMovieTitle, sLabel)  
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        
                        oGui.addLink(SITE_IDENTIFIER, 'addHosters', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

                    if 'vidnow' in sHosterUrl or 'vidsrc.net' in sHosterUrl:
                        sLabel = 'Vidsrc.net'
                        sDisplayTitle = ('%s [COLOR orange] [%s] [/COLOR]') % (sMovieTitle, sLabel)  
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'addHosters', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

                    if 'autoembed' in sHosterUrl:
                        sLabel = 'autoembed'
                        sDisplayTitle = ('%s [COLOR orange] [%s] [/COLOR]') % (sMovieTitle, sLabel)  
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'addHosters', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

                    if 'autoembed' in sHosterUrl or 'vidsrc.to' in sHosterUrl or 'vidsrc.net' in sHosterUrl:
                        continue

                    if 'userload' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'streamtape' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
                                                 
                    oHoster = cHosterGui().checkHoster(sServer)
                    if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sPattern = 'href="([^<]+)" target="_blank" class="download_link">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
        
            url = aEntry

            if url.startswith('//'):
               url = 'http:' + url
				           
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'streamtape' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
     
    oGui.setEndOfDirectory()  

def addHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'vidsrc.to' in sHosterUrl:
        aResult = cVidsrcto().GetUrls(sHosterUrl)
        if (aResult):
            for aEntry in aResult:
                sHosterUrl = aEntry

                sDisplayTitle = sMovieTitle
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler) 

    if 'vidnow' in sHosterUrl or 'vidsrc.net' in sHosterUrl:
        aResult = cVidsrcnet().GetUrls(sHosterUrl)
        if (aResult):
            for aEntry in aResult:
                sHosterUrl = aEntry

                sDisplayTitle = sMovieTitle
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)     

    if "autoembed.to" in sHosterUrl:
        aembed = requests.get(sHosterUrl, headers={"Referer": sHosterUrl})
        aembed_list = re.findall(r'data-server="(.*?)"', aembed.text)
        for aEntry in aembed_list:
            aembed_list_decode = base64.b64decode(aEntry).decode('utf8',errors='ignore')
            if '2embed.me' in aembed_list_decode  or 'remotestre.am' in aembed_list_decode:
                sHosterUrl = aembed_list_decode

                sDisplayTitle = sMovieTitle
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)  

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a class="next page-numbers" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False