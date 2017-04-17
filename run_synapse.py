# -*- encoding: utf-8 -*-

#!venv/bin/python

from app import app, socketio
import os


port_  = 5000
debug_ = True


if __name__ == '__main__':

    if debug_ :

        print
        print "= " *70
        #print " - app.config : ", app.config
        print

    ### for development
    socketio.run(app, debug=debug_, port=port_)
