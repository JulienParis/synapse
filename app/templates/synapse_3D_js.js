// --- GLOBAL VARIABLES --- //
// ------------------------ //

    var start       = Date.now() ;
    var randomStart = Math.random() * 1000. + 100. ;
    var last_pause ;
    var time_paused_total = 0 ; 
    var time_  ; 

    var userCard = "{{ isCard }}" ; 

    var group, groupH ;
    var container, controls, stats ;
    var particlesData    = [] ;
    var clickableObjects = [] ;
    var camera, scene, renderer ;
    var gui ;

    var raycaster, intersects ;
    var mouse, INTERSECTED ;

    var WIDTH  = window.innerWidth;
    var HEIGHT = window.innerHeight;


    var pPositions, pSizes, pColors, pFrequencies, pVelocities ;
    var particlesGeom ;
    var pointCloud, convexHullMesh ;

    var positionsL, colorsL ;
    // var linesMesh ;
    // var meshesList = [] ;
    // var sphereMesh ;

    var maxParticleCount 	= 1000;
    var particleCount    	= 0;
    var Rbasis     	        = 100.;
    var RmarginAngle   		= 0.4 ;
    var RmarginDist   		= Rbasis / 10. ;
    var RbasisHalf 	   		= RmarginAngle / 2.;
    var maxCircleRad ;

    var defaultPointSize     = 10. ; // max size for icon
    var defaultLineTransp    = .85 ;
    var defaultLineColor     = "#ffffff" ;
    var defaultLineColorUser = "#ff0000" ;
    
    // var velocityFactor = 1. ;
    // var scaleFactor    = 1. ;

    var effectController_animate = {
        // showGroup        : true,
        showHelper       : false,
        showParticles    : true,
        showEdges        : true,
        colorLines       : defaultLineColor , 
        colorLineUser    : defaultLineColorUser , 
        transpLines      : defaultLineTransp ,
        // minDistance     : 120,
        // limitConnections: true,
        // maxConnections  : 10,
        // particleCount   : particleCount,
        velocityFactor  : .1 ,
        scaleFactor     : -.6 ,
        breathing       : 1.5 ,
        waveFreq        : .1 ,
        waveAmp         : .65 ,
        // rotationGroup   : 1. ,
    };

    var effectController_pause = {
        showHelper       : false,
        showParticles    : true,
        showEdges        : true,
        colorLines       : defaultLineColor , 
        colorLineUser    : defaultLineColorUser , 
        transpLines      : defaultLineTransp ,
        
        velocityFactor  : .0 ,
        scaleFactor     : -.6 ,
        breathing       : .0 ,
        waveFreq        : .0 ,
        waveAmp         : .0 ,
    };

    var effectController = effectController_animate ;
    
    // add colors to effectcontroler
    $.each( notices_groups_ , function( keyF , family ) { 
        effectController[ keyF ] = family["color"] ;
        $.each( family["List"] , function ( keyG, group )  {
            if ( keyG == null ) { keyG = "None" } ;
            effectController[ keyG ] = group["color"] ;
        });
    })
    

    // var familiesColors = [
    //     "rgb(255,188,158)",
    //     "rgb(79,116,255)",
    //     "rgb(213,209,0)",
    //     "rgb(201,52,72)",
    //     "rgb(156,255,168)",
    //     "rgb(255,133,16)",
    //     "rgb(1,136,116)",
    // ];


    // info div (temp for debugging)
        // var count = 0 ;
        info = document.createElement( 'div' );
        info.style.position = 'absolute';
        info.style.top = '30px';
        info.style.width = '100%';
        info.style.textAlign = 'center';
        info.style.color = '#f00';
        info.style.display = 'none';
        // info.style.backgroundColor = 'transparent';
        info.style.zIndex = '1';
        info.style.fontFamily = 'Monospace';
        info.innerHTML = 'infos' ;
        info.style.userSelect = "none";
        info.style.webkitUserSelect = "none";
        info.style.MozUserSelect = "none";
        document.body.appendChild( info );



// --- GEOMETRICAL FUNCTIONS --- //

    // random number within interval
    function getRandomNumber(min, max) {
        return Math.random() * (max - min) + min;
    } ;

    // function rand() {
        // 	var x = Math.random() ;
        // 	return x ;
    // };

    // randomly create vertex position on a sphere arc
    // function positionVertexOnSphere(radius, phiStart, phiEnd, thetaStart, thetaEnd) {
        //
        // 	var position = new THREE.Vector3();
        //
        // 	var phi   = getRandomNumber(phiStart  , phiEnd)   ;
        // 	var theta = getRandomNumber(thetaStart, thetaEnd) ;
        //
        // 	position.x = radius * Math.sin(phi) * Math.cos(theta) ;
        // 	position.y = radius * Math.sin(phi) * Math.sin(theta) ;
        // 	position.z = radius * Math.cos(phi) ;
        //
        // 	console.log(">>> position V / phiStart / phi / theta", position, phiStart, phi, theta );
        //
        // 	return position ;
    // } ;


    // randomly create vertex position on a sphere arc
    // cf : http://mathinsight.org/spherical_coordinates
    function positionVertexOnProjectedCircleOntoSphere( radiusCircleMax, radiusSphere ) {

        var position = new THREE.Vector3();

        // populate circle with random point
        var te = getRandomNumber( 0, 2. * Math.PI ) ;
        var ra = getRandomNumber( radiusCircleMax/2., radiusCircleMax ) ;
        position.x = ra * Math.cos(te) ;
        position.y = ra * Math.sin(te) ;

        // populate rectangle with random point
        // position.x = getRandomNumber( -radiusCircleMax*1.0, radiusCircleMax*1.0 );
        // position.y = getRandomNumber( -radiusCircleMax*0.6, radiusCircleMax*0.6 );

        lenXY = Math.sqrt( Math.pow( position.x, 2.) + Math.pow(position.y, 2.)  ) ;
        position.z = Math.sqrt( Math.pow(radiusSphere, 2.) - Math.pow( lenXY, 2.)  ) ;
        if ( isNaN(position.z) ) {
            position.z = 0. ;
        };
        return position ;

    };


    // max radius for every plane circle
    function maxCircleRadius ( familiesLength ) {
        var angleIsocele = ( Math.PI * 2. - ( familiesLength * RmarginAngle ) ) / familiesLength  ;
        console.log("___ angleIsocele : ", angleIsocele);
        var maxRadius    = Rbasis * Math.sin( angleIsocele ) * 0.8 ;
        return maxRadius ;
    };

    // for rotation whole family on Y axis
    function familyAngle( familyIndex, familiesLength ) {
        // var angleFa = Math.PI * 2 * familyIndex / familiesLength ;
        var angleFa = ( Math.PI * 2. - ( familiesLength * RmarginAngle ) ) / familiesLength ;
        angleFa += RmarginAngle ;
        angleFa *= familyIndex  ;
        return angleFa ;
    };

    // for rotation whole group on X axis
    function groupAngle( groupIndex, groupsLength, angleLap ) {
        // var angleGr = 1. * ( Math.PI / groupsLength ) ;
        // if ( groupIndex % 2 ) {
        // 	angleGr  *= - groupIndex ;
        // } else {
        // 	angleGr  *= groupIndex ;
        // }
        var angleGr = ( groupIndex - groupsLength/2. ) * Math.PI / angleLap ;
        // if ( groupIndex % 2 ) {
        // 	angleGr  *= - 1 ;
        // }
        return angleGr ;
    };

    // for radius orginal cluster's circle
    function groupRadius( groupsLength ) {
        var absMargin   = Rbasis - Math.cos(RmarginAngle) ;
        var sphereDiam  = Rbasis * 2. -  2. * absMargin ;
        var clusterDiam = sphereDiam / groupsLength - ( absMargin * groupsLength - 1 ) ;
        var clusterRad  = clusterDiam / 2.    ;

        if (clusterRad > maxCircleRad)  {
            clusterRad = maxCircleRad ;
        };

        return clusterRad ;
    };

    // for distance origin to cluster
    function sphereRadius( clusterIndex, margin ) {
        var clusterDist = Rbasis + clusterIndex * margin * 1.4 ;
        return clusterDist ;
    };



// --- DEFINE SHADER MATERIALS : SHADERMATERIAL AND USUAL MATERIAL
function createShaderMaterial ( constantsGroup,
                                // keyFa, keyGroup,
                                // familyIndex,
                                // familiesLength,
                                // groupIndex,
                                // groupsLen,
                                is_wire,
                                is_texture, 
                                is_from_user = false 
                            ) {
    
    console.log("/// createShaderMaterial / constantsGroup : " , constantsGroup) ; 
    
    var keyFa           = constantsGroup["keyFa"] ;
    var keyGroup        = constantsGroup["keyGroup"] ;
    var groupName       = constantsGroup["groupName"] ;
    var familyIndex     = constantsGroup["indexFa"] ;
    var familiesLength  = constantsGroup["familiesLen"] ;
    var groupIndex      = constantsGroup["indexGroup"] ;
    var groupsLen       = constantsGroup["faGroupsLen"] ;

    var roty_angleFa    = constantsGroup["roty_angleFa"] ;
    var rotx_angleGroup = constantsGroup["rotx_angleGroup"] ;
    
    var transp_ = 1. ; 
    
    if ( groupName == null ) {
        groupName = "None" ;
    }

    // colors points
    if ( is_wire == false ) {
        // var colorG = new THREE.Color ( notices_groups_[ keyFa ]["color"] ) ;  
        var colorG = new THREE.Color ( notices_groups_[ keyFa ]["List"][ groupName ]["color"] ) ;  
    } 
    // colors lines
    else {
        if ( is_from_user === true  ) {
            var colorG  = new THREE.Color( defaultLineColorUser ) ;
            // console.log( "colorG / is_from_user : ", colorG ) ; 
        } else {
            var transp_ = defaultLineTransp ; 
            var colorG  = new THREE.Color( defaultLineColor ) ;            
            // console.log( "colorG / !is_from_user : ", colorG ) ; 
        }
    };
    

    // if ( colorG === new THREE.Color( "#ffffff" ) ) {
    //     console.log( " !!! DEBUG WEIRD COLOR HERE !!!", constantsGroup ) ; 
    // }

    // var randColor = Math.random() ;
    // var famColor = familyIndex / familiesLength ;
    // // var randHSl = "hsl(" + randColor + ", 100%, 80%)" ;
    // var colorG  = new THREE.Color( famColor, 0.2,  0.6 ) ;

    // var famColor = familiesColors[familyIndex] ;
    // var colorG  = new THREE.Color( famColor )  ;


    // console.log( "/// createShaderMaterial / familyIndex" , familyIndex );

    var uniforms = {
        time        : { type  : "f"  , value: 0. }, // 1.
        resolution  : { type  : "v2" , value: new THREE.Vector2() },
        velFactor   : { value : effectController.velocityFactor },
        scaFactor   : { value : effectController.scaleFactor },
        breathing   : { value : effectController.breathing },
        waveFreq    : { value : effectController.waveFreq },
        waveAmp     : { value : effectController.waveAmp },
        color       : { value : colorG },
        transp      : { value : transp_ },

        // familyI     : { value : familyIndex },
        // familiesL   : { value : familiesLength },
        // groupI      : { value : groupIndex  },
        // groupsL     : { value : groupsLen  },

        // roty_byFa : { value : roty_angleFa },
        // rotx_byGr : { value : rotx_angleGroup },

    } ;

    if ( is_wire == false ) {
        uniforms.size = { value : defaultPointSize } ;
        uniforms.roty_byFa = { value : roty_angleFa } ;
        uniforms.rotx_byGr = { value : rotx_angleGroup } ;
    } ;

    if ( is_texture == true ) {
        // uniforms.texture = { value: new THREE.TextureLoader().load( "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" ) } ;
        // uniforms.texture = { value: new THREE.TextureLoader().load( "{{ url_for('static', filename='textures/sprites/la_bibliotheque/fiction.png') }}" ) } ;
        uniforms.texture = { value: new THREE.TextureLoader().load( notices_groups_[keyFa]["icon"] ) } ;
    } ;

    // from : https://github.com/mrdoob/three.js/blob/master/examples/webgl_custom_attributes_points.html
    var material_shader = new THREE.ShaderMaterial( {
        uniforms      : uniforms ,
        vertexShader  : document.getElementById( 'vertexshader_points'   ).textContent,
        fragmentShader: document.getElementById( 'fragmentshader_points' ).textContent,
        // transparent:    true,
        // wireframe  :    true,
        alphaTest     : 0.8
    });

    if ( is_wire == true ) {
        material_shader.vertexShader   = document.getElementById( 'vertexshader_lines' ).textContent ;
        material_shader.fragmentShader = document.getElementById( 'fragmentShader_lines' ).textContent ;
        material_shader.transparent    = true ;
        material_shader.wireframe      = false ;
    } ;

    return material_shader ;

};


//// --- DEFINE BASIC LINES MATERIAL
    var materialLines = new THREE.LineBasicMaterial( {
        vertexColors: THREE.VertexColors,
        blending    : THREE.AdditiveBlending,
        transparent : true
    } );

    var wireframeMaterial = new THREE.MeshBasicMaterial( {
        color      : 0xffffff,
        wireframe  : true,
        // transparent: true
    } );


// --- prestock edges --- //
    var vertices3Dict      = { } ; 
    var vertices3UserList_ = [ ] ; 

    // get data for ALL USERS HISTORY from server
        // fake data
            var fake_id_o_list1 = { "parcours" : [ "1412057", "1431565" , "0163823" , "1353951" , "0880467" ]} ;
            var fake_id_o_list2 = { "parcours" : [ "1424811", "0732204" , "0942578" , "0880467"  ] } ;            
            var fakeUserBooksLists = [ fake_id_o_list1 , fake_id_o_list2 ] ;

        // real data
            var realUserBooksLists = {{ listEdges | tojson }};

        console.log( "-+- realUserBooksLists -+- :", realUserBooksLists ) ; 

    // iteratate list realUserBooksLists to store id_o as 
        $.each( realUserBooksLists, function ( i , user ){
            // iterate object user 
            $.each( user.parcours, function ( i_ , id_o ) {
                vertices3UserList_.push( id_o ) ;
            }) ;
        }) ;
        // unique values from vertices3UserList_
        var vertices3UserList = Array.from( new Set(vertices3UserList_) ) ;

        console.log( "-+- vertices3UserList -+- ", vertices3UserList ) ;

// -------------------------------------------------------
// SET PARTICLES SYSTEM <-- returns geomTri_buffer
function addPointsCloud( groupNot, constantsGroup, particlesLength, angleFamily, angleGroup, radiusGroup, radiusCluster, wireORpoints ) {

    // empty arrays variables
        pPositions   = new Float32Array ( particlesLength * 3 );
        pId_o        = new Uint32Array  ( particlesLength     );

        // pColors      = new Float32Array( particlesLength * 3 );
        // pSizes       = new Float32Array( particlesLength     );
        // pFamily      = new Float32Array( particlesLength     ); // those are uniforms --> set in ShaderMaterial
        // pGroup       = new Float32Array( particlesLength     ); // those are uniforms --> set in ShaderMaterial
        // pFrequencies = new Float32Array( particlesLength     );
        // pVelocities  = new Float32Array( particlesLength * 3 );

        // var color     = new THREE.Color( 0xffffff );
        var vertices3     = [] ;
        var vertices2     = [] ;

        // sphere arc variables
        // var radiusCircle 				= Rbasis*2/3 ;
        // var radiusSphere 				= Rbasis ;
        // var phiStart 			= 1.2 ;
        // var phiLength 		= Math.PI - ( phiStart ) ;
        // var thetaStart 		= 2. ;
        // var thetaLength 	= ( Math.PI * 2 ) - ( thetaStart ) ;
        // console.log("sphere variables : radius / thetaLength / phiLength ",radius, thetaLength, phiLength  );
 

    // CREATE EACH PARTICLE
    for ( var i = 0 ; i < particlesLength ; i++ ) {

        
        // var vertex3 = positionVertexOnSphere(radius, phiStart, phiLength, thetaStart, thetaLength) ;
        // var vertex3 = positionVertexOnProjectedCircleOntoSphere(radiusCircle, radiusSphere) ;
        var vertex3 = positionVertexOnProjectedCircleOntoSphere( radiusGroup, radiusCluster ) ;

        // var vertex3 = new THREE.Vector3();
        var vertex2 = new Vertex();

        vertex2.x = vertex3.x ;
        vertex2.y = vertex3.y ;

        // vertex2.x = vertex3.x = Math.random() * Rbasis - Rbasis / 2.;
        // vertex2.y = vertex3.y = Math.random() * Rbasis - Rbasis / 2.;
        // vertex3.z = 0 ; // Math.random() * Rbasis - Rbasis / 2.;

        
        // get back id_o notice
        var id_o = groupNot[i]["id_o"] ;
        var id_o_ = parseInt( id_o ) ; 
        // console.log(id_o_);
        pId_o[ i ] = id_o_ ;
        
        // prestore if is in edges : vertices3UserList from realUserBooksLists
        if ( vertices3UserList.indexOf( id_o ) > -1  ) {
            // console.log( "------- id_o is in vertices3UserList  : ", id_o ) ; 
            // console.log( "------- vertex3 : ", vertex3 ) ; 
            // console.log( "------- constantsGroup : ", constantsGroup ) ; 
            vertices3Dict[ id_o.toString() ] = { "vertex" : vertex3, "constantsGroup" : constantsGroup } ;
            // console.log( "------- vertices3Dict : ", vertices3Dict ) ; 
        };

        vertex3.toArray( pPositions, i * 3 );

        // vertices3[i] = vertex3 ;

        vertices2.push( vertex2 )  ;

        // set color cf : https://www.w3schools.com/colors/colors_hsl.asp
        // color.setHSL(  0., 0., 1. );
        // color.toArray( pColors, i * 3 );

        // push to separate particlesData
        // particlesData.push( {
            // velocity: new THREE.Vector3( -1 + Math.random() , -1 + Math.random(),  -1 + Math.random() ),
            // rotPhi : , // in radians
            // rotThe : , // in radians
            // numConnections: 0
        // } );

        // set default size and frequency

        // pSizes[i]       = 100 ;
        // pFrequencies[i] = 5 * Math.random() + 0.5;
        // velocity        = new THREE.Vector3( -1 + Math.random() , -1 + Math.random(),  -1 + Math.random() ),
        // velocity.toArray( pVelocities, i * 3 );

    }

    // console.log("--- pPositions : ", pPositions);
    // console.log("--- vertices2 : ",  vertices2);
    // console.log("--- vertices3 : ",  vertices3);


    var geomTri_buffer = new THREE.BufferGeometry();
    geomTri_buffer.addAttribute( 'position',  new THREE.BufferAttribute( pPositions,   3 ).setDynamic( true ) ) ;
    geomTri_buffer.addAttribute( 'id_o',      new THREE.BufferAttribute( pId_o,        1 ) )                    ; //.setDynamic( true ) );
    

    if ( wireORpoints == "points" ) {
    // --- ADDING POINTS --- //
        // -----------------------------------------------------------------------
        // console.log(pPositions);
        // var geomTri_buffer = new THREE.BufferGeometry();
        // geomTri_buffer.setDrawRange( 0, particleCount );
        // geomTri_buffer.addAttribute( 'position',        new THREE.BufferAttribute( pPositions,   3 ).setDynamic( true ) );
        
        // geomTri_buffer.addAttribute( 'customColor',     new THREE.BufferAttribute( pColors,      3 ) ); //.setDynamic( true ) );
        
        // geomTri_buffer.addAttribute( 'size',            new THREE.BufferAttribute( pSizes,       1 ) ); //.setDynamic( true ) );
        
        // geomTri_buffer.addAttribute( 'customFrequency', new THREE.BufferAttribute( pFrequencies, 1 ) ); //.setDynamic( true ) );
        // geomTri_buffer.addAttribute( 'customVelocity',  new THREE.BufferAttribute( pVelocities,  3 ) ); //.setDynamic( true ) );
        //
        // // create the particle system with material
        // var materialPoints_shader_custom = createShaderMaterial_points( r,r,r/10, true ) ;
        //
        // console.log("--- materialPoints_shader_custom : ", materialPoints_shader_custom);
        // pointCloud = new THREE.Points( geomTri_buffer, materialPoints_shader_custom );
        //
        // group.add( pointCloud );
    }


    else {
    // --- ADDING TRIANGULATED MESH --- //
        // -----------------------------------------------------------------------
        // TRYING DELAUNAY TRIANGULATION ON VERTICES 2D (projectd on plane XY)
        // cf : https://github.com/callumprentice/callumprentice.github.io/blob/master/apps/delaunay/index.html
        // cf didn't tried it but seems nice : https://github.com/mapbox/delaunator

        var triangles = triangulate(vertices2);
        // console.log("--- triangles : ", triangles);

        var geomTri = new THREE.Geometry();
        var f = 0;

        // topology custom to recreate indexed BufferGeometry
        // cf : https://stackoverflow.com/questions/36730365/how-can-i-add-faces-to-an-indexed-three-buffergeometry
        var uniq_edges_set = new Set() ;
        var facesVIndices  = [] ;

        triangles.forEach( function(tri) {

            // get v1, v2, v3 indices
            var v0_i = vertices2.indexOf(tri.v0);
            var v1_i = vertices2.indexOf(tri.v1);
            var v2_i = vertices2.indexOf(tri.v2);

            // store indices
            facesVIndices.push(v0_i) ;
            facesVIndices.push(v1_i) ;
            facesVIndices.push(v2_i) ;

            // make and store edges vindices

            var e0_   = [v0_i,v1_i].sort() ; var e0 = e0_.join(".") ;
            var e1_   = [v1_i,v2_i].sort() ; var e1 = e1_.join(".") ;
            var e2_   = [v2_i,v0_i].sort() ; var e2 = e2_.join(".") ;

            // add edges to unique edges set
            uniq_edges_set.add(e0).add(e1).add(e2) ;


        })

        // console.log("--- uniq_edges_set : ", uniq_edges_set);
        // make list of edges as couples of vertex indices
        var uniq_edges_v_indices   = [] ;
        for (let eString of uniq_edges_set) {
            var vi_s = eString.split(".") ;
            var vi_0 = parseInt(vi_s[0]) ;
            var vi_1 = parseInt(vi_s[1]) ;
            uniq_edges_v_indices.push(vi_0) ;
            uniq_edges_v_indices.push(vi_1) ;
        };
        // console.log("--- uniq_edges_v_indices : ", uniq_edges_v_indices);

        // var geomTri_buffer = new THREE.BufferGeometry();//.fromGeometry(geomTri) ;
            // var ePositions = new Float32Array( geomTri.vertices.length * 3 );
            // for (i = 0; i < geomTri_buffer.attributes.position.length ; i++){
            // 	var eV = geomTri_buffer.attributes.position[i] ;
            // 	if(i==0) {
            // 		console.log("--- eV --- ", eV);
            // 	}
            // 	eV.toArray( ePositions, i * 3 );
            // };
            // console.log("--- ePositions :", ePositions );
            // geomTri_buffer.setDrawRange( 0, 17984  );
        // geomTri_buffer.addAttribute( 'position',        new THREE.BufferAttribute( pPositions,     3 ).setDynamic( true ) );
        geomTri_buffer.setIndex(      new THREE.BufferAttribute( new Uint16Array ( facesVIndices , 1) ) );
        // geomTri_buffer.addAttribute( 'customFrequency', new THREE.BufferAttribute( pFrequencies,   1 ) ); //.setDynamic( true ) );
        // geomTri_buffer.addAttribute( 'customVelocity',  new THREE.BufferAttribute( pVelocities,    3 ) ); //.setDynamic( true ) );
    }

    // console.log("--- geomTri_buffer : ", geomTri_buffer);

    return geomTri_buffer ;

};



$(document).ready(function(){

// --- FAKE LIGHT JSON NOTICES
var json_fake = {
    "ART": {	"CODE": "A",
                        "STATS": 14082,
                        "CHILDREN": [
                                                    {	"NOTICES": [ {"id_o": "1431521"}, {"id_o": "1444227"}, {"id_o": "0180420"} ],
                                                        "CODE": "A.1",
                                                        "STATS": 1420,
                                                        "NAME": "GRAPHISME"
                                                    },
                                                    {	"NOTICES": [ {"id_o": "1235563"}, {"id_o": "0982809"}, {"id_o": "0982806"} ],
                                                        "CODE": "A.2",
                                                        "STATS": 2408,
                                                        "NAME": "LOISIRS CREATIFS"
                                                    }
                                                ]
                    },

    "JEU": {	"CODE": "J",
                        "STATS": 7102,
                        "CHILDREN": [
                                                    {	"NOTICES": [ {"id_o": "1181008"}, {"id_o": "1181016"} ],
                                                        "CODE": "J.0",
                                                        "STATS": 3524,
                                                        "NAME": "JEUX A REGLES"
                                                    },
                                                    {	"NOTICES": [ {"id_o": "1267718"}, {"id_o": "1267716"}, {"id_o": "1115620"} ],
                                                        "CODE": "J.1",
                                                        "STATS": 808,
                                                        "NAME": "JEUX D'ASSEMBLAGE"
                                                    }
                                                ]
                    },


};


// RESET - PAUSE FUNCTIONS

    function pauseAnimation() {
        // console.log("pauseAnimation / gui : ", gui ) ;
        effectController = effectController_pause ;
        gui.updateDisplay();
    };
    function reanimateAnimation () {
        // console.log("reanimateAnimation / gui : ", gui ) ;
        effectController = effectController_animate ;
        gui.updateDisplay() ;
    };

    $("#animation_pause_start").on( "click", function () {

        // start = Date.now()  ;
        
        // console.log($("#pause_start_span")) ;
        if ( $("#pause_start_span").hasClass("glyphicon-pause" ) ) {
            // console.log("pause_start_span pause") ;
            last_pause = Date.now()  ; 
            // pauseAnimation();
        } else {
            // console.log("pause_start_span play") ;
            // last_delta_ = Date.now() - last_delta_ ;     
            var time_replay       = Date.now() ; 
            var new_paused_lap    = time_replay - last_pause ;
            time_paused_total += new_paused_lap ;
            // reanimateAnimation();
        };
        $(this).find("span").toggleClass("glyphicon-pause").toggleClass("glyphicon-play");
        
    });


// --- LOAD JSON NOTICES AS CALLBACK
    function preload_notices(callback){

        // get parcours all users for edges 
            //

        // get notices for points
            $.getJSON( "{{ url_for('static', filename='data/JSON_notices_nested.json') }}", function( json ) {
            console.log("... JSON_notices_nested loaded with getJSON");

        callback(json);
        }
    )};

// --- START 3D RENDERING AFTER CALLBACK
preload_notices( function(json) {

    //Use your data here
    console.log("... JSON_notices_nested after callback");
    var json_notices = json ;
    console.log( json_notices );


    init();


    initGUI();
    console.log("--- initGUI / gui :", gui);
    
    animate();
    // render() ;


    // GUI controls
    // check : http://learningthreejs.com/blog/2011/08/14/dat-gui-simple-ui-for-demos/
    // check also : https://workshop.chromeexperiments.com/examples/gui/#1--Basic-Usage
    function initGUI( ) {

        console.log( "effectController : ", effectController) ; 

        gui = new dat.GUI( { autoPlace: false } );

        var customContainer = document.getElementById('guiSettings');
        customContainer.appendChild(gui.domElement);

        var f4 = gui.addFolder(" > animation");
            // f4.add( effectController, "minDistance"   ,  10, 300 , 1       );
            f4.add( effectController, "velocityFactor",  0.,  2.  , 0.01  ).listen(); // .onChange( onChangeControl(scene, "velFactor") ) ;
            f4.add( effectController, "scaleFactor",    -1.,  1.  , 0.01  ).listen(); // .onChange( onChangeControl(scene, "scaFactor") ) ;
            f4.add( effectController, "breathing"  ,     0.,  5.  , 0.01  ).listen(); // .onChange( onChangeControl(scene, "breathing") ) ;
            f4.add( effectController, "waveFreq"   ,     0.,  1.  , 0.01  ).listen(); // .onChange( onChangeControl(scene, "breathing") ) ;
            f4.add( effectController, "waveAmp"    ,     0.,  1.  , 0.01  ).listen(); // .onChange( onChangeControl(scene, "breathing") ) ;
            f4.open() ;

        var f1 = gui.addFolder(" > formes") ;
            // f1.add( effectController, "showGroup"  ).onChange( function( value ) {  group.visible   = value; } );
            // f1.add( effectController, "showHelper" ).onChange(    function( value ) {  groupH.visible        = value; } ).listen();
            f1.add( effectController, "showParticles" ).onChange( function( value ) {  groupFa3D_.visible    = value; } ).listen();
            f1.add( effectController, "showEdges" ).onChange(     function( value ) {  groupEdges3D_.visible = value; } ).listen();

        var f2 = gui.addFolder(" > couleurs des lignes");
            f2.add(      effectController, "transpLines",  0.,  1., 0.01 ).listen();
            f2.addColor( effectController, "colorLines"    );
            f2.addColor( effectController, "colorLineUser" );
            // f2.open() ;

        var f3 = gui.addFolder(" > couleurs des points");
            // $.each( notices_groups_ , function( key , family ) { 
            //     f3.addColor( effectController, key    ).listen(); 
            // });           
            $.each( notices_groups_ , function( keyF , family ) { 
                var g3 = f3.addFolder( keyF ); 
                $.each( family["List"] , function ( keyG, group )  {
                    g3.addColor( effectController, keyG  ); 
                });
            })
            f3.open()



       
        gui.closed = false ;
        gui.__ul.style.width = "320px" ;
        // gui.TEXT_CLOSED = "fermer les réglages" ;
        // gui.TEXT_OPEN   = "ouvrir les réglages" ;
        
        // console.log("--- initGUI / gui :", gui);
        
        // hide controls at the beginning
        // $(".dg.ac").hide(); 

    };


    
    // INIT FUNCTION
    function init() {
        
        // --- BASIC STUFF --- //
            container = document.getElementById( 'canvas3D' );

            // set scene
            camera            = new THREE.PerspectiveCamera( 50, window.innerWidth / window.innerHeight, 1, 10000 );
            camera.position.x = 200. ;
            camera.position.y = 50.   ;
            camera.position.z = 200. ;

            scene     = new THREE.Scene();
            scene.fog = new THREE.FogExp2( 0xffffff, 0.002 );

            // empty groups for particles and edges
            groupFa3D_ = new THREE.Group();
            scene.add( groupFa3D_ );
            groupEdges3D_ = new THREE.Group();
            scene.add( groupEdges3D_ );


            groupH = new THREE.Group();
            scene.add( groupH ) ;
            
            var helper = new THREE.BoxHelper( new THREE.Mesh( new THREE.BoxGeometry( Rbasis, Rbasis, Rbasis ) ) );
            helper.name = "helper" ;
            helper.material.color.setHex( 0x080808 );
            helper.material.blending = THREE.AdditiveBlending;
            helper.material.transparent = true;
            groupH.add( helper );
            groupH.visible = effectController["showHelper"] ;

            // console.log("--- meshesList", meshesList );


            // -----------------------------
            // test iteration on fake JSON
            // var maxCluster = 1000 ;
            // iteration on families
            // for (var family in json_fake ){
            // 	console.log( "--- ITERATION FOR / JSON : ", family, json_fake[family] );
            // 	// iteration on groups
            // } ;

            var familiesLen = Object.keys(json_notices).length ;
            console.log("--- ");
            console.log("--- familiesLength", familiesLen);
            maxCircleRad = maxCircleRadius ( familiesLen ) ;
            console.log("--- maxCircleRad", maxCircleRad);


            // RAYCASTING for mouse interaction
                raycaster = new THREE.Raycaster();
                mouse     = new THREE.Vector2();
        

        // --- MAIN GEOM POINTS CREATION FUNCTION --- //
            Object.keys(json_notices).forEach( function (keyFa, indexFa) {

                // -- FOR EACH FAMILY
                console.log("--- ITERATION FA / keyFa, indexFa : ", keyFa, indexFa );

                var angleFa = familyAngle( indexFa, familiesLen);
                console.log("--- ITERATION FA / angleFa : ", angleFa );

                var faGroups     = json_notices[keyFa]["CHILDREN"];
                var faGroupsLen  = Object.keys(faGroups).length   ;
                console.log("--- ITERATION FA / keyFa, faGroupsLen : " , keyFa, faGroupsLen );


                Object.keys(faGroups).forEach( function (keyGroup, indexGroup) {

                    // --- FOR EACH GROUP
                    var groupObj  = faGroups[keyGroup] ;
                    var groupName = groupObj["NAME"]  ;
                    if ( groupName === null ) {
                        groupName = "None" ;
                    };
                    var groupLen  = groupObj["STATS"] ;
                    var groupCod  = groupObj["CODE"] ;
                    var groupNot  = groupObj["NOTICES"] ;
                    
                    var groupFa3D          = new THREE.Group () ;
                    // groupFa3D.customFactor = getRandomNumber( 1, 5);
                    groupFa3D.syn_code  = groupCod ;
                    groupFa3D.syn_name  = groupName ;
                    groupFa3D.syn_stats = groupLen ;
                    
                    // scene.add( groupFa3D );
                    groupFa3D_.add( groupFa3D );
                    
                    console.log("------ ITERATION GR / keyFa, keyGroup, groupName, groupLen : " , keyFa, keyGroup, groupName, groupLen );
                    var distGroup  = sphereRadius( indexGroup, RmarginDist  ) ;
                    var angleGroup = groupAngle(   indexGroup, faGroupsLen, 5. );

                    // Object.keys(faGroups).forEach( function (keyGroup, indexGroup) {

                    
                    /// FOR TRIANGULATED MESH LINES /////////////////////////////////////////////////////////
                        // addPointsCloud -->          particlesLength, angleFamily, angleGroup, radiusGroup,     radiusCluster
                        
                        //var geomTri_buffer = addPointsCloud(maxCluster, angleFa,  angleGroup, maxCircleRad*.8, Rbasis*1.,     "wire") ; // distGroup or Rbasis // <--

                        // var materialLines_shader_custom = createShaderMaterial ( // <--
                        // 															indexFa,
                        // 															familiesLen,
                        // 															indexGroup,
                        // 															faGroupsLen,
                        // 															is_wire    = true,
                        // 															is_texture = false
                        // 														) ;

                        // console.log("--- materialLines_shader_custom : ",materialLines_shader_custom);
                        // geoMesh = new THREE.LineSegments( geomTri_buffer, materialLines_shader_custom) ;
                        
                        // var geoMesh = new THREE.LineSegments( geomTri_buffer, materialLines_shader_custom) ; // <--
                    
                    var groupRandom = getRandomNumber( 0.4, 1.1 );

                    /// FOR POINTS CLOUD + SPRITES  /////////////////////////////////
                    // console.log( "------ ITERATION GR / groupNot", groupNot ) ;

                    var constantsGroup = {
                        "keyFa"        : keyFa , 
                        "keyGroup"     : keyGroup , 
                        "groupName"    : groupName ,
                        "indexFa"      : indexFa , 
                        "familiesLen"  : familiesLen , 
                        "indexGroup"   : indexGroup , 
                        "faGroupsLen"  : faGroupsLen , 

                        "roty_angleFa"      : angleFa, 
                        "rotx_angleGroup"   : angleGroup,
                    };  

                    // var geomTri_buffer_p = addPointsCloud( groupNot, maxCluster, angleFa,  angleGroup, maxCircleRad*.8, distGroup*0.7, "points") ; // distGroup or Rbasis
                    // addPointsCloud( groupNot, constantsGroup, particlesLength, angleFamily, angleGroup, radiusGroup, radiusCluster, wireORpoints )
                    var geomTri_buffer_p = addPointsCloud(  groupNot, constantsGroup,
                                                            groupLen, 
                                                            angleFa,  
                                                            angleGroup, 
                                                            maxCircleRad * groupLen/10000., // radiusGroup
                                                            distGroup * groupRandom,        // radiusCluster
                                                            "points"
                                                        ) ; // distGroup or Rbasis
                    
                    var material_points  = createShaderMaterial (   constantsGroup,
                                                                    is_wire    = false,
                                                                    is_texture = true
                                                                ) ;
                    
                    // console.log( "geomTri_buffer_p : ", geomTri_buffer_p )
                    

                    var geoMesh = new THREE.Points( geomTri_buffer_p, material_points ) ;
                    
                    // store family and group keys
                    geoMesh.family_key = keyFa ; 
                    geoMesh.group_name = groupName ; 
                    

                    // meshesList.push(linesMesh) ;

                    // geoMesh = new THREE.LineSegments( geomTri_buffer, wireframeMaterial) ;

                    // geoMesh = new THREE.Mesh( geomTri, wireframeMaterial) ;
                    // console.log( "--- geoMesh : ", geoMesh );


                    // apply rotation on sub-group
                    // var rot = new THREE.Euler( angleGroup, angleFa, 0, 'XYZ' );
                    // geoMesh.position.applyEuler(rot) ;

                    // geoMesh.eulerOrder = "ZYX" ;

                    // geoMesh.rotation.order = "ZYX" ;
                    // geoMesh.rotation.y += angleFa ;
                    // geoMesh.rotation.x += angleGroup ;


                    groupFa3D.add( geoMesh );
                    clickableObjects.push(geoMesh) ;

                });


                console.log(" ======================================== ");
                console.log(" clickableObjects ", clickableObjects );
                console.log(" scene ", scene );
                console.log(" ======================================== ");
                

            }) ;


        // --- CREATE EDGES --- //

            console.log( "-+- realUserBooksLists -+- :", realUserBooksLists ) ; 
        
            console.log( "-+- vertices3UserList -+- ", vertices3UserList ) ;
            console.log( "-+- vertices3Dict -+- "    , vertices3Dict     ) ;
            console.log(" ======================================== ");
            
            // global group for edges
            var groupEdges3D = new THREE.Group () ;
            // scene.add( groupEdges3D ) ;
            groupEdges3D_.add( groupEdges3D ) ;
            
            // CREATE LINE for each user from users' history list : realUserBooksLists
            // $.each( fakeUserBooksLists , function( index , data_user ) { 
            $.each( realUserBooksLists , function( index , data_user ) { 
                
                console.log( " --- new line (edge) for userCard --- ", userCard ) ;
                
                // check if it is the user's line 
                if ( data_user["n_carte"] === userCard ) {
                    var line_user = true ;
                } else {
                    var line_user = false ;                    
                } 
                
                if ( data_user.parcours.length > 0 ) {
                    
                    console.log( "-- data_user -- ",    data_user    ) ;
                    
                    var id_o_list = data_user.parcours ; 
                    
                    // create geometry
                    var geoUser_buffer  = new THREE.BufferGeometry();

                    // temporary id_o list to except potential errors
                    var id_o_list_except = [] ;
                    $.each( id_o_list, function( i, id_o ) {
                        var isId_o = vertices3Dict[ id_o ] ;
                        if ( isId_o != undefined ) {
                            id_o_list_except.push(id_o)
                        }
                    }); 

                    console.log( "-- id_o_list_except -- ",    id_o_list_except    ) ;

                    var segments   = id_o_list_except.length ; 
                    // var segments   = id_o_list.length ; 
                    var positionsL = new Float32Array( segments * 3 ); 
                    var rotyL      = new Float32Array( segments     ); 
                    var rotxL      = new Float32Array( segments     ); 
                    var vertexL_constants ; 

                    // get back vertex coordinates from id_o attribute in vertices3Dict
                    $.each( id_o_list_except, function( i, id_o ) {
                    // $.each( id_o_list, function( i, id_o ) {
                            
                        // console.log( "-- id_o -- ",    id_o    ) ;
                        
                        // find vertex in vertices3Dict for this id_o /////////////////////// EXCEPT ERRORS 
                        var vertexL       = vertices3Dict[ id_o ]["vertex"] ;
                        // console.log( "-- vertexL -- ", vertexL ) ;

                        vertexL_constants = vertices3Dict[ id_o ]["constantsGroup"] ;
                        // console.log( "-- vertexL_constants -- ", vertexL_constants ) ;
                                                
                        // push to positionsl
                        // vertexL.toArray( positionsL, i * 3 );
                        positionsL[ i * 3 ]     = vertexL.x ;
                        positionsL[ i * 3 + 1 ] = vertexL.y ;
                        positionsL[ i * 3 + 2 ] = vertexL.z ;

                        rotyL[ i ]              = vertexL_constants["roty_angleFa"]    ;
                        rotxL[ i ]              = vertexL_constants["rotx_angleGroup"] ;
                         
                    });

                    geoUser_buffer.addAttribute( 'position', new THREE.BufferAttribute(  positionsL, 3 ).setDynamic( true ) );
                    geoUser_buffer.addAttribute( 'roty_byFa', new THREE.BufferAttribute( rotyL, 1 ) );
                    geoUser_buffer.addAttribute( 'rotx_byGr', new THREE.BufferAttribute( rotxL, 1 ) );
                    

                    // create material with same caracteristics than original vertex
                    // var geoUser_material = new THREE.LineBasicMaterial( { vertexColors : THREE.VertexColors } );
                    var geoUser_material = createShaderMaterial (   vertexL_constants,
                                                                    is_wire    = true,
                                                                    is_texture = false, 
                                                                    is_from_user = line_user,
                    ) ;
                    
                    // compose mesh 
                    line_mesh = new THREE.Line( geoUser_buffer, geoUser_material );
                    
                    // store line basic infos on user
                    line_mesh.is_from_user = line_user ;
                    line_mesh.from_card = data_user["n_carte"] ;

                    // line_mesh = new THREE.Line( geoUser_buffer, geoUser_material );
                    console.log( " line_mesh : ", line_mesh ) ;
                    
                    // add to groupEdges3D 
                    groupEdges3D.add( line_mesh ) ; 
                
                }; // end if statement
                
                console.log( " °°° " ) ;

                
            });


        // --- RENDERING --- //
        // RENDERER
            renderer = new THREE.WebGLRenderer( { antialias: true, alpha : true } ); // alpha true for css background-color
            renderer.setPixelRatio( window.devicePixelRatio );
            renderer.setSize( WIDTH, HEIGHT );
            renderer.gammaInput  = true;
            renderer.gammaOutput = true;
            container.appendChild( renderer.domElement );


        // CONTROLS
            controls = new THREE.OrbitControls( camera, container );
            // controls = new THREE.TrackballControls( camera, container );
            // cf : https://github.com/mrdoob/three.js/blob/master/examples/misc_controls_pointerlock.html
            controls.minDistance   = 1. ;
            controls.maxDistance   = 1000.;
            controls.dampingFactor = 0.1   ;

        // set stats box
            // stats = new Stats();
            // container.appendChild( stats.dom );




        // EVENT LISTENERS 
            window.addEventListener(   'resize',    onWindowResize,      false );
            document.addEventListener( 'mousemove', onDocumentMouseMove, false );
            document.addEventListener( 'mousedown', onDocumentClick,     false );
                


    } // --> end init 


    // UI FUNCTIONS
    function onDocumentMouseMove( event ) {
        event.preventDefault();
        mouse.x =   ( event.clientX / WIDTH )  * 2 - 1;
        mouse.y = - ( event.clientY / HEIGHT ) * 2 + 1;
    };




    // CLICKABLE SPRITES
    function onDocumentClick ( event ) {
        
        var rect = renderer.domElement.getBoundingClientRect();
        mouse.x =   ( ( event.clientX - rect.left ) / ( rect.width  - rect.left ) ) * 2 - 1;
        mouse.y = - ( ( event.clientY - rect.top  ) / ( rect.bottom - rect.top) )   * 2 + 1;
          
        raycaster.setFromCamera( mouse, camera );
    
        intersects = raycaster.intersectObjects( clickableObjects );
        
        // check if modal infos notice already shown or not
        var isModalInfoOpen = $("#mod_info_notice").hasClass("in") ;             
        
        if ( intersects.length > 0 && isModalInfoOpen==false ) {
            
            var INTERSECTED = intersects[0] ;

            // get back id_o from point
            console.log( " INTERSECTED ", INTERSECTED )  ;

            var INTERSECTED_index    = INTERSECTED.index ;
            // console.log( " INTERSECTED_index ", INTERSECTED_index )  ;
            
            var INTERSECTED_ido_list = INTERSECTED.object.geometry.attributes.id_o.array ;
            // console.log( " INTERSECTED_ido_list ", INTERSECTED_ido_list )  ;
            
            var INTERSECTED_id_o  = INTERSECTED_ido_list [ INTERSECTED_index ] ;
            console.log( " INTERSECTED_id_o ", INTERSECTED_id_o )  ;
            
            // get back info with id_o from server : socket_io
            ///////////////////////////////

            
            // include info in div 
            info.innerHTML = 'INTERSECTED_id_o : ' + INTERSECTED_id_o ;  
            $("#not3D_id_o").html(INTERSECTED_id_o) ; 

            // show modal notice
            // $("#mod_info_notice").collapse('show') ; 
            // $('[data-dismiss="modal"]').on('click', function(){
            //     $('.modal').collapse("hide");
            //     $('.modal-backdrop').collapse("hide");
            // });

            console.log(" ");

        }                


    }

    // function onWindowResize() {
        // 	renderer.setSize( WIDTH, HEIGHT );
        // 	camera.aspect = WIDTH / HEIGHT ;
        // 	camera.updateProjectionMatrix();
        // };

    // RESIZE FUNCTION
    function onWindowResize() {
        WIDTH = window.innerWidth ;
        HEIGHT = window.innerHeight ;
        camera.aspect = WIDTH / HEIGHT ;
        camera.updateProjectionMatrix();
        renderer.setSize( WIDTH, HEIGHT );
    };


    // --- TRAVERSE SCENE FUNCTIONS --- //
    function onChangeControl ( factorName ) {

        scene.traverse( function( node ) {

            if ( node instanceof THREE.LineSegments | node instanceof THREE.Points ) {

                if (node.name != "helper") {
                    // console.log("--- traverse / node : ", node );

                    if ( factorName == "velFactor" ) {
                        node.material.uniforms.velFactor.value  = effectController.velocityFactor ;
                    }
                    if ( factorName == "scaFactor" ) {
                        node.material.uniforms.scaFactor.value  = effectController.scaleFactor ;
                    }
                    if ( factorName == "breathing" ) {
                        node.material.uniforms.breathing.value  = effectController.breathing ;
                    }

                }
            }

        });

    };



    // ANIMATE FUNCTION
    function animate() {

        // change main GUI button text
        // $('.close-button').html("<span class='glyphicon glyphicon-tasks' aria-hidden='true'></span> réglages");

        // scene.traverse( function( node ) {
        //
        //   if ( node instanceof THREE.LineSegments | node instanceof THREE.Points ) {
        //
        //     // insert your code here, for example:
        //     // node.material = new THREE.MeshNormalMaterial() ;
        //
        // 		node.geometry.attributes.position.needsUpdate = true;
        // 		node.geometry.verticesNeedUpdate = true;
        // 	}
        //
        // } );

         // optimize rendering = every 1/24 second
        setTimeout( function() {
        requestAnimationFrame( animate );
        }, 1000 / 19 );


        // requestAnimationFrame( animate );
        render();

        // stats.update();


    }


    // RENDER FUNCTION
    function render() {

            
        raycaster.setFromCamera( mouse, camera );

        // UPDATE TIME VALUE IN UNIFORMS
            // var time  = Date.now() * 0.01;

            var isPlay = $("#pause_start_span").hasClass("glyphicon-pause" )  ; 

            if ( isPlay ) { 
                // last_delta_ = Date.now() - last_pause ; 
                time_ = Date.now() - start - time_paused_total   ;
            } else {
                // time_ = Date.now() - start - last_pause   ;
                time_ = time_ ;                
            };

            time_shader = ( time_ * .001 ) + randomStart   ;

            scene.traverse( function( node ) {

                // UPDATE VALUES FROM CONTROLS

                // update animation
                if ( node instanceof THREE.LineSegments | node instanceof THREE.Points  | node instanceof THREE.Line ) {

                    if ( node.name != "helper" ) {
                        // console.log("--- traverse / node : ", node );
                        node.material.uniforms.time.value       = time_shader ; // replace time_shader by 1. for debugging 
                        node.material.uniforms.velFactor.value  = .01 + effectController.velocityFactor ;
                        node.material.uniforms.scaFactor.value  = effectController.scaleFactor ;
                        node.material.uniforms.breathing.value  = effectController.breathing ;
                        node.material.uniforms.waveFreq.value   = effectController.waveFreq ;
                        node.material.uniforms.waveAmp.value    = effectController.waveAmp ;
                        
                        // update colors families
                        if ( node instanceof THREE.Points  ) {
                            var name_group = node.group_name ;
                            var newColorGroup = new THREE.Color(  effectController[ name_group ] ) ;
                            
                            // if ( node.material.uniforms.color.value === new THREE.Color( "#ffffff" ) ) {
                            //     console.log(" !!! weird color here !!! ", name_group ) 
                            // };

                            node.material.uniforms.color.value  = newColorGroup ;                                            
                        };

                        // update color transparency lines
                        if ( node instanceof THREE.Line && node.is_from_user === true ) {
                            var newColorLineU = new THREE.Color( effectController.colorLineUser  )  ;
                            node.material.uniforms.color.value = newColorLineU ;
                        } else if ( node instanceof THREE.Line && node.is_from_user === false  ) {
                            var newColorLines = new THREE.Color( effectController.colorLines  )  ;   
                            node.material.uniforms.color.value  = newColorLines ;                        
                            node.material.uniforms.transp.value = effectController.transpLines ;
                        }
                    }
                };


                    
                // update color transparency lines
                // if ( node instanceof THREE.Line && node.name != "helper" ) {
                //     if ( node.is_from_user === true ) {
                //         var newColorLineU = new THREE.Color( effectController.colorLineUser  )  ;
                //         node.material.uniforms.color.value = newColorLineU ;
                //     } else {
                //         var newColorLines = new THREE.Color( effectController.colorLines  )  ;   
                //         node.material.uniforms.color.value  = newColorLines ;                        
                //         node.material.uniforms.transp.value = effectController.transpLines ;
                //     }
                // }

            });



        // scene.traverse( function( node ) {
        // 	if ( node instanceof THREE.Group ) {
        // 		node.rotation.x = time_ * 0.04 * effectController.rotationGroup * node.customFactor ;
        // 		node.rotation.y = time_ * 0.02 * effectController.rotationGroup * node.customFactor ;
        // 	}
        // }) ;

        // scene.traverse( function( node ) {
           
        //     if ( node instanceof THREE.Points ) {
                
        //         var intersects = raycaster.intersectObjects( node );

        //         if ( intersects.length > 0 ) {
        //             if ( INTERSECTED != intersects[ 0 ].object ) {
        //                 // if ( INTERSECTED ) INTERSECTED.material.program = programStroke;
        //                 INTERSECTED = intersects[ 0 ].object;
        //                 console.log( ">> click INTERSECTED : ", INTERSECTED )
        //                 // INTERSECTED.material.program = programFill;
        //             }
        //         } else {
        //             // if ( INTERSECTED ) INTERSECTED.material.program = programStroke;
        //             INTERSECTED = null;
        //         }
        
        //     }
        // });



        renderer.render( scene, camera );


    }





});


}) ;
