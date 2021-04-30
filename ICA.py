# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 13:53:33 2021

@author: amari
"""

import scipy.stats
import numpy as np



def rotation(theta):
    """Defintion of the rotation matrix in space-2"""
    M=[[np.cos(theta), - np.sin(theta)],
       [np.sin(theta), np.cos(theta)]]
    M=np.array(M)
    return(M)

def Statistical_similarity(angle, X_white, screening=False):
    """Calculus of the entropical statistical similarity between two whitened distributions"""
    #Rotation of the whitened recordings
    Rot=rotation(angle)
    Rotated_whitened_X= Rot.dot(X_white)
    
    #Definition of the law of probability on behalf of the whitened recordings rotated
    P,bins_1=np.histogram(Rotated_whitened_X[0,:],bins=1000)
    Q,bins_2=np.histogram(Rotated_whitened_X[1,:],bins=1000)

    #Noise addition in order to avoid division by zero issues
    epsilon=1e-6
    
    #Divergence of Kullbach Leibler calculus
    DKL=-scipy.stats.entropy(P+epsilon,Q+epsilon)

    return(DKL)