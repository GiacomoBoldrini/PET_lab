import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob
r.gROOT.SetBatch(True)

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

#reads velocities txt
    def Load_reading(userpath):
        filepath = userpath
        steps = []
        degrees = []
        with open(filepath) as fp:
            line = fp.readline()
            h = line.split(",")
            while line:
                steps.append(int(h[0]))
                degrees.append(float(h[1].strip("\n")))
                line = fp.readline()
                h = line.split(",")
        #this returns two colums lists of integers
        return steps, degrees


#draws the plot with title & co.
    def Graph_Plotter(index, x, y, title, xlabel, ylabel, output, *args):
            #define the graph
        g = r.TGraph(index, x, y)
        #g.SetTitle("Peak Shift over Temperature")
        g.SetTitle(title)
        g.SetMarkerStyle(21)
        g.SetMarkerColor(4)
        g.SetLineColor(4)
        #g.GetXaxis().SetTitle("Temperature [C]")
        g.GetXaxis().SetTitle(xlabel)
        #g.GetYaxis().SetTitle("Max Channel")
        g.GetYaxis().SetTitle(ylabel)
        if args:
            #marker = r.TMarker(args[0], args[1], args[2])
            #marker.SetMarkerStyle(21)
            #marker.SetMarkerColor(2)
            g.GetXaxis().SetLimits(args[0], args[1])
            line = r.TLine(args[0],args[2],args[1], args[2])
            line.SetLineColor(r.kRed)
        
        #define the canvas and plot
        c2 = r.TCanvas("c2", "c2",50,50,1000,800)
        c2.SetGridx()
        c2.SetGridy()
        g.Draw("AP")
        if args:
            #marker.Draw()
            line.Draw()
        c2.Draw()
        c2.Show()
        #c2.SaveAs("/Users/boldrinicoder/lab4/prova.pdf", "pdf")
        c2.SaveAs(output, "pdf")
            
            
#draws the plots of rate and resolution in the same canvas
    def Rate_Res_Plotter(n_measures, voltages, res, err_res, rates, err_rates, outpath):
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
            #score.append(rates[i] - res[i])
            #err_score.append(err_res[i] + err_rates[i])
            i += 1
        score = array('f', score)
        err_score = array('f', err_score)
        
        #c1, pad1, pad2 = ClassFunc.Create_Canvas_Pads()
        c1 = r.TCanvas("c1", "c1", 50,50, 1000,800)
        pad1 = r.TPad("pad1", "pad1", 0, 0, 1, 1)
        pad1.SetGridx()
        pad2 = r.TPad("pad2", "pad2", 0, 0, 1, 1)
        pad2.SetFillStyle(4000)
        pad2.SetFrameFillStyle(4000)
        pad2.SetGridx()
        
        
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
        #graph_score = r.TGraphErrors(n_measures,x,score, x_err, err_score)

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
        c1.SaveAs(outpath + "/Rate_Res.pdf", "pdf")
        c1.SaveAs(outpath + "/Rate_Res.root", "root")


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
    def Fitter(measure, file, inf, sup, mean, par):
            #here I open the file (set data and measure) and I fill an array
        f =  open(file, "r")
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
        c2.SaveAs("/Users/boldrinicoder/lab4/{}.pdf".format(measure), "pdf")
        
    #CHOICE: RETURN THE RATE OR XMAX
    #1      returns Rate and Res with their errors
        rate = ClassFunc.Rate(fit, inf_rate, sup_rate, n)
        print("RATE: {}".format(rate))
        Res = ClassFunc.Resolution(fit)
        Xmax = fit.GetMaximumX()
        print('La media è:', fit.GetParameter(1))
        print("Ascissa per il massimo: {}".format(Xmax))
        if par == 0:
            return rate, Res
        if par == 1:
            return Xmax
        if par == 2:
            return rate
            
            
    
#creates a TGraphErrors with given input data and fit them linearly
    def Linear_Plotter(n,x,y,errx, erry, path_name, x_name, y_name, title_name):
        x = array('f', x)
        y = array('f', y)
        errx = array('f', errx)
        erry = array('f', erry)
        gr = r.TGraphErrors(n,x,y,errx, erry)
        gr.SetMarkerStyle(21)
        gr.SetLineColor(2)
        gr.SetMarkerColor(2)
        bottom = min(x)
        top = max(x)
        fit = r.TF1("fit", "x[0]*[0]+[1]",bottom,top, '--')
        fit.SetParameters(100,0)
        fit.SetLineColor(r.kBlue)
        fit.SetParName(0,"Slope")
        fit.SetParName(1,"Intercept")
        c = r.TCanvas("c", "c", 50,50, 1000, 800)
        gr.Draw("AP")
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
        return fit.GetParameter(0), fit.GetParameter(1)
        

    def Normalized_Linear_Plotter(n,x,y,errx, path_name, x_name, y_name, title_name, slope, intercept):
        x = array('f', x)
        alpha_measured = array('f', y)
        alpha_exp = array('f')
        alpha_norm = array('f')
        for i in range(0, len(x)):
            alpha_exp.append(x[i]*slope + intercept)
            alpha_norm.append((alpha_measured[i]-alpha_exp[i])/alpha_exp[i])
            
#Now I will find errors for expected, measured and normalized angles
        err_alpha_measured = 2.5
        err_alpha_exp =0;
        for j in range(0, len(x)):
            err_alpha_exp += intercept+slope*x[i]-alpha_measured[i]  
        err_alpha_exp = err_alpha_exp/(len(alpha_measured)-2)    
        
        print(err_alpha_exp)
        
        err_alpha_norm = array('f')
        for i in range(0, len(x)):
            err_alpha_norm.append(math.sqrt((err_alpha_measured/alpha_exp[i])*(err_alpha_measured/alpha_exp[i]) + ((alpha_measured[i] - alpha_exp[i])/(alpha_exp[i]*alpha_exp[i])*err_alpha_exp)*((alpha_measured[i] - alpha_exp[i])/(alpha_exp[i]*alpha_exp[i])*err_alpha_exp)))
        errx = array('f', errx)
        
#I set to zero the entry [0]
        alpha_norm[0]=0 
        err_alpha_norm[0]=0
        
        gr = r.TGraphErrors(n,x,alpha_norm,errx, err_alpha_norm)
        
        gr.SetMarkerStyle(21)
        gr.SetLineColor(2)
        gr.SetMarkerColor(2)
        bottom = min(x)
        top = max(x)
        fit = r.TF1("fit", "[0]",bottom,top, '--')
        fit.SetLineColor(r.kBlue)
        fit.SetParName(0,"Parameter")
        c = r.TCanvas("c", "c", 50,50, 1000, 800)
        gr.Draw("AP")
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

    def Paint_bin(h, bins, color):
        b = r.TBox(h.GetBinLowEdge(bins),
                   h.GetMinimum(),
                   h.GetBinWidth(bins)+h.GetBinLowEdge(bins),
                   h.GetBinContent(bins))
        b.SetFillColor(color)
        return b


    
    #computes the Rate in Sybchro mode
    def Rate_Synchro(function, a,b, n, live_time):
        #function.SetParameter(3,0)
        #function.SetParameter(4,0)
        #function.SetParameter(5,0)
        Integral = function.Integral(a,b)
#        Err_Integral = function.IntegralError(a,b,n.GetParams())
        Err_Integral = function.IntegralError(a,b)
        print("RATEO:")
        print("INF: {}".format(a))
        print("SUP: {}".format(b))
        print("Integal: {}".format(Integral))
        print("Err_Integral: {}".format(Err_Integral))
        rate = Integral/live_time
        err_live_time = 1/(math.sqrt(12))
        err_integral = math.sqrt(Integral)
        err_rate = math.sqrt((err_integral/live_time)**2 + ((Integral/(live_time)**2)*err_live_time)**2)
        print("Err_Rate_Poiss {}".format(err_rate))
        return rate, err_rate
        #return [Integral/live_time, Err_Integral/live_time]

    
    
    def Fitter_Synchro(measure, file, inf, sup, mean, output, disc):
        #here I open the file (set data and measure) and I fill an array
        f =  open(file, "r")
        list = f.readlines()
        
        first_lines = 12
        #last_lines = -16
        last_lines = -18
            
        arr = np.array([])
            
        for i in list:
            arr = np.append(arr,i.strip())
        if disc == 1:
            live_time = int(arr[9][0:3])
        else:
            live_time = 200


        value0 = arr[first_lines:last_lines]
        value0 = value0.astype(int)
        value = []
        for i in value0:
            value.append(i)
        #fit and draw the spectrum
        bins = sup-inf
        #peak = value.index(max(value[i]))
        gauss_peak = max(value[inf:sup])
        h2 = r.TH1F("h2", "h2", bins, inf, sup)
        h2.SetFillColor(r.kBlue)
        h2.SetFillStyle(3003)
        h2.SetLineWidth(2)
        i = inf
        z = 0
        fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]",inf,sup)
        fit.SetParameters(gauss_peak,mean,18,0.1,0)
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
        c2.SaveAs(output + "/{}.pdf".format(measure), "pdf")
        
        rate , err_rate = ClassFunc.Rate_Synchro(fit, inf_rate, sup_rate, n, live_time)
        print("RATE: {}".format(rate))
        Res = ClassFunc.Resolution(fit)
        Xmax = fit.GetMaximumX()
        print('La media è:', fit.GetParameter(1))
        print("Ascissa per il massimo: {}".format(Xmax))

        return rate, err_rate, Res
