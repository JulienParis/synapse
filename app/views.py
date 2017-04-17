# -*- encoding: utf-8 -*-
### author : Julien Paris - Jpy

import time, os
import datetime
import json

from app   import app, socketio
from flask import Flask, flash, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo ### flask_pymongo instead of flask.ext.pymongo
import flask_mysqldb
import zeep
import bcrypt

from flask_socketio import emit #, send

from werkzeug.routing import Rule
from werkzeug.utils   import secure_filename
#app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_MODELS     = set(['obj', 'stl', 'js', 'json'])

### forms classes
from .forms import LoginForm, UserRegisterForm, ArticleForm, DeleteForm, CommentForm

#### db : MongoDB connection /// PLACED IN CONFIG.PY AT ROOT ####
mongo = PyMongo(app)
print "starting app --- MongoDB connected"



from scripts.app_settings import bootstrap_vars, app_colors, app_metas


import json
from   bson import json_util
from   bson.objectid import ObjectId
from   bson.json_util import dumps
import itertools

import pandas as pd
import numpy as np

### global variables Pandas
idx = pd.IndexSlice




########################################################################################
### INTERNAL FUNCTIONS  #####
def Is_Admin():

    users_session = mongo.db.users_session
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


@app.route('/add_user')
def add_user():

    print
    print "test access mongoDB "

    users = mongo.db.users
    # print users
    users.insert({'name' : 'Julien test'})
    return "user added"




########################################################################################
### ROUTING FUNCTIONS #######################

@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():

    return render_template('index.html',
                           app_metas        = app_metas,
                           app_colors       = app_colors,
                           bootstrap_vars   = bootstrap_vars,
    )

### LOGOUT ######
@app.route('/logout', methods=['GET', 'POST'])
def logout() :
    session.pop('username', None)
    flash('you are now logged out', "success")
    return redirect( url_for('index') )
