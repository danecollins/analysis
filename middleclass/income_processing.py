from math import log, e
import pdb


class Pareto:
    """ Low-level functions implementing the pareto interpolation

        https://en.wikipedia.org/wiki/Pareto_interpolation
    """

    @staticmethod
    def comp_tg(a, Pa, b, Pb):
        theta = (log(1-Pa) - log(1-Pb))/(log(b)-log(a))
        K_tmp = (Pb - Pa) / ((1/a**theta) - (1/b**theta))
        K = K_tmp ** (1/theta)
        return theta, K

    @staticmethod
    def pct_below(threshold, theta, K):
        pct = 1 - (K / threshold) ** theta
        return pct

    @staticmethod
    def med(theta, K):
        return K * (2 ** (1/theta))  # parens are needed around 1/theta

    @staticmethod
    def threshold(pct, theta, K):
        tmp = log(K) - log(1 - pct) / theta
        return e ** tmp


class Bracket:
    """ A bracket stores what percentage of returns are below the amount """
    def __init__(self, amt, cnt, pct):
        self.amount = amt
        self.count = cnt
        self.percent = pct

    def __str__(self):
        return "Bracket(<{}, #{}, {})".format(self.amount, self.count, self.percent)


class County:
    income_thresholds = [1, 10000, 25000, 50000, 75000, 100000, 200000, 1000000]

    def __init__(self, county, counts):
        self.county = county
        if len(self.income_thresholds) != len(counts):
            print("Wrong number of counts for {}".format(county))
            print(counts)
            return None
        total = sum(counts)
        if total == 0:
            return None
        cum_count = 0
        self.brackets = []
        for amt, count in zip(self.income_thresholds, counts):
            cum_count += count
            self.brackets.append(Bracket(amt, count, cum_count/total))

    def linear_income(self, value):
        """ use linear interpolation to compute value threshold """
        # find the brackets to interpolate between
        low = self.brackets[0]
        for high in self.brackets:
            if high.percent > value:
                break
            low = high

        fraction = (value - low.percent) / (high.percent - low.percent)
        return low.amount + (high.amount - low.amount) * fraction

    def linear_median(self):
        return self.linear_income(.5)

    def pareto_income(self, value):
        """ use pareto interpolation to compute value threshold """
        # find the brackets to interpolate between

        low = self.brackets[0]
        for high in self.brackets:
            if high.percent > value:
                break
            low = high

        theta, K = Pareto.comp_tg(low.amount, low.percent,
                                  high.amount, high.percent)

        return Pareto.threshold(value, theta, K)

    def pareto_median(self):
        return self.pareto_income(.5)

    def __str__(self):
        return 'County({},{})'.format(self.county, self.pareto_median())

    def display(self):
        print('County:', self.county)
        for b in self.brackets:
            print(b)
