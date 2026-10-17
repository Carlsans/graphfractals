import copy
import os

import networkx as nx
import numpy as np
from numpy import ma

from GraphFractals.CustomFunctions.selectionsfunctions import image_entropy, image_compression_based_information
import GraphFractals.CustomFunctions.FractalFunctions as fn

from GraphFractals.Edges.Filter import Filter
from GraphFractals.Nodes.Discriminator import Discriminator
from GraphFractals.Nodes.GraphIterator import GraphIterator
from GraphFractals.Nodes.Initiator import Initiator
from GraphFractals.Nodes.Operator import Operator
from GraphFractals.Nodes.OperatorEvolutiveFormula import OperatorEvolutiveFormula
from GraphFractals.Nodes.Outputer import Outputer
from scipy.stats import entropy




class GraphDefinition:
    def __init__(self,fractalprocessing):
        self.fractalprocessing = fractalprocessing
        self.conf = fractalprocessing.conf
        self.sharedvalues = {}
        self.dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.setFrequentlyUsedVariables()
    def setFrequentlyUsedVariables(self):
        #self.funclist = fn.getallonevarfnlist()
        self.funclisttwoparam = fn.getalltwovarfnlist()
        self.funclist = ['ma.angle', 'ma.abs', 'ma.arccos', 'ma.arccosh', 'ma.arcsin', 'ma.arcsinh', 'ma.arctan',
                    'ma.arctanh', 'ma.cos', 'ma.cosh', 'ma.exp',
                    'ma.log', 'ma.log10', 'ma.log2'] + fn.getallonevarfnlist()
        self.funclisttwoparam =  fn.getalltwovarfnlist()

    def getGraphfromDefinition(self):
        return self.evolutivefractalgraph()

    def evolutivefractalgraph(self):

        # functioniterator.setcurrentiteratorvalues()
        coordinatesinitiator = Initiator(sharedvalues=self.sharedvalues, name="CoordinatesInitiator")
        #lowresfractalresolution = (64, 64)

        coordinatesinitiator.setValues(fractalresolution=self.conf.lowresfractalresolution,
                                       hiresfractalresolution=self.conf.resolution,lowresfractalresolution=self.conf.lowresfractalresolution, real=self.conf.limitreal,
                                       imag=self.conf.limitimag, fractaldtype=self.conf.dtype, minimumfractalentropystart = self.conf.minimumfractalentropystart,
                                       minimumfractalentropy = self.conf.minimumfractalentropystart, resetformula = False, evoiterations = 0,evoiterationsmax = self.conf.evoiterationsmax)
        initiator = Operator(sharedvalues=self.sharedvalues, name="Initiate basic variables")
        initiator.addFunction("c=getComplexCoordinates(fractalresolution,real,imag,fractaldtype)")
        #initiator.addFunction("noise=np.random.rand(fractalresolution[0],fractalresolution[1])*.2-.1")


        initiator.addFunction("z=ma.masked_array(copy.deepcopy(c), mask=np.zeros_like(c))")
        # initiator.addFunction("z=ma.zeros_like(c)")
        # z=ma.masked_array(copy.deepcopy(c), mask=np.zeros_like(c))
        initiator.addFunction("i=0")
        initiator.addFunction("hasdropped=ma.ones_like(c, dtype=np.bool_)")
        initiator.addFunction("fractalresult=np.zeros_like(c, dtype=np.int32) - 1")

        fractal1 = OperatorEvolutiveFormula(sharedvalues=self.sharedvalues, name="Fractal1")

        #fractal1.addFunction("z = z + (i % 2 == 1) * npfunc3(-npfunc2(z)  + p1 , npfunc(z+1)  - p2)")
        #fractal1.addFunction("z = z + (i % 2 == 0) * npfunc3( npfunc(z-1)  - p1 , -npfunc2(z)  + p2)")
        # fractal1.addFunction("z = npfunc2(z,z)")  # npfunc()

        fractal1.addFunction("i = i + 1")

        # fractal1.addFunction("printp1 = print('P111',p1)")

        # newdrop = np.all([dropout,hasdropped],axis=0)
        stddropout = Operator(sharedvalues=self.sharedvalues, name="Dropout Operator")
        stddropout.addFunction("dropout = (z.real * z.real)+(z.imag * z.imag) > 8")

        newdrop = Operator(sharedvalues=self.sharedvalues, name="FractalIterator")
        newdrop.addFunction("newdrop = np.all([dropout,hasdropped],axis=0)")
        newdrop.addFunction("z[newdrop] = ma.masked")
        newdrop.addFunction("fractalresult[newdrop] = i")
        newdrop.addFunction("hasdropped = dropout")

        enddiscriminator = Discriminator(sharedvalues=self.sharedvalues, name="MaxIterDiscriminator")

        enddiscriminator.addFunction("i < " + str(self.conf.maxiter), 20, 60, )

        entropycalc = Operator(sharedvalues=self.sharedvalues, name="Entropy Calculator")
        #entropycalc.addFunction("fractalentropy = image_comparision_loss(fractalresult)")
        entropycalc.addFunction("fractalentropy = image_compression_based_information(fractalresult)")
        entropycalc.addFunction("evoiterations = evoiterations + 1")
        entropydiscriminator = Discriminator(sharedvalues=self.sharedvalues, name="EntropyDiscriminator")
        entropydiscriminator.addFunction("i > 10000", 10,None)
        entropydiscriminator.addFunction("fractalresolution == hiresfractalresolution", 70,None)
        entropydiscriminator.addFunction("math.isnan(fractalentropy)", 10, None)
        entropydiscriminator.addFunction("fractalentropy < minimumfractalentropy", 10, 67)
        setlowres = Operator(sharedvalues=self.sharedvalues, name="Set Hi-Res and Update Entropy")
        setlowres.addFunction("fractalresolution = lowresfractalresolution")
        setlowres.addFunction("minimumfractalentropy = minimumfractalentropy + " + str(self.conf.entropyraise))
        setlowres.addFunction("resetformula = minimumfractalentropy > "+str(self.conf.maximumfractalentropystop))
        setlowres.addFunction("evoiterations = 0")
        sethires = Operator(sharedvalues=self.sharedvalues, name="Set Hi-Res")
        sethires.addFunction("fractalresolution = hiresfractalresolution")
        sethires.addFunction("achime = chime.success()")
        outputnode = Outputer(sharedvalues=self.sharedvalues, name="Output")
        outputnode.setOutputVariable("fractalresult")
        outputnode.setLogVariable("fractalentropy")
        outputnode.setLogVariable("minimumfractalentropy")
        outputnode.setLogVariable("evolutivefunction")
        outputnode.setLogVariable("evoiterations")
        # outputnode.setLogVariable("npfunc3")
        # outputnode.setLogVariable("p1")
        # outputnode.setLogVariable("p2")

        endnode = Operator(sharedvalues=self.sharedvalues, name="End Node")
        # filteredge = Filter(name="Output Filter 1")
        # filteredge.addFilter("fractalresult as fractal1")
        # filteredge.addFilter("npfunc_parameter as npfunc_parameter")
        # filteredge.addFilter("npfunc2_parameter as npfunc2_parameter")
        # filteredge.addFilter("npfunc3_parameter as npfunc3_parameter")
        # filteredge.addFilter("npfunc as npfunc")

        G = nx.DiGraph()

        G.add_nodes_from(
            [(5, {'object': coordinatesinitiator}), (10, {'object': initiator}), (20, {'object': fractal1}),
             (30, {'object': stddropout}), (40, {'object': newdrop}), (50, {'object': enddiscriminator}),
             (60, {'object': entropycalc}), (65, {'object': entropydiscriminator}), (67, {'object': sethires}),
             (70, {'object': outputnode}),(75, {'object': setlowres}), (80, {'object': endnode})])

        # G.add_nodes_from([(200,{'object': npfunciterator,'restartgraph': "something"})])
        # G.add_nodes_from([(1,{'fn':np.arcsin}),(2,{'fn':np.tan}),(3,{'fn':np.cos}),(4,{'fn':np.square}),(5,{'fn':np.add})])

        G.add_edges_from(
            [(5, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 20), (50, 60), (60, 65), (65, 70),(65, 10),
             (65, 67), (67, 10),(70,75),(75,10)])

        startingnode = 5
        return G, startingnode
    def singlefractalgraph(self):
        functioniterator = GraphIterator(sharedvalues=self.sharedvalues, name="Functioniterator")
        functioniterator.addIterator(npfunc=self.funclist)
        functioniterator.addIterator(npfunc2=self.funclist)
        functioniterator.addIterator(npfunc3=self.funclisttwoparam)
        # functioniterator.addIterator(npfunc2=self.funclisttwoparam)
        functioniterator.addIterator(p1=list(np.random.uniform(-1, 1, 10) + 1.j * np.random.uniform(-1, 1, 10)))
        functioniterator.addIterator(p2=list(np.random.uniform(-1, 1, 10) + 1.j * np.random.uniform(-1, 1, 10)))

        # functioniterator.setcurrentiteratorvalues()
        coordinatesinitiator = Initiator(sharedvalues=self.sharedvalues, name="CoordinatesInitiator")
        lowresfractalresolution = (64, 64)
        coordinatesinitiator.setValues(fractalresolution=lowresfractalresolution,
                                       hiresfractalresolution=self.conf.resolution, real=self.conf.limitreal,
                                       imag=self.conf.limitimag, fractaldtype=self.conf.dtype)
        initiator = Operator(sharedvalues=self.sharedvalues, name="Initiate basic variables")
        initiator.addFunction("c=getComplexCoordinates(fractalresolution,real,imag,fractaldtype)")
        initiator.addFunction("z=ma.masked_array(copy.deepcopy(c), mask=np.zeros_like(c))")
        # initiator.addFunction("z=ma.zeros_like(c)")
        # z=ma.masked_array(copy.deepcopy(c), mask=np.zeros_like(c))
        initiator.addFunction("i=0")
        initiator.addFunction("hasdropped=ma.ones_like(c, dtype=np.bool_)")
        initiator.addFunction("fractalresult=np.zeros_like(c, dtype=np.int32) - 1")
        # initiator = Initiator(sharedvalues=self.sharedvalues, name="STDInitiator")
        # initialcoordinates = self.fractalprocessing.getComplexCoordinates()
        # initiator.setValues("z=ma.zeros_like(resolution)","c=copy.deepcopy(resolution)")
        # initiator.setValues(z=ma.zeros_like(resolution), c=copy.deepcopy(resolution), i=0,
        #                     hasdropped=ma.ones_like((resolution), dtype=np.bool_),
        #                     fractalresult=np.zeros_like(resolution, dtype=np.int32) - 1)

        # npfunciterator = Operator(name="Numpy iterator")
        # npfunciterator.addFunction("if npfunc is None")
        # npfunciterator.addFunction("npfunc = npfunc + 1")
        fractal1 = Operator(sharedvalues=self.sharedvalues, name="Fractal1")

        fractal1.addFunction("z = z + (i % 2 == 1) * npfunc3(-npfunc2(z)  + p1 , npfunc(z+1)  - p2)")
        fractal1.addFunction("z = z + (i % 2 == 0) * npfunc3( npfunc(z-1)  - p1 , -npfunc2(z)  + p2)")
        # fractal1.addFunction("z = npfunc2(z,z)")  # npfunc()

        fractal1.addFunction("i = i + 1")
        # fractal1.addFunction("printp1 = print('P111',p1)")

        # newdrop = np.all([dropout,hasdropped],axis=0)
        stddropout = Operator(sharedvalues=self.sharedvalues, name="Dropout Operator")
        stddropout.addFunction("dropout = (z.real * z.real)+(z.imag * z.imag) > 4")

        newdrop = Operator(sharedvalues=self.sharedvalues, name="FractalIterator")
        newdrop.addFunction("newdrop = np.all([dropout,hasdropped],axis=0)")

        # fractal[newdrop] = np.nan
        # fractalresult[newdrop] = i
        # hasdropped = dropout

        # newdrop.addFunction("z[newdrop] = np.nan + 1j * np.nan")
        newdrop.addFunction("z[newdrop] = ma.masked")
        # newdrop.addFunction("c[newdrop] = ma.masked")
        # newdrop.addFunction("z[newdrop] = np.NA")
        newdrop.addFunction("fractalresult[newdrop] = i")
        newdrop.addFunction("hasdropped = dropout")

        enddiscriminator = Discriminator(sharedvalues=self.sharedvalues, name="MaxIterDiscriminator")

        enddiscriminator.addFunction("i < " + str(self.conf.maxiter), 20, 60, )

        entropycalc = Operator(sharedvalues=self.sharedvalues, name="Entropy Calculator")
        entropycalc.addFunction("fractalentropy = image_comparision_loss(fractalresult)")
        entropydiscriminator = Discriminator(sharedvalues=self.sharedvalues, name="EntropyDiscriminator")
        entropydiscriminator.addFunction("fractalresolution == hiresfractalresolution", 70)
        entropydiscriminator.addFunction("math.isnan(fractalentropy)", 80, None)
        entropydiscriminator.addFunction("fractalentropy < 0.2", 80, 67)
        sethires = Operator(sharedvalues=self.sharedvalues, name="Set Hi-Res")
        sethires.addFunction("fractalresolution = hiresfractalresolution")
        sethires.addFunction("achime = chime.success()")
        outputnode = Outputer(sharedvalues=self.sharedvalues, name="Output")
        outputnode.setOutputVariable("fractalresult")
        outputnode.setLogVariable("fractalentropy")
        outputnode.setLogVariable("npfunc")
        outputnode.setLogVariable("npfunc2")
        outputnode.setLogVariable("npfunc3")
        outputnode.setLogVariable("p1")
        outputnode.setLogVariable("p2")

        endnode = Operator(sharedvalues=self.sharedvalues, name="End Node")
        # filteredge = Filter(name="Output Filter 1")
        # filteredge.addFilter("fractalresult as fractal1")
        # filteredge.addFilter("npfunc_parameter as npfunc_parameter")
        # filteredge.addFilter("npfunc2_parameter as npfunc2_parameter")
        # filteredge.addFilter("npfunc3_parameter as npfunc3_parameter")
        # filteredge.addFilter("npfunc as npfunc")

        G = nx.DiGraph()
        G.add_nodes_from([(1, {'object': functioniterator})])
        G.add_nodes_from(
            [(5, {'object': coordinatesinitiator}), (10, {'object': initiator}), (20, {'object': fractal1}),
             (30, {'object': stddropout}), (40, {'object': newdrop}), (50, {'object': enddiscriminator}),
             (60, {'object': entropycalc}), (65, {'object': entropydiscriminator}), (67, {'object': sethires}),
             (70, {'object': outputnode}), (80, {'object': endnode})])

        # G.add_nodes_from([(200,{'object': npfunciterator,'restartgraph': "something"})])
        # G.add_nodes_from([(1,{'fn':np.arcsin}),(2,{'fn':np.tan}),(3,{'fn':np.cos}),(4,{'fn':np.square}),(5,{'fn':np.add})])
        G.add_edges_from([(1, 5)])
        G.add_edges_from(
            [(5, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 20), (50, 60), (60, 65), (65, 80), (65, 70),
             (65, 67), (67, 10)])

        startingnode = 1
        return G, startingnode
    def superposedfractalsgraph(self):
        # class MandelInit(Initiator):
        #     def setValues(self,c):
        #         self.z = 0
        #         self.c = c

        functioniterator = GraphIterator(sharedvalues=self.sharedvalues, name="Functioniterator")
        functioniterator.addIterator(npfunc=self.funclist)
        functioniterator.addIterator(npfunc2=self.funclist)
        functioniterator.addIterator(npfunc3=self.funclisttwoparam)
        # functioniterator.setcurrentiteratorvalues()

        initiator = Initiator(sharedvalues=self.sharedvalues, name="STDInitiator")
        initialcoordinates = self.fractalprocessing.getComplexCoordinates()

        initiator.setValues(z=ma.zeros_like(initialcoordinates), c=copy.deepcopy(initialcoordinates), i=0,
                            hasdropped=ma.ones_like((initialcoordinates), dtype=np.bool_),
                            fractalresult=np.zeros_like(initialcoordinates, dtype=np.int32) - 1)
        initiator2 = copy.deepcopy(initiator)

        # npfunciterator = Operator(name="Numpy iterator")
        # npfunciterator.addFunction("if npfunc is None")
        # npfunciterator.addFunction("npfunc = npfunc + 1")
        fractal1 = Operator(sharedvalues=self.sharedvalues, name="Fractal1")

        fractal1.addFunction("z = npfunc3(npfunc(z*z)+c)")  # npfunc()
        fractal1.addFunction("i = i + 1")
        fractal2 = Operator(sharedvalues=self.sharedvalues, name="Fractal2")
        fractal2.addFunction("z = npfunc2(z*z)+c")
        fractal2.addFunction("i = i + 1")

        # newdrop = np.all([dropout,hasdropped],axis=0)
        stddropout = Operator(sharedvalues=self.sharedvalues, name="Dropout Operator")
        stddropout.addFunction("dropout = (z.real * z.real)+(z.imag * z.imag) > 4")

        newdrop = Operator(sharedvalues=self.sharedvalues, name="FractalIterator")
        newdrop.addFunction("newdrop = np.all([dropout,hasdropped],axis=0)")

        # fractal[newdrop] = np.nan
        # fractalresult[newdrop] = i
        # hasdropped = dropout

        # newdrop.addFunction("z[newdrop] = np.nan + 1j * np.nan")
        newdrop.addFunction("z[newdrop] = ma.masked")
        # newdrop.addFunction("c[newdrop] = ma.masked")
        # newdrop.addFunction("z[newdrop] = np.NA")
        newdrop.addFunction("fractalresult[newdrop] = i")
        newdrop.addFunction("hasdropped = dropout")

        enddiscriminator = Discriminator(sharedvalues=self.sharedvalues, name="MaxIterDiscriminator")

        enddiscriminator.addFunction("i < " + str(self.conf.maxiter), 20, 60)
        enddiscriminator2 = Discriminator(sharedvalues=self.sharedvalues, name="MaxIterDiscriminator")
        enddiscriminator2.addFunction("i < " + str(self.conf.maxiter), 120, 60)
        outputnode = Outputer(sharedvalues=self.sharedvalues, name="Output")
        outputnode.setOutputVariable("fractal")
        outputnode.setLogVariable("npfunc")
        outputnode.setLogVariable("npfunc2")
        outputnode.setLogVariable("npfunc3")
        filteredge = Filter(name="Output Filter 1")
        filteredge.addFilter("fractalresult as fractal1")
        # filteredge.addFilter("npfunc_parameter as npfunc_parameter")
        # filteredge.addFilter("npfunc2_parameter as npfunc2_parameter")
        # filteredge.addFilter("npfunc3_parameter as npfunc3_parameter")
        # filteredge.addFilter("npfunc as npfunc")
        filteredge2 = Filter(name="Output Filter 2")
        filteredge2.addFilter("fractalresult as fractal2")
        outputedge = Filter(name="Final output Filter")
        # outputedge.addFilter("npfunc_parameter as npfunc_parameter")
        # outputedge.addFilter("npfunc2_parameter as npfunc2_parameter")
        # outputedge.addFilter("npfunc3_parameter as npfunc3_parameter")
        fractaladder = Operator(sharedvalues=self.sharedvalues, name="Adder")
        fractaladder.addFunction("fractal = fractal2 + fractal1")

        G = nx.DiGraph()
        G.add_nodes_from([(5, {'object': functioniterator})])
        G.add_nodes_from([(10, {'object': initiator}), (20, {'object': fractal1}), (30, {'object': stddropout}),
                          (40, {'object': newdrop}), (50, {'object': enddiscriminator}),
                          (60, {'object': fractaladder})])
        G.add_nodes_from([(110, {'object': initiator2}), (120, {'object': fractal2}), (130, {'object': stddropout}),
                          (140, {'object': newdrop}), (150, {'object': enddiscriminator2}),
                          (160, {'object': outputnode})])
        # G.add_nodes_from([(200,{'object': npfunciterator,'restartgraph': "something"})])
        # G.add_nodes_from([(1,{'fn':np.arcsin}),(2,{'fn':np.tan}),(3,{'fn':np.cos}),(4,{'fn':np.square}),(5,{'fn':np.add})])
        G.add_edges_from([(5, 10), (5, 110)])
        G.add_edges_from([(10, 20), (20, 30), (30, 40), (40, 50), (50, 20), (50, 60, {'object': filteredge})])
        G.add_edges_from(
            [(110, 120), (120, 130), (130, 140), (140, 150), (150, 120), (150, 60, {'object': filteredge2}), (60, 160)])
        # G.add_edges_from([(160,5)])#, {'object': outputedge})])

        startingnode = 5
        return G,startingnode

