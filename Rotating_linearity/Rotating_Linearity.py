#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:38:42 2018

@author: Jack
"""

"""
This program reads velocity txt and fit linearly measured degrees vs steps counter
"""

import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import math
from array import array
import glob
from Linearfunc import ClassFunc

r.gROOT.SetBatch(True)
#reading the steps and the corresponding degrees from the .txt
steps, degrees = ClassFunc.Load_reading("/Users/boldrinicoder/lab4/Rotating_linearity/velocity_180.txt")
#plot and fit them linearly. Full customizable paths and titles. Errors are set to 2.5 degrees
ClassFunc.Linear_Plotter(len(steps), steps, degrees, np.zeros(len(steps)), [2.5]*(len(steps)), "/Users/boldrinicoder/Desktop/prova", "steps [a.u.]", "Degrees", "Rotating Plate Linearity")
