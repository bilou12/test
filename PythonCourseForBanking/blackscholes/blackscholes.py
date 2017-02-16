import math

from scipy.stats import norm  # scipy is one of the tool every python developer needs to know


# this code is following the pep8 norm, and should be compatible Python 2.x and 3.x, I have only tested on Python3.x
# pep8 describes a set of rules to follow given that Python is a permissive language

class BlackScholesPricer:
    def __init__(self, underlying_price, strike_price, rate, time_to_maturity, volatility, call_put='call'):
        self.underlying_price = underlying_price
        self.strike_price = strike_price
        self.rate = rate
        self.time_to_maturity = time_to_maturity
        self.volatility = volatility
        self.call_put = call_put
        self.d1, self.d2 = self._calculate_d1_d2()  # Python functions can return multiple outputs
        self.result_price, self.delta, self.gamma, self.theta, self.rho, self.vega = self.get_price_and_greeks()

    # surcharge native method to make it custom
    def __str__(self):
        return ('result_price = ' + str(self.result_price) + ', delta = ' + str(self.delta) + ', gamma = ' + str(
            self.gamma) + ', theta = ' + str(self.theta) + ', rho = ' + str(self.rho) + ', vega = ' + str(self.vega))

    # this function starts by _ because even though it will accessible from everywhere,
    # it should be used inside the class (pep)
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


# Python can be launched 1) within pyCharm 2) with the Python console 3) with the windows command line
# tips: you can also select the lines you want to play and click on alt + shift + E
# we are going to use 1) within pyCharm
# just write 'main' then enter at the bottom of your page and it will create the line
# this is a part of the code where you can put some tests because it will be used only if you play the module
# not if you import it somewhere else for example
if __name__ == '__main__':
    bsp_call = BlackScholesPricer(underlying_price=60, strike_price=62, rate=0.04, time_to_maturity=0.2,
                                  volatility=0.32, call_put='call')
    print(str(bsp_call))
    bsp_put = BlackScholesPricer(underlying_price=60, strike_price=62, rate=0.04, time_to_maturity=0.2,
                                 volatility=0.32, call_put='call')
    print(str(bsp_put))
