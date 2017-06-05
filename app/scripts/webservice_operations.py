# -*- encoding: utf-8 -*-

from .. import app, STATIC_DATA, SITE_STATIC, SITE_ROOT #, mysql_catalogue
from .app_db_settings import *


import requests
import zeep
import copy

from requests import Session
#from requests.auth import HTTPBasicAuth
#from lxml import etree

### cf Zeep doc : https://media.readthedocs.org/pdf/python-zeep/master/python-zeep.pdf
### cf Zeep API : http://docs.python-zeep.org/en/master/api.html#client
### cf openclassroom services web : https://openclassrooms.com/courses/les-services-web

from zeep import Client, xsd
from zeep.cache import SqliteCache
from zeep.transports import Transport

history = zeep.plugins.HistoryPlugin()

### HTTP authentication --- NOT SET YET
user     = '' #'synapse'
password = '' #'synapse_aloes_pwd'


### connect to webservice
with app.app_context():

    print "starting app --- connect to webservice Aloes"
    ### get authentification args from config.py
    SYNAPSE_IP   = app.config["SYNAPSE_IP"]
    WSDL         = app.config["WSDL"]
    NOM_MACHINE  = app.config["NOM_MACHINE"]

paramSession = {   "NomMachine"    : NOM_MACHINE,
                    "ListeServeurs" : {
                        'ServeurSession': [{
                            'BasesServeurs': {
                                'BaseSession': [{'NomBase': 'Synapse'}]
                                },
                            'NomServeur': SYNAPSE_IP
                        }]
                    }
                }

### param transport : session / cache / timeout
session_  = Session()
transport = Transport(session=session_, cache=SqliteCache(), timeout=2)

try :
    client_   = zeep.Client(wsdl=WSDL, transport=transport, plugins=[history])
    session_  = client_.service.OuvrirSession(Param=paramSession)
    GUID      = session_.GUIDSession
    print "starting app --- connect to webservice Aloes --- OK with GUID : ", GUID

except :
    print "------------------------------------------------------------"
    print "starting app --- PROBLEM connecting to webservice Aloes --- "
    print "------------------------------------------------------------"




# ### WORKING !!!!
# auth_test = {
#     'GUIDSession'  : GUID,
#     'IDEmprunteur' : '123456',
#     'MotDePasse'   : 'PASSWORD',
#     'Place'        : '',
# }
# print "starting app --- connect to webservice Aloes --- auth_test : ", auth_test
#
#
# empr_test = client_.service.EmprAuthentifier(auth_test)
# print "starting app --- connect to webservice Aloes --- empr_test : ", empr_test
#
# paramInfos = {
#     'GUIDSession' : empr_test.GUIDSession,
#     'IdEntite'    : 'ListeInfo'
# }
# resInfos = client_.service.EmprListerEntite(paramInfos)
# print "starting app --- connect to webservice Aloes --- resInfos : ", resInfos
#

class WS_user_infos_ :

    def __init__(self, card_number, password) :

        print " WS_user_infos_light --- connect to webservice Aloes --- start : "

        self.card_number = card_number
        self.password    = password
        self.auth = {
            'GUIDSession'  : GUID,
            'IDEmprunteur' : self.card_number,
            'MotDePasse'   : self.password,
            'Place'        : '',
        }
        self.empr_test = client_.service.EmprAuthentifier(self.auth)
        print " WS_user_infos_light --- connect to webservice Aloes --- self.empr_test : ", self.empr_test


    def get_history (self) :
        paramHisto = {
            'GUIDSession' : self.empr_test.GUIDSession,
            'IdEntite'    : 'ListeHistoPret'
        }

        resHisto = client_.service.EmprListerEntite(paramHisto)
        print ">>> WS_user_infos / resHisto : "
        #print resHisto
        print '- ' * 70

        return resHisto

    def get_infos (self) :
        paramInfo = {
            'GUIDSession' : self.empr_test.GUIDSession,
            'IdEntite'    : 'ListeInfo'
        }

        resInfos = client_.service.EmprListerEntite(paramInfo)
        print ">>> WS_user_infos / resInfos : "
        #print resInfos
        print '- ' * 70

        return resInfos



#WS_user_infos_light('123456', 'PASSWORD')
print "starting app --- connect to webservice Aloes --- end test : "
print '- '*50
print




# ### get user informations
# class WS_user_infos :
#
#     def __init__(self, card_number, password) :
#
#         print ">>> WS_user_infos / __init__  "
#
#         self.card_number = card_number
#         self.password    = password
#
#         # print card_number, type(card_number)
#         # print password, type(password)
#
#         print ">>> WS_user_infos --- %s / %s " %(self.card_number, self.password)
#         #print GUID
#         print
#
#
#         self.client_   = zeep.Client(wsdl=WSDL, transport=transport, plugins=[history])
#         print ">>> WS_user_infos / self.client_ : ", self.client_
#
#         self.session_ = self.client_.service.OuvrirSession(Param=paramSession)
#         print ">>> WS_user_infos / self.session_ : ", self.session_
#
#         self.GUID     = self.session_.GUIDSession
#         print ">>> WS_user_infos / self.GUID : ", self.GUID
#
#         self.auth_ = {
#             'GuidSession'  : self.GUID,
#             'IDEmprunteur' : self.card_number,
#             'MotDePasse'   : self.password,
#             'Place'        : ''
#         }
#         print ">>> WS_user_infos / self.auth_ : ", self.auth_
#
#
#
#
#         ### PROBLEM HERE !!!
#         self.empr_ = self.client_.service.EmprAuthentifier(self.auth_)
#
#
#         print ">>> WS_user_infos / self.empr_ : ", self.empr_
#         print ' -' * 70
#
#
#
#
#
#     def get_history (self) :
#         paramHisto = {
#             'GUIDSession' : self.empr_.GUIDSession,
#             'IdEntite'    : 'ListeHistoPret'
#         }
#
#         resHisto = self.client_.service.EmprListerEntite(paramHisto)
#         print ">>> WS_user_infos / resHisto : "
#         print resHisto
#         print ' -' * 70
#
#         return resHisto
#
#
#     def get_infos (self) :
#         paramInfo = {
#             'GUIDSession' : self.empr_.GUIDSession,
#             'IdEntite'    : 'ListeInfo'
#         }
#
#         resInfos = self.client_.service.EmprListerEntite(paramInfo)
#         print ">>> WS_user_infos / resInfos : "
#         print resInfos
#         print ' -' * 70
#
#         return resInfos
