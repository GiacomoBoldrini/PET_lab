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
file = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190513/*.txt"))
output = "."

inf = 500
sup = 700
mean = 600

f =  open(file[0], "r")
list = f.readlines()

#deleting first 12 and last 18/16 lines. Theese lines only contain general information about
#the spectra and not useful values for the histogram filling.
first_lines = 12
#last_lines = -16
last_lines = -18

arr = np.array([])

#filling the array with bins contents
for i in list:
    arr = np.append(arr,i.strip())

disc = 1
#selecting the live_time by default = 200 or drom the txt
if disc == 1:
    live_time = int(arr[9][0:3])
#print('if', live_time)
else:
    live_time = 200
    #print(' else', live_time)
    
    
value0 = arr[first_lines:last_lines]
value0 = value0.astype(int)
value = []
for i in value0:
    value.append(i)

#bins are defined as integer subtraction of delimeters of the region.
#one bin is equal to one channel of the MCA.
bins = sup-inf
#the peak channel is the bean with maximum value of entries.
gauss_peak = max(value[inf:sup])
#creating and filling the histogram
h2 = ROOT.TH1F("", "", bins, inf, sup)
h2.GetXaxis().SetTitle("Channels")
h2.GetXaxis().SetTitleOffset(0.9)
h2.GetYaxis().SetTitleOffset(1.3)
h2.GetYaxis().SetTitle("Counts")
h2.SetFillColorAlpha(ROOT.kBlue,0.2)
h2.SetLineColorAlpha(ROOT.kBlue, 1)
#h2.SetFillStyle(0)
h2.SetLineWidth(2)
i = inf
z = 0
# defining the fit function as a combination of a gaussian + exponential background.
#Delimeters are set on the fit function.
fit = ROOT.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]",inf,sup)
fit.SetParameters(gauss_peak,mean,18,0.1,0)
fit.SetLineWidth(3)
#Filling the histogram bin by bin.
while i < sup:
    h2.SetBinContent(z,value[i])
    i += 1
    z += 1

n = h2.Fit("fit", "RLS")

a = fit.GetParameter(0)
b = fit.GetParameter(1)
c = fit.GetParameter(2)

print(a,b,c)

gaussian = ROOT.TF1("gaus", "[0]*exp(-((x[0]-[1])^2)/[2]^2)", inf, sup)
gaussian.SetParameter(0, a)
gaussian.SetParameter(1, b)
gaussian.SetParameter(2,c)

gaussian.SetLineColor(ROOT.kGreen)

d = fit.GetParameter(3)
e = fit.GetParameter(4)
f = fit.GetParameter(5)

expo = ROOT.TF1("gaus", "[0]*exp(-[1]*x[0])+[2]", inf, sup)
expo.SetParameter(0,d)
expo.SetParameter(1,e)
expo.SetParameter(2,f)

expo.SetLineColor(ROOT.kPink-3)




c2 = ROOT.TCanvas("c2", "c2",50,50,1000,800)
h2.Draw("histo same")
#gaussian.Draw("same")
#expo.Draw("same")
#fit.Draw("same")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
c2.Draw()
c2.Show()
c2.SaveAs(output + "/spec.pdf", "pdf")






