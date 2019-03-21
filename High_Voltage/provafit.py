#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:38:42 2018

@author: wahid
"""

"""
This program reads spectrum iteration and plots bias vs full width half maximum 
"""

import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math

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
            
#Function which compute the percentage resolution as FWHM/mean*100
def Resolution(function):
    
    #Annullo il fondo
    function.SetParameter(3,0)
    function.SetParameter(4,0)
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
    Integral = function.Integral(a,b)
    Err_Integral = function.IntegralError(a,b,n.GetParams())
    return [Integral/200, Err_Integral/200]
    

"""
Aggiornare alla data dell'esperimento
"""
data = str(181130)

"""
Cambiare solo path dove salvare il canvas e da dove importare i file.
"""

def Fitter(measure, inf, sup, mean):
    f = open("/Users/boldrinicoder/lab4/data/{}/{}{}".format(data,data,measure), "r")
    lists = f.readlines()
    value = []
    for i in lists:
        value.append(i.strip())
    value = list(map(int,value))
    
    #set this manually
    bins = sup-inf
    peak = value.index(max(value))
    h2 = r.TH1F("h2", "h2", bins, inf, sup)
    h2.SetFillColor(r.kBlue)
    h2.SetFillStyle(3003)
    h2.SetLineWidth(2)
    i = inf
    z = 0
    fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]",inf,sup)
    fit.SetParameters(2200,600,18,0.1,0,100)
    fit.SetLineWidth(3)
    while i < sup:
        h2.SetBinContent(z,value[i])
        i += 1 
        z += 1
    integral = 0

    c2 = r.TCanvas("c2", "c2",50,50,1000,800)
    n = h2.Fit("fit", "RLS")
    h2.Draw("histo same")
    r.gStyle.SetOptStat(1111)
    r.gStyle.SetOptFit(1111)
    c2.Draw() 
    c2.Show()
    #c2.SaveAs("/Users/boldrinicoder/lab4/.png")
    
    #returns Rate and Err_rate
    rate = Rate(fit, inf, sup, n)
    
    #returns Res and Err_Res
    Res = Resolution(fit)
    
    return rate, Res

OOS_Resolutions = []
OOS_Res_Errors = []
OOS_Rates=[]
OOS_Err_Rates = []

###############################
rateo, reso = Fitter('09', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('10', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('11', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('12', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('13', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('14', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('15', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('16', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('17', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('18', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('19', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])

###############################
rateo, reso = Fitter('20', 500, 700,600)
print(rateo, reso)
OOS_Resolutions.append(reso[0])
OOS_Res_Errors.append(reso[1])
OOS_Rates.append(rateo[0])
OOS_Err_Rates.append(rateo[1])
