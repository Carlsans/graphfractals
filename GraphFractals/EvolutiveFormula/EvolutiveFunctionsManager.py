import numpy as np

from GraphFractals.EvolutiveFormula.EvolutiveFunction import EvolutiveFunction
import GraphFractals.CustomFunctions.FractalFunctions as fn

class EvolutiveFunctionsManager:
    def __init__(self):
        self.initfunctions()

    def initfunctions(self):
        self.fnlist = []
        self.add = EvolutiveFunction(self,np.add, 'evo.add', (2,4), True)
        #setattr(self, "add", self.add.callfunction)
        self.subtract = EvolutiveFunction(self,np.subtract, 'evo.subtract', (2,4), True)
        self.multiply = EvolutiveFunction(self,np.multiply, 'evo.multiply', (2,4), True)
        self.divide = EvolutiveFunction(self,np.divide, 'evo.divide', (2,4), True)
        self.naturallog = EvolutiveFunction(self,np.log, 'evo.naturallog', 1, False)
        self.one = EvolutiveFunction(self,fn.one, 'evo.one', 1, False,addtofnlist=False)
        self.sin= EvolutiveFunction(self,np.sin, 'evo.sin', 1, False)
        self.cos = EvolutiveFunction(self,np.cos, 'evo.cos', 1, False)
        self.tan = EvolutiveFunction(self,np.tan, 'evo.tan', 1, False)
        self.arcsin = EvolutiveFunction(self, np.arcsin, 'evo.arcsin', 1, False)
        self.arccos = EvolutiveFunction(self, np.arccos, 'evo.arccos', 1, False)
        self.arctan = EvolutiveFunction(self, np.arctan, 'evo.arctan', 1, False)
        self.parallelofz = EvolutiveFunction(self,fn.parallelofz, 'evo.parallelofz', 3, False)
        #self.one = EvolutiveFunction(self,fn.one, 'evo.one', 0, False)
        #self.zero = EvolutiveFunction(self, fn.zero, 'evo.zero', 0, False)
        # self.mod = EvolutiveFunction(np.mod,'np.mod',2)


        # result = mod.callfunction(10, 3)
        # print(result)
# evofunc = EvolutiveFunctionsManager()
# import evofunc as evo
# answer = evofunc.div(3,5,6,3,6)
# print(answer)