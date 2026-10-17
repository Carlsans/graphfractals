import os

import numpy as np


class Configuration:
    def __init__(self):
        istesting = False
        self.resolution = (512, 512)
        #self.resolution = (2682, 2595)
        #if istesting:
        #    self.resolution = (512, 512)
        self.limitreal = [-2,2]
        self.limitimag = [-2,2]
        self.dtype = np.complex128
        self.maxiter = 256
        if istesting:
            self.maxiter = 50
        self.drawgraph = True
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        ### Evo formula
        self.lowresfractalresolution = (64, 64)
        self.evoiterationsmax = 200 #2000

        self.minimumfractalentropystart = 0.13
        #if istesting:
        #    self.minimumfractalentropystart = .2
        self.maximumfractalentropystop = 0.2
        self.entropyraise = 0.01