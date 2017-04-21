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


from scripts.app_settings import bootstrap_vars, app_colors, app_metas, ALLOWED_EXTENSIONS
from scripts.app_db_settings import authorized_collections


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
### MONGODB ROUTES #####

@app.route('/users')
def get_users():

    print
    print "/// test access mongoDB / users "

    users = users_session.find( {}, { "_id":0 , "password" : 0 })

    json_users = dumps(users, default=json_util.default)
    #json_users = df_users.to_json(orient="records", default_handler=str)
    return json_users


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

            print "---- userName : ", userName
            print "---- userCard : ", userCard
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
                                  'email'    : userEmail,
                                  'n_carte'  : userCard,
                                  'is_card'  : userIsCard,
                                  'password' : hashpass,  ### or simply userPassword
                                  'status'   : userStatus,
                                  'parcours' : [ ],
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
