import random

import numpy as np
import numpy.ma as ma
import GraphFractals.CustomFunctions.FractalFunctions as fn
from inspect import signature
class GraphIterator:
    def __init__(self,sharedvalues, verbose = False,name=__name__, randomorder = True):
        self.sharedvalues = sharedvalues
        self.functionlist = []
        self.values = {}
        self.iteratorvalues = {}
        self.iteratorcurrentindex = {}
        self.iterationended = False
        self.verbose = verbose
        self.name = name
        self.color = "#FFFF00"
        self.randomorder = randomorder
        self.currentvalue = None
        self.totalcombinations = 0
        self.currentcombination = 0
        self.combinationorderlist = []

    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def calculatetotalcombinations(self):
        maxpossibilities = 1
        for key, value in self.iteratorvalues.items():
            print(len(value))
            maxpossibilities *= len(value)
        print("self.totalcombinations",maxpossibilities)

    def setcurrentiteratorvalues(self):


        lenlist = []
        maxpossibilities = 1
        for key,value in self.iteratorvalues.items():
            print(len(value))
            maxpossibilities *= len(value)
            lenlist.append(len(value))

        if self.combinationorderlist == []:
            self.combinationorderlist = list(range(0,maxpossibilities))
            if self.randomorder:
                random.shuffle(self.combinationorderlist)
            #print(self.combinationorderlist)

        numbertodecompose = self.combinationorderlist[self.currentcombination]
        print("numbertodecompose", numbertodecompose)
        print("lenlist",lenlist)
        #print(maxpossibilities)
        if numbertodecompose < 0 or numbertodecompose > maxpossibilities - 1:
            print("Exceeded possibility number",numbertodecompose, "maximum is",maxpossibilities)
            return False
        dividerlist = []

        for i in range(1,len(lenlist)):
            divider = 1
            for j in range(i, len(lenlist) ):
                divider *= lenlist[j]
                print("lenlist[j]", lenlist[j])
            dividerlist.append(divider)
        dividerlist.append(1)
        print("dividerlist",dividerlist)
        resultlist = []
        for i in dividerlist:
            division = numbertodecompose / i
            #print("division",division)
            if division >= 1:
                resultlist.append(numbertodecompose // i)
                numbertodecompose -= (numbertodecompose // i) * i
                #print("numbertodecompose",numbertodecompose)
            else:
                resultlist.append(0)
        print(resultlist)
        #self.iteratorvalues[key][self.iteratorcurrentindex[key]]
        i=0
        for key in self.iteratorvalues:
            self.iteratorcurrentindex[key] = resultlist[i]
            i+=1
        print("self.iteratorcurrentindex",self.iteratorcurrentindex)
        return True



    def addIterator(self,**kwargs):
        print(kwargs)

        for key, value in kwargs.items():

            self.iteratorvalues[key] = value
            if(not type(kwargs[key]) == list ):
                print("GraphIterator support list only")
                raise Exception("GraphIterator")
            self.calculatetotalcombinations()
            #key = "function " + key

            self.iteratorcurrentindex[key] = 0

    def getProperties(self):
        returnvalue = ""
        for key, value in self.iteratorvalues.items():
            returnvalue += str(key) + "=" + str(value) + "\n"
        return returnvalue
    def getValues(self):
        returndict ={}
        returndict.update(self.values)
        returndict.update(self.sharedvalues)
        return returndict
    def processNode(self,lastnode):
        if not self.setcurrentiteratorvalues():
            print("Iterator ended")
            self.iterationended = True
            return
        if not lastnode is None:
            print("GraphIterator do not yet support parents")
            exit()
        for key, value in self.iteratorvalues.items():
            #print(key,self.iteratorvalues[key][self.iteratorcurrentindex[key]])
            currentvalue = self.iteratorvalues[key][self.iteratorcurrentindex[key]]
            print("currentvalue",currentvalue)
            if isinstance(currentvalue, complex):
                self.values[key] = currentvalue
            else:
                exec("function = " + currentvalue, globals())
                sig = signature(function)
                params = list(sig.parameters)
                if 'args' in params:
                    params.remove('args')
                if 'kwargs' in params:
                    params.remove('kwargs')
                print("params",params)
                numberofparameters = len(params)
                functionparams = ""
                for i in range(1,numberofparameters+1):
                    functionparams += "p"+str(i)+","
                functionparams = functionparams[0:-1]
                print("functionparams",functionparams)

                #x = lambda p1, p2 : p1 * p2
                functiondeclaration = "myfunction = lambda {} : {}({})".format(functionparams,
                    currentvalue,functionparams)
                print("functiondeclaration",functiondeclaration)

                exec(functiondeclaration, globals())
                self.values[key] = myfunction
            self.sharedvalues[key+"_parameter"] = currentvalue

            #self.iteratorcurrentindex[key] += 1
        self.currentcombination +=1
            # if(self.iteratorcurrentindex[key] > len(self.iteratorvalues[key])-1):
            #     self.iterationended = True


    def applyNode(self):

        #self.runFunctions()
        print(self.values)

        return {'nodereturnstate': self, 'nextnodechoice': -1}

    def __str__(self):
        return ""
    def printnodecontent(self):
        if self.verbose:
            print(self)