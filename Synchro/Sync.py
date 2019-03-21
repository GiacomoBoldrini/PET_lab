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

############MAIN#############
ROOT.gROOT.SetBatch(True)
out_path = "/Users/boldrinicoder/lab4/Grafici_Sincro"
f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190218/Sincro/*.txt"))
index = 0
ClassFunc.mkdir_p(out_path)
rate = []
err_rate = []
for i in f:
    ra , err_ra = ClassFunc.Fitter_Synchro(index, i, 400,750,550, out_path )
    #rate.append(ClassFunc.Fitter_Synchro(index, i, 400,750,550, out_path ))
    rate.append(ra)
    err_rate.append(err_ra)
    index += 1

x = np.arange(0,360,2.25)
err_x = [0]*len(x)
c = ROOT_obj.Create_Canvas(1300,1000)
g = ROOT_obj.TGraph_err_obj(len(rate),x, rate, err_x, err_rate, 20, 4, "Angle [Deg]", "Rate [s^(-1)]", "JustToShow" )
g.SetMarkerSize(0.1)
fit = ROOT.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-((x[0]-[4])^2)/[5]^2) + [6]")
fit.SetParameters(70, 130, 2, 70, 325, 2, 0)
fit.SetNpx(200)
g.Draw("AP")
g.Fit(fit)
ROOT.gStyle.SetOptFit(0)
c.Draw()
c.SetGridx()
c.SetGridy()
c.SaveAs("/Users/boldrinicoder/Desktop/unodueeoudhhuid.pdf", "pdf")


