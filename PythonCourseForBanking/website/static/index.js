$(document).ready(function() {
	$(chart_id).highcharts({
		chart: chart,
		title: title,
		xAxis: xAxis,
		yAxis: yAxis,
		series: series
	});
});


//$(function() {
//    var getPlaceholderIfNotValue = function(input){
//        if (input['value'] == ''){
//            return input['placeholder'];
//        } else {
//            return input['value'];
//        };
//    };
//
//    $(chart_id).highcharts({
//		chart: chart,
//		title: title,
//		xAxis: xAxis,
//		yAxis: yAxis,
//		series: series
//	});
//
//	var get_asset_price = function(e) {
//        $.getJSON($SCRIPT_ROOT + '/chart', {
//            par_value: getPlaceholderIfNotValue($('#get')[0])
//        }, callback);
//    };
//
//    var callback = function(data) {
//        debugger;
//    };
//
//	$('#get').bind('click', get_asset_price);
//};