$(document).ready(function() {
    $('div').fadeIn('slow');
});

var res = '';

function calculate() {
    debugger;
    alert("calculate");
}

var errorCallback = function() {
    debugger;
    alert("Sorry could not proceed");
}

var callback = function(data) {
    debugger;
    res = data;
}

function calculate2() {
//    $("#tableResults tr").remove();
    debugger;

    $.ajax({
        url: "http://127.0.0.1:5000/hello",
        headers: { 'Access-Control-Allow-Origin': '*' }
    }).then(function(data) {
        alert("it worked");
        alert(data);
        res = data;
    });

//    $.ajax({
//        url: "http://rest-service.guides.spring.io/greeting"
//        url: "http://rest-service.guides.spring.io/greeting"
//        type: 'GET',
//        headers: { 'Access-Control-Allow-Origin': '*' },
//        crossDomain: true,
//        datatype: 'jsonp'
//        beforeSend: setHeader
//    }).then(function(data) {
//       alert("it worked");
//       alert(data);
//       res = data;
//    });
    debugger;
}