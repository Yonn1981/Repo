# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import isMatrix

try:        # python 2
    import htmlentitydefs
    import urllib
    import urlparse
except ImportError:     # python 3
    import html.entities as htmlentitydefs
    import urllib.parse as urllib
    urlparse = urllib

import unicodedata
import re
import string

# function util n'utilise pas xbmc, xbmcgui, xbmcaddon ect...
class cUtil:
    def CheckOrd(self, label):
        count = 0
        try:
            label = label.lower()
            label = label.strip()
            label = unicode(label, 'utf-8')
            label = unicodedata.normalize('NFKD', label).encode('ASCII', 'ignore')
            for i in label:
                count += ord(i)
        except:
            pass

        return count

    # str1 : les mots à rechercher
    # str2 : Liste des mots à comparer
    # percent : pourcentage de concordance, 75% = il faut au moins 3 mots sur 4
    # retourne True si pourcentage atteint
    def CheckOccurence(self, str1, str2, percent=75):
        str2 = self.CleanName(str2)
        nbOccurence = nbWord = 0
        list2 = str2.split(' ')   # Comparaison mot à mot
        for part in str1.split(' '):
            if len(part) == 1:    # Ignorer une seule lettre
                continue
            nbWord += 1           # nombre de mots au total
            if part in list2:
                nbOccurence += 1  # Nombre de mots correspondants

        if nbWord == 0:
            return False
        return 100*nbOccurence/nbWord >= percent

    def removeHtmlTags(self, sValue, sReplace=''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)

    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)
        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if iSeconds < 10:
            iSeconds = '0' + str(iSeconds)

        if iMinutes < 10:
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def formatUTF8(self, text):
        # test si nécessaire de convertir
        n2 = re.sub('[^a-zA-Z0-9 ]', '', text)
        if n2 != text:
            bMatrix = isMatrix()
            if not bMatrix:
                try:
                    # converti en unicode pour aider aux convertions
                    text = text.decode('utf8', 'ignore')    
                except Exception as e:
                    pass

            try:
                text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore')
            except Exception as e:
                pass

            if bMatrix:
                try:
                    text = text.decode('utf8', 'ignore')
                except Exception as e:
                    pass
        return text

    def unescape(self, text):
        # determine si conversion en unicode nécessaire        
        isStr = isinstance(text, str)

        def fixup(m):
            text = m.group(0)
            if text[:2] == '&#':
                # character reference
                if isStr:
                    if text[:3] == '&#x':
                        return chr(int(text[3:-1], 16))
                    else:
                        return chr(int(text[2:-1]))
                else:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
            else:
                # named entity
                if isStr:
                    text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
                else:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])

            return text  # leave as is

        return re.sub('&#?\w+;', fixup, text)

    def titleWatched(self, title):
        title = self.formatUTF8(title)

        # cherche la saison et episode puis les balises [color]titre[/color]
        # title, saison = self.getSaisonTitre(title)
        # title, episode = self.getEpisodeTitre(title)
        # supprimer les balises
        title = re.sub(r'\[.*\]|\(.*\)', r'', str(title))
        title = title.replace('VF', '').replace('VOSTFR', '').replace('FR', '')
        # title = re.sub(r'[0-9]+?', r'', str(title))
        title = title.replace('-', ' ')  # on garde un espace pour que Orient-express ne devienne pas Orientexpress pour la recherche tmdb
        title = title.replace('Season', '').replace('season', '').replace('Season', '').replace('Episode', '').replace('episode', '')
        title = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), ' ', title.lower())
        title = re.sub(' +', ' ', title) # vire espace double au milieu
        # title = QuotePlus(title)
        # title = title.decode('string-escape')
        return title

    def CleanName(self, name):

        name = Unquote(name)
        name = name.replace('%20', ' ')

        # on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', name)
        if m:
            annee = str(m.group(0))
            name = name.replace(annee, '')

        # Suppression des ponctuations
        name = re.sub("[\’\'\-\–\:\+\._]", ' ', name)
        name = re.sub("[\,\&\?\!]", '', name)

        # vire tag
        name = re.sub('[\(\[].+?[\)\]]', '', name)
        name = name.replace('[', '').replace(']', '') # crochet orphelin

        # enlève les accents, si nécessaire
        name = self.formatUTF8(name)

        # tout en minuscule
        name = name.lower()
        # vire espace debut et fin
        name = name.strip()
        # vire espace double au milieu
        name = re.sub(' +', ' ', name)

        # on remet l'annee
        if annee:
            name = name + ' ' + annee

        return name

    def CleanMovieName(self, name):
        name = name.replace("مشاهدة وتحميل","").replace("مشاهدة","").replace("مسلسل","").replace("الانمي","").replace("انمي","").replace("أنمي","").replace("أنمى","").replace("مترجم عربي","")\
            .replace("مترجمة","").replace("مترجم","").replace("الفيلم"," ").replace("الفلم"," ").replace("فلم"," ").replace("فيلم","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","")\
            .replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","")\
            .replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("انيمي","")\
            .replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("بلوراي","")\
            .replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","")\
            .replace("الاخيرة","").replace("Arabic","مدبلج").replace("كاملة","").replace("حلقات كاملة","").replace("مباشرة","").replace("انتاج ","")\
            .replace("جودة عالية","").replace("كامل","").replace("السلسلة الوثائقية","").replace("الوثائقي","").replace("عرض","").replace("الرو","")\
            .replace("جميع حلقات","").replace("سلسلة افلام","").replace("سلسلة اجزاء","").replace("تحميل","").replace("مشاهده","").replace("مباشره","")\
            .replace('للعربية','').replace('للعربي','').replace('اونلاين','').replace('أونلاين','').replace('اون لاين','').replace('أون لاين','').replace('اولاين','')\
            .replace("المسلسل العائلي","").replace("كرتون","")
        
        year = ''
        m = re.search('([0-9]{4})', name)
        if m:
            year = str(m.group(0))
            name = name.replace(year, '')

        if name == '':
            try:
                name = year
            except:
                name = name

        name = name.strip()
        return name

    def CleanSeriesName(self, name):
        name = name.replace("مشاهدة وتحميل","").replace("مشاهدة","").replace("المسلسل الباكستاني","").replace("مسلسل باكستاني","").replace("مسلسل","").replace("الانمي","").replace("انمي","").replace("مترجم عربي","")\
            .replace("مترجمة","").replace("مترجم","").replace("الفيلم"," ").replace("الفلم"," ").replace("فلم"," ").replace("فيلم","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","")\
            .replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","")\
            .replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("انيمي","")\
            .replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("بلوراي","")\
            .replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","")\
            .replace("الاخيرة","").replace("Arabic","مدبلج").replace("كاملة","").replace("حلقات كاملة","").replace("مباشرة","").replace("انتاج ","")\
            .replace("جودة عالية","").replace("كامل","").replace("السلسلة الوثائقية","").replace("الوثائقي","").replace("عرض","").replace("الرو","")\
            .replace("جميع حلقات","").replace("سلسلة افلام","").replace("سلسلة اجزاء","").replace("تحميل","").replace("مشاهده","").replace("مباشره","")\
            .replace('للعربية','').replace('للعربي','').replace('اونلاين','').replace('أونلاين','').replace('اون لاين','').replace('أون لاين','').replace('اولاين','')\
            .replace("المسلسل العائلي","").replace("تقرير","").replace("+","").replace("حلقات","").replace("الحلقات","").replace(" ة "," ").replace("القصير","")\
            .replace('جميع مواسم','')
               
        name = self.ConvertSeasons(name)
        
        try:
            name = name.split('الحلقه')[0].split('الحلقة')[0].split('حلقة')[0]
        except:
            name = name

        try:
            name = name.split('الموسم')[0].split('موسم')[0]
        except:
            name = name

        year = ''
        m = re.search('([0-9]{4})', name)
        if m:
            year = str(m.group(0))
            name = name.replace(year, '')

        name = name.strip()
        if name == '':
            try:
                name = year
            except:
                name = name

        return name

    # Convert Seasons Arabic Names
    def ConvertSeasons(self, name):
            name = name.replace("الجزء","الموسم").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13")\
            .replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17")\
            .replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21")\
            .replace("الموسم الحادي والعشرون","S21").replace("الموسم الثاني والعشرون","S22").replace("الموسم الثاني و العشرون","S22")\
            .replace("الموسم الثالث و العشرون","S23").replace("الموسم الثالث والعشرون","S23").replace("الموسم الرابع و العشرون","S24")\
            .replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم الخامس والعشرون","S25")\
            .replace("الموسم السادس و العشرون","S26").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27")\
            .replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن و العشرون","S28").replace("الموسم الثامن والعشرون","S28")\
            .replace("الموسم التاسع و العشرون","S29").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30")\
            .replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الحادي والثلاثون","S31").replace("الموسم الثاني و الثلاثون","S32")\
            .replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث والثلاثون","S33").replace("الموسم الثالث والثلاثون","S33")\
            .replace("الموسم الرابع والثلاثون","S34").replace("الموسم الرابع و الثلاثون","S34").replace("الموسم الخامس و الثلاثون","S35")\
            .replace("الموسم الخامس والثلاثون","S35").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثانى","S2").replace("الموسم الثالث","S3")\
            .replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7")\
            .replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").replace("مترجم","").replace("مترجمة","").replace(" الحادي عشر","11")\
            .replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16")\
            .replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21")\
            .replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25")\
            .replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29")\
            .replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2")\
            .replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7")\
            .replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10")

            return name

    def getSerieTitre(self, sTitle):
        serieTitle = re.sub(r'\[.*\]|\(.*\)', r'', sTitle)
        serieTitle = re.sub('[- –]+$', '', serieTitle)

        if '|' in serieTitle:
            serieTitle = serieTitle[:serieTitle.index('|')]

        return serieTitle

    def getEpisodeTitre(self, sTitle):
        string = re.search('(?i)(e(?:[a-z]+sode\s?)*([0-9]+))', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(1), '')
            return sTitle, True

        return sTitle, False

    def EvalJSString(self, s):
        s = s.replace(' ', '')
        try:
            s = s.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0')
            s = re.sub(r'(\([^()]+)\+\[\]\)', '(\\1)*10)', s)  # si le bloc fini par +[] >> *10
            s = re.sub(r'\[([^\]]+)\]', 'str(\\1)', s)
            if s[0] == '+':
                s = s[1:]
            val = int(eval(s))
            return val
        except:
            return 0


"""
# ***********************
# Fonctions lights
# ***********************
# Pour les avoirs
# from resources.lib import util
# puis util.Unquote('test')
"""


def Unquote(sUrl):
    return urllib.unquote(sUrl)


def Quote(sUrl):
    return urllib.quote(sUrl)


def UnquotePlus(sUrl):
    return urllib.unquote_plus(sUrl)


def QuotePlus(sUrl):
    return urllib.quote_plus(sUrl)


def QuoteSafe(sUrl):
    return urllib.quote(sUrl, safe=':/')


def urlEncode(sUrl):
    return urllib.urlencode(sUrl)


def urlHostName(sUrl):  # retourne le hostname d'une Url
    return urlparse.urlparse(sUrl).hostname
