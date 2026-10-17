import copy
import random
import re

from matplotlib import pyplot as plt

from GraphFractals.EvolutiveFormula.FormulaTree import FormulaTree
from GraphFractals.EvolutiveFormula.StandAloneFormula import StandAloneFormula
from GraphFractals.EvolutiveFormula.utils import nth_repl


class FormulaMutation():
    def __init__(self,evo):
        self.evo = evo
        self.ftree = FormulaTree()
        self.formulatranslation = evo.formulatranslation
        self.fnmanager = evo.fnmanager
        self.ispruning = False
        self.mutationfunctions = [self.switchvariablerandom,self.switchfunctionrandom,self.switchparamrandom,self.addramificationrandom,self.pruneformula,self.crossfromPool]
        ## TEST
        #self.mutationfunctions = [self.crossfromPool]

    def switchfunctionrandom(self,parameters=None):
        if not parameters is None:
            functiontochangeindex = parameters['functiontochangeindex']
            self.formulatranslation.listFN[functiontochangeindex] = parameters['functionchoice']
            self.formulatranslation.formula = parameters['newformula']
            self.formulatranslation.listP = parameters['listP']

            return
        # There is a problem here, retry something else
        if len(self.formulatranslation.getfnfromformula()) <= 1:
            return -1
        fntochange = random.choice(self.formulatranslation.getfnfromformula(showfn=True))

        functiontochangeindex = int(fntochange.replace('fn','')) - 1

        print("current formula",self.formulatranslation.formula)
        print("fntochange",fntochange)
        print("functiontochangeindex", functiontochangeindex)

        functionparam = self.formulatranslation.getFunctionParameters(fntochange)
        newfunction = random.choice(self.fnmanager.fnlist)
        print("functionparam",functionparam)
        print("newfunction.functionname",newfunction.functionname)
        print(newfunction.parameterrange , len(functionparam))
        if newfunction.parameterrange[0] >= len(functionparam) and newfunction.parameterrange[1] <= len(functionparam):
            print("same")
            # Do nothing
        else:
            #print("dif")
            if newfunction.parameterrange[0] < len(functionparam):
                print("Remove params")
                # let trim some params
                while not newfunction.parameterrange[0] == len(functionparam):
                    functionparam.remove(random.choice(functionparam))
                print("params after removal",functionparam)
                self.formulatranslation.setFunctionParameters(fntochange,functionparam)
            else:
                #let add random params
                print("Add randoms params")
                paramstoaddcount =  newfunction.parameterrange[0] - len(functionparam)
                newparams = functionparam + self.createrandomparams(paramstoaddcount)
                print("newparams", newparams)
                print(" formula before", self.formulatranslation.formula)
                self.formulatranslation.setFunctionParameters(fntochange, newparams)

                #print(" formula after",self.formulatranslation.formula)

        print("formula after", self.formulatranslation.formula)
        self.formulatranslation.listFN[functiontochangeindex] = newfunction
        return {'functiontochangeindex': functiontochangeindex,'functionchoice':self.formulatranslation.listFN[functiontochangeindex],'newformula':self.formulatranslation.formula,'listP':self.formulatranslation.listP}
    def createrandomparams(self,paramnumber):
        #raise Exception("TO DO faire fct de 1 creer une param si existe pas 2 choisir.. verfier avec autres fcts qui m utilisent")
        print("paramnumber",paramnumber)
        possibleoptions = copy.deepcopy(self.formulatranslation.availablevariables)
        currentparameters = self.formulatranslation.getpAll()
        possibleoptions += currentparameters

        minimumnumberofparameterstosatisfy =  len(possibleoptions) - paramnumber
        print("minimumnumberofparameterstosatisfy",minimumnumberofparameterstosatisfy)
        if minimumnumberofparameterstosatisfy >= 0:
            Ptoadd = 0
        else:
            Ptoadd = abs(minimumnumberofparameterstosatisfy)
        if Ptoadd > 0 :
            print("Ptoadd",Ptoadd)
            for i in range(Ptoadd):
                addedPindex = self.formulatranslation.addPatend(self.getrandomcomplex())
                possibleoptions.append("p"+str(addedPindex + 1))

        print("possibleoptions",possibleoptions)
        randomparams = []

        for i in range(paramnumber):
            choice = random.choice(possibleoptions)
            possibleoptions.remove(choice)
            randomparams.append(choice)
            if "p" in choice:
                print("choice",choice)
                index = int(choice.replace('p','')) - 1
                if not self.formulatranslation.doesPexist(index):
                    self.formulatranslation.setPat(index,self.getrandomcomplex())

        print("randomparams",randomparams)

        return randomparams
    def switchvariablerandom(self, parameters=None):
        if not parameters is None:
            self.formulatranslation.formula = parameters['newformula']
            return
        variables = self.formulatranslation.getvfromformula()
        indexs = []
        for variable in variables:
            indexs.append({variable : [m.start() for m in re.finditer(variable, self.formulatranslation.formula)]})
        print(self.formulatranslation.formula)
        print(indexs)
        # Something wrong with this step, do something else
        if indexs == []:
            print("No variable to switch")
            return -1
        choosenvariable = random.choice(indexs)
        print(choosenvariable)
        choosenvariablekey = list(choosenvariable.keys())[0]
        choosenvariableindex = random.choice(choosenvariable[choosenvariablekey])
        print(choosenvariable,choosenvariablekey,choosenvariableindex)
        print("Available variables",self.formulatranslation.availablevariables)
        variables = copy.deepcopy(self.formulatranslation.availablevariables)
        variables.remove(choosenvariablekey)
        print("Variables for replacement", variables)
        replacewith = random.choice(variables)
        #print("Old formula",self.formulatranslation.formula)
        formulastart = self.formulatranslation.formula[0:choosenvariableindex]
        formulaend = self.formulatranslation.formula[choosenvariableindex:]
        formulaend = formulaend.replace(choosenvariablekey,replacewith)
        self.formulatranslation.formula = formulastart + formulaend
        print("New formula", self.formulatranslation.formula)

        return {'newformula':self.formulatranslation.formula}

    def getrandomcomplex(self, rangereal=(-2, 2), rangeimag=(-2, 2)):
        return random.random() * (rangereal[1] - rangereal[0]) + rangereal[0] + (
                    random.random() * (rangeimag[1] - rangeimag[0]) + rangeimag[0]) * 1j

    def switchparamrandom(self,rangereal = (-2,2), rangeimag = (-2,2),parameters=None ):
        if not parameters is None:
            paramtochangeindex = parameters['paramtochangeindex']
            self.formulatranslation.listP[paramtochangeindex] = parameters['paramchoice']
            return
        # There is no param to switch
        if self.formulatranslation.listP == []:
            return
        paramtochangeindex = random.randint(0, len(self.formulatranslation.listP) - 1)
        self.formulatranslation.listP[paramtochangeindex] = self.getrandomcomplex(rangereal,rangeimag)
        return {'paramtochangeindex':paramtochangeindex,'paramchoice':self.formulatranslation.listP[paramtochangeindex] }

    def addramificationrandom(self, parameters=None):
        if not parameters is None:
            self.formulatranslation.listFN.append(parameters['addedfunction'])
            #self.formulatranslation.listP.append(parameters['addedparameter'])
            self.formulatranslation.formula = parameters['newformula']
            self.formulatranslation.listP = parameters['listP']
            return
        # Pick expression to replace
        allexpressionlist = []
        # allexpressionlist += ["fn"+str(i+1) for i in range(len(self.listFN))]
        allexpressionlist += ['p' + str(i) for i in self.formulatranslation.getpfromformula()]
        #allexpressionlist += ["p" + str(i + 1) for i in range(len(self.formulatranslation.listP))]
        allexpressionlist += self.formulatranslation.getvfromformula()
        if self.formulatranslation.isZpresent():
            allexpressionlist += "Z"
        if self.formulatranslation.isOpresent():
            allexpressionlist += "O"
        # print("self.listFN",[i.getfunctionname() for i in self.listFN])
        # print("self.listP",self.listP)
        print("formula", self.formulatranslation.formula)
        print("allexpressionlist",allexpressionlist)

        choosenexpression = random.choice(allexpressionlist)
        print("choosenexpression",choosenexpression)
        expressionoccurence = self.formulatranslation.formula.count(choosenexpression)
        # print("expressionoccurence",expressionoccurence)
        choosenvariable = random.choice(self.formulatranslation.availablevariables)

        # if random.random() > 0.5:
        #     replaceby = "fn{}({},p{})".format(str(len(self.formulatranslation.listFN) + 1), choosenvariable,
        #                                       len(self.formulatranslation.listP) + 1)
        # else:
        #     replaceby = "fn{}(p{},{})".format(str(len(self.formulatranslation.listFN) + 1),
        #                                       len(self.formulatranslation.listP) + 1, choosenvariable)

        addedfunction = random.choice(self.fnmanager.fnlist)
        randomparams = self.createrandomparams(random.randint(addedfunction.parameterrange[0], addedfunction.parameterrange[1]))

        #print("addedfunction",addedfunction)
        #print("randomparams",randomparams)
        replaceby = "fn{}(".format(str(len(self.formulatranslation.listFN) + 1))
        for i in randomparams:
            replaceby += i + ","
        replaceby = replaceby[0:-1] +")"
        #print("replaceby",replaceby)

        self.formulatranslation.listFN.append(addedfunction)
        # addedparameter = self.getrandomcomplex()
        # self.formulatranslation.listP.append(addedparameter)
        newformula = nth_repl(self.formulatranslation.formula, choosenexpression, replaceby, expressionoccurence)
        print("Old formula", self.formulatranslation.formula)
        self.formulatranslation.formula = newformula
        print("New formula", self.formulatranslation.formula)
        print("listP",self.formulatranslation.listP)
        return {'addedfunction': addedfunction, 'newformula': newformula,
                'choosenvariable': choosenvariable, 'listP':self.formulatranslation.listP}

    def crossfromPool(self,parameters=None):
        if not parameters is None:
            self.evo.formulatranslation.fromStandaloneFormula(parameters['saformula'])
            return
        #G = self.ftree.formulatograph(self.formulatranslation.formula)
        #Gcross = self.ftree.formulatograph(self.evo.formulapool.getindividualroulette().formula)

        formulaorigin = self.evo.formulatranslation.toStandaloneFormula()
        self.evo.formulatranslation.fromStandaloneFormula(formulaorigin)

        formulafrompool = self.evo.formulapool.getindividualroulette()

        formulaoriginformula = formulaorigin.formula
        shiftedformulafrompool = formulafrompool.shift_formula(len(formulaorigin.listFN),len(formulaorigin.listP),len(formulaorigin.listV))
        concatenatedFN = formulaorigin.listFN + formulafrompool.listFN
        concatenatedP = formulaorigin.listP + formulafrompool.listP
        concatenatedV = formulaorigin.listV + formulafrompool.listV
        concatenatedV = list(set(concatenatedV))
        print("formulaoriginformula", formulaoriginformula)
        print("formulafrompool",formulafrompool)
        print("shiftedformulafrompool",shiftedformulafrompool)
        print("concatenatedFN",concatenatedFN)
        print("concatenatedP",concatenatedP)
        print("concatenatedV",concatenatedV)
        crossedgraph = self.ftree.CrossTwoFormula(formulaoriginformula,shiftedformulafrompool)
        print("crossedgraph.edges",crossedgraph.edges)
        newformula = self.ftree.nx_graph_to_formula(crossedgraph)
        #self.ftree.drawgraph(crossedgraph)
        self.formulatranslation.formula = newformula
        self.formulatranslation.listFN = concatenatedFN
        #print("concatenatedP",concatenatedP)
        self.formulatranslation.listP = concatenatedP
        self.formulatranslation.listV = concatenatedV
        #saformula = StandAloneFormula(newformula,concatenatedFN,concatenatedP,concatenatedV)
        saformula = self.evo.formulatranslation.toStandaloneFormula()
        saformula.removedistinguishers()
        # Simplify with toStandalone and save change with fromStandalone
        self.evo.formulatranslation.fromStandaloneFormula(saformula)
        print("Crossed formula",self.evo.formulatranslation.formula)
        #self.formulatranslation.formula =
        #self.ftree.drawgraphformula(self.evo.formulatranslation.formula)
        return {'saformula': saformula}

    def pruneformula(self,parameters=None):
        if not parameters is None:
            self.formulatranslation.formula = parameters['newformula']
            return
        self.ispruning = True
        self.beforepruninggrade = self.evo.graphoperator.lastfractalentropy
        print("formulabeforegraph",self.formulatranslation.formula)
        G = self.ftree.formulatograph(self.formulatranslation.formula)
        G = self.ftree.trimRandomBranch(G)
        self.formulatranslation.formula = self.ftree.nx_graph_to_formula(G)
        return {'newformula':self.formulatranslation.formula}

