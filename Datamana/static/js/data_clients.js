/*
When selecting client to see the data of:
Loads data for related url to #dataBox and calls charter function.
Charter function generates graphs from datalist generated in #dataBox
and constructs them to chartTables in html table format.
Refreshes data from server every refreshTime.
*/

$(function() {
  "use strict";

  let refreshTime = 1000; // Refresh time for data reloads from database
  let rurl = '';

  // CSS style included to chartTables to ensure it is
  // loaded before a graph is generated
  $('.chartTable').append("<link rel='stylesheet' type='text/css' href=" + chartCSS + ">");

  // Loads data based on selected client
  $( '#clients a' ).on( 'click', function(event) {
    event.preventDefault();
    rurl = $( this ).attr( 'href' );
    $( '.chartTable tr' ).remove();
    $( '#dataBox' ).load( rurl );
    var splitted = rurl.split( '/' );
    $( '#clients a' ).css('background-color', 'black');
    $( '#' + splitted[splitted.length - 1] + 'Client' ).css('background-color', 'grey');
  });

  // Refreshes data from database every refreshTime
  function autoRefresh() {
    if (rurl != '') {
      $( '#dataBox' ).load( rurl ).ajaxComplete(charterManager());
    };
  };
  setInterval(autoRefresh, refreshTime);

  // dataTables is generated in data.html. It has data required
  // for generating all graphs for this client.
  function charterManager() {
    for (let u = 0; u < dataTables.length; u++) {
      charter( dataTables[u], dataTypes[u], dataUnits[u] )
    }
  };

});

function charter( dataTable, dataType, dataUnit ) {

  let chart = [];
  let autoScaling = true;
  let graph = true;

  if ( dataTable != {} && graph) {

    if ( dataType === 'measurement' ) {

      // Convert number strings to floats
      for (let o = 0; o < dataTable.length; o++) {
        dataTable[o].y = parseFloat(dataTable[o].y);
      }

      // Convert meters to cm if deciamls exist in data
      if (dataUnit === 'm' && unitConversion()) {
        dataUnit = 'cm';
      }

      // Chart construction from data to matrix
      let min = getMinY();
      let max = getMaxY();
      let yRange = max - min;
      let xRange = dataTable.length;
      // Scaling if necessary
      let scale = 1;
      if (autoScaling == true) {
        scale = autoScale(dataTable, min, max)
        if ( scale != 1 ) {
          min = getMinY();
          max = getMaxY();
          yRange = max - min;
        }
      }
      chart = Array(xRange + 1).fill().map(()=>Array(yRange).fill());

      // Populating matrix with data to form a graph
      for (let n = min; n <= max; n++) {
        chart[0][n - min] = n * scale;
      }
      for (let x = 0; x < xRange; x++) {
        for (let y = max; y >= min; y--) {
          if (y == dataTable[x].y) {
            chart[x + 1][y - min] = 1;
          }
          else {
            chart[x + 1][y - min] = 0;
          }
        }
      }

      // Chart construction from matrix to html table
      let handler = '#chartTable' + dataType.charAt(0).toUpperCase() + dataType.slice(1);
      let handlerTrLast = handler + ' tr:last';
      // Empty the table first
      $( handler + ' tr' ).remove();
      // Header row with y-axel unit and data type
      $( handler ).append(
        "<tr><th id = 'dataUnit'>(" + dataUnit + ")</th>" +
        "<th id = 'dataType' colspan = '" + xRange + "'>" + dataType.charAt(0).toUpperCase() + dataType.slice(1) + "</th></tr>"
      );
      // Graph construction
      for (let row = yRange; row >= 0; row--) {
        $( handlerTrLast ).after('<tr></tr>');
        for (let col = 0; col <= xRange; col++) {
          // Y-axel value indicators
          if ( col === 0 ) {
            $( handlerTrLast ).append("<td class = 'y-axel'>" + chart[col][row] + "</td>");
          }
          // Data points
          else if ( chart[col][row] != 0 ) {
            $( handlerTrLast ).append("<td class = 'dataCell'>&#9899</td>");
          }
          // Empty cells in graph
          else {
            $( handlerTrLast ).append("<td class = 'dataCell'></td>");
          }
        }
      }
      // X-axel time indicators
      let date = dataTable[0].x;
      let dateM = dataTable[xRange - 1].x;
      $( handlerTrLast ).after(
        "<tr><td></td>" +
        "<td id='xFirst' class='x-axel' colspan='" +(xRange)/2+ "'>" +
        date.getDate() +'/'+ (date.getMonth()+1) +'/'+ date.getFullYear() +' '+ date.getHours() +':'+ date.getMinutes() +
        "</td><td id='xLast' class='x-axel' colspan='" +(xRange)/2+ "'>" +
        dateM.getDate() +'/'+ (dateM.getMonth() + 1) +'/'+ dateM.getFullYear() +' '+ dateM.getHours() +':'+ dateM.getMinutes() +
        "</td></tr>"
      );
    }

    else if ( dataType === 'tally' ) {

      // Convert number strings to ints
      for (let o = 0; o < dataTable.length; o++) {
        dataTable[o].y = parseInt(dataTable[o].y);
      }

      // Grouping tallies by time
      let timeUnit = getTimeUnit(dataTable);
      dataTable = barTimeGroup(dataTable, timeUnit);

      // Chart construction from data to matrix
      let min = 0;
      let max = getMaxY();
      let yRange = max;
      let xRange = dataTable.length;
      // Scaling if necessary
      let scale = 1;
      if (autoScaling == true) {
        scale = autoScale(dataTable, min, max)
        if ( scale != 1 ) {
          max = getMaxY();
          yRange = max;
        }
      }
      chart = Array(xRange + 1).fill().map(()=>Array(yRange).fill());

      // Populating matrix with data to form a graph
      for (let n = 0; n < max; n++) {
        chart[0][n] = (n + 1) * scale;
      }
      for (let x = 0; x < xRange; x++) {
        for (let y = yRange; y > 0; y--) {
          if (y == dataTable[x].y) {
            for (let i = y - 1; i >= 0; i--) {
              chart[x + 1][i] = 1;
            }
            break;
          }
          else {
            chart[x + 1][y - 1] = 0;
          }
        }
      }

      // Chart construction from matrix to html table
      let handler = '#chartTable' + dataType.charAt(0).toUpperCase() + dataType.slice(1);
      let handlerTrLast = handler + ' tr:last';
      // Empty the table first
      $( handler + ' tr' ).remove();
      // Header row with y-axel unit and data type
      $( handler ).append(
        "<tr><th id = 'dataUnit'></th>" +
        "<th id = 'dataType' colspan = '" + xRange + "'>" + dataType.charAt(0).toUpperCase() + dataType.slice(1) + "</th></tr>"
      );
      // Graph construction
      for (let row = yRange - 1; row >= 0; row--) {
        $( handlerTrLast ).after('<tr></tr>');
        for (let col = 0; col <= xRange; col++) {
          // Y-axel value indicators
          if ( col === 0 ) {
            $( handlerTrLast ).append("<td class = 'y-axel'>" + chart[col][row] + "</td>");
          }
          // Data points
          else if ( chart[col][row] != 0 ) {
            $( handlerTrLast ).append("<td class = 'dataCellBar'></td>");
          }
          // Empty cells in graph
          else {
            $( handlerTrLast ).append("<td class = 'dataCell'></td>");
          }
        }
      }
      // X-axel time indicators and time unit
      $( handlerTrLast ).after("<tr><td></td></tr>");
      for (let col = 0; col < xRange; col++) {
        let time;
        if ( timeUnit === 'y') { time = dataTable[col].x.getFullYear(); }
        else if ( timeUnit === 'mo') { time = dataTable[col].x.getMonth() + 1; }
        else if ( timeUnit === 'd') { time = dataTable[col].x.getDate(); }
        else if ( timeUnit === 'h') { time = dataTable[col].x.getHours(); }
        else { time = dataTable[col].x.getMinutes(); }
        $( handlerTrLast ).append("<td class = 'x-axel'>" + time + "</td>");
      }
      $( handlerTrLast ).append("<th>(" + timeUnit + ")</th>");
    }
    // If dataType is not supported, empty the table
    else {$('#chartTable' + dataType.charAt(0).toUpperCase() + dataType.slice(1) + 'tr').remove();}

  }

  // Functions for finding min and max data point from dataTable
  function getYs(){
    return dataTable.map(d => d.y);
  }
  function getMinY() {
    return Math.min(...getYs());
  }
  function getMaxY() {
    return Math.max(...getYs());
  }

  // Unit conversion from m to cm (in this case)
  // by multiplying with 100 if data has decimals
  function unitConversion () {
    for (let n = 0; n < dataTable.length; n++) {
      if (dataTable[n].y % 1 != 0) {
        for (let i = 0; i < dataTable.length; i++) {
          dataTable[i].y = dataTable[i].y * 100;
          dataTable[i].y.toFixed();
        }
        return true;
      }
    }
    return false;
  }

  // Time unit and range finder for bar chart
  function getTimeUnit( dataTable ) {
    let year = false, month = false, day = false, hour = false, minute = false;
    let timeDifference = dataTable[dataTable.length-1].x.getTime() - dataTable[0].x.getTime();
    if ( timeDifference > 31556926000 ) { return 'y'; }
    else if ( timeDifference > 2629743830 ) { return 'mo' }
    else if ( timeDifference > 86400000 ) { return 'd'; }
    else if ( timeDifference > 3600000 ) { return 'h'; }
    else { return 'min'; }
  }

  // Add tally values together based on time and timeUnit
  function barTimeGroup( dataTable, timeUnit ) {
    let len = dataTable.length;
    if ( timeUnit == 'y' ) {
      for (let n = 0; n < len - 1; n++) {
        while (dataTable[n].x.getFullYear() === dataTable[n+1].x.getFullYear()) {
          dataTable[n].y = dataTable[n].y + dataTable[n+1].y;
          dataTable.splice(n+1, 1);
          len--;
          if ( n >= len - 1 ) { break; }
        }
      }
    }
    else if ( timeUnit == 'mo' ) {
      for (let n = 0; n < len - 1; n++) {
        while (dataTable[n].x.getMonth() === dataTable[n+1].x.getMonth()) {
          dataTable[n].y = dataTable[n].y + dataTable[n+1].y;
          dataTable.splice(n+1, 1);
          len--;
          if ( n >= len - 1 ) { break; }
        }
      }
    }
    else if ( timeUnit == 'd' ) {
      for (let n = 0; n < len - 1; n++) {
        while (dataTable[n].x.getDate() === dataTable[n+1].x.getDate()) {
          dataTable[n].y = dataTable[n].y + dataTable[n+1].y;
          dataTable.splice(n+1, 1);
          len--;
          if ( n >= len - 1 ) { break; }
        }
      }
    }
    else if ( timeUnit == 'h' ) {
      for (let n = 0; n < len - 1; n++) {
        while (dataTable[n].x.getHours() === dataTable[n+1].x.getHours() ) {
          dataTable[n].y = dataTable[n].y + dataTable[n+1].y;
          dataTable.splice(n+1, 1);
          len--;
          if ( n >= len - 1 ) { break; }
        }
      }
    }
    else if ( timeUnit == 'min' ) {
      for (let n = 0; n < len - 1; n++) {
        while ( dataTable[n].x.getMinutes() === dataTable[n+1].x.getMinutes() ) {
          dataTable[n].y = dataTable[n].y + dataTable[n+1].y;
          dataTable.splice(n+1, 1);
          len--;
          if ( n >= len - 1 ) { break; }
        }
      }
    }
    return dataTable;
  }

  // Autoscale function scales dataTable data and
  // returns scale based on minimum and maximum values given.
  function autoScale( dataTable, min, max ) {
    let scale = 1;
    if ( max - min > 100) {
      scale = 10;
      for ( let n = 0; n < dataTable.length; n++ ) {
        dataTable[n].y = dataTable[n].y / scale;
        dataTable[n].y = dataTable[n].y.toFixed();
      }
      return scale;
    }
    else if ( max - min > 50) {
      scale = 5;
      for ( let n = 0; n < dataTable.length; n++ ) {
        dataTable[n].y = dataTable[n].y / scale;
        dataTable[n].y = dataTable[n].y.toFixed();
      }
      return scale;
    }
    else if ( max - min > 20) {
      scale = 2;
      for ( let n = 0; n < dataTable.length; n++ ) {
        dataTable[n].y = dataTable[n].y / scale;
        dataTable[n].y = dataTable[n].y.toFixed();
      }
      return scale;
    }
    return scale;
  }

};
