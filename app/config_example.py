# -*- encoding: utf-8 -*-

from app import app
import os

'''
CHANGE THIS FILENAME TO CONFIG.PY
AND UPDATE PASSWORD / CLIENT / URI ...
'''

### SESSIONS CONFIG
SECRET_KEY          = 'My_secret_key
app.secret_key      = 'My_app_secret_key'


### FORMS CONFIG
WTF_CSRF_ENABLED    = True
WTF_CSRF_SECRET_KEY = 'My_WTF_secret_key'


###### TESTS DBs CONFIG ######################################

### MONGO DB CONFIG - test / connecting on localhost
MONGO_DBNAME = 'My_Synapse_MongoDB_name'
MONGO_URI    = 'mongodb://127.0.0.1:27017/My_Synapse_MongoDB_name'


### MYSQLDB CONFIG / CATALOGUE (notices + exemplaires) / connecting on localhost
MYSQL_HOST     = '127.0.0.1'
MYSQL_USER     = 'client_name'
MYSQL_PASSWORD = 'My_MySQL_client_password'
MYSQL_DB       = 'My_MySQL_client_DB_name'
