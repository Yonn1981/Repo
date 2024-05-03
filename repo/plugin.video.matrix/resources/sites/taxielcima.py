# -*- coding: utf-8 -*-
# Checking the site ...

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.multihost import cMegamax
 
SITE_IDENTIFIER = 'taxielcima'
SITE_NAME = 'TaxiElCima'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'افلام-اجنبي/', 'showMovies')
MOVIE_AR = (URL_MAIN + 'افلام-عربي/', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + 'افلام-مدبلجة/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'افلام-هندي/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'افلام-اسيوية/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'افلام-تركي/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'أفلام-انيميشن/', 'showMovies')

SERIE_TR = (URL_MAIN + 'مسلسلات-تركية/', 'showSeries')
SERIE_TR_AR = (URL_MAIN + 'مسلسلات-تركي-مدبلجة/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'مسلسلات-اسيوية/', 'showSeries')
SERIE_HEND = (URL_MAIN + 'مسلسلات-هندية/', 'showSeries')
SERIE_EN = (URL_MAIN + 'مسلسلات-اجنبي/', 'showSeries')
SERIE_AR = (URL_MAIN + 'مسلسلات-عربية/', 'showSeries')

SPORT_WWE = (URL_MAIN + 'عروض-المصارعة/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'مسلسلات-انمي/', 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + 'عروض-تليفزيونية/', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
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

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s='+sSearchText+'+%D9%81%D9%8A%D9%84%D9%85'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s='+sSearchText+'+%D9%85%D8%B3%D9%84%D8%B3%D9%84'
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
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="SMallBloca".+?<a href="([^"]+)" title="([^"]+)".+?img src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'مسلسل' in aEntry[1] or 'موسم' in aEntry[1]:
               continue

            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            siteUrl = aEntry[0] + 'watch/'
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                if 'عرض' in sTitle:
                    sTitle = sTitle.replace('عرض','')
                else:
                    sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)

    sStart = 'class="page-numbers'
    sEnd = '<div class='
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)

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
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="SMallBloca".+?<a href="([^"]+)" title="([^"]+)".+?img src="([^"]+)'
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
            if 'فيلم' in aEntry[1] or 'فلم' in aEntry[1]:
               continue

            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace(" والأخيرة","").replace("اونا","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","").replace("الموسم الحادي عشر","").replace("الموسم الثاني عشر","").replace("الموسم الثالث عشر","").replace("الموسم الرابع عشر","").replace("الموسم الخامس عشر","").replace("الموسم السادس عشر","").replace("الموسم السابع عشر","").replace("الموسم الثامن عشر","").replace("الموسم التاسع عشر","").replace("الموسم العشرون","").replace("الموسم الحادي و العشرون","").replace("الموسم الثاني و العشرون","").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","").replace("الموسم الخامس و العشرون","").replace("الموسم السادس والعشرون","").replace("الموسم السابع والعشرون","").replace("الموسم الثامن والعشرون","").replace("الموسم التاسع والعشرون","").replace("الموسم الثلاثون","").replace("الموسم الحادي و الثلاثون","").replace("الموسم الثاني والثلاثون","").replace("الموسم الاول","").replace("الموسم الثاني","").replace("الموسم الثالث","").replace("الموسم الثالث","").replace("الموسم الرابع","").replace("الموسم الخامس","").replace("الموسم السادس","").replace("الموسم السابع","").replace("الموسم الثامن","").replace("الموسم التاسع","").replace("الموسم","").replace("موسم","").replace("S ","").replace("الحلقة","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("10","").replace("11","").replace("12","").replace("13","").replace("14","").replace("15","").replace("16","").replace("17","").replace("18","").replace("19","").replace("20","").replace("21","").replace("22","").replace("23","").replace("24","").replace("25","").replace("26","").replace("27","").replace("28","").replace("29","").replace("30","").replace("0","").replace("season","")

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle)	

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sStart = 'class="page-numbers'
    sEnd = '<div class='
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

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

	sStart = 'class="Seasons">'
	sEnd = 'class="container">'
	sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

	sPattern = 'href="([^"]+)" title="([^"]+)'
	aResult = oParser.parse(sHtmlContent, sPattern)	
	if aResult[0] is True:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
			sSeason = aEntry[1].split("موسم")[1]
			sTitle = f'{sMovieTitle} {sSeason.replace("العاشر","S10").replace("الحادي عشر","S11").replace("الثاني عشر","S12").replace("الثالث عشر","S13").replace("الرابع عشر","S14").replace("الخامس عشر","S15").replace("السادس عشر","S16").replace("السابع عشر","S17").replace("الثامن عشر","S18").replace("التاسع عشر","S19").replace("العشرون","S20").replace("الحادي و العشرون","S21").replace("الثاني و العشرون","S22").replace("الثالث و العشرون","S23").replace("الرابع والعشرون","S24").replace("الخامس و العشرون","S25").replace("السادس والعشرون","S26").replace("السابع والعشرون","S27").replace("الثامن والعشرون","S28").replace("التاسع والعشرون","S29").replace("الثلاثون","S30").replace("الحادي و الثلاثون","S31").replace("الثاني والثلاثون","S32").replace("الاول","S1").replace("الثاني","S2").replace("الثالث","S3").replace("الثالث","S3").replace("الرابع","S4").replace("الخامس","S5").replace("السادس","S6").replace("السابع","S7").replace("الثامن","S8").replace("التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")}'
			siteUrl = aEntry[0]
			sThumb = sThumb
			sDesc = ""
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

	sPattern = '<div class="SMallBloca".+?href="([^"]+)".+?<span>(.+?)</span>'
	aResult = oParser.parse(sHtmlContent, sPattern)
	if aResult[0] is True:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = f'{sMovieTitle} E{aEntry[1]}'
			siteUrl = aEntry[0] + 'watch/'
			sThumb = sThumb
			sDesc = ""
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
             
    sPattern = 'data-url="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:           
            url = aEntry
            if url.startswith('//'):
               url = 'http:' + url
								
            sHosterUrl = url 
            if 'megamax' in sHosterUrl or 'tuktukcimamulti' in sHosterUrl:
                data = cMegamax().GetUrls(sHosterUrl)
                for item in data:
                    sHosterUrl = item.split(',')[0].split('=')[1]
                    sQual = item.split(',')[1].split('=')[1]
                    sLabel = item.split(',')[2].split('=')[1]

                    sDisplayTitle = ('%s [COLOR coral] [%s][/COLOR][COLOR orange] - %s[/COLOR]') % (sMovieTitle, sQual, sLabel)      
                    oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                    oOutputParameterHandler.addParameter('sQual', sQual)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)

                    oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

            if 'tuktukmulti' in sHosterUrl:
                continue
            if 'megamax' in sHosterUrl:
                continue
 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    sUrl = sUrl.replace('watch/','download/')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="serverA" href="([^"]+)">.+?class="fa fa-desktop"></i>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:           
            url = aEntry[0]
            sTitle = sMovieTitle+'('+aEntry[1]+')' 
            if url.startswith('//'):
               url = 'http:' + url
								
            sHosterUrl = url 
            if 'megamax' in sHosterUrl or 'tuktukcimamulti' in sHosterUrl:
                sHosterUrl = sHosterUrl.replace('download','iframe')
                data = cMegamax().GetUrls(sHosterUrl)
                for item in data:
                    sHosterUrl = item.split(',')[0].split('=')[1]
                    sQual = item.split(',')[1].split('=')[1]
                    sLabel = item.split(',')[2].split('=')[1]

                    sDisplayTitle = ('%s [COLOR coral] [%s][/COLOR][COLOR orange] - %s[/COLOR]') % (sMovieTitle, sQual, sLabel)      
                    oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                    oOutputParameterHandler.addParameter('sQual', sQual)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)

                    oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)
                    
            if 'megamax' in sHosterUrl:
               continue
            if 'tuktuk' in sHosterUrl:
               continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)	                     
				               
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sQual = oInputParameterHandler.getValue('sQual')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sDisplayTitle = ('%s [COLOR coral] [%s] [/COLOR]') % (sMovieTitle, sQual)   
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()