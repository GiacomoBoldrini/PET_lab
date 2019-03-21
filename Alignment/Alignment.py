#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:38:42 2018

@author: Jack bitch
"""

"""
This program reads spectrum iteration and plots bias vs full width half maximum 
"""

import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob

#creates a directory
def mkdir_p(mypath):

    from errno import EEXIST
    from os import makedirs,path

    try:
        makedirs(mypath)
    except OSError as exc: 
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise

def Create_Canvas_Pads():
    c1 = r.TCanvas("c1", "c1", 50,50, 1050,900)
    #pad1 = r.TPad("pad1", "pad1", 0, 0.28, 1, 1)
    pad1 = r.TPad("pad1", "pad1", 0, 0, 1, 1)
    #pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetGridx()
    #pad2 = r.TPad("pad2", "pad2", 0, 0.28, 1, 1)
    pad2 = r.TPad("pad2", "pad2", 0, 0, 1, 1)
    pad2.SetFillStyle(4000)
    pad2.SetFrameFillStyle(4000)
    #pad2.SetBottomMargin(0)  # joins upper and lower plot
    pad2.SetGridx()
    
    """
    # Lower ratio plot is pad3
    c1.cd()  # returns to main canvas before defining pad2
    pad3 = r.TPad("pad3", "pad3", 0, 0.0, 1, 0.28)
    pad3.SetTopMargin(0)  # joins upper and lower plot
    pad3.SetBottomMargin(0.392)
    pad3.SetGridx()
    pad3.SetGridy()
    """


    return c1, pad1, pad2

"""
def Rate_Res_Plotter(n_measures, voltages, res, err_res, rates, err_rates):
    print("n_measures: {}".format(n_measures))
    print("voltages: {}".format(voltages))
    print("res: {}".format(res))
    print("err_res: {}".format(err_res))
    print("rates: {}".format(rates))
    print("err_rates: {}".format(err_rates))
    x = array('f', voltages)
    x_err = array('f', [0]*n_measures)
    y1 = array('f', res)
    y1_err = array('f', err_res)
    y2 = array('f', rates)
    y2_err = array('f', err_rates)
    score = []
    err_score = []
    i = 0
    while i < n_measures:
        score.append(rates[i] - res[i])
        err_score.append(err_res[i] + err_rates[i])
        i += 1
    score = array('f', score)
    err_score = array('f', err_score)
    
    c1, pad1, pad2 = Create_Canvas_Pads()
    graph_res = r.TGraphErrors(n_measures,x,y1, x_err, y1_err)
    graph_res.SetTitle("Voltage Bias")
    graph_res.SetMarkerStyle(21)
    graph_res.SetLineColor(2)
    graph_res.SetMarkerColor(2)
    graph_rates = r.TGraphErrors(n_measures,x,y2, x_err, y2_err)
    graph_rates.SetTitle("")
    graph_rates.SetMarkerStyle(21)
    graph_rates.SetMarkerColor(4)
    graph_rates.SetLineColor(4)
    graph_score = r.TGraphErrors(n_measures,x,score, x_err, err_score)

    pad1.Draw()
    pad1.cd()
    graph_rates.Draw("APL")
    graph_rates.GetXaxis().SetTitle("Voltages [V]")
    histo = graph_rates.GetHistogram()
    axis = histo.GetYaxis()
    axis.SetAxisColor(4)
    axis.SetLabelColor(4)
    axis.SetTitle("Live Rate [counts/sec]")
    axis.SetTitleColor(4)
    axis.SetTitleOffset(1.2)
    pad1.Update()

    pad2.Draw()
    pad2.cd()
    graph_res.Draw("APLY+ sames")
    histo = graph_res.GetHistogram()
    axis = histo.GetYaxis()
    axis.SetAxisColor(2)
    axis.SetLabelColor(2)
    axis.SetTitle("Resolution")
    axis.SetTitleColor(2)
    axis.SetTitleOffset(1.2)
    pad2.Update()

    
    pad3.Draw()
    pad3.cd()
    graph_score.Draw("APL")


    c1.Draw()
    c1.SaveAs("/Users/boldrinicoder/lab4/graph.pdf", "pdf")




            
#Function which compute the percentage resolution as FWHM/mean*100
def Resolution(function):
    
    #Annullo il fondo
    function.SetParameter(3,0)
    function.SetParameter(4,0)
    function.SetParameter(5,0)
    mean = function.GetParameter(1)
    maxi = function.GetMaximum()
    Xmax = function.GetMaximumX()
    temp = Xmax
    estremo_sx = 0
    estremo_dx = 0
    epsilon = 0.0001

#Determino l'estremo sinistro
    while(1):
        if function.Eval(temp) < maxi/2:
            estremo_sx = temp
            break
        temp -= epsilon
    temp = Xmax

#Determino l'estremo destro
    while(1):
        if function.Eval(temp) < maxi/2:
            estremo_dx = temp
            break
        temp += epsilon
        
        
    mean = function.GetParameter(1)
    err_mean = function.GetParError(1)
    err_sigma = function.GetParError(2)
    err_fwhm = 2.355*err_sigma
    fwhm = (estremo_dx - estremo_sx)

    return [(estremo_dx - estremo_sx)*100/mean , 100*math.sqrt(((1/mean)**2)*err_fwhm**2+((fwhm/mean**2)**2)*err_mean**2)]

    
def Rate(function,a,b, n):
    function.SetParameter(3,0)
    function.SetParameter(4,0)
    function.SetParameter(5,0)
    Integral = function.Integral(a,b)
    Err_Integral = function.IntegralError(a,b,n.GetParams())
    print("RATEO:")
    print("INF: {}".format(a))
    print("SUP: {}".format(b))
    print("Integal: {}".format(Integral))
    print("Err_Integral: {}".format(Err_Integral))
    return [Integral/200, Err_Integral/200]


"""
def Rate(function, a, b, n):
    function.SetParameter(3,0)
#    function.SetParameter(4,0)
#    function.SetParameter(5,0)
    Integral = function.Integral(a,b)
    Err_Integral = function.IntegralError(a,b,n.GetParams())
    return [Integral/200, Err_Integral/200]

def Fitter_rate(data, measure, inf, sup, mean):
#Here I open the file (set data and measure) and I fill an array
    f =  open(data, "r")
    list = f.readlines()

    first_lines = 12
    last_lines = -18

    arr = np.array([])

    for i in list:
        arr = np.append(arr,i.strip())

    value0 = arr[first_lines:last_lines]
    value0 = value0.astype(int)
    value = []
    for i in value0:
        value.append(i)
    
#Fit and draw of spectrum    
    bins = sup-inf
    peak = value.index(max(value))
    h2 = r.TH1F("h2", "h2", bins, inf, sup)
    h2.SetFillColor(r.kBlue)
    h2.SetFillStyle(3003)
    h2.SetLineWidth(2)
    i = inf
    z = 0
    #fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]",inf,sup)
    fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]",inf,sup)
    fit.SetParameters(2200,mean,18,0.1,0,100)
    fit.SetLineWidth(3)
    while i < sup:
        h2.SetBinContent(z,value[i])
        i += 1 
        z += 1
    integral = 0
    
    inf_rate=fit.GetParameter(1)-3*fit.GetParameter(2)
    sup_rate=fit.GetParameter(1)+3*fit.GetParameter(2)


    c2 = r.TCanvas("c2", "c2",50,50,1000,800)
    n = h2.Fit("fit", "RLS")
    h2.Draw("histo same")
    r.gStyle.SetOptStat(1111)
    r.gStyle.SetOptFit(1111)
    c2.Draw() 
    c2.Show()
    c2.SaveAs("/Users/boldrinicoder/lab4/data/GraficiAlignHoriz/justtoshow{}.png".format(measure))
    
    rate = Rate(fit, inf_rate, sup_rate, n)
    
    return rate


#def Plotter(index, x, maximum, x_err, y_err, title, xlabel, ylabel, output):
def Plotter(index, x, maximum, title, xlabel, ylabel, output):
    
    #definiamo il grafo
    #g = r.TGraphErrors(index,x,maximum, x_err, y1_err)
    g = r.TGraph(index, x, maximum)
    #g.SetTitle("Peak Shift over Temperature")
    g.SetTitle(title)
    g.SetMarkerStyle(21)
    g.SetMarkerColor(4)
    g.SetLineColor(4)
    #g.GetXaxis().SetTitle("Temperature [C]")
    g.GetXaxis().SetTitle(xlabel)
    #g.GetYaxis().SetTitle("Max Channel")
    g.GetYaxis().SetTitle(ylabel)
    
    fit = r.TF1("fit", "[0]*x[0]+[1]", 13, 15.3218968104)
    fit1 = r.TF1("fit1", "[0]*x[0]+[1]", 15.3218968104, 16.2,'--')
    #fit.SetParameter(1, 15)
    #fit.SetParameter(2, 165)
    #fit.SetParameter(0,-5)
    fit.SetLineColor(r.kRed)
    #definiamo il canvas e plottiamo
    c2 = r.TCanvas("c2", "c2",50,50,1000,800)
    c2.SetGridx()
    c2.SetGridy()
    g.Draw("AP")
    g.Fit("fit", "R")
    g.Fit("fit1", "R")
    fit.Draw("same")
    fit1.Draw("same")
    r.gStyle.SetStatX(.9)
    r.gStyle.SetStatY(.4)
    r.gStyle.SetOptFit(1111)
    c2.Draw()
    c2.Show()
    #c2.SaveAs("/Users/boldrinicoder/lab4/prova.pdf", "pdf")
    c2.SaveAs(output, "pdf")

#################MAIN############################
r.gROOT.SetBatch(True)

#leggiamo e fittiamo tutti gli spettri
f = sorted(glob.glob("/Users/boldrinicoder/lab4/data/190116/*.txt"))
index = 0
mkdir_p("/Users/boldrinicoder/lab4/data/GraficiAlignHoriz")
position = [13, 13.5, 14, 14.2, 14.5, 14.7, 15, 15.2, 15.5, 15.7, 16, 16.2]
rates = []
for i in f:
    rates.append(Fitter_rate(i, index, 550,850,700)[0])
    index += 1

position = array('f', position)
rates = array('f', rates)
#err_rates = array('f', np.zeros(index))
#err_position = array('f', np.full(1,index), 0.1)
print("rates: len: {}, {}".format(len(rates),rates))
print("position: len: {}, {}".format(len(position), position))
print("index: len: {}, {}".format(index, index))

Plotter(len(position), position, rates, "Counting rate over Horizontal position", "Height [cm]", "Rate [count/second]", "/Users/boldrinicoder/lab4/Alignment2.pdf")

######################





