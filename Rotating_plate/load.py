#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:38:42 2018

@author: Jack
"""

"""
This program reads spectrum iteration and plots bias vs full width half maximum 
"""

import ROOT as r
import numpy as np
from loadfunc import ClassFunc

load_index, vibration_index, velocity = ClassFunc.Load_reading("/Users/boldrinicoder/lab4/Rotating_plate/load.txt")

h = r.TH1F("h", "h", 351, 0, 350)
h.GetXaxis().SetTitle("Velocity [a.u.]")
h.GetYaxis().SetTitle("Load_index [a.u.]")
h.SetTitle("Best Velocity range")
#h.SetFillStyle(3004)
h.SetLineColor(r.kGreen-7)
h.SetLineWidth(2)
h.SetFillColor(r.kGreen-7)
i = 0
while i < len(load_index):
    h.SetBinContent(i,load_index[i])
    i += 1

c = r.TCanvas("c", "c", 50,50,1000,800)
h.Draw("hist")
lista_box = []
i = 0
while i < len(vibration_index):
    if vibration_index[i] != 0:
        lista_box.append(ClassFunc.Paint_bin(h, i, r.kRed+1))
    i+=1

for i in lista_box:
    i.Draw()
c.SetGridx()
c.SetGridy()
r.gStyle.SetOptStat(0000)
legend = r.TLegend(.893,.89,0.6,0.75)
legend.SetBorderSize(1)
legend.AddEntry(h, "no vibration", "f")
legend.AddEntry(lista_box[0], "vibration detection")
legend.SetTextSize(.03)
legend.Draw()
c.SaveAs("/Users/boldrinicoder/Desktop/prova2.pdf", "pdf")


