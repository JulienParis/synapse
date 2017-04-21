# -*- encoding: utf-8 -*-

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

### vars for name application / metas
app_metas = {
    "title"       : u"synapse",
    "subtitle"    : u"dataviz 3D",
    "version"     : u"beta 0.1",
    "description" : u"Visualisation 3D du catalogue de la bibliothèque de St Herblain et des parcours de lecture des abonnés",
    "authors"     : u"Julien Paris",
    "licence"     : '...undefined yet...',
    "metas"       : u"""
        dataviz,data visualisation,data visualization,graph,SIG,France,
        pandas,geopandas,socketio,
        opensource,open source,open data,creative commons,github,
        JS,THREE,THREE.js,javascript,python,flask,HTML,CSS,JSON,bootstrap,socketIO
        """
    }

### variables for app colors
colors = {
            "grey_"   : {"hex" : "#e7e7e7"},
            "green_"  : {"hex" : "#d9ecbb"},
            "red_"    : {"hex" : "#f22f59"},
            "ocre_"   : {"hex" : "#ffbb46"},
            "blue_"   : {"hex" : "#2dd6b5", "rgba" : "rgba(46, 214, 180, 0)" },
            "orange_" : {"hex" : "#fe5a34"},
            "purple_" : {"hex" : "#7841a9"},
            "dark_"   : {"hex" : "#3e0963"},
            "water_"  : {"hex" : "#1d91c0", "rgba" : "rgba(29,145,192, 0.9)" }
}

app_colors = {
    'navbar'        : colors['water_']['rgba'],
    'navbar_text'   : colors['grey_']['hex'],
    'navbar_select' : colors['ocre_']['hex'],

    'jumbotron'     : colors['water_']['hex'],

    'btn_primary' : colors['green_']['hex'],
    'btn_success' : colors['green_']['hex'],
    'btn_warning' : colors['ocre_']['hex'],
    'btn_default' : colors['blue_']['hex'],
    'btn_danger'  : colors['red_']['hex'],
    'btn_info'    : colors['purple_']['hex'],
    }

### variables for app sidebar
width_sidebar   = 4
width_full      = 12
width_graph     = width_full - width_sidebar
col_graph_class = "col-xs-"
col_full        = col_graph_class + str(width_full)
col_sidebar     = col_graph_class + str(width_sidebar)
col_graph       = col_graph_class + str(width_graph)

bootstrap_vars  = {
    "width_full"    : width_full,
    "col_full"      : col_full,
    "col_sidebar"   : col_sidebar,
    "col_graph"     : col_graph,
    "width_sidebar" : width_sidebar,
    "width_graph"   : width_graph
}
