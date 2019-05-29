import ROOT
from math import radians,cos,sin,tan
import numpy as np
import os
import pandas as pd
from array import array
import glob

def m_coeff(theta_rad):
    return sin(theta_rad)/(cos(theta_rad)-1)


def retta(m,alphas,X,R):
    first = (m*np.cos(alphas)-np.sin(alphas))/(np.cos(alphas) + m*np.sin(alphas))*X
    second = m*R/(np.cos(alphas)+m*np.sin(alphas))
    return first + second

path_data = "./Rates/"
path_graph = "./Graph_Reconstruction/"

alpha_giro = 160

radius = 31

#thetas =np.array([187.5,210,165])
thetas =np.array([157.5,142.5,187.5,210,165])
thetas_rad = [radians(i) for i in thetas]

alphas = np.arange(0,360,360/alpha_giro)
alphas_rad = [radians(i) for i in alphas]

rates = []
for i in range(1,6):
    s = str(i)
    name_file = "Positioning"+s
    r = np.load(path_data + name_file +"/rate_rel_pos"+s+".npy")
    rates.append(r)

rates = np.array(rates)

data = [[],[],[]]

for i in range(0,len(thetas_rad)):
    for j in range(0,len(alphas_rad)):
        data[0].append(thetas_rad[i])
        data[1].append(alphas_rad[j])
        data[2].append(rates[i][j])

d = np.array(data)
d = d.transpose()
df = pd.DataFrame(d,columns = ["thetas","alphas","rates"])
nbinx = 60
nbiny = 60
inf_x = -20
sup_x = 20
inf_y = -20
sup_y = 20
dimx = (sup_x-inf_x)/nbinx
dimy = (sup_y-inf_y)/nbiny
passo = (sup_x - inf_x) / nbinx

c1 = ROOT.TCanvas("c1","c1",1000,1000,1000,1000)
h2_reconstruction = ROOT.TH2F("h2","h2",nbinx,inf_x,sup_x,nbiny,inf_y,sup_y)

for i in range(0,alpha_giro*len(thetas_rad)):
    for j in range(0,nbinx):
        x = inf_x + passo * j + passo/2
        y=retta(m_coeff(df["thetas"][i]),df["alphas"][i],x,radius)
        h2_reconstruction.Fill(x,y,df["rates"][i])

ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
h2_reconstruction.SetTitle("No Dense")
h2_reconstruction.Draw("COLZ")
h2_reconstruction.SetStats(0)

c1.Print(path_graph+"Reconstruction.png","png")
inf_x_cut = -4
sup_x_cut = 4
inf_y_cut = -17
sup_y_cut = -8
nbinx_cut = int((sup_x_cut - inf_x_cut)/dimx)
nbiny_cut = int((sup_y_cut - inf_y_cut)/dimy)


h2_cut = ROOT.TH2F("h2_cut","h2_cut",nbinx_cut,inf_x_cut,sup_x_cut,nbiny_cut,inf_y_cut,sup_y_cut)

for i in range(0,alpha_giro*len(thetas_rad)):
    for j in range(0,nbinx):
        x = inf_x + passo * j + passo/2
        y=retta(m_coeff(df["thetas"][i]),df["alphas"][i],x,radius)
        h2_cut.Fill(x,y,df["rates"][i])

h2_cut.SetStats(0)
h2_cut.SetTitle("No Dense Cut")
h2_cut.Draw("COLZ")
c1.Print(path_graph+"Reconstruction_cut.png",",png")
#I bin si contano da in basso o da sinistra contando anche una colonna fuori e partendo da 0.

max_bin =h2_cut.GetMaximumBin()
x_max = round((max_bin/(nbinx_cut+2) - int(max_bin/(nbinx_cut+2)))*(nbinx_cut+2))
y_max = int(max_bin/(nbinx_cut+2))

print("Content_Maximum_Bin: {}".format(max_bin))
print("X_max:{}   Y_max:{}".format(x_max,y_max))
projX = ROOT.TH1F("projX","projx",nbinx_cut,inf_x_cut,sup_x_cut)
projY = ROOT.TH1F("projY","projY",nbiny_cut,inf_y_cut,sup_y_cut)

for i in range(1,nbinx_cut+1):
    #print(i + y_max*(nbinx_cut+2))
    #print(h2_cut.GetBinContent(i + y_max*(nbinx_cut+2)))
    projX.SetBinContent(i, h2_cut.GetBinContent(i + y_max*(nbinx_cut+2)))

index = []
for k in range(1,nbiny_cut+1):
    index.append(x_max+k*(nbinx_cut+2))

for j in range(1, nbiny_cut+1):
    #print(j)
    #print(h2_cut.GetBinContent(index[j-1]))
    projY.SetBinContent(j, h2_cut.GetBinContent(index[j-1]))

c2 = ROOT.TCanvas("projc2","projc2",1000,1000,1000,1000)
c2.Divide(1,2)

c2.cd(1)
projX.Draw("")
c2.cd(2)
projY.Draw("")
c2.Print(path_graph+"Projections.png","png")

path_data = "./Dense/"

alpha_giro = 40

radius = 31

thetas =np.array([157.5,142.5,187.5,210,157.5,142.5,187.5,210])
#thetas =np.array([157.5,142.5,187.5,210,165])
thetas_rad = [radians(i) for i in thetas]


#Alphas sono da inserire a mano per tutte le misure
alphas_11 = np.arange(38.78,54.78,0.4)
alphas_12 = np.arange(276.8,292.8,0.4)
alphas_21 = np.arange(5.56,21.56,0.4)
alphas_22 = np.arange(292,308,0.4)
alphas_31 = np.arange(88.1,103.9,0.4)
alphas_32 = np.arange(255.6,271.5,0.4)
alphas_41 = np.arange(126.6,142.6,0.4)
alphas_42 = np.arange(235.6,251.6,0.4)


print(len(alphas_11),len(alphas_12))
alphas_11_rad = [radians(i) for i in alphas_11]
alphas_12_rad = [radians(i) for i in alphas_12]
alphas_21_rad = [radians(i) for i in alphas_21]
alphas_22_rad = [radians(i) for i in alphas_22]
alphas_31_rad = [radians(i) for i in alphas_31]
alphas_32_rad = [radians(i) for i in alphas_32]
alphas_41_rad = [radians(i) for i in alphas_41]
alphas_42_rad = [radians(i) for i in alphas_42]

alphas_rad = [alphas_11_rad,alphas_21_rad,alphas_31_rad,alphas_41_rad,alphas_12_rad,alphas_22_rad,alphas_32_rad,alphas_42_rad]
#alphas = np.arange(0,360,360/alpha_giro)
#alphas_rad = [radians(i) for i in alphas]
alphas_rad = np.array(alphas_rad)

rates = []
for j in range(1,3):
    for i in range(1,5):
        s = str(i)
        k = str(j)
        name_file = "Positioning"+s
        r = np.load(path_data + name_file +"/dense_rate_rel_pos"+s+k+".npy")
        print(name_file +"/dense_rate_rel_pos"+s+k+".npy")
        rates.append(r)

rates = np.array(rates)
len(alphas_rad[4])

data_dense = [[],[],[]]


for i in range(0,len(thetas_rad)):
    for j in range(0,len(alphas_rad[0])):
        data_dense[0].append(thetas_rad[i])
        data_dense[1].append(alphas_rad[i][j])
        #print(alphas_rad[i][j])
        data_dense[2].append(rates[i][j])

d_dense = np.array(data_dense)
d_dense = d_dense.transpose()
df_dense = pd.DataFrame(d_dense,columns = ["thetas","alphas","rates"])
df_dense.head()

nbinx = 60
nbiny = 60
inf_x = -20
sup_x = 20
inf_y = -20
sup_y = 20
dimx = (sup_x-inf_x)/nbinx
dimy = (sup_y-inf_y)/nbiny
passo = (sup_x - inf_x) / nbinx

c3 = ROOT.TCanvas("ciao","ciao",1000,1000,1000,1000)
for i in range(0,alpha_giro*len(thetas_rad)):
    for j in range(0,nbinx):
        x = inf_x + passo * j + passo/2
        y=retta(m_coeff(df_dense["thetas"][i]),df_dense["alphas"][i],x,radius)
        h2_reconstruction.Fill(x,y,df_dense["rates"][i])
#h2_reconstruction_dense.Fill(x,y,df_dense["rates"][i])

ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
h2_reconstruction.SetTitle("With Dense")
h2_reconstruction.Draw("COLZ")
h2_reconstruction.SetStats(0)

c3.Print(path_graph+"Reconstruction_dense.png","png")

nbinx = 60
nbiny = 60
inf_x = -20
sup_x = 20
inf_y = -20
sup_y = 20
dimx = (sup_x-inf_x)/nbinx
dimy = (sup_y-inf_y)/nbiny
passo = (sup_x - inf_x) / nbinx



c3 = ROOT.TCanvas("ciao","ciao",1000,1000,1000,1000)
for i in range(0,alpha_giro*len(thetas_rad)):
    for j in range(0,nbinx):
        x = inf_x + passo * j + passo/2
        y=retta(m_coeff(df_dense["thetas"][i]),df_dense["alphas"][i],x,radius)
        h2_reconstruction.Fill(x,y,df_dense["rates"][i])
#h2_reconstruction_dense.Fill(x,y,df_dense["rates"][i])

ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
h2_reconstruction.SetTitle("With Dense")
h2_reconstruction.Draw("COLZ")
h2_reconstruction.SetStats(0)

c3.Print(path_graph+"Reconstruction_dense.png","png")

inf_x_cut = -4
sup_x_cut = 4
inf_y_cut = -17
sup_y_cut = -8
nbinx_cut = int((sup_x_cut - inf_x_cut)/dimx)
nbiny_cut = int((sup_y_cut - inf_y_cut)/dimy)

c4 = ROOT.TCanvas("ciao4","ciao4",1000,1000,1000,1000)
#h2_cut = ROOT.TH2F("h2_cut","h2_cut",nbinx_cut,inf_x_cut,sup_x_cut,nbiny_cut,inf_y_cut,sup_y_cut)

for i in range(0,alpha_giro*len(thetas_rad)):
    for j in range(0,nbinx):
        x = inf_x + passo * j + passo/2
        y=retta(m_coeff(df_dense["thetas"][i]),df_dense["alphas"][i],x,radius)
        h2_cut.Fill(x,y,df_dense["rates"][i])

h2_cut.SetStats(0)
#h2_cut.SetTitle("No Dense Cut")
h2_cut.Draw("COLZ")
c4.Print(path_graph+"Reconstruction_cut_with_dense.png",",png")

#I bin si contano da in basso o da sinistra contando anche una colonna fuori e partendo da 0.

max_bin =h2_cut.GetMaximumBin()
x_max = round((max_bin/(nbinx_cut+2) - int(max_bin/(nbinx_cut+2)))*(nbinx_cut+2))
y_max = int(max_bin/(nbinx_cut+2))

print("Content_Maximum_Bin: {}".format(max_bin))
print("X_max:{}   Y_max:{}".format(x_max,y_max))

projX_with_dense = ROOT.TH1F("","",nbinx_cut,inf_x_cut,sup_x_cut)
projY_with_dense = ROOT.TH1F("","",nbiny_cut,inf_y_cut,sup_y_cut)

for i in range(1,nbinx_cut+1):
    #print(i + y_max*(nbinx_cut+2))
    #print(h2_cut.GetBinContent(i + y_max*(nbinx_cut+2)))
    projX_with_dense.SetBinContent(i, h2_cut.GetBinContent(i + y_max*(nbinx_cut+2)))

index = []
for k in range(1,nbiny_cut+1):
    index.append(x_max+k*(nbinx_cut+2))

for j in range(1, nbiny_cut+1):
    #print(j)
    #print(h2_cut.GetBinContent(index[j-1]))
    projY_with_dense.SetBinContent(j, h2_cut.GetBinContent(index[j-1]))

c4 = ROOT.TCanvas("projc2_with_dense","projc2_with_dense",1000,1000,1000,1000)
c4.Divide(1,2)

c4.cd(1)
projX_with_dense.Draw("")
c4.cd(2)
projY_with_dense.Draw("")
c4.Print(path_graph+"Projections_with_dense.png","png")

nbinx = 60
nbiny = 60
inf_x = -20
sup_x = 20
inf_y = -20
sup_y = 20
dimx = (sup_x-inf_x)/nbinx
dimy = (sup_y-inf_y)/nbiny
passo = (sup_x - inf_x) / nbinx

c6 = ROOT.TCanvas("c6","c6",1000,1000,1000,1000)
h2_reconstruction_dense = ROOT.TH2F("h2_d","h2_d",nbinx,inf_x,sup_x,nbiny,inf_y,sup_y)

for i in range(0,alpha_giro*len(thetas_rad)):
    for j in range(0,nbinx):
        x = inf_x + passo * j + passo/2
        y=retta(m_coeff(df_dense["thetas"][i]),df_dense["alphas"][i],x,radius)
        h2_reconstruction_dense.Fill(x,y,df_dense["rates"][i])

ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
h2_reconstruction_dense.SetTitle("No Dense")
h2_reconstruction_dense.Draw("COLZ")
h2_reconstruction_dense.SetStats(0)

c6.Print(path_graph+"Reconstruction_only_dense.png","png")



#PROJECTIONS AND TH2F

#defining fit functions:

fit1 = ROOT.TF1("fit1", "[0]*exp(-((x[0]-[1])^2)/[2]^2)", -2, 4)
fit1.SetParameters(20,0,5)
fit2 = ROOT.TF1("fit2", "[0]*exp(-((x[0]-[1])^2)/[2]^2)", -16, -9)
fit2.SetParameters(50,-12,5)
nbinx = 60
nbiny = 60
inf_x = -20
sup_x = 20
inf_y = -20
sup_y = 20
dimx = (sup_x-inf_x)/nbinx
dimy = (sup_y-inf_y)/nbiny
passo = (sup_x - inf_x) / nbinx

ROOT.gStyle.SetOptStat(0)


c1 = ROOT.TCanvas("c", "c", 50,50,1000,1000)
center_pad = ROOT.TPad("center_pad", "center_pad",0.0,0.0,0.7,0.7)
center_pad.Draw()

right_pad = ROOT.TPad("right_pad", "right_pad",0.7,0.0,1,0.7)
right_pad.Draw()

top_pad = ROOT.TPad("top_pad", "top_pad",0.0,0.7,0.7,1.0)
top_pad.Draw()

#plotting central pad
center_pad.cd()
ROOT.gStyle.SetPalette(1)
h2_cut.SetTitle("")
h2_cut.Draw("COLZ")

#plotting X projection
top_pad.cd()
#projX_with_dense.SetLineColor(ROOT.kBlack)
#projX_with_dense.Fit(fit1)
#fit1.SetLineColor(ROOT.kBlack)
projX_with_dense.SetFillColor(ROOT.kBlue)
projX_with_dense.SetFillStyle(3003)
projX_with_dense.SetLineColor(0)
projX_with_dense.Draw("histo")
#fit1.Draw("same")

#plotting Y proj
right_pad.cd()
projY_with_dense.SetFillStyle(3003)
projY_with_dense.SetFillColor(ROOT.kBlue)
projY_with_dense.Draw("hbar")

#title

c1.cd()

c1.Print(path_graph+"projections.png",",png")
"""
inf_x_cut = -4
sup_x_cut = 4
inf_y_cut = -17
sup_y_cut = -8
nbinx_cut = int((sup_x_cut - inf_x_cut)/dimx)
nbiny_cut = int((sup_y_cut - inf_y_cut)/dimy)

c7 = ROOT.TCanvas("ciao7","ciao7",1000,1000,1000,1000)
h2_cut_only_dense = ROOT.TH2F("h2_cut_only_dense","h2_cut_only_dense",nbinx_cut,inf_x_cut,sup_x_cut,nbiny_cut,inf_y_cut,sup_y_cut)

for i in range(0,alpha_giro*len(thetas_rad)):
    for j in range(0,nbinx):
        x = inf_x + passo * j + passo/2
        y=retta(m_coeff(df_dense["thetas"][i]),df_dense["alphas"][i],x,radius)
        h2_cut_only_dense.Fill(x,y,df_dense["rates"][i])

h2_cut_only_dense.SetStats(0)
h2_cut_only_dense.SetTitle("No Dense Cut")
h2_cut_only_dense.Draw("COLZ")
c7.Print(path_graph+"Reconstruction_cut_only_dense.png",",png")
"""



