# -*- encoding: utf-8 -*-

key_username   = u'username'
key_user_id    = u'_id'
key_email      = u'email'
key_n_carte    = u'n_carte'
key_is_card    = u'is_card'
key_password   = u'password'
key_status     = u'status'
key_lastupdate = u"last_update"

dict_db_user = {
              key_username   : u"pseudo",
              key_email      : u"email",
              key_n_carte    : u"n° de carte",
              key_is_card    : u"carte de la bibliothèque",
              key_password   : u"password",
              key_status     : u"autorisation",
              key_lastupdate : u"dernière mise à jour"
              }
dict_user_db = { u:d for d, u in dict_db_user.iteritems() }


authorized_collections = [u"notices", u"exemplaires", u"users"]

# relations exemplaires-notices
key_exemplaires   = u"id_origine"
key_notices       = u"identifiant_origine"
key_synapse       = u"id_o"
key_group_level_1 = u"C1"
key_group_name_1  = u"genre"
key_group_level_2 = u"C2"
key_group_name_2  = u"famille"

key_barcode         = u"cab"
key_parcours        = u"parcours"
key_parcours_status = u"read_status"
key_rendu_date      = u"date_rendu"
key_title           = u"titre"
key_author          = u"auteur_princ"
key_resume          = u"resume"
key_keep            = u"keep"

unknown_notice      = u"notice introuvable"
unknown_author      = u"aucun auteur trouvé"
unknown_title       = u"aucun titre trouvé"
unknown_cab         = u"aucun code barre trouvé"


key_parc_emprunts = u"emprunts"
key_parc_envies   = u"envies"
key_parc_lus      = u"lus"

parcours_status = {
    key_parc_emprunts : 0,
    key_parc_envies   : 1,
    key_parc_lus      : 2
}
parcours_status_ = [ key_parc_emprunts, key_parc_envies, key_parc_lus ]


parcours_indexes = [ key_author, key_title, key_group_name_1, key_group_name_2, key_rendu_date, key_keep ]


# index(s) to keep
indices_exemplaires = [ key_exemplaires, u"emplacement", u"cote", key_barcode ] #, "section"
indices_notices     = [ key_notices, key_title, key_author, u"date_import", u"deleted", u"resume"] #, "provenance" ]

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
        {   u"CODE" : u"F",
            u"List" : [
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
        {   u"CODE" :  u"D",
            u"List" : [
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
        {   u"CODE" : u"S",
            u"List" : [
                u'DANSE',
                u'THEATRE',
                ]
        }
    ,
    u'MUSIQUE' :
        {   u"CODE" : u"M",
            u"List" : [
                u'MUSIQUE ADULTES',
                u'MUSIQUE JEUNESSE',
            ]
        }
    ,
    u'JEU' :
        {   u"CODE" : u"J",
            u"List" : [
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
        {   u"CODE" : u"A",
            u"List" : [
                u'ARTS',
                u'GRAPHISME',
                u'LOISIRS CREATIFS',
            ]
        }
    ,
    u'UNKNOWN' :
        {   u"CODE" : u"U",
            u"List" : [
                u'PRESSE',
                None,
            ]
        }
    ,
 }

print '- '*70

### dict_emplacements --> {u'ROMANS JEUNESSE': {'code1': u'F', 'code2': 0, 'c': u'F.0', 'C': [u'F', '0']}, ...
print "starting app --- dict_emplacements "
dict_emplacements = {}
for key, value in notices_groups.iteritems():
    code = value[u"CODE"]
    for empl in value[u"List"] :
        dict_emplacements[empl] = {
            u"code1" : code,
            u"code2" : value[u"List"].index(empl),
            u"C"     : [ code, str(value[u"List"].index(empl)) ],
            u"c"     : code + "." + str(value[u"List"].index(empl))
        }
print dict_emplacements
print '- '*70


### dict_emplacements_ --> {u'A': {'CHILDREN': [{u'A.0': u'ARTS'}, {u'A.1': u'GRAPHISME'}, {u'A.2': u'LOISIRS CREATIFS'}] ...
print "starting app --- dict_emplacements_ "
dict_emplacements_ = {}
for key, value in notices_groups.iteritems():
    code = value[u"CODE"]
    dict_emplacements_[code] = { u"PARENT" : key, u"CHILDREN" : [] }
    for empl in value[u"List"] :
        temp_dict = { unicode(code + "." + str(value[u"List"].index(empl))) : empl }
        dict_emplacements_[code][u"CHILDREN"].append(temp_dict)
print dict_emplacements_
print '- '*70


### dict_emplacements_C1 --> {u'BD JEUNESSE': u'F', u'SPORTS ET LOISIRS': u'D', u'JEUX SYMBOLIQUES': u'J', u'ROMANS JEUNESSE': u'F', u"JEUX D'ASSEMBLAGE": u'J' ...
print "starting app --- dict_emplacements_C1 "
dict_emplacements_C1 = {}
for d, v in dict_emplacements.iteritems() :
    dict_emplacements_C1[d] = v[u"code1"]
print dict_emplacements_C1
print '- '*70



### dict_emplacements_C2 --> {u'BD JEUNESSE': u'F.3', u'SPORTS ET LOISIRS': u'D.8', u'JEUX SYMBOLIQUES': u'J.4', u'ROMANS JEUNESSE': u'F.0', ...
print "starting app --- dict_emplacements_C2 "
dict_emplacements_C2 = {}
for d, v in dict_emplacements.iteritems() :
    dict_emplacements_C2[d] = v[u"c"]
print dict_emplacements_C2
print '- '*70


print "starting app --- dict_reverse_C2 "
dict_reverse_C2 = {}
for d, v in dict_emplacements_C2.iteritems() :
    dict_reverse_C2[v] = d
print dict_reverse_C2
print '- '*70
