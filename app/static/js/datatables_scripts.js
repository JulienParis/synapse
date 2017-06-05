
$(document).ready( function(){

  // dynamic tables
  var table = $('.tableParcours').DataTable( {

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



});
