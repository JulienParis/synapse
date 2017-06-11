# -*- encoding: utf-8 -*-
### author : Julien Paris - Jpy

import time, os
import datetime

from   app   import app, socketio
from   flask import Flask, flash, render_template, url_for, make_response, request, session, redirect
import bcrypt


from flask_socketio import emit #, send

from werkzeug.routing import Rule
from werkzeug.utils   import secure_filename

### cache system
from werkzeug.contrib.cache import SimpleCache



### forms classes
from .forms import LoginForm, UserRegisterForm, UserUpdateForm, UserHistoryAloesForm, RequestCabForm

### db classes and functions
from scripts.databases_operations import *
### imported from scripts.databases_operations
#from scripts.app_db_settings import * #authorized_collections, key_synapse

### webservice classes and functions
from scripts.webservice_operations import *


from scripts.app_settings import bootstrap_vars, app_colors, app_metas, app_bib_infos, ALLOWED_EXTENSIONS

### imported from scripts.databases_operations
#import gc ### aka garbage collector

import json
from   bson import json_util
from   bson.objectid import ObjectId
from   bson.json_util import dumps
import itertools


########################################################################################
### INTERNAL FUNCTIONS  #####
def Is_Admin():

    # isUser        = None
    # isAdmin       = False

    print

    if 'username' in session:
        print '**** Is_Admin **** you are logged in as : ' + session[key_username]
        isUser        = session[key_username]

        existing_user = users_mongo.find_one({ key_n_carte : session[key_n_carte] })
        print '**** Is_Admin ****  existing_user : ', isUser

        if existing_user[key_status] == 'admin' :
            isAdmin = True
        else:
            isAdmin = False

    else :
        isUser        = None
        isAdmin       = False

    print '**** Is_Admin ****  session : ', session
    print

    return isUser, isAdmin

### cookies
@app.route("/setcookie/<data>")
def setcookie( data, cookie_name="parcours" ):
    print
    print "++++ setcookie ++++ ", cookie_name
    resp = make_response( redirect( url_for('index') ) ) #'setting cookie' + cookie_name )
    # resp = make_response( "tada" ) #'setting cookie' + cookie_name )
    resp.set_cookie( cookie_name, data )
    print
    return resp

@app.route("/get")
def getcookie( cookie_name="parcours" ):
    print
    print "++++ getcookie ++++ ", cookie_name
    data_cookie = request.cookies.get( cookie_name )
    print
    return data_cookie

### CACHES FOR user's parcours in session
### cf; : http://werkzeug.pocoo.org/docs/0.12/contrib/cache/#werkzeug.contrib.cache.BaseCache.set
cache = SimpleCache()

def set_cache( data, cache_name="parcours" ) :
    print
    print "++++ set_cache ++++ ", cache_name
    cache.set( cache_name, data, timeout = 60 * 10) ### default_timeout=300 time in seconds
    print

def get_cache( cache_name="parcours" ) :
    print
    print "++++ get_cache ++++ ", cache_name
    result_cache = cache.get(cache_name)
    print
    return result_cache

'''
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def uploadFile(file_, subdir_):

    filename_ = None

    if allowed_file(file_.filename) :
        filename_  = secure_filename(file_.filename)
        file_.save( os.path.join( subdir_, filename_ ) )
        print "      >>> file --%s-- saved in :" %(filename_), subdir_

    return filename_
'''

########################################################################################
### WEBSERVICE ROUTES #####
@app.route('/WS_user/', methods=['GET'] )
def WS_user_hist(card_number=None, password=None):

    print u'~ '*70

    # check user status
    isUser, isAdmin  = Is_Admin()
    print '~ ~ ~ WS_user_hist --- isUser  : ', isUser
    # print '--- WS_user_hist --- session : ', session
    print '~ ~ ~ WS_user_hist --- session["username"] : ', session[key_username]
    print '~ ~ ~ WS_user_hist --- session["n_carte"]  : ', session[key_n_carte]
    print u'~ '*70


    if isAdmin or isUser :

        ### for internal use : no arguments in function WS_user_hist call from URL
        if card_number is None and password is None :

            if isAdmin :

                print '~ ~ ~ WS_user_hist --- no card_number nor password / using args  '

                ### user auth from args in URL
                card_number = request.args.get("card_number", None )
                password    = request.args.get("password", None )

                ### get user info from users_mongo
                WS_user_ = users_mongo.find_one( {key_n_carte : card_number } )
                print '~ ~ ~ WS_user_hist --- username        : ', WS_user_[key_username]
                print '~ ~ ~ WS_user_hist --- password mongo  : ', WS_user_[key_password].encode('utf-8')

                print '~ ~ ~ WS_user_hist --- bcrypt password : ', bcrypt.hashpw( password.encode('utf-8'), WS_user_[key_password].encode('utf-8') )
                check_pw = bcrypt.hashpw( password.encode('utf-8'), WS_user_[key_password].encode('utf-8') ) == WS_user_[key_password].encode('utf-8')
                print '~ ~ ~ WS_user_hist --- check_pw        : ', check_pw
                print


            else :
                sessionError = u"you don't have admin rights - you can't accesss webservice by Synapse's API "
                flash(sessionError, "warning")
                return redirect( url_for('index') )


        ### for common use : can be called from backend with session
        else :

            ### use user password from request (args)  to send to Aloes

            print '~ ~ ~ WS_user_hist --- card_number & password  '

            ### get user infos from session and from users_mongo
            ### WS_user_     = users_mongo.find_one( {'n_carte' : session['n_carte'] } )
            ### print '~ ~ ~ WS_user_hist --- username / from WS_user : %s / from session : %s ', WS_user_['username'] , session['username']
            ### print '~ ~ ~ WS_user_hist --- password / ', WS_user_['password'].encode('utf-8')

            ### card_number  = WS_user_["n_carte"]
            ### password     = WS_user_["password"]

            pass


        print u'~ '*70
        print '~ ~ ~ WS_user_hist --- card_number : %s / password : %s ' %(card_number, password)
        print u'~ '*70


        ###### retrieve infos from WEBSERVICE ######
        try :
            ### authentify user in WS using WS_user_infos_ class
            user_req = WS_user_infos_(card_number, password)#.get_infos()

            ### retrieve user's history : exemplaires
            #user_  = user_req.get_infos()
            user_hist  = user_req.get_history()
            user_hist_list_cab = []


            ### get corresponding notice for each cab from exemplaires_mongo
            for cab_ in user_hist.Entite.Donnees.Lignes :
                cab = cab_.ValeursDonnees.string
                # print '~ ~ ~ WS_user_hist --- cab[1] :', cab[1]

                try :
                    exemplaire = exemplaires_mongo.find_one( { key_barcode : cab[1] } )
                    #get id_o from exemplaire
                    ex_id_o   = exemplaire[key_synapse]
                    # print '~ ~ ~ WS_user_hist --- ex_id_o :', ex_id_o

                except :
                    ex_id_o   = None
                    # ex_title  = None
                    # ex_author = None

                ex_ = { key_barcode    : cab[1],
                        key_rendu_date : cab[6] ,
                        key_synapse    : ex_id_o ,
                        key_keep       : False,
                        # key_title      : ex_title ,
                        # key_author     : ex_author,
                        #key_parcours_status : parcours_status["emprunt"]
                        }

                user_hist_list_cab.append(ex_)

            print
            print '~ ~ ~ WS_user_hist --- user_hist_list_cab :  '
            print user_hist_list_cab[:2], "..."
            print

            ###### write / update into MongoDB.users : users_mongo ######
            parcours_sub_dir = ".".join([ key_parcours, parcours_status_[0] ])
            #print parcours_sub_dir

            users_mongo.update_one(
                {key_n_carte : card_number},
                {"$set"      : {
                    parcours_sub_dir : user_hist_list_cab,
                    key_lastupdate   : datetime.datetime.now()
                    }
                } ,
                upsert = True
            )
            flash( u"vos derniers emprunts ont été téléchargés et votre liste est mise à jour", "success")


        except :
            sessionError = u"vous n'êtes pas enregistré dans la base de données de " + app_bib_infos["biblio"]
            flash(sessionError, "warning")
            pass



    print '~ ~ ~ WS_user_hist --- END '
    print '~ '*70
    print


    return redirect( url_for('index') )


########################################################################################
### MYSQL ROUTES #####
@app.route('/<update_reset>' )
def update_coll(update_reset="update", secret_key_update=None):

    isUser, isAdmin  = Is_Admin()

    #if coll in authorized_collections :
    print "/// update_coll / update_reset : ", update_reset

    with app.app_context():
        check_key_update = app.config["UPDATE_SECRET_KEY"]

    ### use only if isAdmin or with internal use
    if isAdmin or secret_key_update == check_key_update :

        print "/// update_coll / access MYSQL " #"/ for coll : ", coll
        print

        ### update all mongoDB collections : notices and exemplaires

        if update_reset == "update" :
            mongodb_updates().update_all_coll()
            print "/// update_coll / df_coll created "
            flash(u'les collections sont mises à jour - update', "success")

        elif update_reset == "reset":
            mongodb_updates().reset_all_coll()
            print "/// update_coll / df_coll created "
            flash(u'les collections sont remises à jour - reset', "success")

        elif update_reset == "reset" or update_reset == "reset" or update_reset == "rewrite_JSON" :
            ### update / rewrite json local static file
            mongodb_read('notices', get_ligth=True ).write_notices_json_file( nested=True , debug=True )
            flash(u'les collections sont réécrites en JSON en local ', "success")

        print
        return redirect( url_for('index') )

    else :
        print
        return redirect( url_for('index') )



########################################################################################
### MONGODB ROUTES BACKDOORS #####

@app.route('/users')
def get_users():

    print
    print "/// test access mongoDB / users "

    isUser, isAdmin  = Is_Admin()

    if isAdmin :

        users = users_mongo.find( {}, { "_id":0 } ) #, "password" : 0 })

        json_users = dumps(users, default=json_util.default)
        #json_users = df_users.to_json(orient="records", default_handler=str)
        return json_users

    else :
        return redirect( url_for('index') )



# @app.route('/notices', defaults={'fields': [], 'limit': None})
# @app.route('/notices/fields=<fields>+limit=<int:limit>')
### REST API on pattern : .../notices/?limit=3&field=auteur_princ&field=titre
@app.route('/<coll>/', methods=['GET'] )
def get_coll(coll):

    isUser, isAdmin  = Is_Admin()

    if isAdmin and coll in authorized_collections :

        print

        print "/// test access mongoDB / for coll : ", coll

        ### get all the arguments back from URL route
        # args_url = request.args.to_dict()
        limit   = request.args.get("limit", 0)
        if limit != 0 :
            limit = int(limit)

        fields  = request.args.getlist("field", None )
        if fields == []:
            fields = None
        isLight = request.args.get("isLight", False)
        if isLight == "True" :
            isLight = True

        print "/// get_coll variables / limit : %s, fields : %s, isLight : %s "  %( (limit if limit else "None"), (fields if fields!=None else "None"), (isLight if isLight else "False"))
        mongoRead = mongodb_read( coll, fields=fields, limit=limit, get_ligth=isLight )

        ### calling function from databases_operations.py
        return mongoRead.get_coll_as_json()

    else :
        sessionError = u"vous n'avez pas accès à l'API ou à ce jeu de données"
        flash(sessionError, "warning")

        return redirect( url_for('index') )



########################################################################################
### ROUTING FUNCTIONS #######################

@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():

    print
    print "I "*70
    print

    print "---- INDEX ---- session : %s " % ( session )

    ### DEFAULT SESSION VALUES
    # isUser        = None
    # isAdmin       = False
    sessionError  = None
    # user_data     = None
    # user_parcours = None


    ### FORMS FROM WTF
    loginForm      = LoginForm()
    registerForm   = UserRegisterForm()
    aloesForm      = UserHistoryAloesForm()
    userUpdateForm = UserUpdateForm()
    requestCabForm = RequestCabForm()

    isUser, isAdmin  = Is_Admin()
    print "---- INDEX ---- isAdmin : %s " % ( isAdmin )
    print "---- INDEX ---- isUser  : %s " % ( isUser )
    print "---- INDEX ---- session : %s " % ( session )
    print

    ### RETRIEVE COMPLETE DATA PARCOURS AND STORE IT IF USER
    if isUser :

        ### prepopulating userUpdateForm
        userUpdateForm = UserUpdateForm()
        userUpdateForm.new_userName.data  = session[key_username]
        userUpdateForm.new_userCard.data  = session[key_n_carte]
        userUpdateForm.new_userEmail.data = session[key_email]

        is_userdata = session["is_userdata"]
        print "---- INDEX ---- is_userdata :", is_userdata

        ### get user informations from users_mongo
        # user_rawdata  = users_mongo.find_one( { key_n_carte : session[key_n_carte] }, { "_id":0, "password":0, "status":0 } )
        # user_data = { key : user_rawdata[key] for key in user_rawdata.keys() if key not in ["parcours"] }
        session_light = [ 'csrf_token', '_flashes', 'is_userdata' ]
        user_data = { key : val for key, val in session.iteritems() if not key in session_light }

        ### get user's parcours
        if is_userdata == False :

            user_rawdata  = users_mongo.find_one( { key_n_carte : session[key_n_carte] }, { "_id":0, "password":0, "status":0 } )

            print "---- INDEX ---- is_userdata ---- user_data :", user_data
            print "---- INDEX ---- is_userdata : FALSE  "

            session["is_userdata"]   = True
            print "---- INDEX ---- is_userdata : FALSE ---- session['is_userdata'] : ", session["is_userdata"]

            ### retrieve complete information from CAB listed in user parcours
            print "---- INDEX ---- is_userdata : FALSE  ---- please wait while getting parcours data ... "
            user_parcours_raw = user_rawdata["parcours"]

            user_parcours = {}

            for parcours_type, emprunts_list in user_parcours_raw.iteritems() :

                user_parcours[parcours_type] = []

                for emprunt_data in emprunts_list :

                    ex_id_o   = emprunt_data[key_synapse]
                    ex_cab    = emprunt_data[key_barcode]
                    ex_keep   = emprunt_data[key_keep]
                    # print "---- INDEX ---- ex_id_o : ", ex_id_o

                    try :
                        ex_rendu_ = emprunt_data[key_rendu_date]
                        ex_rendu  = datetime.datetime.strptime( ex_rendu_, '%d/%m/%Y').strftime('%Y/%m/%d')
                    except :
                        ex_rendu  = None

                    ### retrieve infos from notices
                    try :
                        notice    = notices_mongo.find_one( { key_synapse : ex_id_o } )

                        ex_title  = notice[key_title]
                        ex_author = notice[key_author]
                        ex_C1     = dict_emplacements_[ notice[key_group_level_1] ]["PARENT"]
                        ex_C2     = dict_reverse_C2[ notice[key_group_level_2] ]
                    except :
                        ex_title  = unknown_notice
                        ex_author = unknown_notice
                        ex_C1     = unknown_notice
                        ex_C2     = unknown_notice

                    # print "---- %s - %s - %s - %s " %( ex_cab, ex_C2, ex_author, ex_title )
                    # print "---- %s - %s - " %( ex_cab, ex_C2 ), ex_keep
                    ex_dict   = {
                        key_title        : ex_title,
                        key_author       : ex_author,
                        key_group_name_1 : ex_C1,
                        key_group_name_2 : ex_C2,
                        key_barcode      : ex_cab,
                        key_rendu_date   : ex_rendu,
                        key_keep         : ex_keep ,
                    }
                    # print count_debug
                    # print "---- ", ex_dict
                    user_parcours[parcours_type].append(ex_dict)
                    # count_debug += 1
                    # print '.'

                else :
                    pass

            # else :
            #     pass

            print "---- INDEX ---- user_parcours : ",  user_parcours


            # user_parcours_ = json.dumps( user_parcours )
            # # print "---- REAL user_parcours_ : %s " %(user_parcours_)
            # print "---- REAL user_parcours_ ---- isinstance(user_parcours_, str) :",  isinstance(user_parcours_, str)


            set_cache(user_parcours, cache_name="parcours")

            ########## TOO BIG FOR COOKIE ####### SWITCH TO CACHE !!!!
            print "---- INDEX ---- is_userdata : FALSE ---- setcookie(user_parcours_) "
            # setcookie(user_parcours_, cookie_name="parcours")
            # resp = make_response( redirect( url_for('index') ) )
            # resp.set_cookie( "parcours", user_parcours_ )
            # return resp

            # test_cookie = getcookie( cookie_name="parcours" )
            # print "---- INDEX ---- is_userdata : TEST ---- test_cookie "
            # print test_cookie


            print "---- INDEX ---- is_userdata : FALSE ---- user_parcours FINISHED "
            # print session["data_parcours"]
            print

        elif is_userdata == True :

            print "---- INDEX ---- is_userdata : TRUE  "
            # user_parcours_ = getcookie( cookie_name="parcours" )
            user_parcours = get_cache( cache_name="parcours" )
            # print user_parcours

            if user_parcours != None :
                print "---- INDEX ---- is_userdata : TRUE ---- user_parcours_ != None "
                # user_parcours  = json.loads(user_parcours_)
                print

            else :
                print "---- INDEX ---- is_userdata : TRUE ---- user_parcours_ == None "
                session["is_userdata"] = False
                return redirect( url_for('index') )

    else :
        user_data     = None
        user_parcours = None
    # user_parcours     = user_rawdata["parcours"]
    # print "---- INDEX ---- user_parcours : ", user_parcours


    ### if REQUEST == POST is sent from a form : login / register / refresh site
    if request.method == 'POST' :

        print "V "*60
        print

        req_type = request.form['req_type'] ### always add as hidden input in forms
        print "---- INDEX / POST ---- request.form : ", request.form


        if req_type == "update_user" and isUser :

            print "---- INDEX / POST / update_user "
            new_userName     = request.form['new_userName'].encode('utf-8')
            new_userCard     = request.form['new_userCard'].encode('utf-8')
            new_userEmail    = request.form['new_userEmail']
            new_userPassword = request.form['new_userPassword'].encode('utf-8')

            print "---- INDEX / POST / update_user ---- session[key_n_carte] : ", session[key_n_carte]

            form = UserUpdateForm(request.form)
            # for d in form :
            #     print " %s : %s " %(d.name, d.data)
            # print "---- INDEX / POST / update_user ---- form.new_userName.data : ",     form.new_userName.data
            # print "---- INDEX / POST / update_user ---- form.new_userCard.data : ",     form.new_userCard.data
            # print "---- INDEX / POST / update_user ---- form.new_userEmail.data : ",    form.new_userEmail.data
            # print "---- INDEX / POST / update_user ---- form.new_userPassword.data : ", form.new_userPassword.data
            # print "---- INDEX / POST / update_user ---- form.confirmPassword.data : ",  form.confirmPassword.data
            # print "---- INDEX / POST / update_user ---- form.errors.data : ",           form.errors.items()

            if form.validate() : ###################
                existing_user = users_mongo.find_one( { key_n_carte : session[key_n_carte] }, {"_id" : 0 , "parcours" : 0 } )
                print "---- INDEX / POST / update_user ---- retrieving existing_user : ", existing_user
                new_userPassword_crypt = existing_user[key_password]

                ### encrypt new_userPassword if changed
                if new_userPassword != "":
                    new_userPassword_crypt = bcrypt.hashpw(new_userPassword, bcrypt.gensalt() )

                print "new password not encrypted : " , new_userPassword
                print "new password     encrypted : " , new_userPassword_crypt
                print "old password     encrypted : " , existing_user[key_password]

                ### update user's informations
                new_userInfos_dict = {
                    key_username : new_userName,
                    key_n_carte  : new_userCard,
                    key_email    : new_userEmail,
                    key_password : new_userPassword_crypt,
                }
                print new_userInfos_dict
                users_mongo.update_one( { key_n_carte : session[key_n_carte] },
                                        { '$set'      : new_userInfos_dict   },
                                        upsert=False
                                      )

                ### update session
                session[key_username] = new_userName
                session[key_n_carte]  = new_userCard
                session[key_email]    = new_userEmail

                print
                sessionError = u"vos informations personnelles sont à jour"
                flash(sessionError, "success" )
                return redirect( url_for('index') )

            else :
                print "---- INDEX / POST / update_user ---- ERROR "
                print
                sessionError = u'formulaire non valide'
                flash(sessionError, "warning" )
                return redirect( url_for('index') )


        ### ADD ITEM TO USER'S PARCOURS
        elif req_type == "add_item" and isUser :

            print "---- INDEX / POST / add_item ----  "
            form = RequestCabForm(request.form)

            item_cab     = str(request.form['cab_code'])
            item_categ   = request.form['categ'].encode('utf-8')

            if form.validate() :

                print "---- INDEX / POST / add_item ---- adding item - item_cab : %s / item_categ : %s" %(item_cab, item_categ)
                item_ex  = exemplaires_mongo.find_one( { key_barcode : item_cab } )

                if item_ex != None :

                    item_ido   = item_ex[key_synapse]
                    item_not   = notices_mongo.find_one ( { key_synapse : item_ido } )
                    item_rendu = datetime.datetime.now()

                    print "---- INDEX / POST / add_item ---- adding item - title  : %s " %(item_not[key_title])
                    print "---- INDEX / POST / add_item ---- adding item - author : %s " %(item_not[key_author])
                    print "---- INDEX / POST / add_item ---- adding item - resume : %s " %(item_not[key_resume])

                    item_dict = {
                        key_barcode    : item_cab,
                        key_synapse    : item_ido,
                        key_keep       : True,
                        key_rendu_date : item_rendu.strftime('%d/%m/%Y')
                    }
                    print "---- INDEX / POST / add_item ---- adding item - item_dict : %s" %(item_dict)

                    sessionError = u"l'ouvrage a été ajouté à votre parcours"
                    flash(sessionError, "success" )

                    ### select which categ to update
                    parcours_sub_dir = ".".join([ key_parcours, item_categ ])
                    print "---- INDEX / POST / add_item ---- adding item - parcours_sub_dir :", parcours_sub_dir

                    ### check if item already in list


                    ### update user's parcours adding item
                    users_mongo.update_one(
                        {key_n_carte : session[key_n_carte] },
                        {"$push"     : {
                            parcours_sub_dir : item_dict,
                            }
                        }
                        # upsert = True
                    )

                    ### reset user's data
                    session["is_userdata"] = False
                    return redirect( url_for('index') )


            else :
                sessionError = u'code barre non valide'
                flash(sessionError, "warning" )
                return redirect( url_for('index') )


        ### UPDATE USER EMPRUNTS HISTORY FROM FORM
        elif req_type == "update_history" and isUser :

            print "---- INDEX / POST / update_history "
            card_number   = session[key_n_carte]

            ### flash and redirect if no valid card
            if len(card_number)!= 6 :
                flash( u"vous n'avez pas de carte valide à " + app_bib_infos["biblio"], "warning")
                session["is_userdata"] = False
                flash( u"seules vos lectures et vos envies ont été mises à jour ", "warning")
                return redirect( url_for('index') )

            else :
                form = UserHistoryAloesForm(request.form)

                if form.validate():
                    print "---- INDEX / POST / update_history ---- form valid : request WS_user_hist() "
                    card_password = request.form['cardPassword']

                    WS_user_hist(card_number=card_number, password=card_password)
                    session["is_userdata"] = False
                    return redirect( url_for('index') )

                else :
                    flash(u'merci de réessayer', "warning")



        ### LOG IN or REGISTER
        elif req_type == 'log' or req_type == 'reg' or req_type == 'logout' :

            userName     = request.form['userName'].encode('utf-8')
            userCard     = request.form['userCard']
            userPassword = request.form['userPassword'].encode('utf-8')

            session["is_userdata"] = False

            print "---- INDEX / POST / log-reg-logout ---- userName : ",     userName
            print "---- INDEX / POST / log-reg-logout ---- userCard : ",     userCard
            print "---- INDEX / POST / log-reg-logout ---- userPassword : ", userPassword

            print "---- INDEX / POST / log-reg-logout ---- searching for existing user "
            try :
                existing_user = users_mongo.find_one( { key_n_carte : userCard } )
                if not existing_user:
                    raise ValueError('empty string')
            except :
                existing_user = users_mongo.find_one( { key_username : userName } )

            if existing_user != None :
                print "---- INDEX / POST / log-reg-logout ---- existing user : ", existing_user[ key_username ]


            ### if form == register
            if existing_user is None and req_type == "reg":

                form = UserRegisterForm(request.form)

                userIsCard    = True
                userEmail     = form.userEmail.data
                userStatus    = 'read'

                if form.validate():

                    ### generate dummy card number if does not exist
                    # Magalie : 915526
                    if userCard == "" or len(userCard)!= 6 :
                        userIsCard        = False
                        countNotRegistred = users_mongo.find( { key_is_card : False} ).count()
                        userCard          = "X" + str(countNotRegistred+1)

                    ### create new user in MongoDB
                    hashpass   = bcrypt.hashpw(userPassword, bcrypt.gensalt() )
                    users_mongo.insert({
                                  key_username   : userName,
                                  key_email      : userEmail,
                                  key_n_carte    : userCard,
                                  key_is_card    : userIsCard,
                                  key_password   : hashpass,  ### or simply userPassword
                                  key_status     : userStatus,
                                  key_parcours : {
                                    parcours_status_[0] : [],
                                    parcours_status_[1] : [],
                                    parcours_status_[2] : [],
                                  } ,
                                  #'test'     : ["value1", "value2"]
                                  })
                    session[key_username] = userName
                    session[key_n_carte]  = userCard
                    session[key_email]    = userEmail
                    session[key_user_id]  = str(users_mongo.find_one({ key_n_carte : userCard })[key_user_id])

                    print "---- INDEX / POST / reg ---- new user inserted in MongoDB / users_mongo -------- "

                    flash(u'vous êtes connecté(e)', "success")
                    return redirect( url_for('index') )

                else:
                    sessionError = u'non enregistré - cette carte ou ce pseudo sont déjà utilisés ou mauvais password'
                    flash(sessionError, "warning" )
                    return redirect( url_for('index') )

            ### if form == log in
            elif existing_user and req_type == "log" :

                form = LoginForm(request.form)
                print "---- INDEX / POST / log ---- LoginForm : ", form.userName, form.userPassword, form.userPassword.data
                print "---- INDEX / POST / log ---- LoginForm validation : ", form.validate() #, form.validate_on_submit()

                if form.validate() and bcrypt.hashpw( userPassword, existing_user['password'].encode('utf-8') ) == existing_user['password'].encode('utf-8') :
                    session[key_username]    = existing_user[key_username]
                    session[key_n_carte]     = existing_user[key_n_carte]
                    session[key_email]       = existing_user[key_email]
                    session[key_user_id]     = str(existing_user[key_user_id])
                    # session["is_userdata"] = False
                    # isUser                 = session['username']
                    # flash(u'vous êtes connecté en tant que ' + isUser, "success")
                    return redirect(url_for('index') )

                sessionError = u'non connecté - mauvais pseudo ou mauvais password'
                flash(sessionError, "warning")
                return redirect( url_for('index') )

            ### no valid user REQUEST
            else :
                print "---- INDEX / POST ---- problem filling the form, please try again ! --------------- "
                sessionError = u"problème lors de votre login, merci de retenter"
                flash(sessionError, "warning")
                return redirect( url_for('index') )


    print "---- INDEX END ---- session : %s " % ( session )

    return render_template('index.html',
                           app_metas            = app_metas,
                           app_colors           = app_colors,
                           app_bib_infos        = app_bib_infos,
                           dict_db_user         = dict_db_user,
                           bootstrap_vars       = bootstrap_vars,
                           session_u            = session,

                           user_data            = user_data,
                           user_parcours        = user_parcours,

                           parcours_indexes     = parcours_indexes,
                           isUser               = isUser,
                           isAdmin              = isAdmin,
                           sessionError         = sessionError,

                           loginForm            = loginForm,
                           registerForm         = registerForm,
                           aloesForm            = aloesForm,
                           userUpdateForm       = userUpdateForm,
                           requestCabForm       = requestCabForm
    )

### LOGOUT ######
@app.route('/logout', methods=['GET', 'POST'])
def logout() :
    print "XXX"*50
    print " XXXX - EXIT - XXXX "
    # print "XXXX - EXIT - before popping session : ", session

    session.clear()
    cache.clear()

    # session.pop('username', None)
    # session.pop('n_carte', None)
    print " XXXX - EXIT - session : ", session
    print "XXX"*50

    flash(u'vous êtes maintenant déconnecté(e)', "success")
    return redirect( url_for('index') )


@app.route('/view_3D')
def view_3D():

    print
    print "/// test access mongoDB / users "
    return render_template('synapse_3D.html')
    # return render_template('snippet_3D.html')


########################################################################################
### SOCKETIO FUNCTIONS #######################

@socketio.on('connect_')
def test_connect():
    print "***** socket io >>> CONNECTED "
    # emit('my response', {'data': 'Connected'})


@socketio.on('io_request_infos_list')
def return_infos_list(request_client):

    print "***** socket_io >>> return_infos_list / request_client : ", request_client

    inp_type = request_client["inp_type"]
    print "***** socket_io >>> return_infos_list / inp_type : ", inp_type
    query    = u".*" + request_client["data"] + u".*"
    print "***** socket_io >>> return_infos_list / query : ", query

    if inp_type == "inp_titles" :
        key_src = key_title

    elif inp_type == "inp_authors" :
        key_src = key_author

    list_infos_ = notices_mongo.find(   { key_src : { "$regex" : query, "$options" : "i" } },
                                        { "_id" : 0, key_src : 1 } )
    # print "***** socket_io >>> return_titles_list / list_titles_.distinct(key_title) : ", list_titles_.distinct( key_title )
    # list_titles  = list(list_titles_)
    # list_titles  = [ v[key_title] for v in list_titles ]
    list_infos  = list_infos_.distinct( key_src )
    print "***** socket_io >>> return_infos_list / list_titles : ", list_infos[:5], "..."
    print

    emit('io_resp_infos_list', { 'data': list_infos, "resp_type" : inp_type } )


@socketio.on('io_request_cab')
def return_cab(request_client):

    print "***** socket_io >>> return_cab / request_client : ", request_client

    title         = request_client["data"]
    notice_       = notices_mongo.find_one( { key_title : title } )

    if notice_ != None :
        notice_author = notice_[key_author]
        notice_resume = notice_[ key_resume ]
        print "***** socket_io >>> return_cab / notice_ : ", notice_

        notice_ido = notice_[ key_synapse ]
        ex_        = exemplaires_mongo.find_one({ key_synapse : notice_ido })
        print "***** socket_io >>> return_cab / ex_ : ", ex_

        ex_cab     = ex_[ key_barcode ]

        print "***** socket_io >>> return_cab / ex_cab : ", ex_cab
        print

    else :
        ex_cab        = unknown_cab
        notice_author = unknown_author
        notice_resume = unknown_resume

    emit( 'io_resp_cab', { 'cab' : ex_cab, 'author' : notice_author, 'resume' : notice_resume } )


@socketio.on('io_request_refs')
def return_refs_list(request_client):

    print "***** socket_io >>> return_refs_list / request_client : ", request_client

    author     = request_client["data"]
    refs_list_ = notices_mongo.find( { key_author : author }, { "_id" : 0, key_title : 1, key_synapse : 1 } )
    unique_titles  = refs_list_.distinct(key_title)
    unique_titles.sort()
    print "***** socket_io >>> return_refs_list / refs_list : ", unique_titles

    refs = []
    for ref in unique_titles :
        not_   = notices_mongo.find_one( { key_title : ref} )
        resume = not_[key_resume]
        ex_    = exemplaires_mongo.find_one( { key_synapse : not_[key_synapse] } )
        cab    = ex_[ key_barcode ]
        ref_dict = {}
        ref_dict[key_group_level_2] = dict_reverse_C2[not_[key_group_level_2]]
        ref_dict[key_barcode] = cab
        ref_dict[key_title]   = ref
        ref_dict[key_resume]  = resume
        refs.append(ref_dict)

    print "***** socket_io >>> return_refs_list / refs : ", refs
    print

    emit( 'io_resp_refs', { 'refs_list' : refs , "author" : author , 'unique_titles' : unique_titles } )


@socketio.on('io_request_oneref')
def return_oneref(request_client):

    print "***** socket_io >>> return_oneref / request_client : ", request_client
    cab     = request_client["data"]
    ref     = exemplaires_mongo.find_one( { key_barcode : cab })
    print "***** socket_io >>> return_oneref / ref : ", ref

    if ref != None :
        ref_ido = ref[key_synapse]
        notice  = notices_mongo.find_one({ key_synapse : ref_ido })
        author  = notice[key_author]
        title   = notice[key_title]
        resume  = notice[key_resume]
    else:
        author = unknown_author
        title  = unknown_title
        resume = unknown_resume

    print "***** socket_io >>> return_oneref / cab : %s / author : %s / title : %s " %( cab, author, title )
    print

    emit( 'io_resp_oneref', { "author" : author , 'title' : title , 'resume' : resume } )


@socketio.on('io_delete_from_parcours')
def delete_items_list(request_client):

    print "***** socket_io >>> delete_items_list / request_client : ", request_client["data"]
    cab_dict = request_client["data"]

    user_id  = ObjectId( session[ key_user_id ] )
    print "***** socket_io >>> delete_items_list / user_id : ", user_id

    # user_mongo = users_mongo.find_one({key_user_id : user_id})
    # print "***** socket_io >>> delete_items_list / user_mongo['username'] : ", user_mongo[key_username]
    for item_categ, cab_list in cab_dict.iteritems() :
        parcours_sub_dir = ".".join( [ key_parcours, item_categ ] )
        print "***** socket_io >>> delete_items_list / parcours_sub_dir : ", parcours_sub_dir
        # remove items corresponding to cab_list from user's data in mongodb
        users_mongo.update(  { key_user_id : user_id },
                             { "$pull" : {  parcours_sub_dir : {
                                            key_barcode : { "$in" : cab_list }
                                            }
                                        }
                             },
                        )

    session["is_userdata"] = False
    flash(u'les références ont bien été effacées de votre parcours', "success")
    return redirect( url_for('index') )
