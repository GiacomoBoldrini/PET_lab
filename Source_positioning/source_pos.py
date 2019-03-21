"""
Created on Wed Feb 27 13:40:42 2019

@author: Bianca
"""

"""
This program calculate the position (x,y) of the source given some known variables
"""

import numpy as np
import math as mt
import argparse

    #LET THE USER TO INSERT ALL THE PARAMETERS
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--alfa', type=float, required=True, help="alfa angle") 
parser.add_argument('-b', '--beta', type=float, required=True, help="beta angle")
parser.add_argument('-psi', '--psi', type =float, required=True, help="scintillators angle")

args = parser.parse_args()

print('WARNING: Check that you have inserted all the angles in degrees! The program will convert them in radiant by itself')

    #CONVERSION IN RADIANT
a = mt.radians(args.alfa)
b = mt.radians(args.beta)
psi = mt.radians(args.psi)

    #CALCULATION OF X AND Y IN FUNCTION OF THE ENTERED VARIABLES
r = 0.3   
cotan = 1 / mt.tan(psi/2)

q = -0.3*cotan
m = mt.sin(psi)/(mt.cos(psi)-1)

n1 = mt.cos(a)+m*mt.sin(a)-mt.cos(b)-m*mt.sin(b)
n2 = m*mt.cos(a)-mt.sin(a)-m*mt.cos(b)+mt.sin(b)
n3 = n2/n1*(mt.cos(a)+m*mt.sin(a))-m*mt.cos(a)+mt.sin(a)

x = q/n3
y = n2*x/n1

    #CONVERSION IN CENTIMETERS OF X AND Y
x = x * 100
y = y * 100

    #FINAL PRINT WITH THE RESULTS IN CENTIMETERS
print('The source is at the point (x,y) = ({0:.2f},{1:.2f}) in centimeters'.format(x, y))
