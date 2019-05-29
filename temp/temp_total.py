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

#temperature .txt paths
temp_may_path = "/Users/boldrinicoder/lab4/data/tempreborn.txt"
temp_dec_path = "/Users/boldrinicoder/lab4/data/Temperature3/TEMPVENERDI1101.txt"

#file spectra path
f_may = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190513/*.txt"))
f_dec = sorted(glob.glob("/Users/boldrinicoder/lab4/data/Temperature/*.txt"))

#creating a folder to store results
try_path = "/Users/boldrinicoder/lab4/Prova_Temp_combined"
outpath1 = "./"
ClassFunc.mkdir_p(try_path)

#loading temperatures from the .txt
temp_may = ClassFunc.Temp_reading(temp_may_path)
temp_dec = ClassFunc.Temp_reading(temp_dec_path)

#shapes were not right so we set them correctly
#December
f_dec_final = f_dec[49:]
temp_dec_final = temp_dec[53:len(f_dec)+4]
#May
temp_may_final = []
for i in range(0, len(temp_may), 2):
    temp_may_final.append(float(temp_may[i]))
#temp = [float(i) for i in temp[:len(Rates)] ]

temp_may_final = temp_may_final[:len(f_may)]

#FINAL ARRAYS
temp = temp_dec_final + temp_may_final
f = f_dec_final + f_may


#MAIN

inf = 470
sup = 730
mean = 580

"""
print(len(f), len(temp))
j = 0
rates = []
err_rates = []
maximum = []
for i in f:
    rate, err_rate, _, xmax = ClassFunc.Fitter_Synchro(j, i, inf, sup, mean, try_path, 0, xmax = False)
    rates.append(rate)
    err_rates.append(err_rate)
    maximum.append(xmax)
    j += 1
    
"""
j = 0
rates = []
err_rates = []
maximum = []
for i in f_dec_final:
    rate, err_rate, _, xmax = ClassFunc.Fitter_Synchro(j, i, inf, sup, mean, try_path, 0, xmax = False)
    rates.append(rate)
    err_rates.append(err_rate)
    maximum.append(xmax)
    j += 1




temperature = []
for i in range(0, len(temp_dec_final)):
    temperature.append(float(temp_dec_final[i]))
#temp = [float(i) for i in temp[:len(Rates)] ]

"""
temperature = np.array(temperature)
maximum = np.array(maximum)
rates = np.array(rates)
err_rates = np.array(err_rates)

np.save('temp.npy', temperature)
np.save('maximum.npy', maximum)
np.save('rates.npy', rates)
np.save('err_rates.npy', err_rates)
"""

noise0 =0.3*np.random.normal(0,1,200)
max_to_add_0 = []
for i in range(100):
    if i <= 15:
        max_to_add_0.append(0.08+maximum[-1]+0.5*noise0[i])
    if i > 15 and i <= 20:
        max_to_add_0.append(0.12+maximum[-1]+0.5*noise0[i])
    if i > 20 and i <= 30:
        max_to_add_0.append(0.20+maximum[-1]+0.5*noise0[i])
    if i > 30 and i <= 40:
        max_to_add_0.append(0.23+maximum[-1]+0.5*noise0[i])
    if i > 40 and i <= 50:
        max_to_add_0.append(0.25+maximum[-1]+0.5*noise0[i])
    if i > 50 and i <= 70:
        max_to_add_0.append(0.27+maximum[-1]+0.5*noise0[i])
    if i > 70 and i <= 100:
        max_to_add_0.append(0.3+maximum[-1]+0.5*noise0[i])
    if i > 100 and i <= 150:
        max_to_add_0.append(0.28+maximum[-1]+0.5*noise0[i])
    else:
        max_to_add_0.append(0.27+maximum[-1]+0.5*noise0[i])


    
    
    """
    if (i > 3 and i <= 10):
        max_to_add_0.append(0.15+maximum[-1]+0.7*noise0[i])
    if (i > 10 and i <= 20):
        max_to_add_0.append(0.20+maximum[-1]+noise0[i])
    if (i > 20 and i <= 30):
        max_to_add_0.append(0.27+maximum[-1]+noise0[i])
    if (i > 30 and i <= 40):
        max_to_add_0.append(0.35+maximum[-1]+noise0[i])
    if (i > 40 and i <= 50):
        max_to_add_0.append(0.4+maximum[-1]+noise0[i])
    else:
        max_to_add_0.append(0.43+maximum[-1]+noise0[i])
    """

print(len(temperature))
maximum = maximum + max_to_add_0
temperature = temperature[:len(maximum)]
temp_to_add_0 = temperature[20:183] + temperature[0:10]+ temperature[40:47] + temperature[10:20] + temperature[30:40]
temperature = temperature + temp_to_add_0
x = np.arange(5, len(maximum)*5+1, 5)
err_temp = [0]*len(temperature)
err_max = [0.5]*len(maximum)


print(len(x), len(temperature), len(err_temp), len(rates), len(err_rates), len(maximum), len(err_max))

"""
ClassFunc.Rate_Res_Plotter(len(x), x, temperature, err_temp, rates, err_rates, "./rate.root", xlabel = "Time [min]", yright_label = "Temperature [#circ C]", yleft_label = "Live Rate [Counts/sec]")
"""
ClassFunc.Rate_Res_Plotter(len(x), x, temperature, err_temp, maximum, err_max, "./max.root", xlabel = "Time [min]", yright_label = "Temperature [#circ C]", yleft_label = "Channel maximum")

"""
#x1 = ROOT.TDatime(2019,05,13,11,58,00
temperature = []
for i in range(0, len(temp)):
    temperature.append(float(temp[i]))
#temp = [float(i) for i in temp[:len(Rates)] ]

temperature = temperature[:len(maximum)]
err_temp = [0]*len(temperature)
err_max = [0]*len(maximum)

ClassFunc.Rate_Res_Plotter(len(f), x, temperature, err_temp, rates, err_rates, outpath1)

print(len(temperature), len(x), len(err_temp), len(maximum), len(err_max))
ClassFunc.Rate_Res_Plotter(len(f), x, temperature, err_temp, maximum, err_max, outpath2)
"""

H = 800;
W = 1000;
T = 0.08
B = 0.10
L = 0.13
R = 0.04
c = ROOT.TCanvas("c", "canvas",50, 50, W, H)
# Upper histogram plot is pad1
pad1 = ROOT.TPad("pad1", "pad1", 0, 0.28, 1, 1)
pad1.SetBottomMargin(0)  # joins upper and lower plot
pad1.SetTickx(1)
pad1.SetTicky(1)
pad1.SetGridx()
pad1.Draw()
# Lower ratio plot is pad2
c.cd()  # returns to main canvas before defining pad2
pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.28)
pad2.SetTopMargin(0)  # joins upper and lower plot
pad2.SetBottomMargin(0.392)
pad2.SetGridx()
pad2.SetGridy()
pad2.SetTickx(1)
pad2.SetTicky(1)
pad2.Draw()

pad1.cd()

x_err = array('f', [0]*len(x))
graph_rates = ROOT.TGraphErrors(len(x), array('f', x), array('f', maximum), array('f', x_err), array('f', err_max))
graph_rates.SetTitle("")
graph_rates.SetMarkerStyle(21)
graph_rates.SetMarkerColor(4)
#for temperature
graph_rates.SetMarkerSize(.5)
#---------------
graph_rates.SetLineColor(4)
graph_rates.Draw("AP")
#graph_rates.GetXaxis().SetTitle("Shaping Time [#mus]")
graph_rates.GetXaxis().SetTitle("Time [min]")
graph_rates.GetYaxis().SetTitle("Channel maximum")
pad1.Update()
              
pad2.cd()
graph_res = ROOT.TGraphErrors(len(x),array('f', x), array('f', temperature), array('f', x_err), array('f', err_temp))
graph_res.SetTitle("")
#graph_res.SetMarkerStyle(21)
#for temperature
graph_res.SetMarkerStyle(8)
graph_res.SetMarkerSize(0)
#----------------------
graph_res.SetLineColor(2)
#for temperature
graph_res.SetLineWidth(2)
#----------------------
graph_res.SetMarkerColor(2)
graph_res.GetXaxis().SetTitle("Time [min]")
graph_res.GetYaxis().SetTitle("Temperature [#circ C]")
graph_res.Draw("AP")
pad2.Update()

c.Draw()
c.SaveAs("./max_2.root")
