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
import sys
sys.path.insert(0, '/Users/boldrinicoder/lab4/FunctionClass')
from Root_objects import ROOT_obj

def Load_reading(userpath):
    filepath = userpath
    real = []
    measured = []
    err_tmcl = []
    err_chrono = []
    with open(filepath) as fp:
        line = fp.readline()
        h = line.split(",")
        while line:
            real.append(float(h[0]))
            measured.append(float(h[1]))
            err_tmcl.append(float(h[2]))
            err_chrono.append(float(h[3].strip("\n")))
            line = fp.readline()
            h = line.split(",")
    #this returns two colums lists of integers
    return real, measured, err_tmcl, err_chrono

ROOT.gROOT.SetBatch(True)
real, measured, err_tmcl, err_chrono = Load_reading("/Users/boldrinicoder/lab4/TMCLongTime/TMCLLongTime.txt")
y = []
x = []
err_x = []
err_y = []
i = 0
while i < len(real)-3:
    y.append(abs(real[i]-measured[i])*200/real[i])
    x.append(200/real[i]) #numero di cicli per arrivare a 200
    err_x.append(err_tmcl[i]*200/(real[i]**2))
    err_y.append(math.sqrt((err_chrono[i]*200/real[i])**2+((200/real[i]-200/real[i]**2)**2)*err_tmcl[i]**2))
    
    i += 1

#plotting time delay versus measure
g = ROOT_obj.TGraph_err_obj(len(real), real, measured, err_tmcl, err_chrono, 8, 1, "TMCL time [s]", "Real Time [s]", "TMCL Time Linearity [s]")
#fit = ROOT_obj.Linear_fit(inf = 1, sup = 40, color= ROOT.kRed, width = 1)
fit = ROOT_obj.Linear_fit()
fit.SetLineColor(4)
c = ROOT_obj.Create_Canvas(1000,800)
c.SetGridx()
c.SetGridy()
g.Fit(fit)
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetStatX(.9)
ROOT.gStyle.SetStatY(.4)
g.Draw("AP")
c.Draw()
c.SaveAs("/Users/boldrinicoder/lab4/General_Graphs/pdfs/Real_Time_TMCL_time.pdf", "pdf")
c.SaveAs("/Users/boldrinicoder/lab4/General_Graphs/roots/Real_Time_TMCL_time.root", "root")




