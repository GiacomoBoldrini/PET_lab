import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob

class ROOT_obj:
    
    #given cartesian positions, style and color, it creates a marker to be plot anywhere in a canvas.
    def Marker(x,y,style,color):
        marker = r.TMarker(x, y, style)
        marker.SetMarkerStyle(style)
        marker.SetMarkerColor(color)
        return marker
    #given a histogram "h", a bin number "bins" and the color, it colours the bin
    def Paint_bin(h, bins, color):
        b = r.TBox(h.GetBinLowEdge(bins),
                   h.GetMinimum(),
                   h.GetBinWidth(bins)+h.GetBinLowEdge(bins),
                   h.GetBinContent(bins))
        b.SetFillColor(color)
                   
        return b
                   
    #creates canvas pads
    def Create_Canvas(length, height):
        c = r.TCanvas("c","c", 50,50,length,height)
        
        return c
    
    #creates a canvas and a pad attached down below
    def Create_Canvas_Pads():
        c1 = r.TCanvas("c1", "c1", 50,50, 1050,900)
        pad1 = r.TPad("pad1", "pad1", 0, 0, 1, 1)
        #pad1.SetBottomMargin(0)  # joins upper and lower plot
        pad1.SetGridx()
        pad2 = r.TPad("pad2", "pad2", 0, 0, 1, 1)
        pad2.SetFillStyle(4000)
        pad2.SetFrameFillStyle(4000)
        #pad2.SetBottomMargin(0)  # joins upper and lower plot
        pad2.SetGridx()
        
        return c1, pad1, pad2
    
#given number of point "index" x and y coordinates, the style and color( ex:21, 4) and labels
    def TGraph_obj(index, x, y, style, color, xlabel, ylabel, title):
        x = array('f', x)
        y = array('f', y)
        g = r.TGraph(index, x, y)
        g.SetMarkerStyle(style)
        g.SetMarkerColor(color)
        g.SetLineColor(color)
        g.GetXaxis().SetTitle(xlabel)
        g.GetYaxis().SetTitle(ylabel)
        g.SetTitle(title)
        
        return g
    
    #given #points, x,y,error on x and y, style, color and axis label it returns a TGraphErrors
    def TGraph_err_obj(index, x, y, x_err, y_err, style, color, xlabel, ylabel, title):
        x = array('f', x)
        y = array('f', y)
        x_err = array('f', x_err)
        y_err = array('f', y_err)
        g = r.TGraphErrors(index,x,y, x_err, y_err)
        g.SetMarkerStyle(style)
        g.SetMarkerColor(color)
        g.SetLineColor(color)
        g.GetXaxis().SetTitle(xlabel)
        g.GetYaxis().SetTitle(ylabel)
        g.SetTitle(title)
        return g 

    #given a list of values of bins, color, style and width it creates an histo
    #adding any other parameter when calling (*args) it filles the histo in a determined section given by args[0] = inf and args[1]=sup
    def TH1F_obj(values, color, style, width, *args):
        bins = len(values)
        h = r.TH1F("h", "h", bins, 0, bins)
        h.SetFillColor(color)
        h.SetFillStyle(style)
        h.SetLineWidth(width)
        for i in values:
            h.Fill(i)
        
        if args:
            h1 = r.TH1F("h1", "h1", bins, args[0], args[1])
            h1.SetFillColor(color)
            h1.SetFillStyle(style)
            h1.SetLineWidth(width)
            i = inf
            z = 0
            while i < sup:
                h1.SetBinContent(z,value[i])
                i += 1
                z += 1

            if args:
                return h1
            else:
                return h

#returns a fully customizable root TF1 function for fitting
    def Linear_fit(**kwargs):
        fit = r.TF1("fit", "x[0]*[0]+[1]")
        fit.SetParName(0, "slope")
        fit.SetParName(1, "intercept")
        if kwargs:
            for key, value in kwargs.items():
                if key == "inf":
                    inf = value
                if key == "sup":
                    sup = value
                if key == "param":
                    param = value
                if key == "color":
                    color = value
                if key == "width":
                    width = value

            try:
                fit1 = r.TF1("fit1", "[0]*x[0] + [1]", inf, sup)
            except NameError:
                print("inf and sup not defined, returning fit on general interval")
                return fit
            
            else:
                try:
                    param
                except NameError:
                    pass
                else:
                    i = 0
                    while i < len(param):
                        fit1.SetParameter(i, param[i])
                        i += 1
                try:
                    width
                except NameError:
                    pass
                else:
                    fit1.SetLineWidth(width)
                
                try:
                    color
                except NameError:
                    pass
                else:
                    fit1.SetLineColor(color)
    
                return fit1
            
            
        else:
            return fit
    
#returns a fully custoimizable root TF1 gaussian and exp back function for fitting
    def gaussian_back_fit(**kwargs):
        fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]")
        if kwargs:
            for key, value in kwargs.items():
                if key == "inf":
                    inf = value
                if key == "sup":
                    sup = value
                if key == "param":
                    param = value
                if key == "color":
                    color = value
                if key == "width":
                    width = value

            try:
                fit1 = r.TF1("fit1", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]", inf, sup)
            except NameError:
                print("inf and sup not defined, returning fit on general interval")
                return fit
                            
            else:
                try:
                    param
                except NameError:
                    pass
                else:
                    i = 0
                    while i < len(param):
                        fit1.SetParameter(i, param[i])
                        print("sono qui")
                        i += 1
                try:
                    width
                except NameError:
                    pass
                else:
                    fit1.SetLineWidth(width)
                                                                                        
                try:
                    color
                except NameError:
                    pass
                else:
                    fit1.SetLineColor(color)
                                                                                                                
                return fit1
                                                                                                                    
                                                                                                                    
        else:
            return fit

#returns a fully custoimizable root TF1 double gaussian for fitting
    def double_gaussian_back_fit(**kwargs):
        fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-((x[0]-[4])^2)/[5]^2)")
        if kwargs:
            for key, value in kwargs.items():
                if key == "inf":
                    inf = value
                if key == "sup":
                    sup = value
                if key == "param":
                    param = value
                if key == "color":
                    color = value
                if key == "width":
                    width = value
                    
                try:
                    fit1 = r.TF1("fit1", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-((x[0]-[4])^2)/[5]^2)", inf, sup)
                except NameError:
                    print("inf and sup not defined, returning fit on general interval")
                    return fit

                else:
                    try:
                        param
                    except NameError:
                        pass
                    else:
                        i = 0
                        while i < len(param):
                            fit1.SetParameter(i, param[i])
                            i += 1
                    try:
                        width
                    except NameError:
                        pass
                    else:
                        fit1.SetLineWidth(width)
                        
                    try:
                        color
                    except NameError:
                        pass
                    else:
                        fit1.SetLineColor(color)
            
                    return fit1
                
                
        else:
            return fit

