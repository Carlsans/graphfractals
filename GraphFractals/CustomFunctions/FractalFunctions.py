import numpy as np
from numpy import ma


def getallonevarfnlist():
    return ['fn.zmpone','fn.zbyz',"fn.logoneminusp","fn.zmponemultiple", 'fn.flip','fn.inverse'] #'fn.'
## One variable
def one(*args):
    for i in args:
        if len(i.shape) == 2:
            return np.ones_like((i[0],i[1]))
    return 1
def zero(*args):
    for i in args:
        if len(i.shape) == 2:
            return np.zeros_like((i[0],i[1]))
    return 0
def zmpone(z):
    return (z * z / (z - 1)) / ((z + 1) / (z * z))
def zmponemultiple(z):
    return (z*z/(z - 1))/((z+1)/(z*z))*(z*z/(z + 1))/((z-1)/(z*z))   /   (z*z/(z + 1))/((z-1)/(z*z))*(z*z/(z - 1))/((z+1)/(z*z)) + 1
def zbyz(z):
    return np.power(z,z)
def flip(z):
    real, imag = np.real(z),np.imag(z)
    return imag + real * 1j
def inverse(z):
    return 1/z
def logoneminusp(z):
    return np.log(z-1+.000000000001)

## Two variable
def getalltwovarfnlist():
    return ['fn.zbyzplusp','fn.serie','fn.parallel','fn.twovarmean','fn.modulo','fn.floordivide','fn.log2var','fn.power2var']#,'fn.power2var','fn.']

def zbyzplusp(z,p):
    return ma.power(z+p,z)

def serie(z,p1):
    return (np.imag(p1) * np.real(p1)) / (np.imag(p1)+np.real(p1)) + z
def parallel(p1,p2):
    return (p1*p2)/(p1+p2)
def twovarmean(p1,p2):
    return (p1+p2)/2
def power2var(p1,p2):
    return np.power(p1,p2)
def modulo(divided,divider):
    answer = np.abs(divided/divider)

    return answer

def log2var(p1,p2):
    return np.log(p1)/np.log(p2)
def floordivide(divided,divider):
    return np.abs(divided)/np.abs(divider)

### Three Variables
def parallelofz(z,p1, p2):
    parallelc1r1 = (np.imag(p1) * np.real(p1)) / (np.imag(p1)+np.real(p1)+0.00000000000000001) + z
    parallelc2r2 = (np.imag(p2) * np.real(p2)) / (np.imag(p2) + np.real(p2)+0.00000000000000001) + z
    return (parallelc1r1*parallelc2r2)/(parallelc1r1+parallelc2r2+0.00000000000000001)
