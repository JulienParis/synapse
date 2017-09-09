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

  function hide_empty_resultsTable(){
    $("#oneref_resume").css("display", "none") ;
    $("#search_results_table").css("display", "none") ;
    table_c.empty();
  };

  function show_resultsTable() {

    $("#search_results_table").css("display", "") ;
    $("#collapseResults").collapse("show") ;

  };




  /////////////////////////////////////
  // EMIT REQUEST INFOS LISTS TO SERVER
  function EmitRequestInfos(string_, inp_type) {
    console.log(" *** EmitRequestInfos / string_ : ", string_, " / inp_type : ", inp_type );
    socket.emit(  'io_request_infos_list',
                  { data     : string_ ,
                    inp_type : inp_type
                  }
                );
  };

  // GET VALUES INPUT ON CHANGE
  $("#input_title").on("input", function() {

    // clean previous inputs
    $("#cab_code").val("") ;
    $("#input_author").val("") ;
    //table_c.empty();
    hide_empty_resultsTable();

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
    //table_c.empty();
    hide_empty_resultsTable();

    console.log(" --- input : ", inp);
    if (inp.length >= 3 ) {
      // emit request to server
      EmitRequestInfos(inp, "inp_authors") ;
      }
    }
  );


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


  //////////////////////////////
  // EMIT REQUEST CAB TO SERVER
  function EmitRequestCab(string_) {
    console.log(" *** EmitRequestCab / string_ : ", string_ );
    socket.emit(  'io_request_cab',
                  { data     : string_ ,
                  }
                );
  };

  // get cab from title
  $("#ckeck_title").on("click", function() {
    title = $("#input_title").val();
    console.log(" --- search button for / title :", title );
    if (title != "" ) {
      EmitRequestCab(title) ;
    };
  });




  ///////////////////////////////////////
  // EMIT REQUEST AUTHOR'S REFS TO SERVER
  function EmitRequestRefs(author_name) {
    console.log(" *** EmitRequestRefs / author_name : ", author_name );
    socket.emit(  'io_request_refs',
                  { data     : author_name ,
                  }
                );
  };

  // get refs list from author
  $("#ckeck_author_refs").on("click", function() {
    author = $("#input_author").val();
    console.log(" --- search button for / author :", author );
    if (author != "") {
      var $btn = $(this).button('loading');
      EmitRequestRefs(author) ;
    };
  });



  //////////////////////////////////////////
  // EMIT REQUEST AUTHOR AND TITLE TO SERVER
  function EmitRequestOneRef(cab) {
    console.log(" *** EmitRequestOneRef / cab : ", cab );
    socket.emit(  'io_request_oneref',
                  { data     : cab ,
                  }
                );
  };

  $("#cab_code").on("input", function() {

    $("#input_author").val("") ;
    $("#input_title").val("") ;
    //table_c.empty();
    hide_empty_resultsTable();

  });

  // get infos from cab
  $("#ckeck_oneref").on("click", function() {
  //function Check_OneRef() {
    cab = $("#cab_code").val();
    console.log(" --- search button for / cab :", cab );
    EmitRequestOneRef(cab) ;
  });

  // RECEIVE RESPONSE ONEREF FROM SERVER
  socket.on('io_resp_oneref', function(infos_ref) {

    console.log(" *** io_resp_oneref / infos_ref : ", infos_ref );
    oneref_author  = infos_ref.author ;
    oneref_title   = infos_ref.title ;
    oneref_resume  = infos_ref.resume ;


    $("#input_author").focus()  ;
    $("#input_author").val(oneref_author) ;

    $("#input_title").focus()    ;
    $("#input_title").val(oneref_title) ;

    $("#ckeck_author_refs").click();

    AddResume(oneref_resume);


  });






  ////////////////////////////////
  // get data from clickable rows
  $("#search_results").on("click", "tr", function() {
    console.log( "getting cab from table... ", $(this) );
    var resume    = $(this).attr("resume") ;
    console.log( "getting cab from table... resume :  ", resume );

    var infos_ref = $(this).find('td');
    // console.log( "getting cab from table... / infos_ref : ", infos_ref.eq(0).text() );
    var title = infos_ref.eq(0).text() ;
    var cab   = infos_ref.eq(2).text() ;
    console.log("getting cab from table... / cab : ", cab );

    $("#cab_code").focus()  ;
    $("#cab_code").val(cab) ;

    $("#input_title").focus()    ;
    $("#input_title").val(title) ;

    AddResume(resume);

  });


  // RECEIVE RESPONSE CAB AND AUTHOR FROM SERVER
  socket.on("io_resp_cab", function(ref) {
    console.log(" *** io_resp_cab / ref : ", ref );
    var cab_    = ref.cab ;
    var author_ = ref.author ;
    var resume_ = ref.resume ;
    // console.log(" *** io_resp_cab / cab_ : ", cab_ );
    // copy cab_ to input in form
    $("#cab_code").focus()   ;
    $("#cab_code").val(cab_) ;

    $("#input_author").focus()   ;
    $("#input_author").val(author_) ;

    // var prev_author = $("#input_author").val() ;
    //console.log(" *** io_resp_cab / prev_author : ", prev_author );
    // if (author_ != prev_author) {
    $("#ckeck_author_refs").click();
    // };

    AddResume(resume_);

  });


  function AddResume(resume) {

    $("#oneref_resume").css("display", "");

    if (resume != "") { $("#_resume").html(resume) ;
    } else {            $("#_resume").html("pas de résumé") ; };

  };

  // RECEIVE RESPONSE REFS FROM SERVER
  socket.on("io_resp_refs", function(refs) {

    console.log(" *** io_resp_refs / refs : ", refs );

    $("#ckeck_author_refs").button('reset') ;

    var refs_list  = refs.refs_list ;
    console.log(" *** io_resp_refs / refs_list : ", refs_list );

    // new Awesomplete( input_title, {
    //   list: refs.unique_titles ,
    //   minChars : 3 ,
    //   maxItems : 50
    // });

    table_c.empty();
    show_resultsTable();

    var k = "" ;
    for(i = 0; i < refs_list.length; i++){
      k+= '<tr resume="' + refs_list[i].resume + '"></td>'; //value="' + refs_list[i].cab + '"
      // k+= '<td class="col-xs-3">' + refs.author + '</td>';
      k+= '<td>' + refs_list[i].titre + '</td>';
      k+= '<td>' + refs_list[i].C2 + '</td>';
      k+= '<td>' + refs_list[i].cab + '</td>';
      k+= '</tr>';
    };
    table_c.html(k) ;

  });





})
