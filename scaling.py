# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 18:26:37 2021

@author: amari
"""

import numpy as np

def deg_to_rad(theta):
    """Convert a angle from degrees to radians"""
    return(np.pi/180*theta)

def rad_to_deg(theta):
    """Convert a angle from radians to degrees"""
    return(180/np.pi*theta)

def rescaling(X_template,X_target):
    X_target_scaled=[]
    for i in range (0,2):
        scale_template=(max(X_template[i])-min(X_template[i]))/2
        scale_target=(max(X_target[i])-min(X_target[i]))/2
        
        X_target_scaled.append(X_target[i]*scale_template/scale_target)
    return(X_target_scaled)