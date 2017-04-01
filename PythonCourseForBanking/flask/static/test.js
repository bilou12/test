$(function() {
    var displayAlert = function(){
        alert("Someone smart has clicked on the button")
    };
    debugger;
    $('#clicker').bind('click', displayAlert);
});