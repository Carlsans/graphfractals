import numpy as np
from numpy import ma


def getComplexCoordinates(resolution,limitreal,limitimag,dtype):
    coordinatetensor = np.ones([resolution[0], resolution[1]], dtype=dtype)
    rangereal = np.linspace(limitreal[0], limitreal[1], resolution[1])
    coordinatetensor = coordinatetensor * rangereal
    rangeimag = np.linspace(limitimag[0], limitimag[1], resolution[0])
    imagtemptensor = np.ones_like(coordinatetensor) * np.reshape(rangeimag, (1, rangeimag.shape[0])).T * 1j
    # print(imagtemptensor)
    coordinatetensor = coordinatetensor + imagtemptensor
    return coordinatetensor
    #return ma.array(coordinatetensor, mask=np.zeros_like(coordinatetensor))