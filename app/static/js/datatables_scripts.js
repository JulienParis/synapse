
$(document).ready( function(){

  // dynamic tables
  var table = $('#tableParcours').DataTable( {

    "language": {
                "lengthMenu": "montrer _MENU_ ouvrages par page",
                "zeroRecords": "Rien trouvé - sorry",
                "info": "page _PAGE_ de _PAGES_",
                "infoEmpty": "pas d'info disponible",
                "infoFiltered": "(filtré sur _MAX_ entrées)",
                "search":         "rechercher :",
                "paginate": {
                    "first":      "première page",
                    "last":       "dernière",
                    "next":       "suivante",
                    "previous":   "précédente"
                },
      },
      select: {
        style: 'multi'
      },


    initComplete: function () {
      this.api().columns().every( function () {
        var column = this;
        var select = $( '<select class="selectpicker" data-size="15" data-width="75px" title="filter" data-style="btn-info"><option value=""> - FILTRER - </option></select>' )
            .appendTo( $(column.footer()).empty() )
            .on( 'change', function () {
                 var val = $.fn.dataTable.util.escapeRegex(
                     $(this).val()
                );
                column
                    .search( val ? '^'+val+'$' : '', true, false )
                    .draw();
             } );

         column.data().unique().sort().each( function ( d, j ) {
            select.append( '<option value="'+d+'">'+d+'</option>' )
         } );
      } );
   }
        // buttons: [ 'copy', 'excel', 'pdf', 'colvis' ]
        // "scrollY"       : "250px",
        // "scrollCollapse": true,
        // "paging"        : true,
        // "columnDefs"    : [ "order"  : [ [ 5, "desc" ] ]  ],

  });


  ///////////////////////////////////////////
  // EMIT REQUEST DELETE ITEMS LIST TO SERVER
  function EmitDeleteItems(list_items) {
    console.log(" *** EmitDeleteItems / string_ : ", list_items );
    socket.emit(  'io_delete_from_parcours',
                  { data     : list_items ,
                  }
                );
  };


  $('.btn_delete_items').click( function () {

    // var parent_table = $(this).closest('.tableParcours') ;
    // console.log("--- check parent_table : ", parent_table);

    var selected_rows = table.rows('.selected') ;
    console.log("--- check selected_rows : ", selected_rows);

    // get selected_items data
    var selected_rows_ids  = selected_rows.ids() ;
    var selected_rows_data = selected_rows.data() ;
    console.log("--- check selected_rows_data : ", selected_rows_data);

    // recreate dictionary from data
    var list_cab_to_delete = {} ;
    for(i = 0; i < selected_rows_data.length; i++){
      list_cab_to_delete[ selected_rows_data[i][0] ] = []
    };
    for(i = 0; i < selected_rows_ids.length; i++){
      // console.log("--- selected_rows_data[i] : ", selected_rows_data[i] );
      // list_cab_to_delete[ selected_rows_data[i][0] ].push(  {"cab" : selected_rows_ids[i]}  ) ;
      list_cab_to_delete[ selected_rows_data[i][0] ].push(  selected_rows_ids[i]  ) ;
    };

    console.log("--- list_cab_to_delete : ", list_cab_to_delete );

    // emit request
    EmitDeleteItems(list_cab_to_delete) ;

    // remove from datatable
    selected_rows.remove().draw( false );


  });




});
