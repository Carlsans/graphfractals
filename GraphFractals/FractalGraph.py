import copy
import sys

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
#from numpy import NA as NA
from matplotlib.patches import ArrowStyle

from GraphFractals.Edges.Filter import Filter
from GraphFractals.GraphDefinition import GraphDefinition
from GraphFractals.Nodes.Discriminator import Discriminator
from GraphFractals.Nodes.GraphIterator import GraphIterator
from GraphFractals.Nodes.Initiator import Initiator
from GraphFractals.Nodes.Operator import Operator
from GraphFractals.Nodes.Outputer import Outputer


class FractalGraph:
    def __init__(self,fractalprocessing):

        self.fractalprocessing = fractalprocessing
        self.conf = fractalprocessing.conf
        self.setGraph()
    def drawGraph(self):
        #subax1 = plt.subplot(121)
        #nx.draw(self.G, with_labels=True, font_weight='bold')
        figure = plt.figure(figsize=(14, 8))

        labelsname = self.getGraphlabelsname()
        propertylabelsname = self.getGraphpropertylabelsname()
        nodescolor = self.getNodeColors()
        nodepos = nx.circular_layout(self.G)
        nodepos = nx.rescale_layout_dict(nodepos, 1.5)
        commentshift = -.2
        #nodepos = {x:[nodepos[x][0],nodepos[x][1]+1] for x in nodepos}
        shiftedpos = {x:[nodepos[x][0],nodepos[x][1]+commentshift] for x in nodepos}

        #shiftedpos = nx.rescale_layout_dict(shiftedpos, 1.2)
        print(nodepos)
        print(shiftedpos)

        nx.draw(self.G,pos=nodepos) #label
        #print(nx.circular_layout(self.G))
        nx.draw_networkx_nodes(self.G,pos=nodepos,node_color=nodescolor)
        nx.draw_networkx_labels(self.G, pos=nodepos,labels = labelsname)
        nx.draw_networkx_labels(self.G, pos=shiftedpos, labels=propertylabelsname,font_size=8)
        nx.draw_networkx_edges(self.G, pos=nodepos,arrowsize=30,arrowstyle= ArrowStyle.CurveB())
        nx.draw_networkx_edge_labels(self.G,pos=nodepos,edge_labels=self.getGraphEdgeslabelsname())
        plt.xlim(-2, 2)
        plt.ylim(-2,2)
        plt.show()

    def getGraphlabelsname(self):
        nodelist = list(self.G.nodes)
        labelsdict = {}
        for i in nodelist:
            try:
                labelsdict[i] = self.G.nodes[i]['object'].getName()
            except KeyError:
                print("Object not existant for node",i)
        return labelsdict
    def getGraphEdgeslabelsname(self):
        edgelist = list(self.G.edges)
        labelsdict = {}
        for i in edgelist:
            if "object" in self.G.edges[i]:
                labelsdict[i] = self.G.edges[i]['object'].getName() + self.G.edges[i]['object'].getProperties()
            else:
                labelsdict[i] = ""
        return labelsdict
    def getGraphpropertylabelsname(self):
        nodelist = list(self.G.nodes)
        labelsdict = {}
        for i in nodelist:

            labelsdict[i] = self.G.nodes[i]['object'].getProperties()

        return labelsdict
    def getNodeColors(self):
        nodelist = list(self.G.nodes)
        colorlist = []
        for i in nodelist:
            colorlist.append(self.G.nodes[i]['object'].getColor())
        return colorlist
    def setGraph(self):

        graphdefinition = GraphDefinition(self.fractalprocessing)
        self.G,self.startingnode = graphdefinition.getGraphfromDefinition()

        if self.conf.drawgraph :
            self.drawGraph()
        self.processgraph(startingnode=self.startingnode)
        #currentnode = 1

    def travelgraph(self,nodetoprocess,lastnodemessage,startingnode):
        n = 0
        if nodetoprocess is None and not startingnode == -1:
            nodetoprocess = self.getOrphanNodeList()
        if startingnode > 0:
            if self.isnodepartofCycle(startingnode):
                print("The starting node", startingnode, self.G.nodes[startingnode]['object'].getName(),
                      "cant be part of a cycle......")
                exit()
            nodetoprocess = [startingnode]
        lastnodemessagebackup = lastnodemessage
        # On utilise chaque node orphelin comme point de depart du calcul d'un graph
        for currentnode in nodetoprocess:
            reachedend = False
            lastnodeid = -1
            lastnodemessage = lastnodemessagebackup
            # if not graphlastnode is None:
            #
            #     lastnodemessage = graphlastnode['object']
            #     print("graphlastnodemessage",lastnodemessage)
            while not reachedend:
                # print(self.G.nodes[currentnode],currentnode)
                # print(self.G.nodes[currentnode]['object'])
                print("lastnodeid,currentnode", lastnodeid, currentnode)
                hasmorethanonepredecessor = len(list(self.G.predecessors(currentnode))) > 1
                print("hasmorethanonepredecessor", hasmorethanonepredecessor, list(self.G.predecessors(currentnode)))

                if 'visitedby' in self.G.nodes[currentnode]:
                    print("Has been visited by", self.G.nodes[currentnode]['visitedby'])
                if hasmorethanonepredecessor:
                    if not self.isnodepartofCycle(currentnode):
                        if not 'visitedby' in self.G.nodes[currentnode]:
                            self.G.nodes[currentnode]['visitedby'] = [lastnodeid]
                        elif not lastnodeid in self.G.nodes[currentnode]['visitedby']:
                            self.G.nodes[currentnode]['visitedby'].append(lastnodeid)
                        else:
                            print("Attempted to visit this node twice")
                    # print(list(self.G.predecessors(currentnode)))
                    print("resultat", list(self.G.nodes[currentnode]))
                    # print(list(nx.simple_cycles(G)))
                # self.G.nodes[1]["foo"] = "bar"
                # Apply edge
                if not lastnodeid == -1:
                    print("Apply edge :", lastnodeid, currentnode)
                    if 'object' in self.G.edges[lastnodeid, currentnode]:
                        print("blim", self.G.edges[lastnodeid, currentnode]['object'])
                        lastnodemessage = self.G.edges[lastnodeid, currentnode]['object'].processEdge(lastnodemessage)
                # Apply Node
                print("Apply node :", currentnode)
                print("Node predecessors: ", list(self.G.predecessors(currentnode)))

                self.G.nodes[currentnode]['object'].processNode(lastnodemessage)

                if not hasmorethanonepredecessor or self.isnodepartofCycle(currentnode):
                    print(not hasmorethanonepredecessor, self.isnodepartofCycle(currentnode))
                    nodeanswer = self.G.nodes[currentnode]['object'].applyNode()
                elif not "visitedby" in self.G.nodes[
                    currentnode]:  # or len(list(self.G.predecessors(currentnode))) < len(self.G.nodes[currentnode]['visitedby']):
                    print("0 /", len(list(self.G.predecessors(currentnode))),
                          "nodes visited. Waiting to apply current node")
                else:
                    reachedend = True
                    print(len(self.G.nodes[currentnode]['visitedby']), "/", len(list(self.G.predecessors(currentnode))),
                          "nodes visited. Waiting to apply current node")
                    if len(list(self.G.predecessors(currentnode))) == len(self.G.nodes[currentnode]['visitedby']):
                        print("Has been visited by all predecessors. Applying node and clearing visitedby")
                        self.G.nodes[currentnode]['visitedby'] = []
                        nodeanswer = self.G.nodes[currentnode]['object'].applyNode()
                        reachedend = False

                # print("self.G.edge",self.G.edges([currentnode]))
                lastnodemessage = nodeanswer
                lastnodeid = currentnode
                self.G.nodes[currentnode]['object'].printnodecontent()
                # print(nodeanswer)
                # {'nodereturnstate': self, 'nextnodechoice': -1}
                # Si aucun choix n<est determine par le node actuel
                if nodeanswer['nextnodechoice'] == -1:
                    successor = list(self.G.successors(currentnode))
                    if len(successor) > 1:
                        # self.processgraph(nodetoprocess=successor, lastnodemessage=lastnodemessage)
                        #nodetoprocess = None, lastnodemessage = None, startingnode = -1
                        return successor, lastnodemessage, -1



                        # print("Multiple successors are not supported for this node type. Use a discriminator.")
                        # print(successor)
                        # exit()
                    if len(successor) == 0:
                        if 'restartgraph' in self.G.nodes[currentnode]:
                            #self.processgraph(self.G.nodes[currentnode])
                            nodetoprocess = self.G.nodes[currentnode]
                            lastnodemessage = None
                            startingnode = -1
                            return nodetoprocess, lastnodemessage, startingnode
                        if not self.hasalliteratorsnodesended():
                            print("self.startingnode", self.startingnode)
                            # nodetoprocess = None, lastnodemessage = None, startingnode = -1
                            #self.processgraph(startingnode=self.startingnode)
                            nodetoprocess = None
                            lastnodemessage = None
                            startingnode = self.startingnode
                            return nodetoprocess, lastnodemessage, startingnode
                    print("No more successor to node " + str(currentnode))


                    currentnode = successor[0]
                # Sinon si un choix est indique, on change le cours du graph
                else:
                    currentnode = nodeanswer['nextnodechoice']
                    print("currentnode", currentnode)
                    print("succ", successor)
                    lastnodeid = successor[0]
                n += 1

    def processgraph(self,nodetoprocess = None,lastnodemessage = None,startingnode = -1):
        while True:
            nodetoprocess, lastnodemessage, startingnode = self.travelgraph(nodetoprocess, lastnodemessage, startingnode)

        # G.nodes[1]['object'].printValues()
        # G.nodes[2]['object'].printFunctions()
        # G.nodes[2]['object'].runFunctions()

        #print(func)


        # print("is_tree:", nx.is_tree(G))
        # print("is_forest:", nx.is_forest(G))
        # print("is_arborescence:", nx.is_arborescence(G))
        # print("is_branching:", nx.is_branching(G))
        #self.G = G
        #self.dfs_with_edges(G)
        #self.drawGraph()
        #self.iterateGraph([1])

    #def fractfromgraph(self,fractaltensor):
    def hasalliteratorsnodesended(self):
        iteratorsstatelist = []
        for anode in list(self.G.nodes):
            if type(self.G.nodes[anode]['object']).__name__ == "GraphIterator":
                if not self.G.nodes[anode]['object'].iterationended:
                    return False
        return True


    def isnodepartofCycle(self,node):
        for cycle in list(nx.simple_cycles(self.G)):
            if node in cycle:
                return True
        return False
    def getOrphanNodeList(self):
        orphannodelist = []
        for anode in self.G.nodes:
            if list(self.G.predecessors(anode)) == []:
                orphannodelist.append(anode)
        return orphannodelist

    def dfs_with_edges(self,graph):
        visited_nodes = set()
        visited_edges = set()

        def dfs(node):
            if node not in visited_nodes:
                print("node",node)
                visited_nodes.add(node)
                for neighbor in graph.neighbors(node):
                    edge = (node, neighbor)
                    if edge not in visited_edges:
                        print("Edge:", edge)
                        print("Node fn",graph.nodes[node]['fn'])
                        visited_edges.add(edge)
                        dfs(neighbor)

        # Start DFS from each node if the graph is not connected
        for node in graph.nodes():
            dfs(node)

    def iterateGraph(self,successorlist):
        for i in range(1,4+1):
            print("i",i)
            # Perform DFS traversal
            dfstree = list(nx.dfs_tree(self.G,source=i))
            print("DFS dfstree:", dfstree)
            dfs_nodes = list(nx.dfs_preorder_nodes(self.G,source=i))
            print("DFS traversal:", dfs_nodes)
            # Perform BFS traversal
            bfs_nodes = list(nx.bfs_tree(self.G,source=i))
            print("BFS traversal:", bfs_nodes)
            shortest_path = nx.shortest_path(self.G, source=i, target=1)
            print("Shortest path:", shortest_path)

        exit()
        print(list(self.G.successors(3)))

        print("successorlist",successorlist)
        for asuccessor in successorlist:
            print("asuccessor",asuccessor)
            self.iterateGraph(self.G.successors(asuccessor))

