// loader
$('#mod_loader').modal('show') ;


// INITIATE SOCKET IO CONNECTION
// var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket = io.connect('http://' + document.domain + ':' + location.port, { transports: ["websocket"] });
socket.on('connect', function() {
  socket.emit( 'connect_' );
  $('#mod_loader').modal('hide') ;
});


var isSettingsOpen = false ; 
var isActivated    = false ; 

$(document).ready( function(){


  // 
  function close_n_load ( ) {
    
    $.when(   console.log("close_n_load : hide modals ") , 
              $('.modal').modal("hide") , 
          )
      .then(  console.log("close_n_load : show loader 1 ") , 
              // setTimeout( function () { $('#mod_loader').modal("show") }, 2000 ), 
              $('#mod_loader').modal("show"),
              console.log("close_n_load : show loader 2 ") 
           );
    // callback();
  };
  
  function loader_then_submit ( form ) {
    $('.modal').modal("hide") ;
    $.when(   
        close_n_load () ,
    )
     .then( 
        console.log("loader_then_submit : submit form ") , 
        // setTimeout( function () { form.submit()  }, 2000 ), 
        $('#mod_loader').modal("show", function() {
          form.submit() 
        })
        
     )
    
  };

  $(".close_n_load").on("click", function () {
    close_n_load() ;
  })

  // please wait at submit script
  $(".submit_button").on("click", function() {

    $(this).button('loading') ;
    console.log("--- submit_button : ", $(this));

    // var parent_form = $(this).closest('.form_login') ;
    var parent_form = $(this).closest('form') ;
    console.log("--- submit_button : ", parent_form);

    loader_then_submit( parent_form ) ;
    // setTimeout(function(){
    //   parent_form.submit();
    // }, 500) ;

  });


  //
  $(".open_howto").on("click", function(){
    $.when( $(".modal").modal("hide") )
    .then( $("#mod_howto").modal("show") )
  });

  $(".open_about").on("click", function(){
    $.when( $(".modal").modal("hide") )
    .then( $("#mod_about").modal("show") )
  });

  $(".open_intro").on("click", function(){
    $.when( $(".modal").modal("hide") )
    .then( $("#mod_intro").modal("show") )
  });


  // settings state
  $("#btn_settings").on("click", function () {
    $("#collapseSettings").collapse("toggle") 
  });


  // toggle click mode
  $("#btn_click_mode").on("click", function() {

    $("#span_click_mode").toggleClass("fa-toggle-off");
    $("#span_click_mode").toggleClass("fa-toggle-on");

    isActivated = $("#span_click_mode").hasClass("fa-toggle-on") ;
    // console.log("isActivated", isActivated);
    
    if ( isActivated ) {
      $(".modal").modal("hide") ;
      $("#collapseSettings").collapse("hide") ;
    //   console.log("activated btn click mode");
    //   $("#btn_click_mode").attr( "title", " clic sur les points : activé " ) ;
    } else {
      //   console.log("deactivated btn click mode");
    //   $("#btn_click_mode").attr( "title", " clic sur les points : désactivé " ) ;     
    }

  });    

  // show howto or user_form at launch
  var isUser      = $("#meta_isUser").attr("data") ;
  var isUser_data = $("#meta_isData").attr("data") ;

  console.log("--- check if isUser / isUser_data : ", isUser_data);
  if ( isUser === "None" ){
    // $('#mod_intro').modal('show');
    $('#mod_intro').modal('show');
  } else {
    if ( isUser_data == "False" ) {
      // $('#update_user_form').modal('show');
      // $('#mod_intro').modal('show');    
      $('#update_aloes_form').modal('show');    
    }
  };


  $(".dropdown-toggle").dropdown() ;
  $('.carousel').carousel(
    {interval: 5000}
  );

  // close all modals and show loader on click on button .close_n_load
  // function close_n_load(){
  //   // console.log("--- close_n_load ---");
  //   setTimeout(function(){
  //     $(".modal").modal("hide");
  //   }, 100);
  //   $('#mod_loader').modal('show');
  // };

  // $(".close_n_load").click(function(){
  //   close_n_load();
  // });




  // open login modal from intro
  $(".log_from_howto").click( function() {
    $.when( $(".modal").modal("hide") )
     .then( $("#login_form").modal("show") ) 
  }) ;


  // open register modal from login modal or modal howto
  $(".register_trigger").click( function() {
    $.when( $(".modal").modal("hide") )
     .then( $("#register_form").modal("show") ) 
  }) ;

  // // fades alerts
  window.setTimeout(function() {
    $(".alert_fade").fadeTo(1500, 0).slideUp(1500, function(){
      $(this).remove();
    });
  }, 10000);


  // restore btns unfocused state after closing modals
  $('.modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    button.one('focus', function (event) {
        $(this).blur();
    });
  });


    // show settings
    // $("#showSettings").click( function() {
    //   $(".dg").toggle() ;
    // }) ;

    // $(".close-button").hide() ;

    $("#closeSettings").click( function() {
      $("#collapseSettings").collapse("hide") ;
    });

  // dynamic tables
  // var table = $('.tableParcours').DataTable( {
  //
  //   "language": {
  //               "lengthMenu": "montrer _MENU_ ouvrages par page",
  //               "zeroRecords": "Rien trouvé - sorry",
  //               "info": "page _PAGE_ de _PAGES_",
  //               "infoEmpty": "pas d'info disponible",
  //               "infoFiltered": "(filtré sur _MAX_ entrées)",
  //               "search":         "rechercher :",
  //               "paginate": {
  //                   "first":      "première page",
  //                   "last":       "dernière",
  //                   "next":       "suivante",
  //                   "previous":   "précédente"
  //               },
  //           },
  //
  //   initComplete: function () {
  //    this.api().columns().every( function () {
  //        var column = this;
  //        var select = $( '<select class="selectpicker" data-size="15" data-width="75px" title="filter" data-style="btn-info"><option value=""> - FILTRER - </option></select>' )
  //            .appendTo( $(column.footer()).empty() )
  //            .on( 'change', function () {
  //                var val = $.fn.dataTable.util.escapeRegex(
  //                    $(this).val()
  //                );
  //                column
  //                    .search( val ? '^'+val+'$' : '', true, false )
  //                    .draw();
  //            } );
  //
  //        column.data().unique().sort().each( function ( d, j ) {
  //            select.append( '<option value="'+d+'">'+d+'</option>' )
  //        } );
  //    } );
  //  }
  //       // buttons: [ 'copy', 'excel', 'pdf', 'colvis' ]
  //       // "scrollY"       : "250px",
  //       // "scrollCollapse": true,
  //       // "paging"        : true,
  //       // "columnDefs"    : [ "order"  : [ [ 5, "desc" ] ]  ],
  //
  // });



  // activate bootstrap tooltips with custom caller (data-tooltip instead of data-toggle)
  $(function () {
      $('[data-tooltip="tooltip"]').tooltip()
  });

  // manage appear on hover and disappear after x milliseconds
  $('.bstooltip').mouseenter(function(){
      var that = $(this);
      that.tooltip('show');
      // setTimeout(function(){
      //   that.tooltip('hide');
      // }, 10000);
  });

  $('.bstooltip').mouseleave(function(){
      $(this).tooltip('hide');
  });

  // click dropdown on hover
  $('.dropdown').hover(function(){
    $('.dropdown-toggle', this).trigger('click');
  });


  // smooth scrolldown
  $('body').scrollspy({target: ".modal", offset: 0});
  $('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .on('click', function(event) {
    
      // Make sure this.hash has a value before overriding default behavior
      if (this.hash !== "") {
        
        // Prevent default anchor click behavior
        event.preventDefault();
    
        // Store hash
        var hash = this.hash ;
        var parentModal  = $(this).closest('.modal') ;
        var parentHeight = parentModal.height(); 

        // console.log(hash);
        // console.log(parentModal);
        
        // Using jQuery's animate() method to add smooth page scroll
        // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
        // parentModal.animate({ scrollTop: $(hash).offset().top }, 800 );
        // console.log( $(hash).offset() ) ;
        // console.log( $(hash).position() ) ;
        // parentModal.animate({ scrollTop: $(hash).offset().top }, 'slow');
        parentModal.animate({ scrollTop: $(hash).position().top + 20 }, 'slow');
        
      } // End if
    
    });




  // refresh view
  function refreshPage (href){
      //console.log(href);
      window.location = href ;
  };


  // // fades alerts
  window.setTimeout(function() {
      $(".alert_fade").fadeTo(500, 0).slideUp(500, function(){
    $(this).remove();
      });
  }, 4000);



  // tooltip with image inside
  $('.tooltip_img').tooltip({
      animated : 'fade',
      placement: 'left',
      html     : true
  });


  //change app scale if view on mobile screen :
  var screen_width = window.innerWidth;
  // console.log("$(document).ready / screen_width : ", screen_width);
  if (screen_width < 600 ) {
  // if (navigator.userAgent.match(/iPhone/i) || navigator.userAgent.match(/iPad/i)) {
    // console.log("--- !!! --- small screen_width < 600px  ");

    // var viewportmeta = document.querySelector('meta[name="viewport"]');
    // if (viewportmeta) {
    //   viewportmeta.content = 'width=device-width, minimum-scale=1.0, maximum-scale=1.0, initial-scale=0.35';
    //   document.body.addEventListener('gesturestart', function () {
    //       viewportmeta.content = 'width=device-width, minimum-scale=0.35, maximum-scale=1.0';
    //   }, false);
    // }
    // $("meta[name='viewport']").attr("content", "width=device-width, initial-scale=0.1");
    $("meta[name='viewport']").attr("content", "width=device-width, initial-scale=0.35");
  }
  else if (screen_width < 800 ) {
    // console.log("--- !!! --- small screen_width < 800px  ");
    $("meta[name='viewport']").attr("content", "width=device-width, initial-scale=0.7");

  };





});
