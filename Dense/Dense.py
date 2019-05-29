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

ROOT.gROOT.SetBatch()

f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190510/*.txt"))

try_path = "/Users/boldrinicoder/lab4/Prova_Dense"
ClassFunc.mkdir_p(try_path)

inf = 370
sup = 680
mean = 520
Rates = []
Err_Rates = []
Reso = []
Err_Reso = []
j = 0
for i in f:

    rate, err_rate, Res = ClassFunc.Fitter_Synchro(j, i, inf, sup, mean, try_path, 0)
    Rates.append(rate)
    print("RATEEEEEEEEEEEEEEE : ", rate)
    Err_Rates.append(err_rate)
    Reso.append(Res[0])
    Err_Reso.append(Res[1])
    j += 1

x_1 = np.arange(2.25,24.76,2.25)
x_2 = np.arange(25.2, 42.76, 0.45)
x_3 = np.arange(45, 276.76, 2.25)
x_4 = np.arange(277.2, 294.76, 0.45)
x_5 = np.arange(297, 360.1, 2.25)

x = array('f', np.concatenate((x_1,x_2,x_3,x_4,x_5)))
y = array('f', Rates)
y_err = array('f', Err_Rates)
x_err = array('f', [0]*len(x))

print(y)
print(y_err)

g = R_o.TGraph_err_obj(len(x), x, y, x_err, y_err, 8, 1, "#alpha", "Rate [counts/s]", "Dense Positioning... 190510")
c = ROOT.TCanvas("c", "c", 1000,1000,1000,800)
g.Draw("AP")
c.Draw()
c.SaveAs("./dense.png", "png")

fig = plt.figure(figsize=(20,10))
plt.scatter(x,y, s = 5)
fig.savefig('./dense2.png')

