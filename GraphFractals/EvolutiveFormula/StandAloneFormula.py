import copy


class StandAloneFormula:
    def __init__(self,formula,listFN,listP,listV,listSymbols):
        self.formula = formula
        self.listFN = listFN
        self.listP = listP
        self.listV = listV
        self.listSymbols = listSymbols
        valid = self.testformulavalidity()
        if not valid:
            raise Exception("Formula not valid")
    def testformulavalidity(self):
        print("Formula validity",len(self.listFN))
        formula = copy.deepcopy(self.formula)
        for i in range(len(self.listFN),0,-1):
            if 'fn'+str(i) in formula:
                formula = formula.replace('fn'+str(i),"")
            else:
                print("Error in functions")
                print(self)
                return False
        for i in range(len(self.listP),0,-1):
            if 'p'+str(i) in formula:
                formula = formula.replace('p'+str(i),"")
            else:
                print("Error in parameters")
                print(self)
                return False
        if 'fn' in formula:
            print("Not recognized function")
            print("formula",formula)
            print(self)
            return False
        return True


    def shift_formula(self,shiftFN,shiftP,shiftV):
        formulanumber = len(self.listFN)
        formula = copy.deepcopy(self.formula)
        for i in reversed(self.listFN):
            print(formulanumber,i)
            formula = formula.replace("fn"+str(formulanumber),"fnV"+str(formulanumber+shiftFN)+"V")
            formulanumber-=1
        formulanumber = len(self.listP)
        for i in reversed(self.listP):
            print(formulanumber,i)
            formula = formula.replace("p"+str(formulanumber),"pV"+str(formulanumber+shiftP)+"V")
            formulanumber-=1
        for i in self.listV:
            formula = formula.replace(i, "I"+i+"I")

        for i in self.listSymbols:
            formula = formula.replace(i, "I" + i + "I")
        formula = formula.replace("V","")
        return formula
    def removedistinguishers(self):
        self.formula = self.formula.replace("I","")


    def __str__(self):
        functions = [i.getfunctionname() for i in self.listFN]
        ", ".join(functions)
        functions = "["+", ".join(functions) + "]"
        return "Formula : " + str(self.formula) + "\n" + "Functions : " + functions + "\n" + "Parameters : " + str(self.listP)+ "\n" + "Variables : " + str(self.listV)