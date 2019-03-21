import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob

class ClassFunc:

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

#creates canvas pads
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


#reads load.txt
    def Load_reading(userpath):
        filepath = userpath
        temp = []
        with open(filepath) as fp:
            line = fp.readline()
            h = line.split(",")
            sum = 0
            while line:
                media = sum(i for i in h[1:len(h)-1])
                temp.append(h[2])
                line = fp.readline()
                h = line.split(",")
        #this returns a column vector of temperatures
        return temp
                
#Reads the TMLC load.txt
    def Load_reading(userpath):
        filepath = userpath
        load_index = []
        vibration_index = []
        velocity = []
        with open(filepath) as fp:
            line = fp.readline()
            h = line.split(",")
            media = 0
            while line:
                load_index.append(float(sum(int(i) for i in h[1:len(h)-1])/10))
                vibration_index.append(float(h[len(h)-1].strip('\n')))
                velocity.append(int(h[0]))
                #temp.append(h[2])
                line = fp.readline()
                h = line.split(",")

        #this returns 3 vectors
        return load_index, vibration_index, velocity


#draws the plot with title & co.
    def Plotter(index, x, maximum, title, xlabel, ylabel, output):
            #define the graph
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

            #define the canvas and plot
        c2 = r.TCanvas("c2", "c2",50,50,1000,800)
        c2.SetGridx()
        c2.SetGridy()
        g.Draw("APL")
        c2.Draw()
        c2.Show()
        #c2.SaveAs("/Users/boldrinicoder/lab4/prova.pdf", "pdf")
        c2.SaveAs(output, "pdf")
            
            
#draws the plots of rate and resolution in the same canvas
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

        """
        pad3.Draw()
        pad3.cd()
        graph_score.Draw("APL")
        """

        c1.Draw()
        c1.SaveAs("/Users/boldrinicoder/lab4/graph.pdf", "pdf")


#computes the percentage resolution as FWHM/mean*100
    def Resolution(function):
            #cancel the background
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

            #determine the left extreme value
        while(1):
            if function.Eval(temp) < maxi/2:
                estremo_sx = temp
                break
            temp -= epsilon
        temp = Xmax

            #determine the right extreme value
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


#computes the Rate
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


#fits the spectra and returns Rate and Res OR returns XMax
    def Fitter(data, measure, inf, sup, mean):
            #here I open the file (set data and measure) and I fill an array
        f =  open("/Users/boldrinicoder/lab4/data/{}/{}{}.txt".format(data,data,measure), "r")
        list = f.readlines()

        first_lines = 12
        last_lines = -16

        arr = np.array([])

        for i in list:
            arr = np.append(arr,i.strip())

        value0 = arr[first_lines:last_lines]
        value0 = value0.astype(int)
        value = []
        for i in value0:
            value.append(i)
        
            #fit and draw the spectrum    
        bins = sup-inf
        peak = value.index(max(value))
        h2 = r.TH1F("h2", "h2", bins, inf, sup)
        h2.SetFillColor(r.kBlue)
        h2.SetFillStyle(3003)
        h2.SetLineWidth(2)
        i = inf
        z = 0
        fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]",inf,sup)
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
        c2.SaveAs("/Users/boldrinicoder/lab4/justtoshow{}.png".format(measure))
        
    #CHOICE: RETURN THE RATE OR XMAX
    #1      returns Rate and Res with their errors
        rate = Rate(fit, inf_rate, sup_rate, n)
        print("RATE: {}".format(rate))
        Res = Resolution(fit)
        print('La media è:', fit.GetParameter(1))
        return rate, Res
    #2      returns the XMax value of the fit
        Xmax = fit.GetMaximumX()
        print("Ascissa per il massimo: {}".format(Xmax))
        return Xmax

    def Linear_Plotter(n,x,y,errx, path_name, x_name, y_name, title_name):
        gr = r.TGraphErrors(n,x,y,errx)
        bottom = min(x)
        top = max(x)
        fit = r.TF1("fit", "x[0]*[0]+[1]",bottom,top, '--')
        fit.SetParameters(100,0)
        fit.SetLineColor(r.kBlue)
        fit.SetParName(0,"Slope")
        fit.SetParName(1,"Intercept")
        c = r.TCanvas("c", "c", 50,50, 1000, 800)
        gr.Draw()
        gr.SetTitle(title_name)
        gr.GetXaxis().SetTitle(x_name)
        gr.GetYaxis().SetTitle(y_name)
        gr.Fit("fit")
        r.gStyle.SetStatX(.9)
        r.gStyle.SetStatY(.4)
        r.gStyle.SetOptFit(1111)
        c.SetGridx()
        c.SetGridy()
        c.SaveAs(path_name + ".pdf", "pdf")

#this colors single bins
    def Paint_bin(h, bins, color):
        b = r.TBox(h.GetBinLowEdge(bins),
                   h.GetMinimum(),
                   h.GetBinWidth(bins)+h.GetBinLowEdge(bins),
                   h.GetBinContent(bins))
        b.SetFillColor(color)
        return b






















