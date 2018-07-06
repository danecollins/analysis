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


def test_pareto_median():
    """ test data from
        http://www.sipp.census.gov/sipp/sourceac/S%26A01_20060323_Long%28S%26A-3%29.pdf
    """
    # how many points we want in each bin
    theta, k = Pareto.comp_tg(17500, 1 - 0.555, 20000, 1 - 0.409)
    computed_median = Pareto.med(theta, k)
    assert computed_median > 18209
    assert computed_median < 18425


def test_pareto_threshold():
    """ test data from
        http://www.sipp.census.gov/sipp/sourceac/S%26A01_20060323_Long%28S%26A-3%29.pdf
    """
    # how many points we want in each bin
    theta, k = Pareto.comp_tg(17500, 1 - 0.555, 20000, 1 - 0.409)
    computed_median = Pareto.income_thresholds(.5, theta, k)
    assert computed_median > 18209
    assert computed_median < 18425

