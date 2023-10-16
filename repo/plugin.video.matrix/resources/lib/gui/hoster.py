# -*- coding: utf-8 -*-

from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, VSlog
import re

class cHosterGui:
    SITE_NAME = 'cHosterGui'
    ADDON = addon()

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl=False, oInputParameterHandler=False):
        oHoster.setUrl(sMediaUrl)
        oOutputParameterHandler = cOutputParameterHandler()
        if not oInputParameterHandler:
            oInputParameterHandler = cInputParameterHandler()

        # Gestion NextUp
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        site = oInputParameterHandler.getValue('site')
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        sSeason = oInputParameterHandler.getValue('sSeason')
        sEpisode = oInputParameterHandler.getValue('sEpisode')
        nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        movieUrl = oInputParameterHandler.getValue('movieUrl')
        movieFunc = oInputParameterHandler.getValue('movieFunc')
        sLang = oInputParameterHandler.getValue('sLang')
        sRes = oInputParameterHandler.getValue('sRes')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        sFav = oInputParameterHandler.getValue('sFav')
        if not sFav:
            sFav = oInputParameterHandler.getValue('function')
        searchSiteId = oInputParameterHandler.getValue('searchSiteId')
        if searchSiteId:
            oOutputParameterHandler.addParameter('searchSiteId', searchSiteId)
        oOutputParameterHandler.addParameter('searchSiteName', oInputParameterHandler.getValue('searchSiteName'))
        oOutputParameterHandler.addParameter('sQual', oInputParameterHandler.getValue('sQual'))

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')


        # Catégorie de lecture
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat == '4':  # Si on vient de passer par un menu "Saison" ...
                sCat = '8'   # ...  On est maintenant au niveau "Episode"
        else:
            sCat = '5'     # Divers

        oGuiElement.setCat(sCat)
        oOutputParameterHandler.addParameter('sCat', sCat)

        if (oInputParameterHandler.exist('sMeta')):
            sMeta = oInputParameterHandler.getValue('sMeta')
            oGuiElement.setMeta(int(sMeta))

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        oGuiElement.setIcon('host.png')
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)

        sMediaFile = oHoster.getMediaFile()
        if sMediaFile:  # Afficher le nom du fichier plutot que le titre
            oGuiElement.setMediaUrl(sMediaFile)
            if self.ADDON.getSetting('display_info_file') == 'true':
                oHoster.setDisplayName(sMediaFile)
                oGuiElement.setTitle(oHoster.getFileName())  # permet de calculer le cleanTitle
                oGuiElement.setRawTitle(oHoster.getDisplayName())   # remplace le titre par le lien
            else:
                oGuiElement.setTitle(oHoster.getDisplayName())
        else:
            oGuiElement.setTitle(oHoster.getDisplayName())

        title = oGuiElement.getCleanTitle()
        tvShowTitle = oGuiElement.getItemValue('tvshowtitle')

        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        oOutputParameterHandler.addParameter('tvShowTitle', tvShowTitle)
        oOutputParameterHandler.addParameter('sTitle', title)
        oOutputParameterHandler.addParameter('sSeason', sSeason)
        oOutputParameterHandler.addParameter('sEpisode', sEpisode)
        oOutputParameterHandler.addParameter('sLang', sLang)
        oOutputParameterHandler.addParameter('sRes', sRes)
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

        # gestion NextUp
        oOutputParameterHandler.addParameter('sourceName', site)    # source d'origine
        oOutputParameterHandler.addParameter('sourceFav', sFav)    # source d'origine
        oOutputParameterHandler.addParameter('nextSaisonFunc', nextSaisonFunc)
        oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)

        # gestion Lecture en cours
        oOutputParameterHandler.addParameter('movieUrl', movieUrl)
        oOutputParameterHandler.addParameter('movieFunc', movieFunc)

        # Download menu
        if oHoster.isDownloadable():
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(self.ADDON.VSlang(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

            # Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(self.ADDON.VSlang(30326))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        # Liste de lecture
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(self.ADDON.VSlang(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        # Dossier Media
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))

        # Upload menu uptobox
        if cInputParameterHandler().getValue('site') != 'siteuptobox' and self.ADDON.getSetting('hoster_uptobox_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = ['uptobox', 'uptostream', '1fichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'upToMyAccount', self.ADDON.VSlang(30325))
                    break

        # onefichier
        if cInputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting('hoster_onefichier_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = '1fichier'  # les autres ne fonctionnent pas
            if host == accept:
                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteonefichier', 'siteonefichier', 'upToMyAccount', '1fichier')

        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)

    def checkHoster(self, sHosterUrl, debrid=True):
        # securite
        if not sHosterUrl:
            return False


        # Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        sHosterUrl = sHosterUrl.split('?')[0]
        sHosterUrl = sHosterUrl.lower()

        # Fix for mcloud and vidstream m3u8 direct links
        if ('mcloud' in sHosterUrl) or ('vizcloud' in sHosterUrl) or ('vidstream' in sHosterUrl) or ('vidplay' in sHosterUrl):
            return self.getHoster('mcloud')
 
        # Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl

        if debrid:
            # L'user a active l'url resolver ?
            if self.ADDON.getSetting('Userresolveurl') == 'true':
                import resolveurl
                hmf = resolveurl.HostedMediaFile(url=sHosterUrl)
                if hmf.valid_url():
                    tmp = self.getHoster('resolver')
                    RH = sHosterUrl.split('/')[2]
                    RH = RH.replace('www.', '')
                    tmp.setRealHost(RH.split('.')[0].upper())
                    return tmp



            # L'user a activé alldebrid ?
            if self.ADDON.getSetting('hoster_alldebrid_premium') == 'true':
                f = self.getHoster('alldebrid')
                #mise a jour du nom
                f.setRealHost(sHostName)
                return f
					
            # L'user a activé realbrid ?
            if self.ADDON.getSetting('hoster_realdebrid_premium') == 'true':
                f = self.getHoster('realdebrid')
                #mise a jour du nom
                f.setRealHost(sHostName)
                return f
					
            # L'user a activé debrid_link ?
            if self.ADDON.getSetting('hoster_debridlink_premium') == 'true':
                if "debrid.link" not in sHosterUrl:
                    return self.getHoster('debrid_link')
                else:
                    return self.getHoster("lien_direct")

                
        supported_player = ['film77', 'hdup', 'streamable', 'stardima', 'filescdn', 'vidgot', 'videott', 'vidlo', 'sendit', 'thevid', 'vidmoly', 'fastplay', 'cloudy', 'hibridvod', 'arabveturk', 'extremenow', 'yourupload', 'vidspeeds', 'moshahda', 'voe', 'faselhd', 'streamz', 'streamax', 'gounlimited', 'xdrive', 'facebook', 'mixdrop', 'mixloads', 'vidoza',
                            'rutube', 'megawatch', 'vidzi', 'filetrip', 'uptostream', 'speedvid', 'letsupload',
                            'onevideo', 'playreplay', 'prostream', 'vidfast', 'uqload', 'letwatch', 'wishfast',
                            'filepup', 'vimple', 'wstream', 'watchvideo', 'vidwatch', 'up2stream', 'tune', 'playtube',
                            'vidup', 'vidbull', 'vidlox', 'megaup', '33player' 'easyload', 'ninjastream', 'cloudhost',
                            'videobin', 'stagevu', 'gorillavid', 'daclips', 'hdvid', 'vshare', 'vidload',
                            'giga', 'vidbom', 'upvid', 'cloudvid', 'megadrive', 'downace', 'clickopen', 'supervideo',
                            'jawcloud', 'soundcloud', 'mixcloud', 'ddlfr', 'vupload', 'dwfull', 'vidzstore',
                            'pdj', 'rapidstream', 'jetload', 'dustreaming', 'viki', 'flix555', 'onlystream',
                            'upstream', 'pstream', 'vudeo', 'vidia', 'vidbem', 'uptobox', 'uplea', 'vido',
                            'sibnet', 'vidplayer', 'userload', 'aparat', 'evoload', 'vidshar', 'abcvideo', 'plynow', '33player', 'filerio', 'videoraj', 'brightcove', 'detectiveconanar',
                            'myvi', '33player', 'videovard', 'viewsb', 'yourvid', 'vf-manga', 'oneupload', 'darkibox']

        val = next((x for x in supported_player if x in sHostName), None)
        if val:
            return self.getHoster(val.replace('.', ''))

        # Gestion classique
        if ('vadshar' in sHostName) or ('vidshar' in sHostName) or ('vedshaar' in sHostName) or ('vedsharr' in sHostName) or ('vedshar' in sHostName) or ('vidshare' in sHostName) or ('viidshar' in sHostName):
            return self.getHoster('vidshare')

        if ('gettyshare' in sHosterUrl):
            return self.getHoster('gettyshare')

        if ('.aflam' in sHosterUrl):
            return self.getHoster('mixloads')

        if ('sbfull' in sHostName):
            return self.getHoster('viewsb')
        if ('sbrapid' in sHostName):
            return self.getHoster('viewsb')
        if ('sbbrisk' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        if ('videa' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        if ('streamwish' in sHostName) or ('khadhnayad' in sHostName) or ('ajmidyad' in sHostName) or ('yadmalik' in sHostName) or ('kharabnah' in sHostName) or ('hayaatieadhab' in sHostName):
            return self.getHoster('streamwish')
        if ('upstream' in sHosterUrl):
            return self.getHoster('upstream')
        if ('dooood' in sHostName):
            return self.getHoster('dood')
        if ('DoodStream' in sHostName) or ('flixeo' in sHostName):
            return self.getHoster('dood')
        if ('dood' in sHostName) or ('dood' in sHosterUrl):
            return self.getHoster('dood')
        if ('film77' in sHostName):
            return self.getHoster('film77')
        if ('vidguard' in sHostName) or ('fertoto' in sHostName) or ('vgembed' in sHostName) or ('vgfplay' in sHostName):
            return self.getHoster('vidguard')
        if ('filelions' in sHostName) or ('ajmidyadfihayh' in sHostName) or ('alhayabambi' in sHostName) or ('bazwatch' in sHostName) or ('cilootv' in sHostName) or ('motvy55' in sHostName):
            return self.getHoster('filelions')
        if ('vidello' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        if ('hadara.ps' in sHostName):
            return self.getHoster('lien_direct')        
        if ('highload' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        
        if ('embedsito' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('streamlare' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('vanfem' in sHostName):
            return self.getHoster('fembed')

        if ('vidtube' in sHostName) or ('vtbe' in sHostName):
            return self.getHoster('vidtube')

        if ('updown' in sHostName):
            return self.getHoster('updown')

        if ('vod540' in sHostName) or ('hd-cdn' in sHostName) or ('anyvid' in sHostName):
            return self.getHoster('xvideo')

        if ('vidsrc' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('segavid' in sHostName):
            return self.getHoster('arabveturk')

        if ('diasfem' in sHosterUrl):
            return self.getHoster('fembed')

        if ('vidpro' in sHostName):
            return self.getHoster('samashare')
        if ('streamvid' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        if ('vidcloud' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f        
        if ('sblanh' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        
        if ('sbchill' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        
        if ('sbthe' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        
        if ('sbbrisk' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
        
        if ('sbanh' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('streamtape' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('Streamtape')
            return f

        if ('sbhight' in sHostName):
            return self.getHoster('viewsb')
        
        if ('sbface' in sHostName):
            return self.getHoster('viewsb')
        
        if ('viewsb' in sHostName):
            return self.getHoster('viewsb')
        
        if ('tubeload' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('lanesh' in sHosterUrl):
            return self.getHoster('lanesh')

        if ('asiawiki' in sHostName):
            return self.getHoster('asiadtv')

        if ('asiatvplayer' in sHostName):
            return self.getHoster('asiadtv')

        if ('vimeo' in sHostName):
            return self.getHoster('vimeo')

        if ('rrsrrs' in sHostName):
            return self.getHoster('cimanow')

        if ('embed.scdn.' in sHostName):
            return self.getHoster('faselhd')
        
        if ('/run/' in sHosterUrl):
            return self.getHoster('mycima')
                 
        if ('megaupload.' in sHostName) or ('fansubs' in sHostName) or ('us.archive.' in sHostName) or ('ddsdd' in sHostName) or ('ffsff' in sHostName) or ('rrsrr' in sHostName)or ('fbcdn.net' in sHostName) or ('blogspot.com' in sHostName) or ('videodelivery' in sHostName) or ('bittube' in sHostName) or ('amazonaws.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('rumble' in sHostName):
            return self.getHoster('rumble')

        if ('file-upload' in sHostName):
            return self.getHoster('fileupload')

        if ('.googleusercontent.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('archive.org/download' in sHostName):
            return self.getHoster('lien_direct')

        if ('iptvtree' in sHostName):
            return self.getHoster('lien_direct')
        
        if ('ugeen' in sHostName):
            return self.getHoster('lien_direct')

        if ('ak-download' in sHostName):
            return self.getHoster('lien_direct')

        if ('nextcdn' in sHostName):
            return self.getHoster('lien_direct')

        if ('akwam' in sHostName) or ('onesav' in sHostName):
            return self.getHoster('lien_direct')
    

        if ('.vimeocdn.' in sHostName):
            return self.getHoster('lien_direct')

        if ('bokracdn' in sHostName):
            return self.getHoster('lien_direct')

        if ('akoams.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('gcdn' in sHostName):
            return self.getHoster('lien_direct')

        if ('alarabiya' in sHostName):
            return self.getHoster('lien_direct')

        if ('kingfoot' in sHostName):
            return self.getHoster('lien_direct')
            
        if ('vidbm' in sHostName) or ('vadbam' in sHostName) or ('vedbom' in sHostName) or ('vadbom' in sHostName) or ('vidbam' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
				
        if ('mail.ru' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
				
        if ('streamcherry' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
			
        if ('twitch' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
			
        if ('clicknupload' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('vidspeed' in sHostName):
            return self.getHoster('vidspeeds')
				
        if ('megaup.' in sHostName):
            return self.getHoster('megaup')

        if ('linkbox' in sHostName) or ('sharezweb' in sHostName):
            return self.getHoster('resolver')

        if ('vido' in sHostName):
            return self.getHoster('vudeo')
            
        if ('mediafire' in sHostName):
            return self.getHoster('mediafire')

        if ('workupload' in sHostName):
            return self.getHoster('workupload')

        if ('upbam' in sHostName) or ('uppom' in sHostName) or ('uppboom' in sHostName):
            return self.getHoster('uppom')

        if ('allviid' in sHostName):
            return self.getHoster('filemoon')

        if ('upbaam' in sHostName):
            f = self.getHoster('resolver')
            f.setRealHost('UpBaam')
            return f

        if ('filemoon' in sHostName) or ('moonmov' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('Filemoon')
            return f

        if ('hexupload' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('movembed' in sHostName) or ('sbnet' in sHosterUrl):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('rabbitstream' in sHostName) or ('dokicloud' in sHostName):
            return self.getHoster('streamrapid')

        if ('veehd.' in sHostName):
            return self.getHoster('veehd')

        if ('eeggyy' in sHosterUrl):
            return self.getHoster('egybest')

        if ('vidhls' in sHosterUrl):
            return self.getHoster('vidhls')

        if ('play.imovietime' in sHosterUrl):
            return self.getHoster('moviztime')

        if ('send.cm' in sHosterUrl):
            return self.getHoster('sendme')

        if ('shoffree' in sHostName) or ('egy-best' in sHostName):
            return self.getHoster('shoffree')

        if ('streamsforu' in sHostName or 'ylass' in sHostName or 'rsc.cdn' in sHostName or 'btolat' in sHostName):
            return self.getHoster('streamz')
				
        if ('archive.org/embed/"' in sHostName):
            return self.getHoster('archive')
				
        if (('anavids' in sHostName) or ('anavidz' in sHostName)):
            return self.getHoster('anavids')

        if ('guccihide' in sHostName) or ('streamhide' in sHostName) or ('fanakishtuna' in sHostName) or ('ahvsh' in sHostName) or ('animezd' in sHostName) or ('anime7u' in sHostName):
            return self.getHoster('streamhide')

        if (('anonfile' in sHostName) or ('govid.xyz' in sHostName) or ('file.bz' in sHostName) or ('myfile.is' in sHostName) or ('upload.st' in sHostName)):
            return self.getHoster('anonfile')

        if (('cloudvideo' in sHostName) or ('streamcloud' in sHostName) or ('userscloud' in sHostName)):
            return self.getHoster('cloudvid')
            
        if ('myviid' in sHostName) or ('myvid' in sHostName):
            return self.getHoster('myvid')

        if ('streamwire' in sHostName) or ('vup' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f
            
        if ('vidhd' in sHostName) or ('oktube' in sHostName):
            return self.getHoster('vidhd')
            
        if ('nowvid' in sHostName) or ('vegaasvid' in sHostName):
            return self.getHoster('govid')

        if ('skyvid' in sHostName) or ('gvadz' in sHostName):
            return self.getHoster('skyvid')
            
        if ('seeeed' in sHostName):
            return self.getHoster('arabseed')
            
        if ('reviewtech' in sHosterUrl) or ('reviewrate' in sHosterUrl):
            return self.getHoster('arabseed')

        if ('techradar' in sHostName) or ('albrq' in sHostName):
            return self.getHoster('filemoon')

        if ('4shared' in sHostName):
            return self.getHoster('shared')
				
        if ('fajer.live' in sHostName):
            return self.getHoster('fajerlive')
            
        if ('govad' in sHostName) or ('govid.me' in sHostName):
            return self.getHoster('govidme')
            
        if ('govid' in sHostName) or ('drkvid' in sHosterUrl) or ('gvid.' in sHosterUrl) or ('govid.' in sHostName) or ('kopatube' in sHostName) or ('kobatube' in sHostName) or ('darkveed' in sHostName) or ('downvol' in sHosterUrl) or ('telvod' in sHosterUrl):
            return self.getHoster('govid')
            
        if ('vid4up' in sHostName):
            return self.getHoster('vidforup')
            
        if ('mp4upload' in sHostName):
            return self.getHoster('mpupload')
            
        if ('fajer.video' in sHostName):
            return self.getHoster('fajer')
            
        if ('youtube' in sHostName) or ('youtu.be' in sHostName):
            return self.getHoster('youtube')

        if ('sama-share' in sHostName):
            return self.getHoster('samashare')

        if ('anafast' in sHostName) or ('anamov' in sHostName):
            return self.getHoster('anafasts')

        if ('myvi.' in sHostName):
            return self.getHoster('myvi')

        if ('yodbox' in sHostName) or ('youdbox' in sHostName) or ('youdboox' in sHostName):
            return self.getHoster('youdbox')

        if ('yandex' in sHostName) or ('yadi.sk' in sHostName):
            return self.getHoster('yadisk')

        if ('vidbom' in sHostName):
            return self.getHoster('vidbom')

        if ('vedpom' in sHostName) or ('vidbem' in sHostName):
            return self.getHoster('vidbem')

        if ('vkplay' in sHostName):
            return self.getHoster('vkplay')

        if ('sharecast' in sHostName):
            return self.getHoster('sharecast')

        if ('live7' in sHostName):
            return self.getHoster('live7')

        if ('voodc' in sHostName):
            return self.getHoster('voodc')

        if ('vk.com' in sHostName) or ('vkontakte' in sHostName) or ('vkcom' in sHostName) or ('vk.ru' in sHostName):
            return self.getHoster('vk')

        if ('playvidto' in sHostName):
            return self.getHoster('vidto')

        if ('liiivideo' in sHostName):
            return self.getHoster('qfilm')

        if ('hd-stream' in sHostName):
            return self.getHoster('hd_stream')

        if ('livestream' in sHostName):
            return self.getHoster('lien_direct')

        if ('embedo' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        # vidtodo et clone
        val = next((x for x in ['vidtodo', 'vixtodo', 'viddoto', 'vidstodo'] if x in sHostName), None)
        if val:
            return self.getHoster('vidtodo')

        if ('dailymotion' in sHostName) or ('dai.ly' in sHostName):
            try:
                if 'stream' in sHosterUrl:
                    return self.getHoster('lien_direct')
            except:
                pass
            else:
                return self.getHoster('dailymotion')
        if ('flashx' in sHostName) or ('filez' in sHostName):
            return self.getHoster('flashx')

        if ('mystream' in sHostName) or ('mstream' in sHostName):
            return self.getHoster('mystream')

        if ('streamingentiercom/videophp?type=speed' in sHosterUrl) or ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')

        if ('googlevideo' in sHostName) or ('picasaweb' in sHostName) or ('googleusercontent' in sHostName):
            return self.getHoster('googlevideo')

        if ('ok.ru' in sHostName) or ('odnoklassniki' in sHostName):
            return self.getHoster('ok_ru')

        if ('iframe-secured' in sHostName):
            return self.getHoster('iframe_secured')

        if ('iframe-secure' in sHostName):
            return self.getHoster('iframe_secure')

        if ('thevideo' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName):
            return self.getHoster('thevideo_me')

        if ('drive.google.com' in sHostName) or ('docs.google.com' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f

        if ('stream.moe' in sHostName):
            return self.getHoster('streammoe')

        if ('movshare' in sHostName) or ('wholecloud' in sHostName):
            return self.getHoster('wholecloud')

        if ('upvid.' in sHostName):
            return self.getHoster('upvid')

        if ('dynamicrevival' in sHostName):
            return self.getHoster('dynamic')

        if ('upvideo' in sHostName) or ('streamon' in sHostName):
            return self.getHoster('upvideo')

        if ('estream' in sHostName) and not ('widestream' in sHostName):
            return self.getHoster('estream')

        if ('clipwatching' in sHostName) or ('highstream' in sHostName):
            return self.getHoster('clipwatching')

        if ('voe' in sHostName):
            return self.getHoster('voe')

        if ('goo.gl' in sHostName) or ('bit.ly' in sHostName) or ('streamcrypt' in sHostName) or ('opsktp' in sHosterUrl):
            return self.getHoster('allow_redirects')

        if ('netu' in sHostName) or ('waaw' in sHostName) or ('hqq' in sHostName) or ('doplay' in sHostName):
            return self.getHoster('netu')

        # frenchvid et clone
        val = next((x for x in ['french-vid', 'diasfem', 'yggseries', 'fembed', 'fem.tohds', 'feurl', 'fsimg', 'core1player',
                                'vfsplayer', 'gotochus', 'suzihaza', 'sendvid', "femax"] if x in sHostName), None)
        if val:
            return self.getHoster("frenchvid")

        if ('directmoviedl' in sHostName) or ('moviesroot' in sHostName):
            return self.getHoster('directmoviedl')

        # Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('1fichier')

        if ('uploaded' in sHostName) or ('ul.to' in sHostName):
            if ('/file/forbidden' in sHosterUrl):
                return False
            return self.getHoster('uploaded')

        if ('myfiles.alldebrid.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('clientsportals' in sHosterUrl):
            return self.getHoster('lien_direct')
    
        if ('torrent' in sHosterUrl) or ('magnet:' in sHosterUrl):
            return self.getHoster('torrent')
        
        if ('nitroflare' in sHostName or 'tubeload.' in sHostName or 'Facebook' in sHostName  or 'fastdrive' in sHostName or 'megaup.net' in sHostName  or 'openload' in sHostName):
            return False

        if ('tuktuk' in sHosterUrl) or ('volvovideo' in sHostName) or ('lumiawatch' in sHostName):
            return self.getHoster('tuktuk')

        # lien direct ?
        if any(sHosterUrl.endswith(x) for x in ['.mp4', '.avi', '.flv', '.m3u8', '.webm', '.mkv', '.mpd']):
            return self.getHoster('lien_direct')

        if ('avideo.host' in sHosterUrl):
            return self.getHoster('avideo')
        
        else:
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f            
        return False

    def getHoster(self, sHosterFileName):
        mod = __import__('resources.hosters.' + sHosterFileName, fromlist=['cHoster'])
        klass = getattr(mod, 'cHoster')
        return klass()

    def play(self, oInputParameterHandler = False, autoPlay = False):
        oGui = cGui()
        oDialog = dialog()

        if not oInputParameterHandler:
            oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('sTitle')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sCat = oInputParameterHandler.getValue('sCat')
        sMeta = oInputParameterHandler.getValue('sMeta')

        if not sTitle:
            sTitle = sFileName

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        try:
            mediaDisplay = sMediaUrl.split('/')
            VSlog('Hoster %s - play : %s/ ... /%s' % (sHosterIdentifier, '/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except:
            VSlog('Hoster %s - play : ' % (sHosterIdentifier, sMediaUrl))

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        if not autoPlay:
            oDialog.VSinfo(sHosterName, 'Resolve')

        try:
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink(autoPlay)

            if aLink and (aLink[0] or aLink[1]):  # Le hoster ne sait pas résoudre mais a retourné une autre url
                if not aLink[0]:  # Voir exemple avec allDebrid qui : return False, URL
                    oHoster = self.checkHoster(aLink[1], debrid=False)
                    if oHoster:
                        oHoster.setFileName(sFileName)
                        sHosterName = oHoster.getDisplayName()
                        if not autoPlay:
                            oDialog.VSinfo(sHosterName, 'Resolve')
                        oHoster.setUrl(aLink[1])
                        aLink = oHoster.getMediaLink(autoPlay)

                if aLink[0]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(self.SITE_NAME)
                    oGuiElement.setSiteUrl(siteUrl)
                    oGuiElement.setMediaUrl(aLink[1])
                    oGuiElement.setFileName(sFileName)
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setCat(sCat)
                    oGuiElement.setMeta(int(sMeta))
                    oGuiElement.getInfoLabel()

                    from resources.lib.player import cPlayer
                    oPlayer = cPlayer(oInputParameterHandler)

                    # sous titres ?
                    if len(aLink) > 2:
                        oPlayer.AddSubtitles(aLink[2])

                    return oPlayer.run(oGuiElement, aLink[1])

            if not autoPlay:
                oDialog.VSerror(self.ADDON.VSlang(30020))
            return False

        except Exception as e:
            oDialog.VSerror(self.ADDON.VSlang(30020))
            import traceback
            traceback.print_exc()
            return False

        if not autoPlay:
            oGui.setEndOfDirectory()
        return False

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog('Hoster - playlist ' + sMediaUrl)
        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if aLink[0]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            from resources.lib.player import cPlayer
            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            dialog().VSinfo(str(oHoster.getFileName()), 'Playlist')
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        from resources.lib.handler.requestHandler import cRequestHandler
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
