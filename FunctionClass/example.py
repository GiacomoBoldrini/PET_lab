import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob
import os


"""
Example of how to use ROOT_obj to quickly do fits and create root objects.
"""

import sys
sys.path.insert(0, '/Users/boldrinicoder/lab4/FunctionClass')
from Root_objects import ROOT_obj #you can ad "...import ROOT_obj as rob" so it's quicker
r.gROOT.SetBatch(True)
"""
First simple is a linear fit
"""

path_for_canvas = "/Users/boldrinicoder/Desktop"

#creating the linear fit. No parameter passed
fit = ROOT_obj.Linear_fit()
#it returns an object so we can still customize inside a script
fit.SetLineColor(r.kRed)

#define random linear x and y for example
x =  [1,2,3,4,5,6,7]
y = [1,3,7,7,11,12,14]

#easily creating a root TGraph passin number of points, lists, style and color numbers and labels
g = ROOT_obj.TGraph_obj(len(x), x, y, 22, 4, "x [cm]", "y [quad]", "A linear fit")
#defining a canvas
c = ROOT_obj.Create_Canvas(1000,800)
#fitting
g.Fit(fit)
g.Draw("AP")
c.Draw()
c.SaveAs(path_for_canvas + "/Linear_example.pdf", "pdf")

"""
Second is more advanced and is a fit of a gaussian with an exponential background
"""

#Define a somple function to generate our y examples
def gauss_exp(x):
    par_2 = 20
    par_0 = 100
    par_3 = 50
    par_4 = 0.002
    par_5 = 20
    par_1 = 300
    return par_0*math.exp(-((x-par_1)**2)/par_2**2)+par_3*math.exp(-par_4*x)+par_5

#Generating random points
x = np.arange(1,1000, 1)
y = []
for i in x:
    y.append(gauss_exp(i))

#Creating a fit. Note that we pass the inferior and superior limit for the fit AND some parameters (you can choose whatever you want but they must be in order). You can also define the width of the fit and it's color inside the call
fit = ROOT_obj.gaussian_back_fit(inf = 1, sup = 1000, param = [20,300,20,50])
#Creating again a TGraph
g = ROOT_obj.TGraph_obj(len(x), x, y, 22, 4, "x [cm]", "y [quad]", "A gaussian fit")
#creating a canvas
c = ROOT_obj.Create_Canvas(1000,800)
#fitting and drawing
g.Fit(fit)
g.Draw("AP")
c.Draw()
c.SaveAs(path_for_canvas + "/Gauss_exp_example.pdf", "pdf")

