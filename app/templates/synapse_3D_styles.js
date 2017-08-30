var notices_groups_ = {
    "FICTION" :
        {   "CODE"  : "F",
            "color" : "#ff6633",
            "icon"  : "{{ url_for('static', filename='textures/sprites/disc.png') }}" ,
            "List"  : {
                "ROMANS JEUNESSE"   : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "ROMANS ADULTES"    : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "BD ADULTES"        : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "BD JEUNESSE"       : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "ALBUMS"            : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "CINEMA ADULTES"    : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "CINEMA JEUNESSE"   : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
            }
        }
    ,
    "DOCUMENTAIRE" :
        {   "CODE"  :  "D",
            "color" : "#ffcc33",
            "icon"  : "{{ url_for('static', filename='textures/sprites/disc.png') }}" ,
            
            "List"  : {
                "SOCIETE"           : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "VIE PRATIQUE"      : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "SCIENCES"          : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "HISTOIRE"          : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "GEOGRAPHIE"        : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "PHILOSOPHIE"       : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "PSYCHOLOGIE"       : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "LITTERATURE"       : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "SPORTS ET LOISIRS" : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "LANGUES"           : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "INFORMATIQUE"      : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "RELIGIONS"         : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "FONDS LOCAL"       : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
            }
        }
    ,
    "SPECTACLE" :
        {   "CODE"  : "S",
            "color" : "#3366ff", 
            "icon"  : "{{ url_for('static', filename='textures/sprites/disc.png') }}" ,
            
            "List"  : {
                "DANSE"             : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "THEATRE"           : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                }
        }
    ,
    "MUSIQUE" :
        {   "CODE"  : "M",
            "color" : "#ff3366",
            "icon"  : "{{ url_for('static', filename='textures/sprites/disc.png') }}" ,
            
            "List"  : {
                "MUSIQUE ADULTES"   : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "MUSIQUE JEUNESSE"  : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
            }
        }
    ,
    "JEU" :
        {   "CODE"  : "J",
            "color" : "#ff6633",
            "icon"  : "{{ url_for('static', filename='textures/sprites/disc.png') }}" ,
            
            "List"  : {
                "JEUX A REGLES"       : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "JEUX D'ASSEMBLAGE"   : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "LIVRES SUR LES JEUX" : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "JEUX D'EXERCICES"    : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "JEUX SYMBOLIQUES"    : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "JEUX VIDEO"          : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
            }
        }
    ,
    "ART" :
        {   "CODE" : "A",
            "color" : "#cc33ff",        
            "icon"  : "{{ url_for('static', filename='textures/sprites/disc.png') }}" ,
            
            "List" : {
                "ARTS"                : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "GRAPHISME"           : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "LOISIRS CREATIFS"    : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
            }
        }
    ,
    "UNKNOWN" :
        {   "CODE"  : "U",
            "color" : "#ff33cc",     
            "icon"  : "{{ url_for('static', filename='textures/sprites/disc.png') }}" ,
            
            "List"  : {
                "PRESSE"              : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
                "None"                : {"color" : "", "icon" : "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" },
            }
        }
    ,
 }