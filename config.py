# -*- encoding: utf-8 -*-

from app import app
import os


### SESSIONS CONFIG
SECRET_KEY          = 'DZEGQdzqrscv;_qrs123-tb#dzefs36421u'
app.secret_key      = 'fsrDRstQSFQSWXdsfg@ééE4Tgg§557UUre-reEEE_4Z'


### FORMS CONFIG
WTF_CSRF_ENABLED    = True
WTF_CSRF_SECRET_KEY = '23QBWBgrfzqsdqsdftSGDYSet-!(5q34gsQRVdsqf<ds)*$'


### MONGO DB CONFIG
MONGO_DBNAME = 'flaplab_DB'
MONGO_URI    = 'mongodb://admin:Pak0_6938@ds035026.mlab.com:35026/flaplab_DB'
