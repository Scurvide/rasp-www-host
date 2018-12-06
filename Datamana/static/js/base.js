$(function() {
  "use strict";

  var path = window.location.pathname;
  path = path.split( '/' );
  var current = path[1];

  $( '#links a' ).css('background-color', 'black')
  $( '#' + current + 'Link' ).css('background-color', 'grey')

});
