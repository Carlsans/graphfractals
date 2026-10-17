from abc import ABC, abstractmethod
class Initiator():
    def __init__(self,sharedvalues,verbose = False,name=__name__):
        self.sharedvalues = sharedvalues
        self.verbose = verbose
        self.name = name
        self.color = "#0000FF"
    def getName(self):
        return self.name

    def getColor(self):
        return self.color
    def getProperties(self):
        returnvalue = ""
        for key, value in self.values.items():
            returnvalue += str(key) + "\n"
        return returnvalue

    def getValues(self):
        returndict ={}
        returndict.update(self.values)
        returndict.update(self.sharedvalues)
        return returndict
    def setValues(self,*args,**kwargs):
        print(args)
        print(kwargs)
        self.startupvalues = kwargs
        self.values = kwargs

    def processNode(self,lastnode):
        print("Process node",lastnode)

        if not lastnode is None:
           self.precedentnodes = lastnode['nodereturnstate']
           self.values.update(self.precedentnodes.values)
           # The initiator always come back to the values it had been initiated to
           self.values.update(self.startupvalues)


    def applyNode(self):
        return {'nodereturnstate': self, 'nextnodechoice': -1}
    def __str__(self):
        returnvalue = ""
        for key, value in self.values.items():
            returnvalue += "key=" + str(key) + " value="+str(value) +"\n"
            # print("%s == %s" % (key, value))
        return returnvalue
    def printnodecontent(self):
        if self.verbose:
            print(self)