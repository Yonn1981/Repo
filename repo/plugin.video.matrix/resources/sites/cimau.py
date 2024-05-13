# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'cimau'
SITE_NAME = 'Cima4u'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'category/movies-1/افلام-اجنبي-2/', 'showMovies')
MOVIE_AR = (URL_MAIN + 'category/movies-1/افلام-عربى-2/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/movies-1/افلام-هندى-2/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/movies-1/افلام-تركى-2/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/movies-1/افلام-كرتون-2/', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')

RAMADAN_SERIES = (URL_MAIN + 'category/مسلسلات-رمضان-2024-2/', 'showSeries')
SERIE_TR = (URL_MAIN + 'category/series-1/مسلسلات-تركية-2/', 'showSeries')
SERIE_EN = (URL_MAIN + 'category/series-1/مسلسلات-اجنبي-2/', 'showSeries')
SERIE_AR = (URL_MAIN + 'category/series-1/مسلسلات-عربية-2/', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category/series-1/مسلسلات-هندية-2/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/series-1/مسلسلات-اسيوية-2/', 'showSeries')

ANIM_NEWS = (URL_MAIN + 'category/series-1/مسلسلات-كرتون-2/', 'showSeries')
REPLAYTV_NEWS = (URL_MAIN + 'category/other/برامج-تليفزيونية-2/', 'showSeries')
SPORT_WWE = (URL_MAIN + 'category/other/مصارعة-حرة-2/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', 'rmdn.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)

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
 
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيون', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
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
    sEnd = '</ul>\s*</div>'
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
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            if 'series' in siteUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', sTitle, 'mslsl.png', '', '', oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, 'film.png', '', '', oOutputParameterHandler)
 
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

    sPattern = '<li class="MovieBlock">\s*<a href="([^"]+)".+?data-image="([^"]+)".+?class="Category">.+?</div>([^<]+)</div>'
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

    else:
        sPattern = '<li class="MovieBlock">\s*<a href="([^"]+)".+?<div.+?image:url([^<]+);">.+?class="Category">.+?</div>\s*</div>([^<]+)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
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
            siteUrl = aEntry[0].replace('"',"").replace('/page/',"/?page=")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)

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

    sPattern = '<li class="MovieBlock">\s*<a href="([^"]+)".+?data-image="([^"]+)".+?class="Category">.+?</div>([^<]+)</div>'
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
            siteUrl = aEntry[0].replace('"',"").replace('/page/',"/?page=")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showTag', sTitle, 'next.png', oOutputParameterHandler)

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

    sStart = '<div class="PageContent">'
    sEnd = '</ul>'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li class="MovieBlock">\s*<a href="([^"]+)".+?data-image="([^"]+)".+?class="Category">.+?</div>([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent1, sPattern)  
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

    else:
        sPattern = '<li class="MovieBlock">\s*<a href="([^"]+)".+?<div.+?image:url([^<]+);">.+?class="Category">.+?</div>\s*</div>([^<]+)</div>'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
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
            siteUrl = aEntry[0].replace('"',"").replace('/page/',"/?page=")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

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
    
    sStart = 'class="EpisodesList"'
    sEnd = '<div class'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)<em>([^<]+)</em>'
    aResult = oParser.parse(sHtmlContent1, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sEp = aEntry[2]
            sTitle = f'{sMovieTitle} E{sEp}'           
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''

            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("حلقة "," E").replace("الموسم","S").replace("S ","S")
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    else:
        sPattern = 'itemprop="name">([^<]+)</h1>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sTitle = aResult[1][0].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثانى","S2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")

        oOutputParameterHandler = cOutputParameterHandler() 
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    mov_name_match = re.search(r'name="mov_name" value="(.*?)"', sHtmlContent)
    mov_url_match = re.search(r'name="mov_url" value="(.*?)"', sHtmlContent)
    submit_match = re.search(r'type="submit" value="(.*?)"', sHtmlContent)
    action_url_match = re.search(r'<form action="(.*?)"', sHtmlContent)

    if mov_name_match:
        mov_name = mov_name_match.group(1)

    if mov_url_match:
        mov_url = mov_url_match.group(1)

    if submit_match:
        submit = submit_match.group(1)

    if action_url_match:
        murl = action_url_match.group(1)

    tmp_url = base64.b64decode(mov_url).decode('utf8',errors='ignore')

    oRequestHandler = cRequestHandler(murl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Origin', getHost(sUrl))
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addParameters('mov_name', mov_name)
    oRequestHandler.addParameters('mov_url', mov_url)
    oRequestHandler.addParameters('submit', submit)
    sHtmlContent = oRequestHandler.request()

    #sLinks = sHtmlContent["watch"]
    sLinks = re.findall(r'data-value="(.*?)"', sHtmlContent)
    for link in sLinks:
        sHosterUrl = link
        sDisplayTitle = sMovieTitle + get_resolution_label(link) 

        if 'userload' in sHosterUrl:
            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
        if 'streamtape' in sHosterUrl:
            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
        if 'mystream' in sHosterUrl:
            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
        
        if 'mp4' in sHosterUrl:
            sHosterUrl = sHosterUrl + '|User-Agent=' + UA + '&Referer=' + sUrl
            oHoster = cHosterGui().getHoster('lien_direct')
        else:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
     
    oGui.setEndOfDirectory()  

def get_resolution_label(link):
    match = re.search(r"\b(?:240p|360p|480p|720p|1080p|2060p)\b", link, flags=re.IGNORECASE)
    if match:
        resolution = match.group(0).lower()
        if resolution == "2060p":
            return "4k (2060p)"
        elif resolution == "1080p":
            return "Full HD (1080p)"
        elif resolution == "720p":
            return "HD (720p)"
        elif resolution == "480p":
            return "SD (480p)"
        elif resolution == "360p":
            return "Low (360p)"
        elif resolution == "240p":
            return "Mobile (240p)"
        
    return "Unknown"

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a class="next page-numbers" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False

def getHost(url):
    parts = url.split('//', 1)
    host = parts[0] + '//' + parts[1].split('/', 1)[0]
    return host