# -*- encoding: utf-8 -*-

import os
import gc ### aka garbage collector

from .. import app, STATIC_DATA, SITE_STATIC, SITE_ROOT #, mysql_catalogue
from .app_db_settings import *

import pandas as pd
from pandas.io import sql

import numpy as np

import json
from   bson import json_util
from   bson.objectid import ObjectId
from   bson.json_util import dumps

# current working directory
# cwd = os.getcwd()

from pprint import pprint

#### distant DBs : MySQL
from   flask_mysqldb import MySQL
#from flask.ext.mysqldb import MySQL


#### local DBs : MongoDB
from   flask_pymongo import PyMongo ### flask_pymongo instead of flask.ext.pymongo
#### db : MongoDB connection /// PLACED IN CONFIG.PY AT ROOT with tokens

# set as OK to run with app.context()
with app.app_context():

    ### set mysql connection
    mysql_catalogue = MySQL(app)

    # cur = mysql_catalogue.connection.cursor()
    # cur.execute('''SELECT * FROM exemplaires''')
    # rows           = cur.fetchall()
    # df_exemplaires = pd.DataFrame( [[ij for ij in i] for i in rows] )
    # print df_exemplaires.head()


    print "starting app --- mysql_catalogue connected"


    mongo = PyMongo(app)
    print "starting app --- MongoDB connected"
    ### access mongodb collections ###
    users_mongo       = mongo.db.users
    notices_mongo     = mongo.db.notices
    exemplaires_mongo = mongo.db.exemplaires

    mongoColls = {  "notices"     : notices_mongo,
                    "exemplaires" : exemplaires_mongo,
                    "users"       : users_mongo,
                }



def get_df_from_MySQL(coll) :

    #def __init__ (self, coll) :
    # cf : http://flask-mysqldb.readthedocs.io/en/latest/
    print ">>> get_df_from_MySQL ---,  %s --- start " %(coll), "--"*50

    #self.coll = coll

    #cf = app.config
    #print cf

    ### connect to distant MySQL
    #with app.app_context():
    # mysql_catalogue = MySQL(app)
    #mysql_catalogue = MySQL().init_app(app)
    #mysql_catalogue = MySQL.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    #mysql_catalogue = MySQL.connect(cf['MYSQL_HOST'], cf['MYSQL_USER'], cf['MYSQL_PASSWORD'], cf['MYSQL_DB'])

    #with app.app_context():

    query_string = '''SELECT * FROM %s''' %(coll)
    print ">>> get_df_from_MySQL --- query_string : ", query_string
    print ">>> get_df_from_MySQL --- indices_mysql[ coll ]['ind'] : ",indices_mysql[ coll ]['ind']
    cur = mysql_catalogue.connection.cursor()

    print '>>> get_df_from_MySQL --- %s --- df_sql' %(coll), '--'*50
    df_sql = pd.read_sql( query_string , con=mysql_catalogue.connection)
    print df_sql.head(3)


    print '>>> get_df_from_MySQL --- %s --- df_sql_light' %(coll), '--'*50

    # cur.execute(query_string)
    # rows           = cur.fetchall()
    # df_sql = pd.DataFrame( [[ij for ij in i] for i in rows] )
    # print df_sql.head()

    # reduce information / columns
    df_sql_light = df_sql[ indices_mysql[ coll ]['ind'] ].copy()
    print df_sql_light.head(3)

    ### trying to empty memory for better performance
    del df_sql
    gc.collect()
    print '>>> get_df_from_MySQL --- EMPTYING MEMORY', '--'*50

    print '>>> get_df_from_MySQL --- %s --- df_sql_light renamed' %(coll), '--'*50

    # rename id_origine
    df_sql_light = df_sql_light.rename(columns = { indices_mysql[coll ]['key'] : key_synapse})
    print df_sql_light.head(3)

    # mysql_catalogue.close()
    # print ">>> get_df_from_MySQL.get_df_notices --- MySQL closed"

    print ">>> get_df_from_MySQL --- %s --- finished" %(coll)
    print

    return df_sql_light




    # def get_df_exemplaires(self) :
    #
    #     print ">>> get_df_from_MySQL.get_df_exemplaires --- MySQL connected"
    #
    #     # connect to MYSQL
    #     #df_exemplaires = pd.read_sql('SELECT * FROM exemplaires', con=mysql_catalogue)
    #
    #     # reduce information / columns
    #     df_exemplaires_light = df_exemplaires[indices_exemplaires].copy()
    #
    #     # rename id_origine
    #     df_exemplaires_light = df_exemplaires_light.rename(columns = {key_exemplaires:key_synapse})
    #
    #     mysql_catalogue.close()
    #     print ">>> get_df_from_MySQL.get_df_exemplaires --- MySQL closed"
    #
    #     return df_exemplaires_light
    #
    #
    # def get_df_notices(self) :
    #
    #     print ">>> get_df_from_MySQL.get_df_notices --- MySQL connected"
    #
    #     # connect to MYSQL
    #     df_notices = pd.read_sql('SELECT * FROM notices', con=mysql_catalogue)
    #
    #     # reduce information / columns
    #     df_notices_light = df_notices[indices_notices].copy()
    #
    #     # rename id_origine
    #     df_notices_light = df_notices_light.rename(columns = {key_notices:key_synapse})
    #
    #     mysql_catalogue.close()
    #     print ">>> get_df_from_MySQL.get_df_notices --- MySQL closed"
    #
    #     return df_exemplaires_light


class mongodb_updates :

    def __init__(self) :

        print ">>> mongodb_updates --- "

        self.df_exemplaires_light = get_df_from_MySQL('exemplaires')
        self.df_notices_light_    = get_df_from_MySQL('notices')

        ### add emplacements codes in df_exemplaires_light
        self.df_exemplaires_light[key_group_level_1] = self.df_exemplaires_light['emplacement'].map(dict_emplacements_C1)
        self.df_exemplaires_light[key_group_level_2] = self.df_exemplaires_light['emplacement'].map(dict_emplacements_C2)

        ### add emplacements codes in df_notices_light by merging
        self.df_exemplaires_mini = self.df_exemplaires_light[[ key_synapse, 'C1', 'C2']].copy()
        self.df_notices_light    = pd.merge(self.df_notices_light_, self.df_exemplaires_mini, on='id_o')

        print '>>> mongodb_updates --- df_exemplaires_mini ', '--'*50
        print self.df_exemplaires_mini.sample(3)
        print '>>> mongodb_updates --- df_notices_light_ ', '--'*50
        print self.df_notices_light_.sample(3)

        ### empty memory from cache dataframes for performance issues
        print '>>> mongodb_updates --- EMPTYING MEMORY', '--'*50
        del self.df_exemplaires_mini
        del self.df_notices_light_
        gc.collect()



    def reset_coll(self, coll_name, coll_mongo, df_mysql_light, key_ ) :

        print ">>> mongodb_updates.reset_coll / for coll : ", coll_name
        ### remove all documents
        coll_mongo.drop()

        ### drop duplicated records
        # print "df_mysql_light.shape : ", df_mysql_light.shape
        df_records_light = df_mysql_light.copy().drop_duplicates(key_)

        ### to JSON
        records_json = json.loads(df_records_light.T.to_json()).values()

        ### insert JSON exemplaires_new_records to mongoDB
        coll_mongo.insert_many(records_json)

        print ">>> mongodb_updates.reset_coll / RESET FINISHED / for coll : ", coll_name
        print
        # print "... coll_mongo.count() : ", coll_mongo.count()


    def check_write_new_records (self, coll_name, old_db_mongo, new_df_mysql_light, id_ ) :

        print ">>> mongodb_updates.check_write_new_records / for coll : ", coll_name

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

            ### insert new_records_json to mongoDB
            old_db_mongo.insert_many(new_records_json)
            print ">>> mongodb_updates.check_write_new_records / df_new_records_light inserted to old_db_mongo"
            print

        return new_records_ids



    def reset_all_coll(self) :
        self.reset_coll("exemplaires", exemplaires_mongo, self.df_exemplaires_light, key_barcode )
        ### trying to empty memory for better performance
        del self.df_exemplaires_light
        gc.collect()
        print  ">>> mongodb_updates.update_all_coll / EMPTYING MEMORY : "

        self.reset_coll("notices",     notices_mongo,     self.df_notices_light, key_synapse)
        ### trying to empty memory for better performance
        del self.df_notices_light
        gc.collect()
        print  ">>> mongodb_updates.update_all_coll / EMPTYING MEMORY : "


    def update_all_coll(self) :
        new_exemplaires = self.check_write_new_records("exemplaires", exemplaires_mongo, self.df_exemplaires_light, key_barcode )
        print  ">>> mongodb_updates.update_all_coll / new_exemplaires : ", new_exemplaires

        ### trying to empty memory for better performance
        del self.df_exemplaires_light
        gc.collect()
        print  ">>> mongodb_updates.update_all_coll / EMPTYING MEMORY : "

        new_notices     = self.check_write_new_records("notices",     notices_mongo,     self.df_notices_light,     key_synapse )
        print  ">>> mongodb_updates.update_all_coll / new_notices : ", new_notices

        ### trying to empty memory for better performance
        del self.df_notices_light
        gc.collect()
        print  ">>> mongodb_updates.update_all_coll / EMPTYING MEMORY : "





class mongodb_read :

    def __init__(self,  coll, fields=None, limit=0, get_ligth=False) :

        print ">>> mongodb_read --- "
        self.coll = coll
        self.mongoColl  = mongoColls[ self.coll ]

        self.limit  = limit
        self.fields = fields
        self.query_fields = { "_id":0 }
        self.get_ligth = get_ligth

        if self.coll == "users" :
            self.query_fields["password"] = 0
            self.query_fields["email"] = 0


        if self.fields != None :
            for f in self.fields :
                self.query_fields[f] = 1
        elif self.fields == None and limit == 0 :
            self.get_ligth = True

        if self.get_ligth == True :
            if self.coll == "notices" :
                self.query_fields = {"_id":0, key_synapse:1}
            if self.coll == "exemplaires" :
                self.query_fields = {"_id":0, key_barcode:1}


        print ">>> mongodb_read --- coll : %s, limit : %s, fields : %s, get_ligth : %s "  %( coll, (self.limit if self.limit else "None"), (self.fields if self.fields!=[] else "None"), (self.get_ligth if self.get_ligth else "False"))


    def get_coll_as_json(self):

        coll_light = self.mongoColl.find( {}, self.query_fields ).limit(self.limit)

        # elif self.get_ligth == False :
        #
        #     ### this file will be used to render the THREE.JS --> needs to be light --> only keep ID_O
        #     # cf : https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/
        #     coll_light = self.mongoColl.find( {}, self.query_fields ).limit(self.limit)

        print ">>> mongodb_read --- get_coll_as_json / global count : %s documents " %( coll_light.count() )
        return coll_light


    def write_notices_json_file(self, nested=True, debug=False):

        print ">>> mongodb_read --- write_notices_json_file / start / nested = %s " %(nested)
        print

        static_filename = json_filename

        if nested == True :

            static_filename += "_nested"
            nodes_JSON = {}

            ### iterate through dict_emplacements_ to  create nested json

            for parent, values in dict_emplacements_.iteritems():
                name_parent             = values["PARENT"]
                nodes_JSON[name_parent] = { "CODE"     : parent,
                                            "CHILDREN" : [] ,
                                            "STATS"    : 0 }

                children_list           = nodes_JSON[name_parent]["CHILDREN"]

                print ">>> mongodb_read --- write_notices_json_file / nested : ", parent,"/", name_parent
                print

                ### iterate through CHILDREN
                for child in values["CHILDREN"] :

                    # print child, "/", child.keys()[0]
                    child_dict = { "NAME"    : child.values()[0],
                                   "CODE"    : child.keys()[0],
                                   "NOTICES" : [],
                                   "STATS"   : 0 }

                    ### get all notices for sub-group
                    for code, name in child.iteritems():
                        ### get notices from mongoDB with just their id_o
                        notices_     = notices_mongo.find( { key_group_level_2 : code }, self.query_fields )
                        notices_list = list(notices_)
                        ### add notices to child_dict
                        child_dict["NOTICES"]             = notices_list

                        # print "number notices for %s : %s" %( name, len(notices_list) )

                        # update stats
                        len_child_notices                 = len(notices_list)
                        child_dict["STATS"]               = len_child_notices
                        nodes_JSON[name_parent]["STATS"] += len_child_notices

                        # append child_dict to children_list
                        children_list.append(child_dict)



                        #print

                # print "-"*25

            print ">>> mongodb_read --- write_notices_json_file / in NESTED iteration / EMPTYING MEMORY "
            del children_list
            gc.collect()

            ### print in console for debugging purposes
            if debug == True :
                print
                print ">>> mongodb_read --- write_notices_json_file / nested : recap  "
                print

                for k, v in nodes_JSON.iteritems() :
                    print "code parent : %s / name parent : %s / stats : %s " %( v["CODE"], k, v["STATS"])
                    print

                    for e in v["CHILDREN"] :
                        print "    code : %s / name child : %s / len : %s / sample : %s " %(e["CODE"], e["NAME"], e["STATS"], e["NOTICES"][0])

                    print "-"*50
                    print




        elif nested == False :

            static_filename += "_raw"

            coll_light = self.get_coll_as_json()
            nodes_JSON = list(coll_light)


        static_filepath = os.path.join( STATIC_DATA, static_filename + json_extension )

        with open(static_filepath, "w") as f :
            json.dump( nodes_JSON , f)
            f.close()

        print ">>> mongodb_read --- write_notices_json_file / after writing JSON / EMPTYING MEMORY "
        del nodes_JSON
        gc.collect()


        print ">>> mongodb_read --- write_notices_json_file / finished "
        print "- "*70
