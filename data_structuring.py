# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 21:11:11 2022

@author: moelg
"""
import numpy as np

def moving_average(a, n=10) :
    a = a.astype(float)
    """
    Parameters
    ----------
    a : Input list or array
        List to do moving average on.
    n : Integer, optional
        Window to smooth over. The default is 10.

    Returns
    -------
    ret : numpy.array
        Array has same dimensions as input.
        Using simple linear interpolation between points.
        Last n-values are calculated on a simple extrapolated version
        of the original values.

    """
    a_extrapolated = np.concatenate([a,[a[-1]]*(n-1)])
    a_interpolated = np.interp(np.arange(len(a_extrapolated)), 
                               np.arange(len(a_extrapolated))[np.isnan(a_extrapolated) == False], 
                               a_extrapolated[np.isnan(a_extrapolated) == False])
    ret = np.nancumsum(a_interpolated#, dtype=float
                       )
    ret[n:] = ret[n:] - ret[:-n]
    ret = ret[n - 1:] / n
    ret = np.where(np.isnan(a),a,ret)
    return ret

def random_patient(dictionary_of_patients = patient_dict):
    from numpy import random
    patient_ID = random.randint(len(list(patient_dict.keys())))
    random_patient = list(patient_dict.keys())[patient_ID]