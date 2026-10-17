import chime

from GraphFractals.EvolutiveFormula.EvolutiveFormula import EvolutiveFormula
from GraphFractals.Nodes.Operator import Operator
import numpy as np
import GraphFractals.CustomFunctions.FractalFunctions as fn

import GraphFractals.EvolutiveFormula.EvolutiveFunctionsManager as evo
#from my_module import my_instance as my_functions

class OperatorEvolutiveFormula(Operator):
    def __init__(self,sharedvalues,verbose = False,name=__name__):
        super().__init__(sharedvalues,verbose ,name=name)
        self.lastfractalentropy = 0
        self.evo = EvolutiveFormula(self)
        self.evofunction = self.evo.formulatranslation.translateformula() #Unresolved
        self.getNewEvolutiveFunction()
    def getNewEvolutiveFunction(self):
        self.evofunction = self.evo.trystep()
    def runFunctions(self):
        waspruning = False
        # If a new fractal is starting
        if self.values['i']==0:
            simplifiedformula = self.evo.formulatranslation.toStandaloneFormula()
            print(simplifiedformula)

            self.evo.formulatranslation.formula = simplifiedformula.formula
            self.evo.formulatranslation.listFN = simplifiedformula.listFN
            self.evo.formulatranslation.listP = simplifiedformula.listP
            #print(self.evo.formulatranslation.toStandaloneFormula())

            if 'fractalentropy' in self.values and not self.values['fractalresolution'] == self.values['hiresfractalresolution']:
                self.lastfractalentropy = self.values['fractalentropy']
                waspruning = self.evo.formulamutation.ispruning
                self.getNewEvolutiveFunction()
                # Already done at least one fractal but the fractal has not been selected for hi res
            if waspruning:
                # The last move was a pruning function, determine it's validity by comparing
                # the entropy before pruning and after pruning
                self.evo.formulamutation.ispruning = False
                if self.evo.formulamutation.beforepruninggrade <= self.values['fractalentropy']:
                    self.evo.performstep(self.evo.teststepslist[-1]) # The pruning is successful, apply it

                # Si entropy ne descend pas : self.evo.performbeststep()
            elif self.values['resetformula']:
                # The graph is instructing the restart of a new formula
                self.values['resetformula'] = False
                self.values['minimumfractalentropy'] = self.values['minimumfractalentropystart']
                self.evo.resetformula()
                self.evofunction = self.evo.formulatranslation.translateformula()
            elif self.values['fractalresolution'] == self.values['hiresfractalresolution']:
                # The graph instructed a hi res version of the current fractal
                # It select the current step has the new formula
                self.evo.setlastgrade(self.values['fractalentropy'])
                issuccess = self.evo.performbeststep()


                if issuccess == -1:
                    self.values['fractalresolution'] = self.values['lowresfractalresolution']
                    self.values['i'] = 10000000
                else:
                    # Add selected formula to pool
                    saformula = self.evo.formulatranslation.toStandaloneFormula()
                    self.evo.formulapool.addformula(saformula,self.values['fractalentropy'])
                    print(self.evo.formulapool)

            elif self.values['evoiterations'] > self.values['evoiterationsmax']:
                # The last iterations were not successful to generate a proper fractal.
                # The system choose the best fractal of all and select it has the new formula
                self.values['evoiterations'] = 0
                self.evo.setlastgrade(self.values['fractalentropy'])
                self.evo.performbeststep()
                # Add selected formula to pool
                saformula = self.evo.formulatranslation.toStandaloneFormula()
                self.evo.formulapool.addformula(saformula, self.values['fractalentropy'])
                #chime.info()



        self.values['evolutivefunction'] = self.evofunction
        print("Evolutive function",self.evofunction,"minimum entropy",self.values['minimumfractalentropy'])
        # Call evolutive function manager
        global evo
        evo = self.evo.fnmanager
        try:
            result = eval(self.evofunction, globals(), self.getValues())
        except Exception:
            print(self.values)
            print(self.getValues())
            print("function", self.evofunction)
            raise
        if isinstance(result,complex) or isinstance(result,float):
            self.values['z'] = np.zeros_like(self.values['z'])
            self.values['i'] = 1000000000
            print("Bad evo function")
        elif not len(result.shape) == 2:
           self.values['z'] = np.zeros_like(self.values['z'])
           self.values['i'] = 1000000000
           print("Bad evo function")
        else:
            self.values['z'] = result

        super().runFunctions()

