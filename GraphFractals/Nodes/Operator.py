#from abc import ABC, abstractmethod
import inspect
import re

import numpy as np
import numpy.ma as ma
from scipy.stats import entropy
from GraphFractals.CustomFunctions.selectionsfunctions import image_entropy,image_compression_based_information,image_comparision_loss
from GraphFractals.CustomFunctions.fractaldomainfunctions import getComplexCoordinates
import chime
import GraphFractals.CustomFunctions.FractalFunctions as fn
import copy
class Operator():
    #@abstractmethod
    def __init__(self,sharedvalues,verbose = False,name=__name__):
        self.sharedvalues = sharedvalues
        self.functionlist = []
        self.values = {}
        self.verbose = verbose
        self.name = name
        self.color = "#00FF00"
    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def getProperties(self):
        returnvalue = ""
        for afunc in self.functionlist:
            returnvalue += afunc + "\n"
        return returnvalue
    def getValues(self):
        returndict ={}
        returndict.update(self.values)
        returndict.update(self.sharedvalues)
        return returndict
    def processNode(self,lastnode):
        #print(lastnode)
        self.precedentnodes = lastnode['nodereturnstate']
        self.values.update(self.precedentnodes.values)

    def applyNode(self):

        self.runFunctions()
        #print(self.values)
        return {'nodereturnstate': self, 'nextnodechoice': -1}
    def runFunctions(self):
        for func in self.functionlist:
            variable, function = func.split("=",1)
            variable, function = variable.strip(),function.strip()
            match = re.search(r'(\[.*?\])', variable)
            if match:
                bracket = match.group(1)
                variable = variable.replace(bracket, '')
                #print("bracket",bracket)

            else:
                bracket = None
            # Evaluate the expression using eval() with the variables dictionary
           # print("variable",variable,"function",function)
            # if isinstance(variable, np.array()):
            #     print("blou")


            if bracket is None:
                # print(self.values)
                # print(self.getValues())
                # print("function",function)
                try:

                    result = eval(function, globals(), self.getValues())

                except Exception:
                    print(self.values)
                    print(self.getValues())
                    print("function",function)
                    raise
                self.values[variable] = result


            else:

                bracketresult = eval(bracket[1:-1], globals(), self.getValues())
                #print("variable  + bracket",variable  + bracket,"bracketresult",bracketresult,bracketresult.shape)
                #print("function",function)
                #print(self.values)
                self.values[variable][bracketresult] = eval(function, globals(), self.getValues())

        #print(self.values)

    def addFunction(self,func):
        self.functionlist.append(func)

    def __str__(self):
        returnvalue = "Operator\n"
        for key, value in self.values.items():
            returnvalue += "key=" + str(key) + " value="+str(value) +"\n"
            # print("%s == %s" % (key, value))
        return returnvalue


    def printFunctions(self):
        for afunc in self.functionlist:
            print(afunc)

            #attribute_value = getattr(obj, attribute_name)
    def printnodecontent(self):
        if self.verbose:
            print(self)