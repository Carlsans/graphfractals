from GraphFractals.EvolutiveFormula.StandAloneFormula import StandAloneFormula


class FormulaTranslation:
    def __init__(self,evo):
        self.evo = evo
        self.listV = ['z', 'c']
        self.availablevariables = ['z', 'c']
        self.listP = []
        self.listFN = []
        self.listSymbols = ['O','Z']
        self.formula = ""

    def translateformula(self):
        fnfromformula = self.getfnfromformula()
        fnfromformula.sort(reverse=True)
        #print(fnfromformula)
        pfromformula = self.getpfromformula()
        pfromformula.sort(reverse=True)
        #print(pfromformula)
        rewroteformula = self.formula
        for i in fnfromformula:
            rewroteformula = rewroteformula.replace("fn"+str(i),self.listFN[i-1].functionname)
        #print(rewroteformula)
        for i in pfromformula:
            rewroteformula = rewroteformula.replace("p" + str(i), str(self.listP[i - 1]))
        #print(rewroteformula)
        rewroteformula = rewroteformula.replace("Z", "fn.one()")
        rewroteformula = rewroteformula.replace("O", "fn.zero()")
        print("rewroteformula",rewroteformula)
        return rewroteformula
    def getfnfromformula(self,showfn=False):
        isrecording=False
        fn = ""
        fnlist = []

        for i in self.formula:
            if i == 'f':
                isrecording = True
                continue
            if i == 'n':
                continue
            if isrecording and i.isnumeric():
                fn += i
            if isrecording and not i.isnumeric():
                isrecording = False
                if showfn:
                    fnlist.append("fn"+fn)
                else:
                    fnlist.append(int(fn))
                fn = ""
        return fnlist

    def setFunctionParameters(self,function, parameters):
        functionindex = self.formula.find(function)
        parenthesis = None
        paramstoreplace = ""
        for i in self.formula[functionindex:]:
            if parenthesis is None and i == '(':
                parenthesis = 1
            elif not parenthesis is None and i == '(':
                parenthesis += 1
            if i == ")":
                parenthesis -= 1
            if parenthesis == 0:
                paramstoreplace += i
                break
            if not parenthesis is None:
                paramstoreplace += i
        #print("paramstoreplace",paramstoreplace)
        replacebyparams = "("
        for i in parameters:
            replacebyparams += i + ','
        replacebyparams = replacebyparams[0:-1] + ')'
        #print("replacebyparams",replacebyparams)
        formulabefore = self.formula[:functionindex]
        formulaafter = self.formula[functionindex:]
        formulaafter = formulaafter.replace(paramstoreplace,replacebyparams,1)
        self.formula = formulabefore + formulaafter
        print(self.formula)

        #self.formula = self.formula.replace(paramstoreplace,replacebyparams)

    def getFunctionParameters(self,function):
        print("function",function)
        functionindex = self.formula.find(function)
        parameters = ""
        parenthesis = None
        for i in self.formula[functionindex:]:
            if parenthesis is None and i == '(':
                parenthesis=1
            elif not parenthesis is None and i == '(':
                parenthesis+=1
            if i == ")":
                parenthesis-=1
            if parenthesis == 0:
                parameters += i
                break
            if not parenthesis is None:
                parameters += i
        #print("self.formula",self.formula)
        #print(parameters)
        return self.functionparameterstolist(parameters)

    def functionparameterstolist(self,parameters):
        parameters = parameters[1:-1]
        currentparam = ""
        paramslist = []
        parenthesis = 0
        for i in parameters:
            if i == "(":
                parenthesis+=1
            if i == ")":
                parenthesis-=1
            if i == "," and parenthesis == 0:
                paramslist.append(currentparam)
                currentparam = ""
                continue
            currentparam += i
        paramslist.append(currentparam)
        return paramslist

    def isZpresent(self):
        return 'Z' in self.formula
    def isOpresent(self):
        return 'O' in self.formula
    def getpAll(self):
        return ["p" + str(i + 1) for i in range(len(self.listP))]
    def doesPexist(self,index):
        if index > len(self.listP)-1:
            return False
        return True
    def addPatend(self,value):
        self.listP.append(value)
        return len(self.listP)-1
    def setPat(self,index,pvalue):
        if index > len(self.listP)-1:
            # Add blanks
            blanks = abs(len(self.listP) - 1 - index)
            for i in range(blanks):
                self.listP.append(0+0j)
        self.listP[index] = pvalue
    def getpfromformula(self,addp = False):
        isrecording = False
        p = ""
        plist = []

        for i in self.formula:
            if i == 'p':
                isrecording = True
                continue
            if isrecording and i.isnumeric():
                p += i
            if isrecording and not i.isnumeric():
                isrecording = False
                if addp:
                    plist.append("p"+str(int(p)))
                else:
                    plist.append(int(p))
                p = ""
        return plist
    def getvAll(self):
        return self.listV
    def getvfromformula(self):

        vlist = []

        for i in self.formula:
            if i in self.availablevariables:
                if i not in vlist:
                    vlist.append(i)

        return vlist

    def fromStandaloneFormula(self,saformula):
        self.formula = saformula.formula
        self.listFN = saformula.listFN
        self.listP = saformula.listP
        self.listV = saformula.listV

    def toStandaloneFormula(self):
        print("self.formula,self.listFN,self.listP,self.listV",self.formula,self.listFN,self.listP,self.listV)
        print("self.getfnfromformula(showfn=True),self.getpfromformula(addp=True),self.getvfromformula()",self.getfnfromformula(showfn=True),self.getpfromformula(addp=True),self.getvfromformula())
        print("self.translateformula()",self.translateformula())
        fnnamelist = sorted(list(set(self.getfnfromformula(showfn=False))))
        fnnamelist = ["fn" + str(i) for i in fnnamelist]
        fnindex = sorted(list(set(self.getfnfromformula(showfn=False))))
        pnamelist = sorted(list(set(self.getpfromformula(addp=False))))
        pnamelist = ["p" + str(i) for i in pnamelist]
        pindex = sorted(list(set(self.getpfromformula(addp=False))))
        vlist = sorted(list(set(self.getvfromformula())))
        print("fnnamelist,pnamelist,vlist",fnnamelist,pnamelist,vlist)
        print("fnindex,pindex",fnindex,pindex)
        # Get current used fn and p values
        fnvalues = [self.listFN[i-1] for i in fnindex]
        pvalues = [self.listP[i-1] for i in pindex]
        print("fnvalues",[self.listFN[i-1].getfunctionname() for i in fnindex])
        print("pvalues",pvalues)
        rewroteformula = self.formula
        n = len(fnnamelist)
        print("origin formula",self.formula)
        print("len(fnnamelist)",len(fnnamelist))
        for i in reversed(fnnamelist):
            rewroteformula = rewroteformula.replace(i,'UfnU'+str(n))
            print("fnrewriting",rewroteformula)
            n-=1
        n = len(pnamelist)
        print("origin formula", self.formula)
        print("len(pnamelist)",len(pnamelist))
        for i in reversed(pnamelist):
            rewroteformula = rewroteformula.replace(i, 'UpU' + str(n))
            print("prewriting", rewroteformula)
            n-=1
        rewroteformula = rewroteformula.replace("U","")
        print("rewroteformula",rewroteformula)
        return StandAloneFormula(rewroteformula,fnvalues,pvalues,vlist,self.listSymbols)
