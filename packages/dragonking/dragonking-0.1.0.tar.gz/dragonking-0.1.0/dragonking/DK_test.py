# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 15:07:16 2018

@author: Daniel
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f

def dk_test(vals,r):
    r = int(r)
    n = len(vals)
    x = np.zeros(n)
    y = np.zeros(n)
    z = np.zeros(n)
    for j in range(0, n):
        x[j] = vals[j][0]
    x = np.sort(x)[ : :-1]
    
    for i in range(0, n):
        if i == n - 1:
            y[i] = x[i]
        else:
            y[i] = x[i] - x[i+1]
   
    for i in range(0, n):
        z[i] = (i + 1) * y[i]
    
    num = 1.0 / r * sum(z[ :r])
    den = 1.0 / (n - r) * sum(z[r: ])
    test_stat = num / den    
    
    p_val = 1 - f.cdf(test_stat, 2.0 * r, 2.0 * (n - r))
    
    ans = [test_stat, p_val]
    print(ans)
    return(ans)

dk_file1 = pd.read_csv('DK-file.csv')
dkvalues1 = dk_file1.iloc[ : , : ].values
#plt.hist(dkvalues1)

dk_file2 = pd.read_csv('DK-file2.csv')
dkvalues2 = dk_file2.iloc[ : , : ].values
#splt.hist(dkvalues2)

dk_test(dkvalues1, 3)
dk_test(dkvalues2, 3)

