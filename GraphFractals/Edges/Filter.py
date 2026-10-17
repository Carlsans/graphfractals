class Filter:
    def __init__(self,verbose = False,name=__name__):
        self.verbose = verbose
        self.name = name
        self.color = "#00FF00"
        self.filterlist = []
    def getName(self):
        return self.name
    def getProperties(self):
        returnvalue = "\n"
        for afilter in self.filterlist:
            returnvalue += afilter + "\n"
        return returnvalue
    def addFilter(self,filter):
        self.filterlist.append(filter)
    def processFilters(self,precedentnodesvalues):
        returnvaluedict = {}
        for filter in self.filterlist:
            oldvariable, newvariable = filter.split("as", 1)
            oldvariable, newvariable = oldvariable.strip(), newvariable.strip()
            print("precedentnodesvalues",precedentnodesvalues[oldvariable])
            returnvaluedict[newvariable] = precedentnodesvalues[oldvariable]
        return returnvaluedict
    def processEdge(self, lastnode):
        self.precedentnodes = lastnode['nodereturnstate']
        self.values = self.processFilters(self.precedentnodes.values)
        return {'nodereturnstate': self, 'nextnodechoice': -1}