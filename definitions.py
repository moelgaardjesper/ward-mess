# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 12:13:46 2022

@author: moelg
"""


"""
    ME_Definitions in the format: Variable, Low Threshold, High Treshold, Duration
"""
ME_definitions = [

    ['SAT',0,92,60], # Values [0-91] for >= 60 minutes
    ['SAT',0,88,10],
    ['SAT',0,85,5],
    ['SAT',0,80,1],
    ['RR',23,999,5] # Values 24 - 999 for >= 5 minutes
    
    
    ]

"""
ME_definitions  = [

    ['SAT',88,92,60], # Values [0-91] for >= 60 minutes
    ['SAT',85,88,10],
    ['SAT',80,85,5],
    ['SAT',0,80,1],
    ['RR',23,999,5] # Values 24 - 999 for >= 5 minutes
    
    
    ]
"""