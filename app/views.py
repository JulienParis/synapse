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
from werkzeug.contrib.cache import SimpleCache



### forms classes
from .forms import LoginForm, UserRegisterForm, UserHistoryAloesForm

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
        print '**** Is_Admin **** you are logged in as : ' + session['username']
        isUser        = session['username']

        existing_user = users_mongo.find_one({'n_carte' : session['n_carte'] })
        print '**** Is_Admin ****  existing_user : ', isUser

        if existing_user['status'] == 'admin' :
            isAdmin = True

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

### CACHES
### cf; : http://werkzeug.pocoo.org/docs/0.12/contrib/cache/#werkzeug.contrib.cache.BaseCache.set
cache = SimpleCache()

def set_cache( data, cache_name="parcours" ) :
    print
    print "++++ set_cache ++++ ", cache_name
    cache.set( cache_name, data)
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
    print '~ ~ ~ WS_user_hist --- session["username"] : ', session['username']
    print '~ ~ ~ WS_user_hist --- session["n_carte"]  : ', session['n_carte']
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
                WS_user_ = users_mongo.find_one( {'n_carte' : card_number } )
                print '~ ~ ~ WS_user_hist --- username        : ', WS_user_['username']
                print '~ ~ ~ WS_user_hist --- password mongo  : ', WS_user_['password'].encode('utf-8')

                print '~ ~ ~ WS_user_hist --- bcrypt password : ', bcrypt.hashpw( password.encode('utf-8'), WS_user_['password'].encode('utf-8') )
                check_pw = bcrypt.hashpw( password.encode('utf-8'), WS_user_['password'].encode('utf-8') ) == WS_user_['password'].encode('utf-8')
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
                {"n_carte" : card_number},
                {"$set" : {
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
    loginForm    = LoginForm()
    registerForm = UserRegisterForm()
    aloesForm    = UserHistoryAloesForm()

    isUser, isAdmin  = Is_Admin()
    print "---- INDEX ---- isAdmin : %s " % ( isAdmin )
    print "---- INDEX ---- isUser  : %s " % ( isUser )
    print "---- INDEX ---- session : %s " % ( session )
    print

    ### RETRIEVE COMPLETE DATA PARCOURS AND STORE IT IF USER
    if isUser :

        is_userdata = session["is_userdata"]

        user_rawdata  = users_mongo.find_one( { "n_carte" : session["n_carte"] }, { "_id":0, "password":0, "status":0 } )
        user_data = { key : user_rawdata[key] for key in user_rawdata.keys() if key not in ["parcours"] }
        print "---- INDEX ---- is_userdata ---- user_data :", user_data
        print "---- INDEX ---- is_userdata :", is_userdata


        if is_userdata == False :

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
                        ex_rendu  = emprunt_data[key_rendu_date]
                    except :
                        ex_rendu  = "."

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
                        key_title        : ex_author,
                        key_author       : ex_title,
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

            user_parcours_ = json.dumps( user_parcours )
            # print "---- REAL user_parcours_ : %s " %(user_parcours_)
            print "---- REAL user_parcours_ ---- isinstance(user_parcours_, str) :",  isinstance(user_parcours_, str)

            # user_parcours_ = json.dumps({"Test" : 1, "nest" : [ {"A" : False }, {"B" : None } ] })
            # print "---- FAKE user_parcours_ : %s " %(user_parcours_)
            # print "---- FAKE user_parcours_ ---- isinstance(user_parcours_, str) :",  isinstance(user_parcours_, str)

            set_cache(user_parcours_, cache_name="parcours")

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
            user_parcours_ = get_cache( cache_name="parcours" )

            print "---- INDEX ---- is_userdata : TRUE ---- user_parcours_ "
            user_parcours  = json.loads(user_parcours_)

            print

    else :
        user_data     = None
        user_parcours = None
    # user_parcours     = user_rawdata["parcours"]
    # print "---- INDEX ---- user_parcours : ", user_parcours


    ### if REQUEST == POST is sent from a form : login / register / refresh site
    if request.method == 'POST' :

        print "-"*60

        req_type = request.form['req_type'] ### always add as hidden input in forms
        print "---- INDEX ---- request.form : ", request.form


        ### UPDATE USER EMPRUNTS HISTORY FROM FORM
        if req_type == "update_history" and isUser :

            card_number   = session['n_carte']

            ### flash and redirect if no valid card
            if len(card_number)!= 6 :
                flash( u"vous n'avez pas de carte valide à " + app_bib_infos["biblio"], "warning")

            else :
                form = UserHistoryAloesForm(request.form)

                if form.validate():
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

            print "---- INDEX ---- userName : ",     userName
            print "---- INDEX ---- userCard : ",     userCard
            print "---- INDEX ---- userPassword : ", userPassword

            try :
                existing_user = users_mongo.find_one({'username' : userName })
                if not existing_user:
                    raise ValueError('empty string')
            except :
                existing_user = users_mongo.find_one({'n_carte' : userCard })
            print "---- INDEX ---- existing user : ", existing_user["username"]


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
                        countNotRegistred = users_mongo.find( {"is_card": False} ).count()
                        userCard          = "X" + str(countNotRegistred+1)

                    ### create new user in MongoDB
                    hashpass   = bcrypt.hashpw(userPassword, bcrypt.gensalt() )
                    users_mongo.insert({'username' : userName,
                                  'email'      : userEmail,
                                  'n_carte'    : userCard,
                                  'is_card'    : userIsCard,
                                  'password'   : hashpass,  ### or simply userPassword
                                  'status'     : userStatus,
                                  key_parcours : {
                                    parcours_status_[0] : [],
                                    parcours_status_[1] : [],
                                    parcours_status_[2] : [],
                                  } ,
                                  #'test'     : ["value1", "value2"]
                                  })
                    session['username'] = userName
                    session['n_carte']  = userCard

                    print "---- INDEX ---- new user inserted in MongoDB / users_mongo -------- "

                    flash(u'vous êtes connecté', "success")
                    return redirect( url_for('index') )

                else:
                    sessionError = u'non enregistré - cette carte ou ce pseudo sont déjà utilisés ou mauvais password'
                    flash(sessionError, "warning" )
                    return redirect( url_for('index') )

            ### if form == log in
            elif existing_user and req_type == "log" :

                form = LoginForm(request.form)
                print "---- INDEX ---- LoginForm : ", form.userName, form.userPassword, form.userPassword.data
                print "---- INDEX ---- LoginForm validation : ", form.validate() #, form.validate_on_submit()

                if form.validate() and bcrypt.hashpw( userPassword, existing_user['password'].encode('utf-8') ) == existing_user['password'].encode('utf-8') :
                    session['username']    = existing_user["username"]
                    session['n_carte']     = existing_user["n_carte"]
                    # session["is_userdata"] = False
                    # isUser                 = session['username']
                    # flash(u'vous êtes connecté en tant que ' + isUser, "success")
                    return redirect(url_for('index') )

                sessionError = u'non connecté - mauvais pseudo ou mauvais password'
                flash(sessionError, "warning")
                return redirect( url_for('index') )

            ### no valid user REQUEST
            else :
                print "---- INDEX ---- problem filling the form, please try again ! --------------- "
                sessionError = u"problème lors de votre login, merci de retenter"
                flash(sessionError, "warning")
                return redirect( url_for('index') )


    print "---- INDEX END ---- session : %s " % ( session )

    return render_template('index.html',
                           app_metas            = app_metas,
                           app_colors           = app_colors,
                           app_bib_infos        = app_bib_infos,
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
    )

### LOGOUT ######
@app.route('/logout', methods=['GET', 'POST'])
def logout() :
    print "XXX"*50
    print " XXX - EXIT - XXX "
    # print " XXX - EXIT - before popping session : ", session

    session.clear()
    cache.clear()

    # session.pop('username', None)
    # session.pop('n_carte', None)
    print " XXX - EXIT - before popping session : ", session
    print "XXX"*50

    flash(u'vous êtes maintenant déconnecté(e)', "success")
    return redirect( url_for('index') )



########################################################################################
### SOCKETTIO FUNCTIONS #######################

@socketio.on('io_request_user')
def return_user_data(request_client):

    print
    print "***** io_request_user / request from client : ", request_client

    user_name  = request_client['user_name']
    user_card  = request_client['user_card']

    # find corresponding user
    user_mongo = users_mongo.find( { "$or": [ { "n_carte": user_card }, { "username" : user_name } ] } )

    # convert cursor to json
    user_json  = json.dumps(user_mongo)

    # send results
    results = {
            'request_sent' : request_client,
            'user'         : user_json
            }

    ### emit the json
    emit( 'io_user_from_server', results )
