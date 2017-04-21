# -*- encoding: utf-8 -*-

from .. import app, STATIC_DATA, SITE_STATIC, SITE_ROOT
from .app_db_settings import *

import pandas as pd
import numpy as np

# current working directory
# cwd = os.getcwd()

'''
# relations exemplaires-notices
key_exemplaires = "id_origine"
key_notices     = "identifiant_origine"
key_synapse     = "id_o"

# index(s) à garder
indices_exemplaires = [ key_exemplaires, "emplacement", "section", "cote", "cab" ]
indices_notices     = [ key_notices, "titre", "auteur_princ", "date_import", "deleted", "resume"] #, "provenance" ]
'''

#### distant DBs : MySQL and SOAP service
import zeep
from   flask_mysqldb import MySQL


#### local DBs : MongoDB
from   flask_pymongo import PyMongo ### flask_pymongo instead of flask.ext.pymongo
#### db : MongoDB connection /// PLACED IN CONFIG.PY AT ROOT with tokens

# set as OK to run with app.context()
with app.app_context():
    mongo = PyMongo(app)
    print "starting app --- MongoDB connected"
    ### access mongodb collections ###
    users_session     = mongo.db.users
    notices_mongo     = mongo.db.notices
    exemplaires_mongo = mongo.db.exemplaires


class get_df_from_MySQL :

    # def __init__ (self) :
        # cf : http://flask-mysqldb.readthedocs.io/en/latest/
        # print "starting app --- mySQL catalogue connected"

    def get_df_exemplaires(self) :

        mysql_catalogue = MySQL(app)
        print ">>> get_df_from_MySQL.get_df_exemplaires --- MySQL connected"

        # connect to MYSQL
        df_exemplaires = pd.read_sql('SELECT * FROM exemplaires', con=mysql_catalogue)

        # reduce information / columns
        df_exemplaires_light = df_exemplaires[indices_exemplaires].copy()

        # rename id_origine
        df_exemplaires_light = df_exemplaires_light.rename(columns = {key_exemplaires:key_synapse})

        mysql_catalogue.close()

        return df_exemplaires_light

    def get_df_notices(self) :

        mysql_catalogue = MySQL(app)
        print ">>> get_df_from_MySQL.get_df_notices --- MySQL connected"

        # connect to MYSQL
        df_notices = pd.read_sql('SELECT * FROM notices', con=mysql_catalogue)

        # reduce information / columns
        df_notices_light = df_notices[indices_notices].copy()

        # rename id_origine
        df_notices_light = df_notices_light.rename(columns = {key_notices:key_synapse})

        mysql_catalogue.close()

        return df_exemplaires_light


class mongodb_updates :

    def __init__(self) :

        print ">>> mongodb_updates --- "

        self.df_exemplaires_light = get_df_from_MySQL.df_exemplaires()
        self.df_notices_light     = get_df_from_MySQL.df_notices()
        self.static_filename      = json_filename
        self.static_filepath      = os.path.join( STATIC_DATA, self.static_filename )

    def reset_coll(coll_mongo, df_mysql_light, key_ ) :

        ### remove all documents
        coll_mongo.drop()

        ### drop duplicated records
        #print "df_mysql_light.shape : ", df_mysql_light.shape
        df_records_light = df_mysql_light.copy().drop_duplicates(key_)

        ### to JSON
        records_json = json.loads(df_records_light.T.to_json()).values()

        ### insert JSON exemplaires_new_records to mongoDB
        coll_mongo.insert_many(records_json)

        # print "... coll_mongo reset"
        # print "... coll_mongo.count() : ", coll_mongo.count()

    def check_write_new_records (old_db_mongo, new_df_mysql_light, id_ ) :

        ### get existing "cab" exemplaires from old_db_mongo
        list_old_ids = old_db_mongo.distinct(id_)
        # print "list_old : ", list_old_ids[:3], "..."

        ### get existing "id_" exemplaires from new_df_mysql_light
        list_new_ids = new_df_mysql_light[id_].tolist()
        # print "list_new : ", list_new_ids[:3], "..."

        ### get difference between new and old cab lists
        new_records_ids = list(set(list_new_ids)-set(list_old_ids))
        # print "new_records_ids : ", new_records_ids[:3], "..."
        # print "new_records_ids length : ", len(new_records_ids)

        if len(new_records_ids) > 0 :

            ### only get new records from dataframe
            df_new_records_light = new_df_mysql_light.copy().loc[new_df_mysql_light[id_].isin(new_records_ids)]

            ### to JSON
            new_records_json = json.loads(df_new_records_light.T.to_json()).values()
            # print "..."

            ### insert JSON exemplaires_new_records to mongoDB
            old_db_mongo.insert_many(new_records_json)

            # print "df_new_records_light inserted to old_db_mongo"

        return new_records_ids

    def reset_coll_exemplaires(self) :
        reset_coll(exemplaires_mongo, self.df_exemplaires_light, key_barcode )

    def reset_coll_notices(self) :
        reset_coll(notices_mongo,     self.df_notices_light, key_synapse)

    def update_all(self) :
        new_exemplaires = check_write_new_records(exemplaires_mongo, self.df_exemplaires_light, key_barcode )
        new_notices     = check_write_new_records(notices_mongo,     self.df_notices_light,     key_synapse )

    def write_notices_json_file(self):
        ### this file will be used to render the THREE.JS --> needs to be light --> only keep ID_O
        # cf : https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/
        notices_light = notices_mongo.find( {}, { "_id":0, key_synapse :1 } )
        with open(self.static_filepath, "w") as f:
            json.dump(list(notices_light), f)

    def get_notices_json(self):
        ### this file will be used to render the THREE.JS --> needs to be light --> only keep ID_O
        notices_light = notices_mongo.find( {}, { "_id":0, key_synapse :1 } )
        return json.dumps(notices_light)
