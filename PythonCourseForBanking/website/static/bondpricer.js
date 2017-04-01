$(function() {
    var getPlaceholderIfNotValue = function(input){
        if (input['value'] == ''){
            return input['placeholder'];
        } else {
            return input['value'];
        };
    };

    var calculateBondPrice = function(e) {
        if ($('#noCoupon')[0]['checked'] == true) {
            coupon_periodicity = 'no_coupon';
        } else if ($('#monthly')[0]['checked'] == true) {
            coupon_periodicity = 'monthly';
        } else if ($('#quarterly')[0]['checked'] == true) {
            coupon_periodicity = 'quarterly';
        } else if ($('#semiAnnual')[0]['checked'] == true) {
            coupon_periodicity = 'semi_annual';
        } else if ($('#annual')[0]['checked'] == true) {
            coupon_periodicity = 'annual';
        } else {
            alert("You need to select the coupon periodicity.")
        };

        $.getJSON($SCRIPT_ROOT + '/price_bonds', {
            par_value: getPlaceholderIfNotValue($('#parValue')[0]),
            annual_discount_rate: getPlaceholderIfNotValue($('#annualDiscountRate')[0]),
            annual_coupon_rate: getPlaceholderIfNotValue($('#annualCouponRate')[0]),
            maturity: getPlaceholderIfNotValue($('#maturity')[0]),
            coupon_periodicity: coupon_periodicity
        }, callback);
    };

    var callback = function(data) {
        $('#tableResults tbody').remove();
        coupons = data['coupons'];
        var table = document.getElementById("tableResults");
        var tbody = document.createElement("tbody");
            table.appendChild(tbody);
            for (var i = 0; i < coupons.length; i++) {
                var row = document.createElement("tr");

                // Period
                var cell = document.createElement("td");
                cell.textContent = coupons[i]['Period'];
                row.appendChild(cell);
                // Payment
                var cell = document.createElement("td");
                cell.textContent = coupons[i]['Payment'];
                row.appendChild(cell);
                // Present Value
                var cell = document.createElement("td");
                cell.textContent = coupons[i]['PresentValue'];
                row.appendChild(cell);

                tbody.appendChild(row);
            }

        $('#bondPrice').html(data.price);
        $('#sensitivity').html(data.sensitivity);
        $('#convexity').html(data.convexity);
    };

    $('#price').bind('click', calculateBondPrice);
});
