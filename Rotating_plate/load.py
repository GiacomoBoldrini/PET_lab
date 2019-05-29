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
h.GetXaxis().SetTitle("Velocity [TMCL units]")
h.GetYaxis().SetTitle("Load index [TMCL units]")
h.SetTitle("")
#h.SetFillStyle(3004)
h.SetLineColor(r.kAzure-4)
h.SetLineWidth(0)
h.SetFillColor(r.kAzure-4)
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
        if i > 220 and i < 230:
            b = r.TBox(h.GetBinLowEdge(i),
                       h.GetMinimum(),
                       h.GetBinWidth(i)+h.GetBinLowEdge(i),
                       load_index[i]+.1)
            b.SetFillColor(r.kRed+1)
            b.SetLineWidth(0)
            lista_box.append(b)
        
        else:
            #lista_box.append(ClassFunc.Paint_bin(h, i, r.kRed+1))
            b = r.TBox(h.GetBinLowEdge(i),
                       h.GetMinimum(),
                       h.GetBinWidth(i)+h.GetBinLowEdge(i),
                       load_index[i])
            b.SetFillColor(r.kRed+1)
            b.SetLineWidth(0)
            lista_box.append(b)
    i+=1

for i in lista_box:
    i.Draw()

r.gStyle.SetOptStat(0000)
legend = r.TLegend(.893,.89,0.6,0.75)
legend.SetBorderSize(1)
legend.AddEntry(h, "no vibration", "f")
legend.AddEntry(lista_box[0], "vibration detection", "f")
legend.SetTextSize(.03)
legend.Draw()
c.SaveAs("/Users/boldrinicoder/lab4/General_Graphs/roots/load.root", "root")
c.SaveAs("/Users/boldrinicoder/lab4/General_Graphs/pdfs/load.pdf", "pdf")


