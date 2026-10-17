from matplotlib import pyplot as plt


class EvolutiveFunction:
    def __init__(self,functionmanager,functioncall,functionname,parameterrange,paramsfollowable=False,addtofnlist=True):
        self.functionmanager = functionmanager
        if addtofnlist:
            self.functionmanager.fnlist.append(self)
        self.functioncall = functioncall
        self.functionname = functionname
        if type(parameterrange) is tuple:
            self.parameterrange = parameterrange
        elif isinstance(parameterrange, (int)):
            self.parameterrange = (parameterrange,parameterrange)
        else:
            print("Evolutive function parameter range must be a tuple or an int")
            raise
        self.paramsfollowable = paramsfollowable
    def __call__(self, *args, **kwargs):

        return self.callfunction(*args)
    def __str__(self):
        return self.functionname
    def areparamsvalids(self,parametercount):
        return parametercount >= self.parameterrange[0] and parametercount <= self.parameterrange[1]
    def getfunctionname(self):
        return self.functionname
    def callfunction(self,*args):

        if not (self.areparamsvalids(len(args)) or self.paramsfollowable ):
            #print("Invalid number of argument when calling evolutive function")
            print("Invalid number of argument when calling evolutive function :" + str(self.functionname))
            plt.show()
            raise Exception("Invalid number of argument when calling evolutive function :" + str(self.functionname))
        if self.paramsfollowable:
            if len(args)<2:
                return args[0]
            answer = self.functioncall(args[0], args[1])
            for i in range(2,len(args)):
                answer = self.functioncall(answer, args[i])
            return answer
        else:
            return self.functioncall(*args)

