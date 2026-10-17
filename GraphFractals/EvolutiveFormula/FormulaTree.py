import copy
import random
import re

import networkx as nx
import numpy as np
import sympy
from matplotlib import pyplot as plt
from sympy.parsing.sympy_parser import parse_expr
from sympy import preorder_traversal, symbols
from sympy.series.order import Order
class FormulaTree:
    def formulatograph(self,formula):

        # Parse formula to tree
        _, nodes, _ = self.parse_formula_to_tree(formula)
        print(nodes)
        formula = self.formatformulaforgraph(formula,nodes)
        root, nodes, edges = self.parse_formula_to_tree(formula)
        #print(root, nodes, edges)
        G = self.tree_to_nx_graph(root, nodes, edges)
        print(root, nodes, edges)

        return G

    def formatformulaforgraph(self,formula,nodeslist):
        formula = copy.deepcopy(formula)
        it = 1
        print("nodeslist",nodeslist)
        for node in nodeslist:
            n=0

            for i in formula:
                if formula[n:n+len(node)] == node and not formula[n+len(node)] == "_" and not formula[n+len(node)].isnumeric():
                    formulabegin,formulaend = formula[0:n],formula[n+len(node):]
                    #print("formulabegin",formulabegin)
                    #print("formulaend", formulaend)
                    formula = formulabegin +  node + "_" + str(it) + formulaend
                    #print(formula)
                    it+=1
                n=n+1
        return formula
    def drawgraph(self,G):
        plt.clf()
        nx.draw(G, with_labels=True)
        plt.show()

    def drawgraphformula(self,formula):
        G = self.formulatograph(formula)
        plt.clf()
        nx.draw(G, with_labels=True)
        plt.show()
    def parse_formula_to_tree(self,formula):
        #print("formula",formula)
        expr = parse_expr(formula)
        nodes = []
        edges = []

        def build_tree(expr):
            if expr.is_Atom:
                return str(expr)
            else:
                #print("expr",expr.func,expr.args,type(expr.args))
                if isinstance(expr.func,property):
                    return "O"
                op = str(expr.func)
                nodes.append(op)
                # Regle un bug avec l utilisation du O pour zero
                #print("type",type(expr.func))


                for arg in expr.args:
                    arg_str = build_tree(arg)
                    nodes.append(arg_str)
                    edges.append((op, arg_str))
                return op

        root = build_tree(expr)
        return root, nodes, edges



    def tree_to_nx_graph(self,root, nodes, edges):
        G = nx.DiGraph()
        for node in nodes:
            G.add_node(node)
        G.add_edges_from(edges)
        return G

    def nx_graph_to_formula(self,G):
        root = 'fn1_1'
        global formulaoutput
        formulaoutput = ""
        # Traverse the graph starting from the root node
        def traverse(node):
            global formulaoutput
            formulaoutput += str(node)
            if not list(G.successors(node)) == []:
                formulaoutput += '('
            successorscount = len(list(G.successors(node)))
            n=1
            for successors in G.successors(node):
                traverse(successors)
                if not n == successorscount:
                    formulaoutput += ','
                n+=1
            if not list(G.successors(node)) == []:
                formulaoutput += ')'
        traverse(root)
        underscoredetected = False
        filteredformula = ""
        for i in formulaoutput[:]:
            if i == '_':
                underscoredetected = True
                continue
            if underscoredetected:
                if i.isnumeric():
                    continue
                else:
                    underscoredetected = False
            filteredformula += i

        return filteredformula

    def randomgraphfromnodetoleafs(self,G):
        lastfn = None
        print(list(G.edges))
        root = self.getRoot(G)
        print(root)
        longestpath = nx.dag_longest_path_length(G)
        randomsearch = random.randint(1,longestpath)
        nodetoprocess = root[0]

        for i in range(0,randomsearch):
            successors = G.successors(nodetoprocess)
            successors = list(successors)
            print(successors)
            fnlist = [i for i in list(successors) if "fn" in i]
            print("fnlist", fnlist)
            if not fnlist == []:
                lastfn = random.choice(list(fnlist))
                print("lastfn",lastfn)
            if successors == []:
                break

            nodetoprocess= random.choice(list(successors))
            print("nodetoprocess", nodetoprocess)
        if lastfn is None:
            successors = nx.dfs_tree(G,root[0])
            print("successorsbydefault",successors)
            return successors
        successors = nx.dfs_tree(G, lastfn)
        print("successors",successors.nodes,successors.edges)
        #print(longestpath)
        return successors

    def randompathfromleaftoroot(self,G,leaf):
        leafs = self.getLeafs(G)
        if not isinstance(leaf,list):
            leaf = [leaf]
        currentnode = [i for i in leafs if leaf[0] in i]
        #print("leafs",leafs)
        #print(currentnode)
        nodespathlist = []
        while not currentnode == []:
            choosennode = random.choice(currentnode)
            currentnode = list(G.predecessors(choosennode))
            nodespathlist.append(choosennode)
            #print(choosennode)
        #print(nodespathlist)
        return nodespathlist

    def getLeafs(self,G):
        leafs = [x for x in G.nodes() if G.out_degree(x) == 0 and G.in_degree(x) == 1]
        return leafs
    def getRoot(self,G):
        root = [x for x in G.nodes() if G.in_degree(x) == 0]
        return root
    def trimRandomBranch(self,G):
        leafs = self.getLeafs(G)
        print("leafs",leafs)
        selectedleaf = random.choice(leafs)
        print("selectedleaf",selectedleaf)
        selectedpath = self.randompathfromleaftoroot(G,selectedleaf)
        #selectedpath.reverse()
        print("selectedpath",selectedpath)
        print(1,len(selectedpath)-2)
        pathtodelete = selectedpath[:random.randint(1,len(selectedpath)-1)]
        print("pathtodelete",pathtodelete)
        trimmedtree = copy.deepcopy(G)
        n=0
        for i in pathtodelete:
            print("Trimming",i)
            trimedge = (selectedpath[n+1],i)
            print("trimedge",trimedge)
            trimmedtree.remove_edge(trimedge[0],trimedge[1])
            n+=1
        # Modify last trimmed edge by one or zero
        nodereplacement = random.choice(["O","Z"])
        print("nodereplacement",nodereplacement)
        trimmedtree.add_edge(trimedge[0],nodereplacement)
        return trimmedtree

    def CrossTwoFormula(self,receiver,giver):
        # Remove a random branch from the receiver
        #print("receiver",receiver)
        G = self.formulatograph(receiver)

        # plt.clf()
        # nx.draw(G, with_labels=True)
        # plt.show()

        leafs = self.getLeafs(G)
        #print("leafs",leafs)
        selectedleaf = random.choice(leafs)
        #print("selectedleaf",selectedleaf)
        selectedpath = self.randompathfromleaftoroot(G,selectedleaf)
        #selectedpath.reverse()
        #print("selectedpath",selectedpath)
        #print(1,len(selectedpath)-2)
        pathtodelete = selectedpath[:random.randint(1,len(selectedpath)-1)]
        #print("pathtodelete",pathtodelete)
        trimmedtree = copy.deepcopy(G)
        n=0
        for i in pathtodelete:
            #print("Trimming",i)
            trimedge = (selectedpath[n+1],i)
            #print("trimedge",trimedge)
            trimmedtree.remove_edge(trimedge[0],trimedge[1])
            n+=1
        trimmedtree.remove_nodes_from(list(nx.isolates(trimmedtree)))
        # plt.clf()
        # nx.draw(trimmedtree, with_labels=True)
        # plt.show()
        # Modify last trimmed edge by one or zero
        # nodereplacement = random.choice(["O","Z"])
        # print("nodereplacement",nodereplacement)

        # Select a random branch for the giver
        G = self.formulatograph(giver)
        G = self.randomgraphfromnodetoleafs(G)
        # plt.clf()
        # nx.draw(G, with_labels=True)
        # plt.show()
        trimmedtree.add_nodes_from(G)
        #print(list(G.edges))
        trimmedtree.add_edges_from(list(G.edges))
        #print(trimedge[0],self.getRoot(G))
        print("Added edge :",trimedge[0],self.getRoot(G)[0])
        trimmedtree.add_edge(trimedge[0],self.getRoot(G)[0])
        print("after edge trimmed tree",trimmedtree.edges)
        trimmedtree.remove_nodes_from(list(nx.isolates(trimmedtree)))
        plt.clf()
        nx.draw(trimmedtree, with_labels=True)
        #trimmedtree.add_edges_from(trimedge[-1],G)
        print("receiver",receiver)
        print("giver",giver)

        print("trimmedtree",trimmedtree)
        # plt.clf()
        # nx.draw(trimmedtree, with_labels=True)
        # plt.show()

        return trimmedtree
formula = "fn1(fn2(p1),p10,Z)"
print("formula",formula)
formulatree = FormulaTree()



G = formulatree.formulatograph(formula)
print("formula",formula)
print("edges",G.edges)

# leafsparents = [list(G.predecessors(x)) for x in leafs ]
# print("leafs",leafs)
#print("leafsparents",leafsparents)
print("Leafs of G",formulatree.getLeafs(G))

randompath = formulatree.randompathfromleaftoroot(G,'p1')
print("randompath",randompath)

trimmedtree = formulatree.trimRandomBranch(G)
print("trimmedtree",list(trimmedtree.edges))

# not list(G.predecessors(currentnode)) == []

#pos = nx.kamada_kawai_layout(G)
#nx.draw(G, pos=pos, with_labels=True)
#nx.draw(G,  with_labels=True)
#plt.show()

outputformula = formulatree.nx_graph_to_formula(trimmedtree)
#print("formula",formula)
print("outputformula",outputformula)

print("formula==outputformula",formula==outputformula)
#print("outputformula",outputformula)
#pos = nx.nx_agraph.graphviz_layout(G, prog="twopi")



