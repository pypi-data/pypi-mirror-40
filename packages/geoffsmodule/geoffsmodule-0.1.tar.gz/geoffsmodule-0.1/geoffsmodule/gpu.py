from numba import jit, cuda
import numpy as np


@jit
def mm_jit(a,b):
    '''matrix multiply'''
    I,J = a.shape
    K,L = b.shape
    assert J == K, 'cols of a must match rows of b for matrix multiplication'
    s = np.zeros((I,L))
    for i in range(I):
        for l in range(L):
            for k in range(K):
                s[i,l] += a[i,k]*b[k,l]
    return(s)

