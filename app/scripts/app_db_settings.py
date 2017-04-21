# -*- encoding: utf-8 -*-


# relations exemplaires-notices
key_exemplaires = "id_origine"
key_notices     = "identifiant_origine"
key_synapse     = "id_o"
key_barcode     = "cab"

# index(s) to keep
indices_exemplaires = [ key_exemplaires, "emplacement", "section", "cote", "cab" ]
indices_notices     = [ key_notices, "titre", "auteur_princ", "date_import", "deleted", "resume"] #, "provenance" ]

# json file export name in STATIC_DATA
json_filename = "test_notices.json"
