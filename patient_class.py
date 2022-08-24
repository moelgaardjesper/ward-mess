# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 20:56:08 2022

@author: moelg
"""

class patient:
    def __init__(self,
                 p_type       = None,
                 arrival_ward = None,
                 first_SAE    = None,
                 SAE_during_mon     = None,
                 PR           = None,
                 RR           = None,
                 SAT          = None):
    
      self.p_type    = p_type
      self.first_SAE = first_SAE
      self.SAE_during_mon  = SAE_during_mon
      self.PR        = PR
      self.RR        = RR
      self.SAT       = SAT
      

