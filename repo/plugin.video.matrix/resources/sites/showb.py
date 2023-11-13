# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import base64
import requests
from urllib.parse import unquote, quote
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon

import sys, os, json
to_unicode = str
from urllib.parse import unquote

SITE_IDENTIFIER = 'showb'
SITE_NAME = 'ShowBox'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_4k = (URL_MAIN + 'movie?quality=4K&release_year=all&genre=all&rating=all', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')

DOC_NEWS = (URL_MAIN + 'movie?genre=7&quality=4K', 'showMovies')

URL_SEARCH_MOVIES = (URL_MAIN + '/filter?keyword=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4k[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' 4k أفلام', '4k.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?keyword='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def moviesGenres():
    oGui = cGui()
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="sidebar_subs_genre"'
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)" title="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sGenre = aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', f'https://www.showbox.media{aEntry[0]}&quality=4K') 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ','+')
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="flw-item">.+?quality">(.+?)</div>\s*<img src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2]
            sQual = f'[{aEntry[0]}]'
            siteUrl = showb_function(aEntry[3])
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            sDisplayTitle = f'{sTitle} {sQual}'

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  
 
def showLinks(oInputParameterHandler = False):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'share/' not in sUrl:
        sTitle = 'No resources Found'
        oGui.addText(SITE_IDENTIFIER, f'[COLOR red]{sTitle}[/COLOR]')
    else:
        Subtitle = subs_function(sMovieTitle)  
        share_key = sUrl.split('share/')[1]
        streams = requests.get(f'https://febbox.com/file/file_share_list?share_key={share_key}&pwd=').json()
        show_data = max(streams['data']['file_list'], key=lambda x: x['file_size'])

        quality_map = ['4k', '1080p%252B']
        for quality in quality_map:
            oOutputParameterHandler = cOutputParameterHandler()
            stream_url = f'https://febbox.com/hls/main/{show_data["oss_fid"]}.m3u8?q={quality}'
            sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, quality.replace('%252B',''))
            m3u8_response = requests.get(stream_url)
            if m3u8_response:
                url = stream_url


                oOutputParameterHandler.addParameter('siteUrl', url)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('Subtitle', Subtitle)

                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Subtitle = oInputParameterHandler.getValue('Subtitle')

    sHosterUrl = sUrl
    if Subtitle is not False:
        sHosterUrl = sUrl +'?sub.info='+Subtitle
    oHoster = cHosterGui().getHoster('febb') 
    if oHoster:
        sDisplayTitle = sMovieTitle
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="page-item active"><a class="page-link">(.+?)</a></li>.+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = 'https://www.showbox.media'+aResult[1][0][1]
        return sNextPage

    return False, 'none'

def showb_function(sURL):
    show_link = sURL
    show_id = show_link.split('/')[3]
    feb_box_result = requests.get(f'https://www.showbox.media/index/share_link?id={show_id}&type=1')
    feb_box_data = feb_box_result.json()
    feb_box_data = feb_box_data['data']['link']

    if feb_box_data:
        return feb_box_data
        
    return False, False

def subs_function(sSearchText):
    oParser = cParser()
    sSubtitle = ''
    sUrl = 'https://fmoviesz.to/filter?keyword='+sSearchText + '&type%5B%5D=movie&sort=most_relevance'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="poster"> <a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            sUrl = aResult[1][0]
            sUrl = f'https://fmoviesz.to{sUrl}' 

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<div class="watch".+?data-id="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    sId = aEntry
                    vrf = getVerid(sId)
                    sUrl = f'https://fmoviesz.to/ajax/episode/list/{sId}?vrf={vrf}'
                    oRequestHandler = cRequestHandler(sUrl)
                    sHtmlContent = oRequestHandler.request().replace('\\','')

                    sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
                    aResult = oParser.parse(sHtmlContent, sPattern)  
                    if aResult[0]:
                        for aEntry in aResult[1]:
                            sSubtitle = f'https://fmoviesz.to/ajax/episode/subtitles/{aEntry[0]}'

                    if sSubtitle:
                        return sSubtitle
        
    return False

def DecodeLink(mainurl):
	mainurl = mainurl.replace('_', '/').replace('-', '+')
	ab=mainurl[0:6]
	
	ab= 'hlPeNwkncH0fq9so'
	ab = '8z5Ag5wgagfsOuhz'
	
	ac= decode2(mainurl)
	
	link = dekoduj(ab,ac)
	link = unquote(link)
	return link

def dekoduj(r,o):

    t = []
    e = []
    n = 0
    a = ""
    for f in range(256): 
        e.append(f)

    for f in range(256):

        n = (n + e[f] + ord(r[f % len(r)])) % 256
        t = e[f]
        e[f] = e[n]
        e[n] = t

    f = 0
    n = 0
    for h in range(len(o)):
        f = f + 1
        n = (n + e[f % 256]) % 256
        if not f in e:
            f = 0
            t = e[f]
            e[f] = e[n]
            e[n] = t

            a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])
        else:
            t = e[f]
            e[f] = e[n]
            e[n] = t
            if sys.version_info >= (3,0,0):
                a += chr((o[h]) ^ e[(e[f] + e[n]) % 256])
            else:
                a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])

    return a

try:
	import string
	STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	CUSTOM_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

	ENCODE_TRANS = string.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
	DECODE_TRANS = string.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)
except:
	STANDARD_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	CUSTOM_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	
	
	ENCODE_TRANS = bytes.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
	DECODE_TRANS = bytes.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)

def encode2(input):
	return base64.b64encode(input).translate(ENCODE_TRANS)
def decode2(input):
	try:	
		xx= input.translate(DECODE_TRANS)
	except:
		xx= str(input).translate(DECODE_TRANS)
	return base64.b64decode(xx)

	
def endEN(t, n) :
    return t + n;

def rLMxL(t, n):
    return t < n;

def VHtgA (t, n) :
    return t % n;

def DxlFU(t, n) :
    return rLMxL(t, n);

def dec2(t, n) :
    o=[]
    s=[]
    u=0
    h=''
    for e in range(256):
        s.append(e)

    for e in range(256):
        u = endEN(u + s[e],ord(t[e % len(t)])) % 256
        o = s[e];
        s[e] = s[u];
        s[u] = o;
    e=0
    u=0
    c=0
    for c in range(len(n)):
        e = (e + 1) % 256
        o = s[e]
        u = VHtgA(u + s[e], 256)
        s[e] = s[u];
        s[u] = o;
        try:
            h += chr((n[c]) ^ s[(s[e] + s[u]) % 256]);
        except:
            h += chr(ord(n[c]) ^ s[(s[e] + s[u]) % 256]);
    return h

def getVerid(id):
    def convert_func(matchobj):
        m =  matchobj.group(0)

        if m <= 'Z':
            mx = 90
        else:
            mx = 122
        mx2 = ord( m)+ 13  
        if mx>=mx2:
            mx = mx2
        else:
            mx = mx2-26
        gg = chr(mx)
        return gg

    def but(t):
        o=''
        for s in range(len(t)):
            u = ord(t[s]) 
            if u==0:
                u=0
            else:
                if (s % 5 == 1 or s % 5 == 4):
                    u -= 2
                else:
                    if (s % 5 == 3):
                        u += 5;
                    else:
                        if s % 5 == 0 :
                            u -= 4;
                        else:
                            if s % 5 == 2 :
                                u -= 6
            o += chr(u) 
			
			
			
        if sys.version_info >= (3,0,0):
            o=o.encode('Latin_1')

        if sys.version_info >= (3,0,0):
            o=(o.decode('utf-8'))

        return o
    ab = 'DZmuZuXqa9O0z3b7' #####stare
    ab = 'MPPBJLgFwShfqIBx'
    ab = 'rzyKmquwICPaYFkU'
    ab = 'FWsfu0KQd9vxYGNB'
    ac = id
    hj = dec2(ab,ac) #

    if sys.version_info >= (3,0,0):
        hj=hj.encode('Latin_1')

    hj2 = encode2(hj)   

    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
    hj2 = re.sub("[a-zA-Z]", convert_func, hj2) 
    if sys.version_info >= (3,0,0):
        hj2=hj2.encode('Latin_1')
	
    hj2 = encode2(hj2)   
    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
		

    xc= but(hj2) 

    return xc
		
	