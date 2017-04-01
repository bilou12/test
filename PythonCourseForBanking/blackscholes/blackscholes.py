import math

from flask import Flask, request, jsonify, render_template
from scipy.stats import norm

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


@app.route('/')
def index():
    return render_template('blackscholes.html')


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


if __name__ == '__main__':
    # app.run()
    underlying_price = 52
    strike_price = 50
    rate = 0.02
    time_to_maturity = 0.3
    volatility = 0.32
    call_put = 'call'
    bsp = BlackScholesPricer(underlying_price=underlying_price, strike_price=strike_price, rate=rate,
                             time_to_maturity=time_to_maturity, volatility=volatility, call_put=call_put)
    print(str(bsp))
