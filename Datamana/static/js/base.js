/*
Changes selected buttons color to grey
*/

$(function() {
  "use strict";

  let path = window.location.pathname;
  path = path.split( '/' );
  let current = path[1];

  $( '#links a' ).css('background-color', 'black')
  $( '#' + current + 'Link' ).css('background-color', 'grey')

});
