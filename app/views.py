# -*- encoding: utf-8 -*-
### author : Julien Paris - Jpy

import time, os
import datetime

from app   import app, socketio
from flask import Flask, flash, render_template, url_for, request, session, redirect
import bcrypt


from flask_socketio import emit #, send

from werkzeug.routing import Rule
from werkzeug.utils   import secure_filename


### forms classes
from .forms import LoginForm, UserRegisterForm

### db classes and functions
from scripts.databases_operations import *
import gc ### aka garbage collector

### webservice classes and functions
from scripts.webservice_operations import *


from scripts.app_settings import bootstrap_vars, app_colors, app_metas, ALLOWED_EXTENSIONS
from scripts.app_db_settings import authorized_collections, key_synapse


import json
from   bson import json_util
from   bson.objectid import ObjectId
from   bson.json_util import dumps
import itertools



########################################################################################
### INTERNAL FUNCTIONS  #####
def Is_Admin():

    # users_session = mongo.db.users
    isUser        = None
    isAdmin       = False

    if 'username' in session:
        print '**** Is_Admin **** you are logged in as : ' + session['username']
        isUser        = session['username']

        existing_user = users_session.find_one({'username' : session['username'] })
        print '**** Is_Admin ****  existing_user : ', existing_user

        if existing_user['status'] == 'admin' :
            isAdmin = True

    return isUser, isAdmin


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

    ### "/WS_users/?card_number=123456&password=PASSWORD"
    # isUser, isAdmin  = Is_Admin()
    # print isUser

    print '--- WS_user --- session : ', session['username']

    # check user status
    isUser, isAdmin  = Is_Admin()
    print '--- WS_user --- isUser : ', isUser

    WS_user = users_session.find_one( {'username' : session['username'] } )

    print '--- WS_user --- WS_user from mongoDB : ', WS_user
    print '--- WS_user --- WS_user password : ',     WS_user["password"]
    print


    print u'~ '*70


    if isAdmin or isUser :

        ### for internal use
        if card_number is None and password is None :

            ### user auth from args in URL
            card_number = request.args.get("card_number", None )
            password    = request.args.get("password", None )

            WS_user_ = users_session.find_one( {'n_carte' : card_number } )
            print bcrypt.hashpw( password, WS_user['password'].encode('utf-8') )
            print WS_user['password'].encode('utf-8')
            print bcrypt.hashpw( userPassword, existing_user['password'].encode('utf-8') ) == WS_user['password'].encode('utf-8')


        ### for common use
        else :
            ### get user from mongoDB
            WS_user     = users_session.find_one( {'username' : session['username'] } )
            card_number = WS_user["n_carte"]
            password    = WS_user["password"]


        print '--- WS_user --- card_number : %s / password : %s ' %(card_number, password)

        ###### retrieve infos from WEBSERVICE ######
        ### authentify user in WS
        user_req = WS_user_infos_(card_number, password)#.get_infos()

        ### retrieve user's history : exemplaires
        #user_  = user_req.get_infos()
        user_hist  = user_req.get_history()
        user_hist_list_cab = []

        for cab_ in user_hist.Entite.Donnees.Lignes :
            cab = cab_.ValeursDonnees.string
            #print cab[1]

            ### get corresponding notice for each cab from exemplaires_mongo
            try :
                exemplaire = exemplaires_mongo.find_one( {key_barcode : cab[1]} )
                #get id_o from exemplaire
                id_o_ex = exemplaire[key_synapse]
            except :
                id_o_ex = None

            ex_ = { key_barcode    : cab[1],
                    key_rendu_date : cab[6] ,
                    key_synapse    : id_o_ex ,
                    #key_parcours_status : parcours_status["emprunt"]
                    }

            user_hist_list_cab.append(ex_)

        print '--- WS_user --- user_hist_list_cab :  '
        #print user_hist_list_cab
        print

        ###### write / update into MongoDB.users : users_session ######
        user_mongo = users_session.find_one( {"n_carte" : card_number }, { "_id":0, "password":0 })
        #print user_mongo

        parcours_sub_dir = ".".join([ key_parcours, parcours_status_[0] ])
        #print parcours_sub_dir

        users_session.update_one(
            {"n_carte" : card_number},
            {"$set" : {
                parcours_sub_dir : user_hist_list_cab,
                key_lastupdate   : datetime.datetime.now()
                }
            } ,
            upsert = True
        )

    ### update user's "parcours"


    print '--- WS_user --- END '
    print '- '*70


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

        users = users_session.find( {}, { "_id":0 } ) #, "password" : 0 })

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

    ### DEFAULT SESSION VALUES
    isUser        = None
    isAdmin       = False
    sessionError  = None

    ### FORMS FROM WTF
    loginForm    = LoginForm()
    registerForm = UserRegisterForm()

    isUser, isAdmin  = Is_Admin()
    print "----- session : user %s / isAdmin %s " % (session, isAdmin)

    ### if REQUEST == POST is sent from a form : login / register / refresh site
    if request.method == 'POST' :

        print "-"*60

        req_type = request.form['req_type'] ### always add as hidden input in forms
        print "---- request.form : ", request.form

        ### LOG IN or REGISTER
        if req_type == 'log' or req_type == 'reg' or req_type == 'logout' :

            userName     = request.form['userName'].encode('utf-8')
            userCard     = request.form['userCard']
            userPassword = request.form['userPassword'].encode('utf-8')

            print "---- userName : ",     userName
            print "---- userCard : ",     userCard
            print "---- userPassword : ", userPassword

            try :
                existing_user = users_session.find_one({'username' : userName })
                if not existing_user:
                    raise ValueError('empty string')
            except :
                existing_user = users_session.find_one({'n_carte' : userCard })
            print "existing user : ", existing_user


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
                        userIsCard = False
                        countNotRegistred = users_session.find( {"is_card": False} ).count()
                        userCard = "X" + str(countNotRegistred+1)

                    ### create new user in MongoDB
                    hashpass   = bcrypt.hashpw(userPassword, bcrypt.gensalt() )
                    users_session.insert({'username' : userName,
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

                    print "------- new user inserted in MongoDB / users_session -------- "

                    flash(u'vous êtes connecté', "success")
                    return redirect( url_for('index') )

                else:
                    sessionError = u'non enregistré - cette carte ou ce pseudo sont déjà utilisés ou mauvais password'
                    flash(sessionError, "warning" )
                    return redirect( url_for('index') )

            ### if form == log in
            elif existing_user and req_type == "log" :

                form = LoginForm(request.form)
                print "---- LoginForm : ", form.userName, form.userPassword, form.userPassword.data
                print "---- LoginForm validation : ", form.validate() #, form.validate_on_submit()

                if form.validate() and bcrypt.hashpw( userPassword, existing_user['password'].encode('utf-8') ) == existing_user['password'].encode('utf-8') :
                    session['username'] = existing_user["username"]
                    isUser              = session['username']
                    # flash(u'vous êtes connecté en tant que ' + isUser, "success")
                    return redirect(url_for('index') )

                sessionError = u'non connecté - mauvais pseudo ou mauvais password'
                flash(sessionError, "warning")
                return redirect( url_for('index') )

            ### no valid user REQUEST
            else :
                print "------------ problem filling the form, please try again ! --------------- "
                sessionError = u"problème lors de votre login, merci de retenter"
                flash(sessionError, "warning")
                return redirect( url_for('index') )


    return render_template('index.html',
                           app_metas        = app_metas,
                           app_colors       = app_colors,
                           bootstrap_vars   = bootstrap_vars,
                           isUser           = isUser,
                           isAdmin          = isAdmin,
                           sessionError     = sessionError,
                           loginForm        = loginForm,
                           registerForm     = registerForm,
    )

### LOGOUT ######
@app.route('/logout', methods=['GET', 'POST'])
def logout() :
    print "XXX"*50
    print " XXX - EXIT - XXX "
    print session
    session.pop('username', None)
    flash(u'vous êtes maintenant déconnecté', "success")
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
    user_mongo = users_session.find( { "$or": [ { "n_carte": user_card }, { "username" : user_name } ] } )

    # convert cursor to json
    user_json  = json.dumps(user_mongo)

    # send results
    results = {
            'request_sent' : request_client,
            'user'         : user_json
            }

    ### emit the json
    emit( 'io_user_from_server', results )
