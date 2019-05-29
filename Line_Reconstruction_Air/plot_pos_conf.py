from VectorClass import vector as vct
import math as mt
import ROOT as r
import numpy as np
from array import array
import sys
import re
from scipy.stats import pearsonr


def ellipse_confidence(x,y, t):

    #http://www.visiondummy.com/2014/04/draw-error-ellipse-representing-covariance-matrix/
    
    #calcola la media
    center_x = x.mean()
    center_y = y.mean()
    #calcolo deviazioni
    s_x = np.std(x)
    s_y = np.std(y)
    #covariance matrix
    cov = np.cov(x,y)
    eigenvalues, eigv = np.linalg.eig(cov)
    
    #maj_axis = 2*np.sqrt(2.35*max(eigenvalues))
    #min_axis = 2*np.sqrt(2.35*min(eigenvalues))
    maj_axis = np.sqrt(t*max(eigenvalues))
    min_axis = np.sqrt(t*min(eigenvalues))
    
    i = np.where(eigenvalues==max(eigenvalues))
    max_eigenvector = eigv[:,i]
    
    theta = mt.atan(max_eigenvector[1][0][0]/max_eigenvector[0][0][0])

    return [center_x, center_y], maj_axis, min_axis, theta


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

print('Best pos {}+-{}, {}+-{}'.format(average_x, std_dev_x, average_y, std_dev_y))

print('x:', x)
print('y:', y)
#now plotting everything on the rotating plate:
c = r.TCanvas("c", "c", 1000,1000,2000,1500)
legend = r.TLegend(0.15,0.71,0.35,0.89)
legend.SetHeader("", "C")
legend.SetLineWidth(0)

g = r.TGraph(len(x), np.array(x), np.array(y))
g.SetTitle('')
g.GetXaxis().SetLimits(-50,18)
g.GetYaxis().SetRangeUser(-20,20)
g.SetMarkerSize(1)
g.SetMarkerStyle(r.kStar)

g_sub = r.TGraph(len(x), np.array(x), np.array(y))
g_sub.SetTitle('')
g_sub.GetXaxis().SetLimits(-0.5,1.9)
g_sub.GetYaxis().SetRangeUser(-16,-11)
g_sub.SetMarkerSize(1)
g_sub.SetMarkerStyle(r.kStar)


l1 = r.TLine(-17.5,0,17.5,0)
l2 = r.TLine(0,-17.5,0,17.5)


circle = r.TEllipse(0,0,17.5,17.5)
circle.SetLineColor(1)
circle.SetLineWidth(3)
circle.SetFillStyle(0)

sub_circle = r.TEllipse(0,0,17.5,17.5)
sub_circle.SetLineColor(1)
sub_circle.SetLineWidth(3)
sub_circle.SetFillStyle(0)

real_slit = r.TEllipse(0,0,13.3,13.3)
real_slit.SetLineColor(1)
real_slit.SetLineWidth(1)
real_slit.SetFillStyle(0)
real_slit.SetLineStyle(9)

#confidence levels
[center_x, center_y], maj_axis, min_axis, theta = ellipse_confidence(np.array(x), np.array(y), 2.35)

cl = r.TEllipse(center_x,center_y,min_axis,maj_axis,0,360, theta)
cl.SetLineColor(0)
cl.SetFillColorAlpha(r.kBlue, 0.2)
cl.SetFillStyle(1100)
legend.AddEntry(cl,"68% cl","f")

[center_x, center_y], maj_axis1, min_axis1, theta1 = ellipse_confidence(np.array(x), np.array(y), 5.991)

cl1 = r.TEllipse(center_x,center_y,min_axis1,maj_axis1,0,360, theta1)
cl1.SetLineColor(0)
cl1.SetFillColorAlpha(r.kGreen, 0.2)
cl1.SetFillStyle(1100)
legend.AddEntry(cl1,"95% cl","f")

t1 = r.TLatex(.8,-11,"68% ellipse")
t1.SetTextAngle(-45)
t1.SetTextSize(.035)

t2 = r.TLatex(1,-10.5,"95% ellipse")
t2.SetTextAngle(-45)
t2.SetTextSize(.035)

t3 = r.TLatex(-8.6,11,"4th slit")
t3.SetTextSize(.025)
t3.SetTextAngle(28)

zoom_box = r.TBox(-0.8,-16,2.2,-11)
zoom_box.SetLineColor(1)
zoom_box.SetLineWidth(1)
zoom_box.SetFillStyle(0)
zoom_box.SetLineStyle(1)

zoom_sigma = r.TBox(average_x-std_dev_x,average_y-std_dev_y,average_x+std_dev_x,average_y+std_dev_y)
zoom_sigma.SetLineColor(0)
zoom_sigma.SetFillColorAlpha(r.kBlue, 0.2)
zoom_sigma.SetFillStyle(1100)
#legend.AddEntry(zoom_sigma,"1#sigma region","f")

zoom_2sigma = r.TBox(average_x-2*std_dev_x,average_y-2*std_dev_y,average_x+2*std_dev_x,average_y+2*std_dev_y)
zoom_2sigma.SetLineColor(0)
zoom_2sigma.SetFillColorAlpha(r.kGreen, 0.2)
zoom_2sigma.SetFillStyle(1100)
#legend.AddEntry(zoom_2sigma,"2#sigma region","f")




legend.AddEntry(g,"All measures","P");


m = r.TMarker(average_x, average_y, 20)
m.SetMarkerSize(1)
m.SetMarkerColor(r.kRed)
legend.AddEntry(m,"Mean Position","P")

#drawing
g.Draw('AP')
l1.Draw()
l2.Draw()
circle.Draw()
real_slit.Draw()
m.Draw()
zoom_box.Draw()
t3.Draw()
legend.Draw()


subpad = r.TPad("subpad","",0.17,0.14,0.39,0.6)
subpad.Draw()
subpad.cd()
g_sub.Draw('AP')
real_slit.Draw()
sub_circle.Draw()
#zoom_sigma.Draw()
#zoom_2sigma.Draw()
cl.Draw()
cl1.Draw()
m.Draw()
#t1.Draw()
#t2.Draw()



c.cd()
c.Draw()
#c.SaveAs('./paired_326_cl.png', 'png')
#c.SaveAs('./paired_326_cl.root', 'root')



