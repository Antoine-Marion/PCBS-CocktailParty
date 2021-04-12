# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:59:31 2021

@author: amari
"""
import numpy as np
import numpy.linalg as alg


def centering(X):
    """Centering of a data vector with a zero mean"""
    centered_data=[]
    for i in range(0,len(X)):
        Mean_X=np.mean(X[i])
        row=[]
        for j in range(0,len(X[1])):
            row.append(X[i,j]-Mean_X)
        centered_data.append(row)
    centered_data=np.array(centered_data)
    return(centered_data)



def whitening(X, checks = False):
    """X_whitened = (D^(-1/2)E^T)X calculus"""
    #Where <XX^T>=EDE^T when diagonalised in the orthonormal basis of its eigen vectors
    
    #<XX^T> calculus
    Cov_X=np.cov(X)
       
    #Diagonalization
    eigen_values=alg.eigvals(Cov_X)
    # D=np.diag(eigen_values)
    
    #Eigen vectors
    E=alg.eig(Cov_X)[1]

    #Whitened data calculus
    D_sqrt_inv=np.diag(1/np.sqrt(eigen_values))
    X_whitened = D_sqrt_inv.dot(np.transpose(E)).dot(X)
    X_whitened = np.array(X_whitened)
    #Check of the whitening property
    #Some checks
    if checks==True:
        print(Cov_X.shape)
        print(Cov_X)
        
        Cov_X_whitened=np.cov(X_whitened)
        print(Cov_X_whitened)
        #Must have a variance equal to 1 and no inter correlation
        
    return(X_whitened)

def orthogonal_projection(X):
    #<XX^T> calculus
    Cov_X=np.cov(X)
           
    #Passage matrix
    P=alg.eig(Cov_X)[1]
    #X_projected=1
    X_projected=np.transpose(P).dot(X)
    
    return(X_projected)