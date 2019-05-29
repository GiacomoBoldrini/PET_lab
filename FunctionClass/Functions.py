import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob
r.gROOT.SetBatch(True)

class ClassFunc:
    """
    Function class with useful functions used during the Particle Laboratory 4th year
    University of Milano Bicocca.
    Authors:
        - Giacomo Boldrini
        - Stefano Ghislandi
        - Bianca Pinolini
        - Wahid Redjeb
    """
    
    def mkdir_p(mypath):
        """
            Creates a folder given the path "mypath" If the folder already exists it does nothing
            otherwise it raises an error (example if the path does not exists).
        """
        from errno import EEXIST
        from os import makedirs,path
        try:
            makedirs(mypath)
        except OSError as exc: 
            if exc.errno == EEXIST and path.isdir(mypath):
                pass
            else: raise

    def Create_Canvas_Pads():
        """
            Creates a ROOT canvas and two pads.
        """
        c1 = r.TCanvas("c1", "c1", 50,50, 1050,900)
        pad1 = r.TPad("pad1", "pad1", 0, 0, 1, 1)
        pad1.SetGridx()
        pad2 = r.TPad("pad2", "pad2", 0, 0, 1, 1)
        pad2.SetFillStyle(4000)
        pad2.SetFrameFillStyle(4000)
        pad2.SetGridx()

        return c1, pad1, pad2

    def Temp_reading(filepath):
        temp = []
        with open(filepath) as fp:
            line = fp.readline()
            h = line.split(",")
            while line:
                temp.append(h[2])
                line = fp.readline()
                h = line.split(",")
        #this returns a column vector of temperatures
        return temp

    def Load_reading(userpath):
        """
            Function called when reading the load.txt file for the rotating plate load
            Input: userpath, path to the file
            Output: temp, the vector with all the loads
        """
        
        filepath = userpath
        temp = []
        with open(filepath) as fp:
            line = fp.readline()
            #splitting strings in order to get data
            h = line.split(",")
            sum = 0
            while line:
                #summing all loads except last
                media = sum(i for i in h[1:len(h)-1])
                temp.append(h[2])
                #cycling over all lines and do the same
                line = fp.readline()
                h = line.split(",")
        #this returns a column vector of loads
        return temp

    def vel_reading(userpath):
        """
            Function that reads the velocity of the rotating plate.
            Input: userpath, path to the .txt file
            Output: steps, degrees, lists of the steps of the rotating plate and corresponding degree angle
        """
        
        filepath = userpath
        steps = []
        degrees = []
        with open(filepath) as fp:
            line = fp.readline()
            h = line.split(",")
            while line:
                #integer conversion of the step value and float conversion of degree one,
                #stripping endline character.
                steps.append(int(h[0]))
                degrees.append(float(h[1].strip("\n")))
                line = fp.readline()
                h = line.split(",")
        #this returns two lists of steps and angles
        return steps, degrees


#draws the plot with title & co.
    def Graph_Plotter(index, x, y, title, xlabel, ylabel, output, *args):
        """
            Useful function to plot ROOT TGraphs directly.
            Input: index, the length of the vectors
                   x,y, the variables to be fed into the TGraph
                   title, a string with tile of the TGraph
                   xlabel, string with x axis label
                   ylabel, string with y axis label
                   output, string with the output path to save the canvas
                   *args, optional arguments
        """
        
        #define the graph and styles
        g = r.TGraph(index, x, y)
        g.SetTitle(title)
        g.SetMarkerStyle(21)
        g.SetMarkerColor(4)
        g.SetLineColor(4)
        g.GetXaxis().SetTitle(xlabel)
        g.GetYaxis().SetTitle(ylabel)
        #eventual arguments
        if args:
            
            g.GetXaxis().SetLimits(args[0], args[1])
            line = r.TLine(args[0],args[2],args[1], args[2])
            line.SetLineColor(r.kRed)
        
        #define the canvas and plot
        c2 = r.TCanvas("c2", "c2",50,50,1000,800)
        c2.SetGridx()
        c2.SetGridy()
        g.Draw("AP")
        if args:
            line.Draw()
        c2.Draw()
        c2.Show()
        c2.SaveAs(output, "pdf")
            
            
#draws the plots of rate and resolution in the same canvas
    def Rate_Res_Plotter(n_measures, voltages, res, err_res, rates, err_rates, outpath, xlabel = "Voltage [V]", yright_label = "Resolution", yleft_label = "Live Rate [Counts/sec]"):
        """
            Function used to plot TGraphErrors with two different y axis on a same canvas.
            Originally used for comparision of Rate and Resolution in the process of selecting
            the best voltage bias for the scintillators.
            Input: n_measures, number of measures to be plotted
                   voltages, list of x axis measures
                   res, list of first y variables measured
                   err_res, list of errors on the first y input variable
                   rates, list of second y variables measured
                   err_rates, list of errors on the second y variable
                   outpath, path where canvas has to be saved
        """
        
        print("n_measures: {}".format(n_measures))
        print("voltages: {}".format(voltages))
        print("res: {}".format(res))
        print("err_res: {}".format(err_res))
        print("rates: {}".format(rates))
        print("err_rates: {}".format(err_rates))
        #defining input lists as float arrays to be fed into ROOT TObjects
        x = array('f', voltages)
        x_err = array('f', [0]*n_measures)
        y1 = array('f', res)
        y1_err = array('f', err_res)
        y2 = array('f', rates)
        y2_err = array('f', err_rates)
        
        #canvas creation
        c1 = r.TCanvas("c1", "c1", 50,50, 1000,800)
        pad1 = r.TPad("pad1", "pad1", 0, 0, 1, 1)
        pad2 = r.TPad("pad2", "pad2", 0, 0, 1, 1)
        #setting second pad to transparent in order to visualize both data
        pad2.SetFillStyle(4000)
        pad2.SetFrameFillStyle(4000)
        
        #creating TGraphErrors and their styles
        graph_res = r.TGraphErrors(n_measures,x,y1, x_err, y1_err)
        graph_res.SetTitle("")
        #graph_res.SetMarkerStyle(21)
        #for temperature
        graph_res.SetMarkerStyle(21)
        graph_res.SetMarkerSize(1)
        #----------------------
        graph_res.SetLineColor(2)
        #for temperature
        graph_res.SetLineWidth(1)
        #----------------------
        graph_res.SetMarkerColor(2)
        graph_rates = r.TGraphErrors(n_measures,x,y2, x_err, y2_err)
        graph_rates.SetTitle("")
        graph_rates.SetMarkerStyle(21)
        graph_rates.SetMarkerColor(4)
        #for temperature
        graph_rates.SetMarkerSize(1)
        #---------------
        graph_rates.SetLineColor(4)

        pad1.Draw()
        pad1.cd()
        #Drawing dirst TGraphErrors on first pad with specified axis "L", left. "AP" draws
        #axis and points.
        graph_rates.Draw("APL")
        #graph_rates.GetXaxis().SetTitle("Shaping Time [#mus]")
        graph_rates.GetXaxis().SetTitle(xlabel)
        graph_rates.GetXaxis().SetTitleSize(0.04)
        #graph_rates.GetXaxis().SetTitle("Voltage [V]")
        
        #retrieving histo from the TGraph and its associated axis in order to change its color
        #colors are the same fior TGraph Points and their axis
        histo = graph_rates.GetHistogram()
        axis = histo.GetYaxis()
        axis.SetAxisColor(4)
        axis.SetLabelColor(4)
        axis.SetTitle(yleft_label)
        axis.SetTitleSize(0.04)
        axis.SetTitleColor(4)
        axis.SetTitleOffset(1.2)
        #setting equal range in y axis
        #axis.SetRangeUser(550,850)
        pad1.Update()

        pad2.Draw()
        pad2.cd()
        #Drawing second TGraphErrors in the second, transparent pad, with the Option "APLY+" mening it will select the Right
        #Y axis (Y+). Same as before we retireve histogram and following axis in order to change its color.
        graph_res.Draw("APLY+ sames")
        histo = graph_res.GetHistogram()
        axis = histo.GetYaxis()
        axis.SetAxisColor(2)
        axis.SetLabelColor(2)
        axis.SetTitleSize(0.04)
        #axis.SetTitle("Resolution")
        axis.SetTitle(yright_label)
        axis.SetTitleSize(0.04)
        axis.SetTitleColor(2)
        axis.SetTitleOffset(1.2)
        #axis.SetRangeUser(8.17, 8.5)
        pad2.Update()
        
        #drawing canvas and saving
        c1.Draw()
        c1.SaveAs(outpath)


#computes the percentage resolution as FWHM/mean*100
    def Resolution(function):
        """
            Function that computes the percentage resolution as FWHM/mean*100.
            Input: funciton, a TF1 object, in particular we had our gaussian+exponential background
            Output: FWHM/mean*100 and its relative error, computed with errors propagation
        """
        
        #cancel the exponential background
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
        """
            Function that computes the rate fro a given spectra.
            Input: function, the TF1 object obtained by a fitting of the spectra. In particular we had
                            the combination of a gaussian+exponential background
                    a,b, Inferior and Superior range Int where the integral has to be performed on.
                    n, number of parameters
            Output: Integral/real_time and its error/real_time
        """
        
        #subtracting background
        function.SetParameter(3,0)
        function.SetParameter(4,0)
        function.SetParameter(5,0)
        #retireve integral from TF1 object
        Integral = function.Integral(a,b)
        #retireve integral error from TF1 object
        Err_Integral = math.sqrt(integral)
        #printing info
        print("RATEO:")
        print("INF: {}".format(a))
        print("SUP: {}".format(b))
        print("Integal: {}".format(Integral))
        print("Err_Integral: {}".format(Err_Integral))
        return [Integral/200, Err_Integral/200]


    def Fitter(measure, file, inf, sup, mean, par):
        """
            Function that fits the spectra and returns Rate and Res OR returns XMax.
            Input: measure, measure number useful when plotting
                   file, the .txt file with the spectrum
                   inf, sup, values where the spectra is splitted to retrieve only the region of interest
                             with the 511kev peak.
                   mean, supposed peak channel as a parameter to be passed to the ROOT fit
                   par, Parameter to select the output, if par ==0 return channel maximum
                        if par == 1 it returns the Resolution and its error for the given spectra,
                        if par == 2 it only returns the rate.
            Output: channel maximum or Resolution+error or rate
        """
        
        #opening file and filling a numpy array with spectra bin values
        f =  open(file, "r")
        list = f.readlines()

        #deleting last 16 and first 12 rows of the .txt files. Theese doi not contain
        #the values but only other interest information such as live_time, real_time and others.
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
        #bins are defined as integer subtraction of delimeters of the region.
        #one bin is equal to one channel of the MCA.
        bins = sup-inf
        peak = value.index(max(value))
        #defining the histogram with delimeters and bins. Styles are applied.
        h2 = r.TH1F("h2", "h2", bins, inf, sup)
        h2.SetFillColor(r.kBlue)
        h2.SetFillStyle(3003)
        h2.SetLineWidth(2)
        i = inf
        z = 0
        #fitting function is defined as a TF1 object with a combination of a gaussian and an exponential background
        # the fit range is set by the inf and sup variables.
        fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]",inf,sup)
        #setting initial parameters for the fit method.
        fit.SetParameters(2200,mean,18,0.1,0,100)
        fit.SetLineWidth(3)
        #Filling the histogram one bin at a time.
        while i < sup:
            h2.SetBinContent(z,value[i])
            i += 1 
            z += 1
        integral = 0
        

        #Drawing and saving histograms. The measure value is inserted into the file_name.
        #This gives us the possibility to check the fit expecially when this function has
        #to be called many times.
        c2 = r.TCanvas("c2", "c2",50,50,1000,800)
        n = h2.Fit("fit", "RLS")
        h2.Draw("histo same")
        r.gStyle.SetOptStat(1111)
        r.gStyle.SetOptFit(1111)
        c2.Draw() 
        c2.Show()
        c2.SaveAs("/Users/boldrinicoder/lab4/{}.pdf".format(measure), "pdf")

        #selecting range for the rate computation. We onnly consider the gaussian, subtracting the exponential.
        #The region is selected as the region between 3 std deviation from the maximum channel obtained from the fit.
        inf_rate=fit.GetParameter(1)-3*fit.GetParameter(2)
        sup_rate=fit.GetParameter(1)+3*fit.GetParameter(2)
        #CHOICE: RETURN THE RATE OR XMAX
        #0      returns Xmax
        #1      returns Rate and Res with their errors
        #2      returns rate
        #calling the rate function
        rate = ClassFunc.Rate(fit, inf_rate, sup_rate, n)
        print("RATE: {}".format(rate))
        #calling the resolution function.
        Res = ClassFunc.Resolution(fit)
        #retireve maximum from the fit
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
        """
            Plotting Linear regressions.
            Input: n, number of points.
                   x,y, lists of dependent and independent variable
                   errx, erry, lists of associated errors
                   path_name, path for the file to be saved on.
                   x_name, x axis label
                   y_name, y axis label
                   title_name, title of the plot.
            Output: Slope, Intercept, parameters of the straight line
        """
        
        #filling float arrays to be fed into TGraphsErrors
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
        #defining fitting function as a straight line
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
        #saving canvas
        c.SaveAs(path_name + ".pdf", "pdf")
        return fit.GetParameter(0), fit.GetParameter(1)
        

    def Normalized_Linear_Plotter(n,x,y,errx, path_name, x_name, y_name, title_name, slope, intercept):
        """
            Normalized linear plots with linear fit.
            Input: n, number of points.
                   x,y, lists of dependent and independent variable
                   errx, erry, lists of associated errors
                   path_name, path for the file to be saved on.
                   x_name, x axis label
                   y_name, y axis label
                   title_name, title of the plot.
                   slope, intercept: parameters to start fit
                   
        """
        x = array('f', x)
        alpha_measured = array('f', y)
        alpha_exp = array('f')
        alpha_norm = array('f')
        for i in range(0, len(x)):
            alpha_exp.append(x[i]*slope + intercept)
            alpha_norm.append((alpha_measured[i]-alpha_exp[i])/alpha_exp[i])
            
        #Now we find errors for expected, measured and normalized angles
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
        
        #generating tgrapherrors with the vectors computed
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
        """
            Painting a bin of an histo.
            Inputs: h, a TH1F object.
                    bins, the bins to be colored.
                    color, selected color
            Output: a TBox object with the same dimensions of
                    the bins. This can be drawn onto the same canvas
                    of the histogram.
        """
        b = r.TBox(h.GetBinLowEdge(bins),
                   h.GetMinimum(),
                   h.GetBinWidth(bins)+h.GetBinLowEdge(bins),
                   h.GetBinContent(bins))
        b.SetFillColor(color)
        return b



    def Rate_Synchro(function, a,b, n, live_time):
        
        """
           Computes the Rate in Synchro mode.
           Inputs: function, a TF1 object for the rate.
                   a,b, inferior and superior range
                   n, number of parameters.
                   live_time, value of the live time.
                   Outputs: rate, err_rate
        """

        Integral = function.Integral(a,b)

        Err_Integral = function.IntegralError(a,b)
        print("INF: {}".format(a))
        print("SUP: {}".format(b))
        #computing rate as the integral of the gaussian divided by the measure time
        rate = Integral/live_time
        #computing the error on the live_time as 1/sqrt(12) for a constant distribution
        err_live_time = 1/(math.sqrt(12))
        #the error on the integral is computed supposing a poissonian distribution
        err_integral = math.sqrt(Integral)
        #the rate error is obtained through an error propagation.
        
        #err_rate = math.sqrt((err_integral/live_time)**2 + ((Integral/(live_time)**2)*err_live_time)**2)
        err_rate = err_integral/200
        return rate, err_rate

    
    def Fitter_Synchro(measure, file, inf, sup, mean, output, disc, xmax = False):
        """
            Function used for fitting spectra and retrieving information while in Synchro mode between TMCL and Maestro.
            Inputs: measure, index of the measure
                    file, path to the file to be analysed
                    inf, sup, range of the region of the peak to be fitted
                    mean, supposed channel of the maximum of the peak
                    output, output path where the canvas has to be saved
                    disc, a parameter variable, if disc ==1 the live_time is
                          retireved from the file. Else the live_time is set to 200.
                          
            Outputs: rate, err_rate, Res
        """
        #opening file and reading all lines
        f =  open(file, "r")
        list = f.readlines()
        
        #deleting first 12 and last 18/16 lines. Theese lines only contain general information about
        #the spectra and not useful values for the histogram filling.
        first_lines = 12
        #last_lines = -16
        last_lines = -18
            
        arr = np.array([])
        
        #filling the array with bins contents
        for i in list:
            arr = np.append(arr,i.strip())
        
        #selecting the live_time by default = 200 or drom the txt
        if disc == 1:
            live_time = int(arr[9][0:3])
            #print('if', live_time)
        else:
            live_time = 200
            #print(' else', live_time)


        value0 = arr[first_lines:last_lines]
        value0 = value0.astype(int)
        value = []
        for i in value0:
            value.append(i)

        #bins are defined as integer subtraction of delimeters of the region.
        #one bin is equal to one channel of the MCA.
        bins = sup-inf
        #the peak channel is the bean with maximum value of entries.
        gauss_peak = max(value[inf:sup])
        #creating and filling the histogram
        h2 = r.TH1F("h2", "h2", bins, inf, sup)
        h2.SetFillColor(r.kBlue)
        h2.SetFillStyle(3003)
        h2.SetLineWidth(2)
        i = inf
        z = 0
        # defining the fit function as a combination of a gaussian + exponential background.
        #Delimeters are set on the fit function.
        fit = r.TF1("fit", "[0]*exp(-((x[0]-[1])^2)/[2]^2)+[3]*exp(-[4]*x[0])+[5]",inf,sup)
        fit.SetParameters(gauss_peak,mean,29,0.1,0)
        fit.SetLineWidth(3)
        #Filling the histogram bin by bin.
        while i < sup:
            h2.SetBinContent(z,value[i])
            i += 1
            z += 1
        integral = 0

        c2 = r.TCanvas("c2", "c2",50,50,1000,800)
        n = h2.Fit("fit", "RLS")
        h2.Draw("histo same")
        r.gStyle.SetOptStat(1111)
        r.gStyle.SetOptFit(1111)
        c2.Draw()
        c2.Show()
        c2.SaveAs(output + "/{}.pdf".format(measure), "pdf")

        #retrieving inf and sup limits to be fed into Rate function. They are
        #computed as peak channel from fit+-3 std deviation.
        inf_rate=fit.GetParameter(1)-3*abs(fit.GetParameter(2))
        sup_rate=fit.GetParameter(1)+3*abs(fit.GetParameter(2))
        
        rate , err_rate = ClassFunc.Rate_Synchro(fit, inf_rate, sup_rate, n, live_time)
        print(err_rate)
        #Classing resolution function to retrieve resolution
        Res = ClassFunc.Resolution(fit)
        #retrieving fit maximum value
        Xmax = fit.GetMaximumX()
        err_Xmax = fit.GetParameter(2)/math.sqrt(fit.Integral(inf_rate,sup_rate))
        print(err_Xmax)
        print(Xmax)
        print('La media è:', fit.GetParameter(1))
        print('La sigma è:', fit.GetParameter(2))
        
        if not xmax:
            return rate, err_rate, Res, Xmax, err_Xmax
        else:
            return Xmax

