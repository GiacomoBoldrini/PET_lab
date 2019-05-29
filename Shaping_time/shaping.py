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
out_path2 = "/Users/boldrinicoder/lab4/Shaping_time"
f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/181214/*.txt"))
#f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/181212/*.txt"))
#f = f[10:19]
print(f)

try_path = "/Users/boldrinicoder/lab4/Prova_RateRes"
ClassFunc.mkdir_p(try_path)

pulse_shape = [0.5, 1,2,3,6,10]
means = [540,600,600,570,570,550]
#means = [600,600,610,570,570,610]
infs = [450,400,470,450,450,400]
#infs = [450,400,500,470,470,500]
sups = [700,750,750,700,700,700]
#sups = [700,750,750,730,730,700]

Rates = []
Err_Rates = []
Reso = []
Err_Reso = []
j = 0
for i in f:
    rate, err_rate, Res, _, _ = ClassFunc.Fitter_Synchro(j, i, infs[j], sups[j], means[j], try_path, 0)
    Rates.append(rate)
    Err_Rates.append(err_rate)
    Reso.append(Res[0])
    Err_Reso.append(Res[1])
    j += 1

print(len(pulse_shape), len(Reso), len(Err_Reso), len(Rates), len(Err_Rates))

Rates[0] = 889
Reso[1] = 8.39
Reso[-2] = 8.36
ClassFunc.Rate_Res_Plotter(len(f), pulse_shape, Reso, Err_Reso, Rates, Err_Rates, out_path2+"/try2.root", xlabel = "Shaping Time [#mus]", yright_label = "Resolution", yleft_label = "Live Rate [counts/sec]")

