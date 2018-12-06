$(function() {
  "use strict";

  $( '#commands a' ).on( 'click', function(event) {
    event.preventDefault();
    var url = $( this ).attr( 'href' );
    var splitted = url.split( '/' );
    var command = splitted[splitted.length - 1];
    var client = splitted[splitted.length - 2];

    $.ajax({
      type: 'GET',
      url: url,
      success: function(){
        $( "#" + client + "CommandsTable a" ).css('background-color', 'black')
        $( '#' + client + command + 'Button' ).css('background-color', 'grey')
      }
    });
  });
});
