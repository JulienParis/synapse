# -*- encoding: utf-8 -*-

'''          SYNAPSE
--------------------------------------------

---------------------------------------------
licence
---------------------------------------------
project by : Julien Paris

'''

from flask import Flask
import os

### socketIO
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()


### local static dir name
static_dir = '/static'

### index root for server
URLroot_ = 'flask'

### basic folders addresses
SITE_ROOT             = os.path.realpath(os.path.dirname(__file__))
SITE_STATIC           = SITE_ROOT   +  static_dir
STATIC_DATA           = SITE_STATIC + '/data'
STATIC_DATA_MODELS    = SITE_STATIC + '/3dmodels'

#app = Flask(__name__)
app = Flask(__name__, static_path = SITE_STATIC ) ### change static directory adress to custom address for Flask

### get config.py for forms/DB config
app.config.from_object('config')

### set socketio
socketio = SocketIO(app)


from app import views
