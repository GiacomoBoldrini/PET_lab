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
from Root_objects import ROOT_obj as robj

############MAIN#############
ROOT.gROOT.SetBatch(True)
out_path1 = "/Users/boldrinicoder/lab4/General_Graphs/pdfs"
out_path2 = "/Users/boldrinicoder/lab4/General_Graphs/roots"
f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190118/*.txt"))

try_path = "/USers/boldrinicoder/lab4/Prova_Rateres"
ClassFunc.mkdir_p(try_path)

Voltages = [600,650,700,750,800,850,900,950,1000]
means = [540,600,600,570,570,550,590,610,750]
infs = [350,400,470,470,470,450,430,480,600]
sups = [700,750,750,730,730,750,700,750,950]
Rates = []
Err_Rates = []
Reso = []
Err_Reso = []
j = 0
for i in f:
    rate, err_rate, Res = ClassFunc.Fitter_Synchro(j, i, infs[j], sups[j], means[j], try_path, 0)
    Rates.append(rate)
    Err_Rates.append(err_rate)
    Reso.append(Res[0])
    Err_Reso.append(Res[1])
    j += 1

print(len(Voltages), len(Reso), len(Err_Reso), len(Rates), len(Err_Rates))
ClassFunc.Rate_Res_Plotter(len(f), Voltages, Reso, Err_Reso, Rates, Err_Rates, out_path1)

