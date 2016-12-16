/**
 * Created by SRIN on 2/13/2015.
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


// QUERY URLS
function getURLParameterByName(key){
    var target = document.URL;
    var values = [];
    if(!target){
        target = location.href;
    }

    key = key.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");

    var pattern = key + '=([^&#]+)';
    var o_reg = new RegExp(pattern,'ig');
    while(true){
        var matches = o_reg.exec(target);
        if(matches && matches[1]){
            values.push(matches[1]);
        }
        else{
            break;
        }
    }

    if(!values.length){
        return null;
    }
    else{
        return values.length == 1 ? values[0] : values;
    }

}
/*
// QUERY URLS
function getURLParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? null : decodeURIComponent(results[1].replace(/\+/g, " "));
}*/
function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp); // timestamp is millisecond unit
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = checkTime(a.getHours());
  var min = checkTime(a.getMinutes());
  var sec = checkTime(a.getSeconds());
  var millisecond = a.getMilliseconds();
//  var time = hour + ':' + min + ':' + sec + "." + millisecond;
  var time = min + ':' + sec + "." + millisecond;
  return time;
}
function timeConverterLong(UNIX_timestamp){
  var a = new Date(UNIX_timestamp); // timestamp is millisecond unit
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = checkTime(a.getHours());
  var min = checkTime(a.getMinutes());
  var sec = checkTime(a.getSeconds());
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
//  var time = hour + ':' + min + ':' + sec ;
  return time;
}

function numberWithCommas(x,precision) {
    if (precision>0){
        multiplier = Math.pow(10,precision);
        x = parseFloat(Math.round(x * multiplier) / multiplier).toFixed(precision);
    }
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function checkTime(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

function handleAjaxError( xhr, textStatus, error ) {
    if ( textStatus === 'timeout' ) {
        alert( 'The server took too long to send the data.' );
    }
    else {
        alert( 'An error occurred on the server. Please try again in a minute.' );
    }
}