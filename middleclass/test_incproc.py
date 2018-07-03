""" tests for income processing
    income ranges[1, 10000, 25000, 50000, 75000, 100000, 200000, 1000000]
"""
import numpy as np

from income_processing import County


def get_bins(i):
    return [len(i[i < 1]),
            len(i[(i >= 1) & (i < 10000)]),
            len(i[(i >= 10000) & (i < 25000)]),
            len(i[(i >= 25000) & (i < 50000)]),
            len(i[(i >= 50000) & (i < 75000)]),
            len(i[(i >= 75000) & (i < 100000)]),
            len(i[(i >= 100000) & (i < 200000)]),
            len(i[i >= 200000])
            ]


def compute_bin(x):
    for i, r in enumerate(County.income_thresholds):
        if x > r:
            return i


def test_linear_median_bin_edge():
    # incomes
    i = np.arange(500, 149000, 1000)
    bins = get_bins(i)
    obj = County('dummy', bins)
    linear_median = obj.linear_median()
    actual_median = np.median(i)
    assert linear_median == actual_median


def test_linear_median_bin_center():
    # incomes
    i = np.arange(500, 123000, 1000)
    bins = get_bins(i)
    obj = County('dummy', bins)
    linear_median = obj.linear_median()
    actual_median = np.median(i)
    assert linear_median == actual_median


def test_pareto_median_():
    """ It's hard to create real data that the pareto interpolation will
        give good results on. I would need to generate the points based on
        the right algorithm but I don't know what that is.
    """
    # how many points we want in each bin
    cnts = [320, 2110, 3060, 3230, 1820, 1190, 1850]
    # try to create a distribution that is somewhat close to this
    i = np.random.normal(loc=35000, scale=35000, size=13580)
    i = np.append(i, np.random.normal(loc=150000, scale=40000, size=1800))
    i = i[i > 1]
    i = np.append(np.zeros(320), i)  # fix the bottom bin

    bins = get_bins(i)
    obj = County('dummy', bins)
    pareto_median = obj.pareto_median()
    actual_median = np.median(i)
    pct_error = abs((pareto_median - actual_median) / actual_median)
    assert pct_error < 0.04


