
// INITIATE SOCKET IO CONNECTION
// var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket = io.connect('http://' + document.domain + ':' + location.port, { transports: ["websocket"] });
socket.on('connect', function() {
  socket.emit( 'connect_' );
});

// loader
$('#mod_loader').modal('show') ;


$(document).ready( function(){


  // please wait at login script
  $(".login_button").on("click", function() {

    $(this).button('loading') ;
    console.log("--- login button : ", $(this));

    var parent_form = $(this).closest('.form_login') ;
    console.log("--- login form : ", parent_form);

    setTimeout(function(){
      //$("#form_login").submit() ;
      parent_form.submit();
    }, 100) ;
  });

  // activate bootstrap dropdown / carousel
  $('#mod_loader').modal('hide');


  var isUser_data = $("#meta_isUser").attr("data") ;
  console.log("--- check if isUser / isUser_data : ", isUser_data);
  if (isUser_data == "None"){
    // $('#mod_intro').modal('show');
    $('#mod_howto').modal('show');
  } else {
    $('#update_user_form').modal('show');
  };


  $(".dropdown-toggle").dropdown() ;
  $('.carousel').carousel(
    {interval: 5000}
  );

  // close all modals and show loader on click on button .close_n_load
  function close_n_load(){
    // console.log("--- close_n_load ---");
    setTimeout(function(){
      $(".modal").modal("hide");
    }, 100);
    $('#mod_loader').modal('show');
  };

  $(".close_n_load").click(function(){
    close_n_load();
  });

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
