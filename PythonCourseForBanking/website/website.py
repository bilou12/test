import datetime
import math

import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from scipy.stats import norm
from yahoo_finance import Share

app = Flask(__name__)


class BlackScholesPricer:
    def __init__(self, underlying_price, strike_price, rate, time_to_maturity, volatility, call_put='call'):
        self.underlying_price = underlying_price
        self.strike_price = strike_price
        self.rate = rate
        self.time_to_maturity = time_to_maturity
        self.volatility = volatility
        self.call_put = call_put
        self.d1, self.d2 = self._calculate_d1_d2()
        self.option_price, self.delta, self.gamma, self.theta, self.rho, self.vega = self.get_price_and_greeks()

    def __str__(self):
        return ('result_price = ' + str(self.option_price) + ', delta = ' + str(self.delta) + ', gamma = ' + str(
            self.gamma) + ', theta = ' + str(self.theta) + ', rho = ' + str(self.rho) + ', vega = ' + str(self.vega))

    def _calculate_d1_d2(self):
        d1 = (math.log(self.underlying_price / self.strike_price) + (
            self.rate + self.volatility * self.volatility / 2) * self.time_to_maturity) / (
                 self.volatility * math.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * math.sqrt(self.time_to_maturity)
        return d1, d2

    def get_price_and_greeks(self):
        result_price = self._calculate_option_price()
        delta = self._calculate_delta()
        gamma = self._calculate_gamma()
        theta = self._calculate_theta()
        rho = self._calculate_rho()
        vega = self._calculate_vega()
        return result_price, delta, gamma, theta, rho, vega

    def _calculate_option_price(self):
        if self.call_put.upper() == 'CALL':
            return norm.cdf(self.d1) * self.underlying_price - norm.cdf(self.d2) * self.strike_price * math.exp(
                -self.rate * self.time_to_maturity)
        elif self.call_put.upper() == 'PUT':
            return self.strike_price * math.exp(-self.rate * self.time_to_maturity) * norm.cdf(
                -self.d2) - self.underlying_price * norm.cdf(-self.d1)

    def _calculate_delta(self):
        if self.call_put.upper() == 'CALL':
            return norm.cdf(self.d1)
        elif self.call_put.upper() == 'PUT':
            return norm.cdf(self.d1) - 1

    def _calculate_gamma(self):
        return norm.pdf(self.d1) / (self.underlying_price * self.volatility * math.sqrt(self.time_to_maturity))

    def _calculate_theta(self):
        if self.call_put.upper() == 'CALL':
            return -((self.underlying_price * norm.pdf(self.d1) * self.volatility) / (
                2 * math.sqrt(self.time_to_maturity)) - self.rate * self.strike_price * math.exp(
                -self.rate * self.time_to_maturity) * norm.cdf(self.d2)) / 365
        elif self.call_put.upper() == 'PUT':
            return -((self.underlying_price * norm.pdf(self.d1) * self.volatility) / (
                2 * math.sqrt(self.time_to_maturity)) + self.rate * self.strike_price * math.exp(
                -self.rate * self.time_to_maturity) * (1 - norm.cdf(self.d2))) / 365

    def _calculate_rho(self):
        if self.call_put.upper() == 'CALL':
            return 0.01 * self.time_to_maturity * self.strike_price * math.exp(
                - self.rate * self.time_to_maturity) * norm.cdf(self.d2)
        elif self.call_put.upper() == 'PUT':
            return -0.01 * self.time_to_maturity * self.strike_price * math.exp(
                - self.rate * self.time_to_maturity) * (1 - norm.cdf(self.d2))

    def _calculate_vega(self):
        return 0.01 * self.underlying_price * math.sqrt(self.time_to_maturity) * norm.pdf(self.d1)


class BondPricer:
    def __init__(self, par_value, annual_discount_rate, annual_coupon_rate, maturity, coupon_periodicity):
        self.par_value = par_value
        self.annual_discount_rate = annual_discount_rate
        self.annual_coupon_rate = annual_coupon_rate
        self.maturity = maturity
        self.coupon_periodicity = self._get_coupon_periodicity(coupon_periodicity)
        self.nb_coupons = self.maturity * self.coupon_periodicity
        self.coupons = self._get_coupons()
        self.price, self.sensitivity, self.convexity = self._calculate_price_and_trading_indicators()

    @staticmethod
    def _get_coupon_periodicity(coupon_periodicity):
        dic_convert_coupons = {'no_coupon': 0, 'monthly': 12, 'quarterly': 4, 'semi_annual': 2, 'annual': 1}
        if coupon_periodicity in dic_convert_coupons.keys():
            return dic_convert_coupons[coupon_periodicity]
        else:
            return None

    def _get_coupons(self):
        if self.nb_coupons != 0:
            result_df = pd.DataFrame(data=np.arange(1, 1 + self.nb_coupons), columns=['Period'])
            result_df['Payment'] = self.par_value * self.annual_coupon_rate
            result_df['PresentValue'] = result_df.apply(self._calculate_present_value, axis=1)
            return result_df
        else:
            return pd.DataFrame(columns=['Period', 'Payment', 'PresentValue'])

    def _calculate_present_value(self, x):
        return round(x['Payment'] * (1 / (1 + self.annual_discount_rate) ** x['Period']), 2)

    def _calculate_price_and_trading_indicators(self):
        price = self._get_price()
        sensitivity = self._get_sensitivity(price)
        convexity = self._get_convexity(price)
        return price, sensitivity, convexity

    def _get_price(self):
        return self.coupons['PresentValue'].sum() + self.par_value / ((1 + self.annual_discount_rate) ** self.maturity)

    def _get_sensitivity(self, price):
        if self.coupons.empty:
            sensitivity = 0
        else:
            self.coupons['IntermediaryCalculSensitivity'] = self.coupons.apply(self._intermediate_calculus_sensitivity,
                                                                               axis=1)
            duration = self.coupons['IntermediaryCalculSensitivity'].sum() / price
            sensitivity = duration / (1 + self.annual_discount_rate)
        return sensitivity

    def _get_convexity(self, price):
        if self.coupons.empty:
            convexity = 0
        else:
            self.coupons['IntermediaryCalculConvexity'] = self.coupons.apply(self._intermediate_calculus_convexity,
                                                                             axis=1)
            duration = self.coupons['IntermediaryCalculConvexity'].sum() / price
            convexity = duration / (1 + self.annual_discount_rate) * (1 + self.annual_discount_rate)
        return convexity

    def _intermediate_calculus_sensitivity(self, x):
        return x['PresentValue'] * x['Period'] / self.coupon_periodicity

    def _intermediate_calculus_convexity(self, x):
        return x['PresentValue'] * x['Period'] / (
            self.coupon_periodicity * self.coupon_periodicity + self.coupon_periodicity)


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/price_bonds')
def price_bonds():
    par_value = request.args.get('par_value', 0, type=float)
    annual_discount_rate = request.args.get('annual_discount_rate', 0, type=float)
    annual_coupon_rate = request.args.get('annual_coupon_rate', 0, type=float)
    maturity = request.args.get('maturity', 0, type=float)
    coupon_periodicity = request.args.get('coupon_periodicity', 0, type=str)
    bond_pricer = BondPricer(par_value=par_value, annual_discount_rate=annual_discount_rate,
                             annual_coupon_rate=annual_coupon_rate, maturity=maturity,
                             coupon_periodicity=coupon_periodicity)
    return jsonify(price=round(bond_pricer.price, 2),
                   coupons=bond_pricer.coupons[['Period', 'Payment', 'PresentValue']].to_dict(orient='records'),
                   sensitivity=round(bond_pricer.sensitivity, 4),
                   convexity=round(bond_pricer.convexity, 4))


@app.route('/price_with_blackscholes')
def price_with_blackscholes():
    underlying_price = request.args.get('underlying_price', 0, type=float)
    strike_price = request.args.get('strike_price', 0, type=float)
    rate = request.args.get('rate', 0, type=float)
    time_to_maturity = request.args.get('time_to_maturity', 0, type=float)
    volatility = request.args.get('volatility', 0, type=float)
    call_put = request.args.get('call_put', 0, type=str)
    bsp = BlackScholesPricer(underlying_price=underlying_price,
                             strike_price=strike_price,
                             rate=rate,
                             time_to_maturity=time_to_maturity,
                             volatility=volatility,
                             call_put=call_put)
    return jsonify(option_price=round(bsp.option_price, 5),
                   delta=round(bsp.delta, 5),
                   gamma=round(bsp.gamma, 5),
                   theta=round(bsp.theta, 5),
                   rho=round(bsp.rho, 5),
                   vega=round(bsp.vega, 5))


@app.route('/blackscholes')
def blackscholes():
    return render_template('blackscholes.html')


@app.route('/bondpricer')
def bondpricer():
    return render_template('bondpricer.html')


@app.route('/chart/share/', defaults={'code': 'YHOO'})
@app.route('/chart/share/<code>')
def function_chart(code):
    share = Share(code)
    historicals = (share.get_historical('2017-01-01', datetime.datetime.today().strftime('%Y-%m-%d')))
    result_df = pd.DataFrame(data=historicals)
    chart_id = 'chart_ID'
    chart_type = 'line'
    chart_height = 500
    chart_width = 1000
    chart = {"renderTo": chart_id, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": 'Close', "data": result_df["Close"].astype(float).tolist()},
              {"name": 'Low', "data": result_df["Low"].astype(float).tolist()},
              {"name": 'High', "data": result_df["High"].astype(float).tolist()}]
    title = {"text": 'My awesome HighChart'}
    xAxis = {"categories": result_df["Date"].tolist()}
    yAxis = {"title": {"text": 'Price Ccy'}}
    return render_template('index.html', chartID=chart_id, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


if __name__ == '__main__':
    app.run()
