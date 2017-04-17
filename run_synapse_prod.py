# -*- encoding: utf-8 -*-

#!venv/bin/python


from app import app, socketio
import os


if __name__ == '__main__':


    ### for production
    socketio.run(app, host='0.0.0.0')
