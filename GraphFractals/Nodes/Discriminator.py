import numpy as np
import math
class Discriminator:
    def __init__(self,sharedvalues,verbose=False,name=__name__):
        self.sharedvalues = sharedvalues
        self.verbose = verbose
        self.name = name
        self.values = {}
        self.color = "#FF0000"
        self.discriminatorfunctions = []
    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def getProperties(self):
        returnstring = ""
        for i in self.discriminatorfunctions:
            returnstring += str(i) +"\n"
        return returnstring

    def getValues(self):
        returndict ={}
        returndict.update(self.values)
        returndict.update(self.sharedvalues)
        return returndict
    def processNode(self,lastnode):
        self.precedentnodes = lastnode['nodereturnstate']
        self.values.update(self.precedentnodes.values)
    def applyNode(self):

        return {'nodereturnstate': self, 'nextnodechoice': self.runFunctions()}
    def runFunctions(self):

        # variable, function = self.discriminator.split("=")
        # variable, function = variable.strip(),function.strip()

        # Evaluate the expression using eval() with the variables dictionary
        #print("self.values",self.values)
        for acondition in self.discriminatorfunctions:
            result = eval(acondition[0], globals(), self.getValues())
            if result:
                if acondition[1] is None:
                    continue
                else:
                    return acondition[1]
            if not acondition[2] is None:
                return acondition[2]

    def addFunction(self, func,nodetrue = None,nodefalse = None):
        self.discriminatorfunctions.append([func,nodetrue,nodefalse])

    def __str__(self):
        returnvalue = "Discriminator func =" + str(self.discriminatorfunction)
        return returnvalue

    def printnodecontent(self):
        if self.verbose:
            print(self)