#-*- coding: utf-8 -*-
#
# Benz
#
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
import xbmc
#import xbmcvfs
import json
import web_pdb

SITE_IDENTIFIER = 'tva'
SITE_NAME = 'TVA En direct'
SITE_DESC = 'Retrouvez l\'univers de TVA : les émissions en rattrapage ou en direct, les rendez-vous cinéma, les actualités, les jeux, les concours, les artistes et plus encore…'  # description courte de votre source
SITE_THUMB = 'https://i.imgur.com/L9a2n1K.png'
# constant api data, this may change once in a while
API_URL = 'https://edge.api.brightcove.com/playback/v1/accounts/5481942443001/videos/5536901934001'
API_KEY = 'BCpkADawqM1hywVFkIaMkLk5QCmn-q5oGrQrwYRMPcl_yfP9blx9yhGiZtlI_V45Km8iey5HKLSiAuqpoa1aRjGw-VnDcrCVf86gFp2an1FmFzmGx-O-ed-Sig71IJMdGs8Wt9IyGrbnWNI9zNxYG_noFW5dLBdPV3hXo4wgTzvC2KvyP4uHiQxwyZw'

# TODO: implement this, (the non-live 'rattrapage' rest of the website)
URL_MAIN = 'https://videos.tva.ca/'


URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

LIVE_STREAM = (URL_MAIN + 'page/direct?clip=5972573923eec6000b4fe248',
               'showMovies')
SPORT_SPORTS = (URL_MAIN + 'url', 'showMovies')
MOVIE_NETS = (URL_MAIN + 'url', 'showMovies')
REPLAYTV_REPLAYTV = (URL_MAIN + 'url', 'showMovies')


def load():
    oGui = cGui() 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche',
                'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', LIVE_STREAM[0])
    oGui.addDir(SITE_IDENTIFIER,
                LIVE_STREAM[1], SITE_NAME, 'series_news.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()  

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = cGui()  
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(API_URL)
    oRequestHandler.addHeaderEntry('Accept', 'application/json;pk=' + API_KEY)
    oRequestHandler.addHeaderEntry('Host', 'edge.api.brightcove.com')
    oRequestHandler.addHeaderEntry('Origin', 'https://videos.tva.ca')
    oRequestHandler.addHeaderEntry(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')

    sHtmlContent = oRequestHandler.request()
    jsonResponse = json.loads(sHtmlContent)

    for m3u in jsonResponse['sources']:
        # Maybe one day implement a proper parser for m3u8 output resolution.
        #bContent = cRequestHandler(m3u['src']).request()
        # fh = xbmcvfs.File('/storage/.kodi/temp/tva_m3u/' +
        #                  m3u['asset_id'] + '.m3u8', 'w')
        # fh.write(bContent)
        # fh.close()
        #web_pdb.set_trace()
        # Trick to force the wrapper hoster.py into put this url into direct link.
        oHoster = cHosterGui().checkHoster(m3u['src'] + '#.m3u8')
        if (oHoster != False):
            oHoster.setDisplayName(SITE_NAME)
            oHoster.setFileName(SITE_NAME)
            cHosterGui().showHoster(oGui, oHoster, m3u['src'], SITE_THUMB)

    if not sSearch:
        oGui.setEndOfDirectory()
