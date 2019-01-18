/*
Sends get request to url based on button clicked.
Changes selected buttons and commands color to grey.
*/

$(function() {
  "use strict";

  $( '#commands a' ).on( 'click', function(event) {
    event.preventDefault();

    let url = $( this ).attr( 'href' );
    let splitted = url.split( '/' );
    let command = splitted[splitted.length - 1];
    let client = splitted[splitted.length - 2];

    // Ajax request to save selected command to database
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
