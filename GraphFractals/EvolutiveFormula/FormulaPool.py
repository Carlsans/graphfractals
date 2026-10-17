import pickle
import os

import numpy as np


class FormulaPool:
    def __init__(self):
        self.minimumgrade = 0.2
        self.maxpoolsize = 100
        self.pool = []
        self.poolfilepath = os.path.dirname(os.path.realpath(__file__))+"/pool/pool.pickle"
        if os.path.isfile(self.poolfilepath):
            self.loadpool()
            print(self.loadpool())


    def getindividualroulette(self):
        individualindex = self.roulette()
        return self.pool[individualindex]['saformula']
    def roulette(self):
        normgrades = self.normalizedgrades()
        #print(normgrades)
        normgrades = np.clip(normgrades,self.minimumgrade,1)
        #print(normgrades)
        cumulatedgrades = np.sum(normgrades)
        #print("cumulatedgrades",cumulatedgrades)
        choosenindividual = np.random.rand() * cumulatedgrades
        #print("choosenindividual",choosenindividual)
        count = 0
        n=0
        for i in normgrades:
            start,end = count,count + i
            #print(start, end)
            if start <= choosenindividual and end > choosenindividual  :
                choosen = n
            count += i
            n+=1
        #print("choosen",choosen)
        #print(self.pool)
        return choosen
        #print(self.pool)
    def normalizedgrades(self):
        grades = np.array([i['grade'] for i in self.pool])
        print(grades)
        min,max = np.min(grades),np.max(grades)
        print("min,max",min,max)
        normalizedgrades = (grades - min)/(max - min)
        return normalizedgrades


    def addformula(self,saformula,grade):
        if len(self.pool) >= self.maxpoolsize:
            choosenindex = self.roulette()
            del self.pool[choosenindex]
        self.pool.append({'saformula':saformula,'grade':grade})
        self.savepool()

    def savepool(self):
        with open(self.poolfilepath, 'wb') as handle:
            pickle.dump(self.pool, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadpool(self):
        with open(self.poolfilepath, 'rb') as handle:
            self.pool = pickle.load(handle)
        print("Pool loaded : ", self)
    def __str__(self):
        returnstr = "Formula Pool : \n"
        for i in self.pool:
            returnstr += "Fractal Grade "+str(i['grade'])+ "\n"
            returnstr += str(i['saformula']) + "\n__________________\n"
        return returnstr