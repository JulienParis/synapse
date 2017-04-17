# -*- encoding: utf-8 -*-

from app import app
import os


### SESSIONS CONFIG
SECRET_KEY          = 'DZEGQdzqrscv;_qrs123-tb#dzefs36421u'
app.secret_key      = 'fsrDRstQSFQSWXdsfg@ééE4Tgg§557UUre-reEEE_4Z'


### FORMS CONFIG
WTF_CSRF_ENABLED    = True
WTF_CSRF_SECRET_KEY = '23QBWBgrfzqsdqsdftSGDYSet-!(5q34gsQRVdsqf<ds)*$'


### MONGO DB CONFIG - production
# MONGO_DBNAME = 'synapse_test'
# MONGO_URI    = 'mongodb://127.0.0.1:27017/synapse_test'

### MONGO DB CONFIG - test / connecting on localhost
MONGO_DBNAME = 'synapse_test'
MONGO_URI    = 'mongodb://127.0.0.1:27017/synapse_test'
