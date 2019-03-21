"""
    Created by Jack  12/03/2019
"""

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
from Root_objects import ROOT_obj as R_o

############MAIN#############
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetStatX(.9)
ROOT.gStyle.SetStatY(.4)


ROOT.gStyle.SetOptFit(1111)

#definisco due cartelle una per i root e una per i pdf importo poi i dati della misura
out_path1 = "/Users/boldrinicoder/lab4/General_Graphs/pdfs"
out_path2 = "/Users/boldrinicoder/lab4/General_Graphs/roots"
f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190313/*.txt"))

#i primi due txt si riferiscono alla linearità nel gain dell'amplificatore 575


j = 0
for i in f:
    x = np.loadtxt(i ,usecols = 0)
    y = np.loadtxt(i, usecols = 1)
    erry = np.loadtxt(i, usecols = 2)
    errx= [0]*len(x)
    g = R_o.TGraph_err_obj(len(x), x, y, errx, erry, 8, 1, "Ticks [a.u.]", "Mean Time [t]", "TMCL Tick Time conversion")
    g.SetMarkerSize(0.6)
    fit = R_o.Linear_fit()
    fit.SetLineColor(4)
    c = R_o.Create_Canvas(1000, 800)
    g.Fit(fit)
    g.Draw("AP")
    c.SetGridx()
    c.SetGridy()
    c.Draw()
    c.SaveAs(out_path1 + "/TMCL_Tick_Time_{}.pdf".format(j), "pdf")
    c.SaveAs(out_path2 + "/TMCL_Tick_Time_{}.root".format(j), "root")
    j += 1


