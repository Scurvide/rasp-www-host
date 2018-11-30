
$(function() {
  "use strict";

  var rurl = '';

  $( '#clients a' ).on( 'click', function(event) {

      event.preventDefault();
      rurl = $( this ).attr( 'href' );
      $( '#dataBox' ).load( rurl );
      var splitted = rurl.split( '/' );
      $( '#clients a' ).css('background-color', 'black');
      $( '#' + splitted[splitted.length - 1] + 'Client' ).css('background-color', 'grey');
  });

  function autoRefresh() {
    if (rurl != '') {
      $( '#dataBox' ).load( rurl );
    };
  };
  setInterval(autoRefresh, 1000);

});
