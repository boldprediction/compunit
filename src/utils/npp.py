"""
This module contains one line functions that should, by all rights, by in numpy.
"""
import numpy as np


# Demean -- remove the mean from each column
def demean(v):
    """
    Removes the mean from each column of [v].
    """
    return v-v.mean(0)


dm = demean


# Z-score -- z-score each column
def zscore(v):
    """
    Z-scores (standardizes) each column of [v].
    """
    return (v-v.mean(0))/v.std(0)


zs = zscore


# Rescale -- make each column have unit variance
def rescale(v):
    """
    Rescales each column of [v] to have unit variance.
    """
    return v/v.std(0)


rs = rescale


# Matrix corr -- find correlation between each column of c1 and the corresponding column of c2
def mcorr(c1, c2):
    """
    Matrix correlation. Find the correlation between each column of [c1] and the corresponding column of [c2].
    """
    return (zs(c1)*zs(c2)).mean(0)


# Cross corr -- find corr. between each row of c1 and EACH row of c2
def xcorr(c1, c2):
    """
    Cross-column correlation. Finds the correlation between each row of [c1] and each row of [c2].
    """
    return np.dot(zs(c1.T).T, zs(c2.T)) / (c1.shape[1])
