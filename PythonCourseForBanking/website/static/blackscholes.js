$(function() {

    var getPlaceholderIfNotValue = function(input){
        if (input['value'] == ''){
            return input['placeholder'];
        } else {
            return input['value'];
        };
    };

    var calculateBlackScholes = function(e) {

        if ($('#call')[0]['checked'] == true) {
            call_put = 'call';
        } else if ($('#put')[0]['checked'] == true) {
            call_put = 'put';
        } else {
            alert("You need to select the option type.")
        };
        $.getJSON($SCRIPT_ROOT + '/price_with_blackscholes', {
            underlying_price: getPlaceholderIfNotValue($('#underlyingPrice')[0]),
            strike_price: getPlaceholderIfNotValue($('#strikePrice')[0]),
            rate: getPlaceholderIfNotValue($('#rate')[0]),
            time_to_maturity: getPlaceholderIfNotValue($('#timeToMaturity')[0]),
            volatility: getPlaceholderIfNotValue($('#volatility')[0]),
            call_put: call_put
        }, callback);
    };

    var callback = function(data) {
        $('#optionPrice').html(data.option_price);
        $('#delta').html(data.delta);
        $('#gamma').html(data.gamma);
        $('#vega').html(data.vega);
        $('#theta').html(data.theta);
        $('#rho').html(data.rho);
        return data;
    }

    $('#calculate').bind('click', calculateBlackScholes);
});
