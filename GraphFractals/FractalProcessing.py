import os
import sys

import numpy as np
import numpy.ma as ma
#import torch

from GraphFractals.Configuration import Configuration
from PIL import Image
from matplotlib import cm

from GraphFractals.FractalGraph import FractalGraph


class FractalProcessing:
    def __init__(self):
        self.conf = Configuration()
        self.G = FractalGraph(self)
        exit()
        self.mandelbrottestcase()

    def getComplexCoordinates(self):
        coordinatetensor = np.ones([self.conf.resolution[0], self.conf.resolution[1]], dtype=self.conf.dtype)
        rangereal = np.linspace(self.conf.limitreal[0], self.conf.limitreal[1], self.conf.resolution[0])
        coordinatetensor = coordinatetensor * rangereal
        rangeimag = np.linspace(self.conf.limitimag[0], self.conf.limitimag[1], self.conf.resolution[1])
        imagtemptensor = np.ones_like(coordinatetensor) * np.reshape(rangeimag, (1, rangeimag.shape[0])).T * 1j
        # print(imagtemptensor)
        coordinatetensor = coordinatetensor + imagtemptensor
        return ma.array(coordinatetensor,mask=np.zeros_like(coordinatetensor))
    def mandelbrottestcase(self):
        coordinatetensor = self.getComplexCoordinates()

        #print(imagtemptensor)
        #print(rangeimag)
        #print(coordinatetensor)
        flattenedcoordinatetensor = coordinatetensor.flatten()
        #print(flattenedcoordinatetensor)
        fractalresult = np.zeros((flattenedcoordinatetensor.shape[0]),dtype=np.int16)-1
        fractal = flattenedcoordinatetensor.copy()
        hasdropped = np.ones((flattenedcoordinatetensor.shape[0]),dtype=np.bool_)
        countnewdrop = 0
        for i in range(self.conf.maxiter):
            print("i",i)
            fractal = fractal * fractal + flattenedcoordinatetensor
            dropout = fractal.imag * fractal.imag + fractal.real * fractal.real > 4

            #newdrop = not(dropout == hasdropped)
            newdrop = np.all([dropout,hasdropped],axis=0)
            fractal[newdrop] = np.nan
            fractalresult[newdrop] = i
            hasdropped = dropout
            #print("dropout",dropout, np.sum(dropout))
            #print("newdrop",np.sum(newdrop))
            countnewdrop += np.sum(newdrop)
            #print("fractal",fractal)
            #print("hasdropped",np.sum(hasdropped))

            #print("_____")
        #np.set_printoptions(threshold=sys.maxsize)
        print("fractalresult",fractalresult)
        print("countnewdrop", countnewdrop)
        self.drawfractal(fractalresult.reshape(self.conf.resolution))
    def drawfractal(self,nparray):
        nparray = nparray / np.max(nparray)
        im = Image.fromarray(np.uint8(cm.binary(nparray) * 255))
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imagefilepath = dir_path + "/fractal.png"
        im.save(imagefilepath)
        os.system('viewnior '+ imagefilepath)
fractalprocessing = FractalProcessing()