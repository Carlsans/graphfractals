import os
import sys
import time
from datetime import datetime
from dill.source import getsource
from PIL import Image
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt

import inspect
class Outputer:
    def __init__(self,sharedvalues,verbose = False,name=__name__,outputtype = "image",show = False,savetodisk = True):
        self.sharedvalues = sharedvalues
        self.verbose = verbose
        self.name = name
        self.dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.color = "#FF00FF"
        self.values = None

        self.outputtype = outputtype
        self.show = show
        self.savetodisk = savetodisk
        self.outputvariables = []
        self.logvariables = []
    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def getProperties(self):
        result = ""
        for i in self.outputvariables:
            result += "output " + i +"\n"
        for i in self.logvariables:
            result += "log " + i + "\n"
        return result
    def getValues(self):
        returndict ={}
        returndict.update(self.values)
        returndict.update(self.sharedvalues)
        return returndict
    def processNode(self,lastnode):
        self.values = lastnode['nodereturnstate'].values


    def applyNode(self):
        print("Output :")
        print(self.values)
        for outputvariable in self.outputvariables:
            if self.outputtype == "image":
                print(self.values[outputvariable])
                normalizedmatrix = (self.values[outputvariable] - np.min(self.values[outputvariable])) / (
                    np.max(self.values[outputvariable] + 1))
                # print(normalizedmatrix)

                im = Image.fromarray(np.uint8(cm.binary(normalizedmatrix) * 255),mode="RGB")
                plt.imshow(im)
                if self.show:
                    plt.show()
                path = self.dir_path + "/lowres/unlabeled/" + datetime.now().strftime("%Y_%m_%d_%Hh%Mm%Ss%f")
                if self.savetodisk:

                    print(path,normalizedmatrix.size)

                    #np.save(path+".npy",self.values[outputvariable].data)

                    plt.imsave(path+".png",normalizedmatrix,cmap="binary")
                    #plt.imsave(path + "col.png", normalizedmatrix, cmap="prism")
                # Note : logs variables of iterators have the _parameter suffix otherwise it refer to a lambda
                if len(self.logvariables)>0:
                    self.savelog(path+".log")
        return {'nodereturnstate': self, 'nextnodechoice': -1}
    def savelog(self,filenameandpath):
        print(self.getValues())
        f = open(filenameandpath,mode = "w")
        for i in self.logvariables:
            # Automaticaly fetch the value of the parameter, not the lambda func
            if not i in self.getValues() or i + "_parameter" in self.getValues():
                i = i + "_parameter"
            f.write(i + " = "+ str(self.getValues()[i]) +"\n")
        f.close()
    def setOutputVariable(self,outputvariable):
        self.outputvariables.append(outputvariable)
    def setLogVariable(self,logvariable):
        self.logvariables.append(logvariable)
    def __str__(self):
        np.set_printoptions(threshold=sys.maxsize)
        returnvalue = "Outputer \n"
        if self.values is None:
            return ""
        for key, value in self.values.items():
            returnvalue += "key=" + str(key) + " value="+str(value) +"\n"
            # print("%s == %s" % (key, value))
        return returnvalue
    def printnodecontent(self):
        if self.verbose:
            print(self)