from math import log, e
from numpy import arange

def comp_tg(a, Pa, b, Pb):
    theta = (log(1-Pa) - log(1-Pb))/(log(b)-log(a))
    K_tmp = (Pb - Pa) / ((1/a**theta) - (1/b**theta))
    K = K_tmp ** (1/theta)
    return theta, K

def pct_below(threshold, theta, K):
    pct = 1 - (K / threshold) ** theta
    return pct
    
def med(theta, K):
    return K * (2 ** 1/theta)

def threshold(pct, theta, K):
    tmp = log(K) - log(1 - pct) / theta
    return e ** tmp


class Bracket:
    def __init__(self, amt, cnt, pct):
        self.amount = amt
        self.count = cnt
        self.percent = pct


class County:
    def __init__(self, amts, counts):
        total = sum(counts)
        cum_count = 0
        self.brackets = []
        for amt, count in zip(amts, counts):
            cum_count += count
            self.brackets.append(Bracket(amt, count, cum_count/total))

    def lin_pct(self, value):
        """ use linear interpolation to compute value threshold """
        # find the brackets to interpolate between
        low = self.brackets[0]
        for high in self.brackets:
            if high.percent > value:
                break
            low = high

        fraction = (value - low.percent) / (high.percent - low.percent)
        return low.amount + (high.amount - low.amount) * fraction

    def print_lin(self, v):
        for i in v:
            print('{:0.2f} {:,}'.format(i, self.lin_pct(i)))

    def pareto_pct(self, value):
        """ use pareto interpolation to compute value threshold """
                # find the brackets to interpolate between
        low = self.brackets[0]
        for high in self.brackets:
            if high.percent > value:
                break
            low = high

        theta, K = comp_tg(low.amount, low.percent,
                           high.amount, high.percent)
        return threshold(value, theta, K)

    def print_pareto(self, v):
        for i in v:
            print('{:0.2f} {:,}'.format(i, self.pareto_pct(i)))       



amt = [1, 10, 25, 50, 75, 100, 200]
cnts = [320, 2110, 3060, 3230, 1820, 1190, 1850]
x = arange(.1, .9, .1)

austin = County(amt, cnts)
austin.print_lin(x)
print()
austin.print_pareto(x)


