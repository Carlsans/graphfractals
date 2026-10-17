import copy
import math
import random
import re

import numpy as np

from GraphFractals.EvolutiveFormula.EvolutiveFunction import EvolutiveFunction
from GraphFractals.EvolutiveFormula.EvolutiveFunctionsManager import EvolutiveFunctionsManager
from GraphFractals.EvolutiveFormula.FormulaMutation import FormulaMutation
from GraphFractals.EvolutiveFormula.FormulaPool import FormulaPool
from GraphFractals.EvolutiveFormula.FormulaTranslation import FormulaTranslation
from GraphFractals.EvolutiveFormula.utils import nth_repl


class EvolutiveFormula:
    def __init__(self,graphoperator):
        self.graphoperator = graphoperator
        self.fnmanager = EvolutiveFunctionsManager()
        self.formulatranslation = FormulaTranslation(self)
        self.formulamutation = FormulaMutation(self)
        self.formulapool = FormulaPool()
        self.createrandomformula()
        self.teststepslist = []
        self.savelastloop()

    def resetformula(self):
        self.teststepslist = []
        self.createrandomformula()
        self.savelastloop()
    def savelastloop(self):
        self.lastloop = {'formula': copy.deepcopy(self.formulatranslation.formula), 'listFN':copy.deepcopy(self.formulatranslation.listFN), 'listP':copy.deepcopy(self.formulatranslation.listP), 'listV':copy.deepcopy(self.formulatranslation.listV)}
    def restorelastloop(self):
        self.formulatranslation.formula = copy.deepcopy(self.lastloop['formula'])
        self.formulatranslation.listFN = copy.deepcopy(self.lastloop['listFN'])
        self.formulatranslation.listP = copy.deepcopy(self.lastloop['listP'])
        self.formulatranslation.listV = copy.deepcopy(self.lastloop['listV'])

    def setlastgrade(self,grade):
        # may bring more issues !!
        if self.teststepslist == []:
            print("There is no previous step list !!")
            return
        if math.isnan(grade):
            grade = 0
        print("teststepslist", self.teststepslist)
        self.teststepslist[-1]['grade'] = grade

    def trystep(self):
        self.restorelastloop()
        self.teststep()
        return self.formulatranslation.translateformula()
    def performbeststep(self):
        beststep = self.getbeststep()
        print("beststep",beststep)
        if beststep == -1:
            return -1
        self.performstep(beststep)
    def performstep(self,step):
        self.restorelastloop()
        # switchfunctionrandom,self.switchparamrandom,self.addramificationrandom
        parameters = copy.deepcopy(step['parameters'])
        if step['action'] == 'switchvariablerandom':
            self.formulamutation.switchvariablerandom(parameters=parameters)
        if step['action'] == 'switchfunctionrandom':
            self.formulamutation.switchfunctionrandom(parameters=parameters)
        if step['action'] == 'switchparamrandom':
            self.formulamutation.switchparamrandom(parameters=parameters)
        if step['action'] == 'addramificationrandom':
            self.formulamutation.addramificationrandom(parameters=parameters)
        if step['action'] == 'pruneformula':
            self.formulamutation.pruneformula(parameters=parameters)
        if step['action'] == 'crossfromPool':
            self.formulamutation.crossfromPool(parameters=parameters)
        self.savelastloop()
        self.teststepslist = []
    def getbeststep(self):
        if self.teststepslist == []:
            return -1
        return max(self.teststepslist, key=lambda x: x['grade'])

    def teststep(self):
        currentdict = {}
        possibleactions = self.formulamutation.mutationfunctions
        currentaction = random.choice(possibleactions)
        print("Current action :", currentaction.__name__)
        currentdict['action'] = currentaction.__name__
        parameters = currentaction()
        # If there is an impossibility to execute the step retry something else
        if parameters == -1:
            self.teststep()
            return
        currentdict['parameters'] = parameters
        print("Step parameters",parameters)
        print("Step formula",self.formulatranslation.formula)
        print("Step translated formula",self.formulatranslation.translateformula())
        currentdict['grade'] = float('nan')
        #currentdict['grade'] = random.random()*5
        self.teststepslist.append(currentdict)

    def callformulatest(self):
        z = np.random.rand(3, 3) + np.random.rand(3, 3) * 1j
        callformula = "{}".format(self.formulatranslation.translateformula())
        print(eval(callformula, globals(), locals()))

    def createrandomformula(self):
        #nbrfn,nbrp = random.randint(3,5),random.randint(0,2)
        # A refaire, pour le moment on utilise une formule de depart
        self.formulatranslation.formula = "fn1(z,p1,p2)"
        # evo.add(evo.add(evo.multiply(z,evo.subtract(z,(-0.9889899408053138+1.5579467266785252j))),evo.multiply(z,evo.add(z,(0.6795770715357303+0.7443002835048418j)),(1.2343+0.03456j))),evo.multiply(z,(-0.9816017388395752+1.5527395139781692j)),(0.732553+0.234j))
        self.formulatranslation.listFN = [self.fnmanager.multiply]
        # Note, les P supplementaires sont consideres lors de l'ajout de fonctions addramificationrandom
        # En mettre quelque uns en plus
        self.formulatranslation.listP = [.232553+1.234j,   1.2343 + .03456j,   .732553+0.234j,   .132553+1.234j,   4+0.234j,   .00732553+0.00234j]
        self.formulatranslation.listV = ['z', 'c']
        for i in range(2):
            self.formulamutation.addramificationrandom()
        print("New random formula",self.formulatranslation.formula)
        # exit()


#evofor = EvolutiveFormula()