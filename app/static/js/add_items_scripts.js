// START ConnectSocketIO = function () {
// function ConnectSocketIO () {
$(document).ready(function(){


  // auto complete input
  var input_title  = document.getElementById("input_title");
  var awesomplete_title = new Awesomplete( input_title, { minChars : 3 , maxItems : 50} ) ;

  var input_author = document.getElementById("input_author");
  var awesomplete_auth = new Awesomplete( input_author , { minChars : 3 , maxItems : 50} ) ;
  // new Awesomplete(input_title, {
  // 	list: [ ]
  // });

  var table_c = $("#search_results");

  // INITIATE SOCKET IO CONNECTION
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('connect', function() {
    socket.emit( 'connect_' );
  });


  // EMIT REQUEST INFOS LISTS TO SERVER
  function EmitRequestInfos(string_, inp_type) {
    console.log(" *** EmitRequestInfos / string_ : ", string_, " / inp_type : ", inp_type );
    socket.emit(  'io_request_infos_list',
                  { data     : string_ ,
                    inp_type : inp_type
                  }
                );
  };

  // EMIT REQUEST CAB TO SERVER
  function EmitRequestCab(string_) {
    console.log(" *** EmitRequestCab / string_ : ", string_ );
    socket.emit(  'io_request_cab',
                  { data     : string_ ,
                  }
                );
  };

  // EMIT REQUEST AUTHOR'S REFS TO SERVER
  function EmitRequestRefs(author_name) {
    console.log(" *** EmitRequestRefs / author_name : ", author_name );
    // $('#mod_loader').modal('show');
    socket.emit(  'io_request_refs',
                  { data     : author_name ,
                  }
                );
  };



  // GET VALUES INPUT ON CHANGE
  $("#input_title").on("input", function() {

    // clean previous inputs
    $("#cab_code").val("") ;
    $("#input_author").val("") ;
    table_c.empty();

    inp = $("#input_title").val();
    console.log(" --- input : ", inp);
    if (inp.length >= 3 ) {
      // emit request to server
      EmitRequestInfos(inp, "inp_titles") ;
      }
    }
  );

  $("#input_author").on("input", function() {

    $("#cab_code").val("") ;
    $("#input_title").val("") ;

    inp = $("#input_author").val();
    table_c.empty();
    console.log(" --- input : ", inp);
    if (inp.length >= 3 ) {
      // emit request to server
      EmitRequestInfos(inp, "inp_authors") ;
      }
    }
  );

  // get cab from title
  $("#ckeck_title").on("click", function() {
    title = $("#input_title").val();
    console.log(" --- search button for / title :", title );
    EmitRequestCab(title) ;
  });

  // get refs list from author
  $("#ckeck_author_refs").on("click", function() {
    author = $("#input_author").val();
    console.log(" --- search button for / author :", author );
    EmitRequestRefs(author) ;
  });

  // get data from clickable rows
  $("#search_results tr").on("click", function() {
    console.log("getting cab from table... ");
    // var cab_a = $(this).attr("value");
    // console.log("href text : ", cab_a);
  });

  // RECEIVE RESPONSE TITLES_LIST FROM SERVER
  socket.on('io_resp_infos_list', function(infos) {

    console.log(" *** io_resp_infos_list / infos : ", infos );
    infos_type  = infos.resp_type ;
    infos_list  = infos.data ;
    var inp ;

    if (infos_type == "inp_titles") {
      var inp = input_title ;
      awesomplete_title.list = infos_list ;
    }
    else if (infos_type == "inp_authors") {
      var inp = input_author ;
      awesomplete_auth.list = infos_list ;
    };

    inp.focus();
    var inpLen = inp.val().length;
    inp[0].setSelectionRange(inpLen, inpLen);;

  });

  // RECEIVE RESPONSE CAB AND AUTHOR FROM SERVER
  socket.on("io_resp_cab", function(ref) {
    console.log(" *** io_resp_cab / ref : ", ref );
    var cab_    = ref.cab ;
    var author_ = ref.author ;
    // console.log(" *** io_resp_cab / cab_ : ", cab_ );
    // copy cab_ to input in form
    $("#cab_code").focus()   ;
    // $("#cab_code").click()   ;
    $("#cab_code").val(cab_) ;

    $("#input_author").focus()   ;
    $("#input_author").val(author_) ;

  });

  // RECEIVE RESPONSE REFS FROM SERVER
  socket.on("io_resp_refs", function(refs) {
    console.log(" *** io_resp_refs / refs : ", refs );
    // $('#mod_loader').modal('hide');

    var refs_list  = refs.refs_list ;
    console.log(" *** io_resp_refs / refs_list : ", refs_list );

    // new Awesomplete( input_title, {
    //   list: refs.unique_titles ,
    //   minChars : 3 ,
    //   maxItems : 50
    // });

    table_c.empty();
    var k = "" ;
    for(i = 0; i < refs_list.length; i++){
      k+= '<tr value="' + refs_list[i].cab + '">';
      // k+= '<td class="col-xs-3">' + refs.author + '</td>';
      k+= '<td>' + refs_list[i].titre + '</td>';
      k+= '<td>' + refs_list[i].C2 + '</td>';
      k+= '<td>' + refs_list[i].cab + '</td>';
      k+= '</tr>';
    };
    table_c.html(k) ;

  });





})
