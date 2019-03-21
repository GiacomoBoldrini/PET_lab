#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:38:42 2018

@author: Jack
"""

"""
This program reads spectra for energetic window fit and compare them
"""

#this line is just to call the function forom an outside directory
import sys
sys.path.insert(0, '/Users/boldrinicoder/lab4/FunctionClass')

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob
from Functions import ClassFunc

ROOT.gROOT.SetBatch(True)
#reading all the txts
f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190206/*.txt"))
histos = []
xmax = []
"""
for i in f[:2]:
    #histos.append(ClassFunc.Histo_Filler(i, 300, 850))
    Rate.append(ClassFunc.Fitter(i, 300, 850,400, 0)[0])
    Res.append(ClassFunc.Fitter(i, 300, 850,400, 0)[1])

"""

real = ClassFunc.Fitter("1", f[1], 380, 570,480, 1)
#xmax.append(real)
xm = ClassFunc.Fitter("2",f[2], 350, 570,480, 1)
xmax.append(xm)
xm = ClassFunc.Fitter("3",f[3], 380, 570,480, 1)
xmax.append(xm)
xm = ClassFunc.Fitter("4",f[4], 380, 570,480, 1)
xmax.append(xm)
xm = ClassFunc.Fitter("5",f[5], 380, 570,480, 1)
xmax.append(xm)
xm = ClassFunc.Fitter("6",f[6], 380, 570,480, 1)
xmax.append(xm)

n = len(xmax)
y = array('f', xmax)
x = array('f', [560, 470,680,820,660])
real = float(real)
ClassFunc.Graph_Plotter(n, x, y, "Splitting", "Resistance [#Omega]", "Channel", "/Users/boldrinicoder/lab4/graph.pdf", 468,822, real)

normal = []
for i in xmax:
    normal.append(i-real)

normal = array('f', normal)
n = len(normal)
ClassFunc.Graph_Plotter(n, x, normal, "Distance from best", "Resistance [#Omega]", "Channel", "/Users/boldrinicoder/lab4/graph2.pdf",468,822, 0)
