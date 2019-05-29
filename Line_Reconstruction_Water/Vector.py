from VectorClass import vector as vct
import math as mt
import ROOT as r
import numpy as np
from array import array
import sys

#Degrees to radians conversion function

def to_rad(degrees):    
    return (mt.pi/180)*degrees

def rad_vec(vec):
    vec_rad = np.array([])
    
    for i in vec:
        vec_rad = np.append(vec_rad,(mt.pi/180)*i)
    
    return vec_rad


############### Main ##################

#Creating the circle centered in (0,0)

circ = r.TEllipse(0,0,20,20)
circ.SetLineColor(1)
circ.SetLineWidth(3)
circ.SetFillColor(0)


#Creating the Canvas

c = r.TCanvas("c","c",0,0,1000,1000)
c.SetTickx()
c.SetTicky()



#Creating a TGraphs centered in 0 with semi-amplitude n/2

n = 60

x = []
y = []

for i in range(0,n):            #Building two vectors from -n/2 up to n/2.
    x.append(i-n/2)
    y.append(i-n/2)

x = array("f",x)
y = array("f",y)    #Converting the two numpy array in two standard array


gr = r.TGraph(n,x,y)
gr.SetTitle("Geometric Reconstruction")
gr.GetXaxis().SetTitle("X Coordinate (cm)")
gr.GetYaxis().SetTitle("Y Coordinate (cm)")
gr.GetYaxis().SetTitleOffset(1.2)
gr.SetMarkerColor(r.kWhite)

c.cd()
gr.Draw("AP")
circ.Draw() 

struct_array = np.array([]) #Creating the struct array


#Initializing the parameters for the struct - all the angles are in radians (converted)

radius = 30 #In centimeters
thetas = rad_vec(np.array([157.5,142.5,187.5,210,165])) #Angles between the scintillators
alphas = rad_vec(np.array([46.78,304,100.1,138.6,59.87])) #First angles
betas = rad_vec(np.array([284.9,12.6,263.6,240.6,278.4])) #Second angles

try:
    N_meas= int(sys.argv[1])      #Read from the terminal
except:
    N_meas = len(betas)


for i in range(0,N_meas):
    
    v1_a = r.TVector3() 
    v1_b = r.TVector3()
    
    v1_a = r.TVector3(-radius,0,0)
    v1_b = r.TVector3(-radius,0,0)
    v2_a = r.TVector3(radius * mt.cos(mt.pi - thetas[i]),-radius*mt.sin(mt.pi - thetas[i]),0)    
    v2_b = r.TVector3(radius * mt.cos(mt.pi - thetas[i]),-radius*mt.sin(mt.pi - thetas[i]),0)  
    
    v1_a.RotateZ(-alphas[i])
    v1_b.RotateZ(-betas[i])
    v2_a.RotateZ(-alphas[i])
    v2_b.RotateZ(-betas[i])
    
    l1 = r.TLine()
    l2 = r.TLine()       
    
    l1.SetX1(v1_a.X())
    l1.SetY1(v1_a.Y())
    l1.SetX2(v2_a.X())
    l1.SetY2(v2_a.Y())
    
    l2.SetX1(v1_b.X())
    l2.SetY1(v1_b.Y())
    l2.SetX2(v2_b.X())
    l2.SetY2(v2_b.Y())   
    
    
    struct = vct(vector1_a = v1_a, vector1_b = v1_b,
                 vector2_a = v2_a, vector2_b = v2_b, line1 = l1, line2 = l2)
    
    struct_array = np.append(struct_array,struct)


for j in range(0,N_meas):
    
    struct_array[j].line1.SetLineWidth(2)
    struct_array[j].line1.SetLineStyle(9)
    struct_array[j].line2.SetLineWidth(2)
    struct_array[j].line2.SetLineStyle(9)    
    
    if(j>4):
        if(j==5):
            struct_array[j].line1.SetLineColor(30)
            struct.struct_array[j].line2.SetLineColor(28)
        
        #else: 
            #if(j==6):
                #struct_array[j].line1.SetLineColor(30)
                #struct_array[j].line2.SetLineColor(28)
        #else:
            #if(j==7):
                #struct_array[j].line1.SetLineColor(46)
                #struct_array[j].line2.SetLineColor(49)
        
    else:
        struct_array[j].line1.SetLineColor(3+2*(j+1))
        struct_array[j].line2.SetLineColor(3+2*(j+1))
        
    struct_array[j].line1.Draw()
    struct_array[j].line2.Draw()

Number = 2*N_meas
Number = str(Number)
c.Draw()
c.Print("/Users/boldrinicoder/lab4/Line_rot_plate/graphs/"+Number+"lines.root","root")
c.Print("/Users/boldrinicoder/lab4/Line_rot_plate/graphs/"+Number+"lines.png","png")
#s = input()
#if(s =='s'):
    #print("Chiuso")




