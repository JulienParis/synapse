# -*- encoding: utf-8 -*-


authorized_collections = ["notices", "exemplaires", "users"]

# relations exemplaires-notices
key_exemplaires = "id_origine"
key_notices     = "identifiant_origine"
key_synapse     = "id_o"
key_barcode     = "cab"
key_parcours    = "parcours"
key_parcours_status = "read_status"
key_rendu_date  = "date_rendu"

parcours_status = {
    "emprunt" : 0,
    "envie"   : 1,
    "lu"      : 2
}

parcours_status_ = ["emprunts","envies","lus"]

# index(s) to keep
indices_exemplaires = [ key_exemplaires, "emplacement", "section", "cote", "cab" ]
indices_notices     = [ key_notices, "titre", "auteur_princ", "date_import", "deleted", "resume"] #, "provenance" ]

# dict indices
indices_mysql = {
    'exemplaires' : {'ind' : indices_exemplaires , 'key' : key_exemplaires},
    'notices'     : {'ind' : indices_notices,      'key' : key_notices}
}

# json file export name in STATIC_DATA
json_filename = "test_notices.json"
