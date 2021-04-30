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


def rescaling(X_source,X_target, checking_parameter):
    """Scales signal source to the amplitude of the siganl target"""
    #Checking parameter enables to see the coefficient of proportionnality from source to target
    X_source_scaled=[]
    for i in range (0,2):
        scale_template=(max(X_source[i])-min(X_source[i]))/2
        scale_target=(max(X_target[i])-min(X_target[i]))/2
        if checking_parameter == True:
            print('Scaling coefficient from source to target equals: '+ str(scale_target/scale_template))
        X_source_scaled.append(X_source[i]*scale_target/scale_template)
    return(X_source_scaled)

def norming(audio):
    """Norming of a signal to a 1 amplitude"""
    audio_normed=audio/np.max(np.abs(audio))
    return(audio_normed)