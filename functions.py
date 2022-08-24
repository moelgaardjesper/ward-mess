# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 21:11:11 2022

@author: moelg
"""
import numpy as np

def moving_average(a, n=10) :
    a = a.astype(float)
    """
    Pandas has a better and more robust moving_average function.
    But this is to use only numpy for computational efficiency
    
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

def random_patient(dictionary_of_patients):
    from numpy import random
    patient_ID = random.randint(len(list(dictionary_of_patients.keys())))
    random_patient = list(dictionary_of_patients.keys())[patient_ID]
    return dictionary_of_patients[random_patient]


#Microevent calculator
def MicroeventCalculator(data_in,
                         value='PR',
                         threshold_low=0,
                         threshold_high=110,
                         duration=30,
                         smoothing=False):
  """
    

    Parameters
    ----------
    data : TYPE, optional
        DESCRIPTION. The default is patient_dict['rs432'].hr.
    value : TYPE, optional
        DESCRIPTION. The default is 'hr'.
    threshold_low : TYPE, optional
        DESCRIPTION. The default is 0.
    threshold_high : TYPE, optional
        DESCRIPTION. The default is 110.
    duration : TYPE, optional
        DESCRIPTION. The default is 30.

    Returns
    -------
    number_of_microevents : Integer
        DESCRIPTION. Total number of microevent as an integer
    stretches : List of indices
        DESCRIPTION. [[Start, Stop of microevent]]
    length : List
        DESCRIPTION. Duration in minutes

    """
  if   value == 'PR': data = data_in.PR
  elif value == 'SAT': data = data_in.SAT
  elif value == 'RR': data = data_in.RR
  if smoothing: data = moving_average(data[:,2],10)
  else: data = data[:,2]
  
  value_changes = np.diff((data.astype(float)>threshold_low)&
                          (data.astype(float)<threshold_high), prepend=0, append=0) #Returns 1 and -1 when values dip within thresholds
  intervals = np.where(value_changes)[0].reshape(-1,2) #returns 2xn array with index-position of values inside thresholds
  positions = np.diff(intervals)>=duration #tests if length of intervals are longer than duration-criteria
  #stretches = np.split(data, intervals.reshape(-1))[1::2]
  stretches = intervals[positions.reshape(-1)] # returns streches that fulfill duration criteria
  number_of_microevents = len(intervals[positions.reshape(-1)]) #count total number of true microevents
  length = [len(range(x[0],x[1])) for x in stretches]
  #pd.DataFrame(data).to_csv('validation_data.csv')
  return number_of_microevents,stretches,length