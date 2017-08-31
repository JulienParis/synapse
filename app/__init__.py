# -*- encoding: utf-8 -*-

'''          SYNAPSE
--------------------------------------------

---------------------------------------------
licence    : .... 
---------------------------------------------
project by : Julien Paris

'''

from flask import Flask
import os
from   os import environ
import socket


### socketIO
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()

# from   flask_mysqldb import MySQL

### scheduler for utilities tasks
from   flask_apscheduler import APScheduler
import logging


### local static dir name
static_dir = '/static'

### index root for server
URLroot_ = 'flask'

### basic folders addresses
SITE_ROOT             = os.path.realpath(os.path.dirname(__file__))
SITE_STATIC           = SITE_ROOT   +  static_dir
STATIC_DATA           = SITE_STATIC + '/data'

### starting app
############################################################
#app = Flask(__name__)
app = Flask( __name__ , static_path = SITE_STATIC ) ### change static directory adress to custom address for Flask

### get config.py for forms/DB config and the rest
app.config.from_object('config')


### set socketio
############################################################
socketio = SocketIO( app, async_mode="eventlet" )



### set an apscheduler for updating the db / each 24h with cron at 4.00 am
############################################################

host_IP = socket.gethostbyname( socket.gethostname() )

print "__init__ / setting scheduler ... host_IP : ", host_IP
# logging.basicConfig()
scheduler               = APScheduler()
# scheduler.allowed_hosts = [ 'localhost', host_IP, app.config["SYNAPSE_IP"], "127.0.0.1" ]
scheduler.init_app( app )
scheduler.start()



from app import views
