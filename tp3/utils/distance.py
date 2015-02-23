#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
http://fr.wikipedia.org/wiki/Distance_%28math%C3%A9matiques%29
'''

import math

def euclidienne(x,y):
    '''
    distance euclidienne pour 2scalaires
    :param x:  
    :param y:
    :type x: int/float
    :type y: int/float
    :return: la distance euclidienne entre x et y
    :rtype: float 
    '''
    return math.sqrt((x-y)**2)


def manhattan(x,y):
   return  abs(x-y)

def cartesien(a,b):    
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)


print manhattan(2,6.5)
print euclidienne(2,6.5)
a = (1,2)
b = (1,5)
print cartesien(a,b)
