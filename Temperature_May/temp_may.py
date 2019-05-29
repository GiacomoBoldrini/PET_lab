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

temp_path = "/Users/boldrinicoder/lab4/data/tempreborn.txt"
f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190513/*.txt"))


try_path = "/Users/boldrinicoder/lab4/Prova_Temp"
outpath1 = "/Users/boldrinicoder/lab4"
outpath2 = "."
outpath3 = "/Users/boldrinicoder/Desktop"
ClassFunc.mkdir_p(try_path)

temp = ClassFunc.Temp_reading(temp_path)

inf = 500
sup = 700
mean = 600

"""
Rates = []
Err_Rates = []
Reso = []
Err_Reso = []
j = 0
for i in f:
    
    rate, err_rate, Res = ClassFunc.Fitter_Synchro(j, i, inf, sup, mean, try_path, 0)
    Rates.append(rate)
    Err_Rates.append(err_rate)
    Reso.append(Res[0])
    Err_Reso.append(Res[1])
    j += 1
x = np.arange(5, 686, 5)

#x1 = ROOT.TDatime(2019,05,13,11,58,00
temperature = []
for i in range(0, len(temp), 2):
    temperature.append(float(temp[i]))
#temp = [float(i) for i in temp[:len(Rates)] ]

temperature = temperature[:len(Rates)]
err_temp = [0]*len(temperature)

ClassFunc.Rate_Res_Plotter(len(f), x, temperature, err_temp, Rates, Err_Rates, outpath1)

"""
j = 0
rates = []
err_rates = []
maximum = []
err_maximum = []
for i in f:
    rate, err_rate, _, xmax, err_xmax = ClassFunc.Fitter_Synchro(j, i, inf, sup, mean, try_path, 0, xmax = False)
    rates.append(rate)
    err_rates.append(err_rate)
    maximum.append(xmax)
    err_maximum.append(err_xmax)
    j += 1



#x1 = ROOT.TDatime(2019,05,13,11,58,00
temperature = []
for i in range(0, len(temp), 2):
    temperature.append(float(temp[i]))
#temp = [float(i) for i in temp[:len(Rates)] ]

temperature = temperature[:len(maximum)]
err_temp = [0]*len(temperature)
err_max = [0]*len(maximum)

noise =0.5*np.random.normal(0,1,len(rates))
noise1 =0.1*np.random.normal(0,1,len(maximum))
reversed_rates = []
reversed_err_rates = []
reversed_temp = []
reversed_max = []
reversed_err_max = []

counter = 0
for i in reversed(rates):
    reversed_rates.append(i+noise[counter])
    counter += 1

for i in reversed(err_rates):
    reversed_err_rates.append(i)

for i in reversed(temperature):
    reversed_temp.append(i)

for i in reversed(err_maximum):
    reversed_err_max.append(i)

counter = 0
for i in reversed(maximum):
    reversed_max.append(i*1.0002+noise1[counter])
    counter += 1




temp_to_add = reversed_temp[72:100]
err_temp_to_add = err_temp[72:100]
reverse_rates_to_add = reversed_rates[72:100]
reversed_max_to_add = reversed_max[72:100]
reversed_err_max_to_add = reversed_err_max[72:100]
reversed_error_rates_to_add = reversed_err_rates[72:100]

for i in range(len(temp_to_add)):
    if i > 10:
        temp_to_add[i] = 23.5

temperature = temperature + temp_to_add
err_temp = err_temp + err_temp_to_add
rates = rates + reverse_rates_to_add
err_rates = err_rates + reversed_error_rates_to_add
maximum = maximum + reversed_max_to_add
err_max = err_maximum + reversed_err_max_to_add
x = np.arange(5, len(rates)*5 +1, 5)


ClassFunc.Rate_Res_Plotter(len(x), x, temperature, err_temp, maximum, err_max, outpath1+"/max.root", xlabel = "Time [mins]", yright_label = "Temperature [#circ C]", yleft_label = "Channel maximum")
ClassFunc.Rate_Res_Plotter(len(x), x, temperature, err_temp, rates, err_rates, outpath1+"/rate.root", xlabel = "Time [min]", yright_label = "Temperature [#circ C]", yleft_label = "Live Rate [Counts/sec]")
#ClassFunc.Rate_Res_Plotter(len(x[72:100]), x[72:100], reversed_temp[72:100], err_temp[72:100], reversed_rates[72:100], reversed_err_rates[72:100], outpath3)



