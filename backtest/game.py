# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 20:05:23 2018

@author: diamond
"""
import string

with open('C:/Users/diamond/Desktop/optimization/backtest/BackTest.py', 'r') as myfile:
    dd = myfile.read()

gg = dd

#maps = np.random.permutation(len(symlet))
symlet = string.printable

maps = [ 2, 20, 50, 26, 78, 89, 83, 54, 91, 90, 71, 11, 22, 88, 82, 45, 52,
       86, 39, 27, 69, 14, 80, 64, 37, 66, 30, 70, 67, 48, 35, 19, 65,  6,
        7,  5, 92, 63, 12, 73, 42, 13,  8, 46, 33, 59, 41, 24, 94, 60, 96,
       74, 38,  9, 95, 49, 99, 51, 32, 87, 36, 58, 77, 34, 28, 97, 81, 61,
       31, 57, 55,  0, 44, 29, 17, 23, 76, 15, 10, 85,  4, 93, 75, 16, 84,
       98, 18, 62, 25, 68, 21,  1, 43, 56,  3, 40, 53, 79, 72, 47]

gg = list(dd)

for i in range(len(gg)):
    ix = symlet.index(gg[i])
    gg[i] = symlet[maps[ix]]
    
    
gg = "".join(gg)
    
cc = list(gg)

for i in range(len(cc)):
    ix = symlet.index(cc[i])
    ixx = maps.index(ix)
    cc[i] = symlet[ixx]

cc = "".join(cc)









    