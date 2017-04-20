# -*- encoding: utf-8 -*-
### author : Julien Paris - Jpy

import time, os
import datetime
import json

from app   import app, socketio
from flask import Flask, flash, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo ### flask_pymongo instead of flask.ext.pymongo
from flask_mysqldb import MySQL
import zeep
import bcrypt

from flask_socketio import emit #, send

from werkzeug.routing import Rule
from werkzeug.utils   import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#ALLOWED_MODELS     = set(['obj', 'stl', 'js', 'json'])

### forms classes
from .forms import LoginForm, UserRegisterForm



#### db : MongoDB connection /// PLACED IN CONFIG.PY AT ROOT ####
# cf :
mongo = PyMongo(app)
print "starting app --- MongoDB connected"

#### distant DBs : MySQL and SOAP service
# cf : http://flask-mysqldb.readthedocs.io/en/latest/
mysql_catalogue = MySQL(app)
print "starting app --- mySQL catalogue connected"



from scripts.app_settings import bootstrap_vars, app_colors, app_metas


import json
from   bson import json_util
from   bson.objectid import ObjectId
from   bson.json_util import dumps
import itertools

import pandas as pd
import numpy as np

### global variables Pandas
#idx = pd.IndexSlice




########################################################################################
### INTERNAL FUNCTIONS  #####
def Is_Admin():

    users_session = mongo.db.users
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




########################################################################################
### MONGODB ROUTES #####
@app.route('/users')
def sitemap_users():

    print
    print "test access mongoDB "

    users_list = []
    users      = mongo.db.users.find()
    # print users
    for user in users :
        users_list.append(user)
    json_users = json.dumps(users_list, default=json_util.default)
    return json_users


'''
@app.route('/add_user')
def add_user():

    print
    print "test access mongoDB "


    users = mongo.db.users
    # print users
    users_session.insert({'name' : 'Julien test'})
    return "user added"
'''



########################################################################################
### ROUTING FUNCTIONS #######################

@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():

    ### access mongodb collections ###
    users_session = mongo.db.users
    notices       = mongo.db.notices
    exemplaires   = mongo.db.exemplaires

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
            except :
                existing_user = users_session.find_one({'n_carte' : userCard })
            print "existing user : ", existing_user


            ### if form == register
            if existing_user is None and req_type == "reg":

                form = UserRegisterForm(request.form)

                userEmail     = form.userEmail.data
                userStatus    = 'read'

                if form.validate():

                    ### create new user in MongoDB
                    hashpass   = bcrypt.hashpw(userPassword, bcrypt.gensalt() )
                    users_session.insert({'username' : userName,
                                  'email'    : userEmail,
                                  'n_carte'  : userCard,
                                  'password' : hashpass,  ### or simply userPassword
                                  'status'   : userStatus,
                                  'parcours' : None
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
                    session['username'] = userName
                    isUser              = session['username']
                    flash(u'vous êtes connecté en tant que ' + userName, "success")
                    return redirect(url_for('index') )

                sessionError = u'non connecté - mauvais pseudo ou mauvais password'
                flash(sessionError, "warning")
                return redirect( url_for('index') )

            ### no valid user REQUEST
            else :
                print "------------ problem filling the form, please try again ! --------------- "
                sessionError = u"problème de connexion, merci de retenter"
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
