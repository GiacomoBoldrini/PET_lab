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
real, measured, err_tmcl, err_chrono = Load_reading("/Users/boldrinicoder/lab4/MCATimeLinearity/MCATime.txt")

#plotting time delay versus measure
g = ROOT_obj.TGraph_err_obj(len(real), real, measured, np.array(err_tmcl), np.array(err_chrono), 8, 1, "MCA time [s]", "Real Time [s]", "")

g1 = ROOT_obj.TGraph_err_obj(len(real), real, measured, np.array(err_tmcl)*100, np.array(err_chrono)*100, 8, 1, "MCA time [s]", "Real Time [s]", "")

legend = ROOT.TLegend(0.15,0.80,0.35,0.89)
legend.SetHeader("", "C")
legend.SetLineWidth(0)

legend.AddEntry(g, "x100 Errors", "p")
#fit = ROOT_obj.Linear_fit(inf = 1, sup = 40, color= ROOT.kRed, width = 1)
fit = ROOT_obj.Linear_fit()
fit.SetLineColor(4)
c = ROOT_obj.Create_Canvas(1000,800)
g.Fit(fit)
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetStatX(.9)
ROOT.gStyle.SetStatY(.4)
g.Draw("AP")
g1.Draw("P same")
legend.Draw()
c.Draw()
c.SaveAs("/Users/boldrinicoder/lab4/General_Graphs/pdfs/MCATimeLinearity.pdf", "pdf")
c.SaveAs("/Users/boldrinicoder/lab4/General_Graphs/roots/MCATimeLinearity.root", "root")




