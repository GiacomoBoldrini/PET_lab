from VectorClass import vector as vct
import math as mt
import ROOT as r
import numpy as np
from array import array
import sys
import re

#first we need to find the average position:

f = open('./positions_bianca.txt', 'r')
lines = f.readlines()
x = []
y = []

for line in lines:
    line = re.split(',|:', line)
    x_pos_ind = line.index(list(l for l in line if 'x' in l)[0])+1
    x_pos = float(line[x_pos_ind])
    x.append(x_pos)
    y_pos_ind = line.index(list(l for l in line if 'y' in l)[0])+1
    y_pos= float(line[y_pos_ind])
    y.append(y_pos)

average_x = np.mean(x)
average_y = np.mean(y)
std_dev_x = np.std(x)
std_dev_y = np.std(y)

#print('Best pos {}+-{}, {}+-{}'.format(average_x, std_dev_x, average_y, std_dev_y))

#now plotting everything on the rotating plate:
c = r.TCanvas("c", "c", 1000,1000,1500,1000)
legend = r.TLegend(0.1,0.7,0.35,0.9)
legend.SetHeader("Legend", "C")

g = r.TGraph(len(x), np.array(x), np.array(y))
g.SetTitle('Geometrical Reconstruction')

g_sub = r.TGraph(len(x), np.array(x), np.array(y))
g_sub.SetTitle('Zoom CL')
g_sub.GetXaxis().SetLimits(0,1.4)
g_sub.GetYaxis().SetRangeUser(-14.3,-10)
g_sub.SetMarkerSize(1)
g_sub.SetMarkerStyle(r.kStar)


l1 = r.TLine(-15,0,15,0)
l2 = r.TLine(0,-15,0,15)
g.GetXaxis().SetLimits(-40,18)
g.GetYaxis().SetRangeUser(-20,18)
g.SetMarkerSize(1)
g.SetMarkerStyle(r.kStar)

circle = r.TEllipse(0,0,15,15)
circle.SetLineColor(1)
circle.SetLineWidth(3)
circle.SetFillStyle(0)

real_slit = r.TEllipse(0,0,13.3,13.3)
real_slit.SetLineColor(1)
real_slit.SetLineWidth(1)
real_slit.SetFillStyle(0)
real_slit.SetLineStyle(9)

#confidence levels
cl = r.TBox(average_x-std_dev_x/2, average_y-std_dev_y/2, average_x+std_dev_x/2, average_y+std_dev_y/2)
cl.SetLineColor(0)
cl.SetFillColorAlpha(r.kBlue, 0.2)
cl.SetFillStyle(1100)

cl1 = r.TBox(average_x-std_dev_x, average_y-std_dev_y, average_x+std_dev_x, average_y+std_dev_y)
cl1.SetLineColor(0)
cl1.SetFillColorAlpha(r.kGreen, 0.2)
cl1.SetFillStyle(1100)

cl2 = r.TBox(average_x-(3/2)*std_dev_x, average_y-(3/2)*std_dev_y, average_x+(3/2)*std_dev_x, average_y+(3/2)*std_dev_y)
cl2.SetLineColor(0)
cl2.SetFillColorAlpha(r.kRed, 0.2)
cl2.SetFillStyle(1100)

legend.AddEntry(cl,"1#sigma region","f")
legend.AddEntry(cl1,"2#sigma region", "f")
legend.AddEntry(cl2,"3#sigma region", "f")

t1 = r.TLatex(0.85,-12.2,"1#sigma")
t1.SetTextAngle(-90)
t2 = r.TLatex(0.96,-12.2,"2#sigma")
t2.SetTextAngle(-90)
t3 = r.TLatex(-8.6,11,"4th slit")
t3.SetTextSize(.025)
t3.SetTextAngle(28)




legend.AddEntry(g,"All measures","P");


m = r.TMarker(average_x, average_y, 20)
m.SetMarkerSize(1)
m.SetMarkerColor(r.kRed)
legend.AddEntry(m,"Averaged","P")

#drawing
g.Draw('AP')
l1.Draw()
l2.Draw()
circle.Draw()
real_slit.Draw()
m.Draw()
t3.Draw()
legend.Draw()


subpad = r.TPad("subpad","",0.14,0.14,0.45,0.45)
subpad.Draw()
subpad.cd()
g_sub.Draw('AP')
cl.Draw()
cl1.Draw()
cl2.Draw()
real_slit.Draw()
m.Draw()
t1.Draw()
t2.Draw()



c.cd()
c.Draw()
c.SaveAs('./prova.png', 'png')



