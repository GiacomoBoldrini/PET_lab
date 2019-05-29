import ROOT as r
import math as mt
import numpy as np

class vector():      

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

