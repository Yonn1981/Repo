# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################
# Thanks to TSIPlayer Creators

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress,VSlog, siteManager, dialog, addon

import json
import requests


SITE_IDENTIFIER = 'linkbox'
SITE_NAME = 'Telebox [COLOR orange]- Linkbox -[/COLOR]'
SITE_DESC = 'A Box Linking The World'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERVER_A = ('46Qaojv', 'showContent')
SERVER_B =('_ig_2z1IFpK_4702801_f98c', 'showContent')
SERVER_C =('xgLMOew', 'showContent')
SERVER_D =('64b7U9d', 'showContent')
SERVER_E =('DERRaVk', 'showContent')
SERVER_F =('ypev9W9', 'showContent')
SERVER_G =('ho3FrEE', 'showContent')
SERVER_H =('bNA04cJ', 'showContent')
SERVER_I =('SD9p5bO', 'showContent')
SERVER_J =('UiLE7sU', 'showContent')
SERVER_K =('app01e2f1adf1aca4a3a2a1a7aea4adf2aca4a3a2a1a7aea4', 'showContent')
SERVER_L =('app01e2f1adf1aca4a1afaea4a5a1adf2aca4a1afaea4a5a1', 'showContent')
SERVER_M =('app01e2f1adf1aca1afaea6a7adf2aca1afaea6a7', 'showContent')
SERVER_N =('_ig_app01e2f1adf0f2acf0e6a5f5fdf5a6a6a6a3f0a3_237634_f725', 'showContent')
SERVER_O =('app01e2f1adf1aca5a2aea1a2a6a3adf2aca5a2aea1a2a6a3', 'showContent')
SERVER_P =('_ig_app01e2f1adf0f2acf0e6a5faeca2a6a6e6eef3fb_4890590_e417', 'showContent')
SERVER_Q =('app01e2f1adf2acaea7a5a2a3a5a4adf1acaea7a5a2a3a5a4', 'showContent')
SERVER_R =('app01e2f1adf2acafafa4a2a3a2adf1acafafa4a2a3a2', 'showContent')
SERVER_S =('_ig_app01e2f1adf0f2acf0e6a5fda0aea6a6a6f3afe0_2674587_0ddd', 'showContent')
SERVER_T =('_ig_app01e2f1adf0f2acf0e6a5fbf9e5a6a6a6eefdf8_3589656_8ed8', 'showContent')
SERVER_U =('app01e2f1adf1aca7a4a5a3a1a3aeadf2aca7a4a5a3a1a3ae', 'showContent')
SERVER_V =('app01e2f1adf1aca7a1a1a4a2a7a0adf2aca7a1a1a4a2a7a0', 'showContent')
SERVER_W =('app01e2f1adf1aca4a3a5aea3aea0adf2aca4a3a5aea3aea0', 'showContent')
SERVER_X =('app01e2f1adf2acaeafa3a3afa3adf1acaeafa3a3afa3', 'showContent')
SERVER_Y =('_ig_app01e2f1adf0f2acf0e6a5fde4e1a6a6a6e3e3af_2934696_5b94', 'showContent')
SERVER_Z =('_ig_app01e2f1adf0f2acf0e6a5fde3aea6a6a6aff7f2_3576258_c91a', 'showContent')
SERVER_1 =('app01e2f1adf2aca7a3a6a0a1a1a5adf1aca7a3a6a0a1a1a5', 'showContent')
SERVER_2 =('_ig_app01e2f1adf0f2acf0e6a5f9e4f1a6a6a5fcfba2_4250624_a55c', 'showContent')
SERVER_3 =('_ig_app01e2f1adf0f2acf0e6a5e7e5e1a6a6a4a1eefe_10100689_6184', 'showContent')
SERVER_4 =('app01e2f1adf1aca0a3a1a1a0a0adf2aca0a3a1a1a0a0', 'showContent')
SERVER_5 =('app01e2f1adf1aca3a7afa4a0a0a0adf2aca3a7afa4a0a0a0', 'showContent')
SERVER_6 =('app01e2f1adf2acaeaea5a2aea4afadf1acaeaea5a2aea4af', 'showContent')
SERVER_7 =('app01e2f1adf1aca5aea7afa0a6a5adf2aca5aea7afa0a6a5', 'showContent')
SERVER_8 =('_ig_app01e2f1adf0f2acf0e6a5fcaff5a6a6a6afa7fe_2609502_fdae', 'showContent')
SERVER_9 =('_ig_app01e2f1adf0f2acf0e6a5f9faa2a6a6a2e6f4e2_2751140_2b6c', 'showContent')
SERVER_10 =('_ig_app01e2f1adf0f2acf0e6a5fae2fda6a6a6f1a3ae_1077534_cc7b', 'showContent')
SERVER_11 =('_ig_app01e2f1adf0f2acf0e6a5fbe6fda6a6a6eef4ff_6032611_496c', 'showContent')
SERVER_12 =('_ig_app01e2f1adf0f2acf0e6a5fdf3aea6a6a5e6f8af_3519730_d7ac', 'showContent')
SERVER_13 =('app01e2f1adf2aca0aeaeafa2a1adf1aca0aeaeafa2a1', 'showContent')
SERVER_14 =('app01e2f1adf2aca7aea5a5a6a6a3adf1aca7aea5a5a6a6a3', 'showContent')
SERVER_15 =('paG344x', 'showContent')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SERVER_A[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_A[1], 'Netflix', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_B[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_B[1], 'Netflix 2', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_C[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_C[1], 'Egybest', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_D[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_D[1], 'ONE cima TV', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_E[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_E[1], 'إجي بيست', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_F[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_F[1], 'مسلسلات و أفلام أجنبية', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_G[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_G[1], 'For You', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_H[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_H[1], 'AflamHQ', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_I[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_I[1], 'Marvel Morocco', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_J[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_J[1], 'Cinema Baghdad', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_K[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_K[1], 'Cinema Club Movies', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_L[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_L[1], 'Cinema Club Series', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_M[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_M[1], 'Star Cinema', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_N[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_N[1], 'Cima Now TV', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_O[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_O[1], 'سينما أونلاين', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_P[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_P[1], 'أفلام', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_Q[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_Q[1], 'مجتمع الأفلام و المسلسلات', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_R[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_R[1], 'عشاق الأفلام', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_S[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_S[1], 'Netflix 3', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_T[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_T[1], 'Egybest إجي بيست', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_U[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_U[1], 'Cinema Crown', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_V[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_V[1], 'البيت سينما', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_W[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_W[1], 'Cinemaclub إنمي', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_X[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_X[1], 'The Movie night', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_Y[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_Y[1], 'Atwa', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_Z[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_Z[1], 'دراما نيوز', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_1[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_1[1], 'EGY-BEST', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_2[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_2[1], 'Kowaya Cinema', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_3[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_3[1], 'Cinema Dose', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_4[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_4[1], 'Cinema Sold', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_5[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_5[1], 'كل المسلسلات و الأفلام', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_6[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_6[1], 'أنميات', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_7[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_7[1], 'Cinema Mix', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_8[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_8[1], 'فرجني شكرا', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_9[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_9[1], 'اجي بيست', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_10[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_10[1], 'أفلام ومسلسلات أجنبية', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_11[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_11[1], 'مسلسلات أجنبية أكشن إثارة', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_12[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_12[1], 'تلفازك المتنقل', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_13[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_13[1], 'إنميات و تصنيفات الإنمي', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_14[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_14[1], 'عالم موبيس', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERVER_15[0])
    oGui.addDir(SITE_IDENTIFIER, SERVER_15[1], 'Shahid4u', 'genres.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showContent(sSearch = ''):
    import requests
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    spage = int(oInputParameterHandler.getValue('page'))   
    spid = oInputParameterHandler.getValue('spid')
    
    
    nb_elm = 50
    shareToken = sUrl

    page = 1
    pid = spid

    if spage > 1:
        page = spage
    else:
        page = 1
    VSlog(page)
    sUrl = URL_MAIN + '/api/file/share_out_list/?sortField=name&sortAsc=1&pageNo='+str(page)+'&pageSize='+str(nb_elm)+'&'+'shareToken='+shareToken+'&pid='+str(pid)+'&needTpInfo=1&scene=singleGroup&name=&platform=web&pf=web&lan=en'

    data = requests.get(sUrl).json()
    data = data.get('data',{})
    data = data.get('list',[])
    if not data: data = []
    elm_count = 0
    for elm in data:
                sTitle = elm.get('name','')
                type_ = elm.get('type','')

                pid   = elm.get('id','')

                desc  = ''
                elm_count = elm_count + 1
                
                icon  = 'host.png'

                link  = elm.get('url','')

                oOutputParameterHandler.addParameter('spid', pid) 
                oOutputParameterHandler.addParameter('sTitle', sTitle)            
                oOutputParameterHandler.addParameter('sThumb', '') 
                oOutputParameterHandler.addParameter('siteUrl',shareToken)
                if type_=='dir':
                    oGui.addDir(SITE_IDENTIFIER, 'showContent', sTitle, icon, oOutputParameterHandler)
                    
                if elm_count + 1 > nb_elm:
                    page = page + 1
                    oOutputParameterHandler.addParameter('page',page)
                    oOutputParameterHandler.addParameter('siteUrl',shareToken)
                    oGui.addDir(SITE_IDENTIFIER, 'showContent', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

                elif type_=='video':
                    sHosterUrl = link
            
                    oHoster = cHosterGui().getHoster('lien_direct')        
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, icon)                
 
    oGui.setEndOfDirectory()