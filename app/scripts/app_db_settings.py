# -*- encoding: utf-8 -*-


authorized_collections = ["notices", "exemplaires", "users"]

# relations exemplaires-notices
key_exemplaires   = "id_origine"
key_notices       = "identifiant_origine"
key_synapse       = "id_o"
key_group_level_1 = "C1"
key_group_level_2 = "C2"

key_barcode         = "cab"
key_parcours        = "parcours"
key_parcours_status = "read_status"
key_rendu_date      = "date_rendu"
key_lastupdate      = "last_update"

parcours_status = {
    "emprunt" : 0,
    "envie"   : 1,
    "lu"      : 2
}

parcours_status_ = ["emprunts","envies","lus"]

# index(s) to keep
indices_exemplaires = [ key_exemplaires, "emplacement", "cote", "cab" ] #, "section"
indices_notices     = [ key_notices, "titre", "auteur_princ", "date_import", "deleted", "resume"] #, "provenance" ]

# dict indices
indices_mysql = {
    'exemplaires' : {'ind' : indices_exemplaires , 'key' : key_exemplaires},
    'notices'     : {'ind' : indices_notices,      'key' : key_notices}
}

# json file export name in STATIC_DATA
json_filename  = "JSON_notices"
json_extension = ".json"


#### NOTICES GROUPS
notices_groups = {
    u'FICTION' :
        {   "CODE" : u"F",
            "List" : [
                u'ROMANS JEUNESSE',
                u'ROMANS ADULTES',
                u'BD ADULTES',
                u'BD JEUNESSE',
                u'ALBUMS',
                u'CINEMA ADULTES',
                u'CINEMA JEUNESSE',
            ]
        }
    ,
    u'DOCUMENTAIRE' :
        {   "CODE" :  u"D",
            "List" : [
                u'SOCIETE',
                u'VIE PRATIQUE',
                u'SCIENCES',
                u'HISTOIRE',
                u'GEOGRAPHIE',
                u'PHILOSOPHIE',
                u'PSYCHOLOGIE',
                u'LITTERATURE',
                u'SPORTS ET LOISIRS',
                u'LANGUES',
                u'INFORMATIQUE',
                u'RELIGIONS',
                u'FONDS LOCAL',
            ]
        }
    ,
    u'SPECTACLE' :
        {   "CODE" : u"S",
            "List" : [
                u'DANSE',
                u'THEATRE',
                ]
        }
    ,
    u'MUSIQUE' :
        {   "CODE" : u"M",
            "List" : [
                u'MUSIQUE ADULTES',
                u'MUSIQUE JEUNESSE',
            ]
        }
    ,
    u'JEU' :
        {   "CODE" : u"J",
            "List" : [
                u'JEUX A REGLES',
                u"JEUX D'ASSEMBLAGE",
                u'LIVRES SUR LES JEUX',
                u"JEUX D'EXERCICES",
                u'JEUX SYMBOLIQUES',
                u'JEUX VIDEO',
            ]
        }
    ,
    u'ART' :
        {   "CODE" : u"A",
            "List" : [
                u'ARTS',
                u'GRAPHISME',
                u'LOISIRS CREATIFS',
            ]
        }
    ,
    u'UNKNOWN' :
        {   "CODE" : u"U",
            "List" : [
                u'PRESSE',
                None,
            ]
        }
    ,
 }

print '- '*70

print "starting app --- dict_emplacements "
dict_emplacements = {}
for key, value in notices_groups.iteritems():
    code = value["CODE"]
    for empl in value["List"] :
        dict_emplacements[empl] = {
            "code1" : code,
            "code2" : value["List"].index(empl),
            "C"     : [ code, str(value["List"].index(empl)) ],
            "c"     : code + "." + str(value["List"].index(empl))
        }
print dict_emplacements
print '- '*70


print "starting app --- dict_emplacements_ "
dict_emplacements_ = {}
for key, value in notices_groups.iteritems():
    code = value["CODE"]
    dict_emplacements_[code] = { "PARENT" : key, "CHILDREN" : [] }
    for empl in value["List"] :
        temp_dict = { unicode(code + "." + str(value["List"].index(empl))) : empl }
        dict_emplacements_[code]["CHILDREN"].append(temp_dict)
print dict_emplacements_
print '- '*70



print "starting app --- dict_emplacements_C1 "
dict_emplacements_C1 = {}
for d, v in dict_emplacements.iteritems() : #[None]
    dict_emplacements_C1[d] = v["code1"]
print dict_emplacements_C1
print '- '*70



print "starting app --- dict_emplacements_C2 "
dict_emplacements_C2 = {}
for d, v in dict_emplacements.iteritems() : #[None]
    dict_emplacements_C2[d] = v["c"]
print dict_emplacements_C2
print '- '*70
