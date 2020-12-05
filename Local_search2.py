from helper import *
import random
import math
import copy
from time import time


def get_neighbors(c,g):
    """Returns neighbors of the argument state for your solution."""
    result = True

    #Make a copy of the curr solution
    copy1 = copy.deepcopy(c)
    vertex = random.choice(list(copy1))
    copy1.remove(vertex)
    neighbors = list(g[vertex])
    for v in neighbors:
        if v not in copy1:
            result = False
            break
    if result:
        return copy1
    else:
        return c


def getEdges(g):
    output = []
    
    for key, values in g.items():
        currVertex = key
        listVertices = list(values)
        for i in range(len(listVertices)):
            if not listVertices[i] is None:
                tempEdge1 = [currVertex, listVertices[i]]
                tempEdge2 = [listVertices[i],currVertex]
                if tempEdge1 not in output and tempEdge2 not in output:
                    output.append(tempEdge1)
                    output.append(tempEdge2)
    return output



def removeEdges(edges,vertex):
    for i in reversed(range(len(edges))):
        temp = edges[i]
        if vertex in temp:
            edges.remove(temp)


def computeCost(G,C):
    cost = 0
    uncover = set()
    C = set(C)
    for key,values in G.items():
        if key not in C:
            e = values.difference(C)
            cost += len(e)
    return cost


class LocalSearch2:
    def __init__(self, G, E, out_dir="./LS2_out/", cut_off=300, seed=5, rho=0.5, gamma=None):
        random.seed(seed)

        self.G = G
        self.E = E
        self.W = E
        self.cut_off = cut_off
        self.out_dir = out_dir
        self.C = dict()

        self.V = len(self.G)

        self.dscore = {}
        self.confChange = dict(zip(self.G.keys(), [1] * self.V))
        self.uncover = None

        for s, slist in self.G.items():
            self.dscore[s] = len(slist)
    
    def initialization(self):
        copyGraph = copy.deepcopy(self.G)
        edges = getEdges(copyGraph)
        output = []
        dscore_sorted = {k: v for k, v in sorted(self.dscore.items(), key=lambda item: item[1], reverse=True)}
        for s in dscore_sorted.keys():
            self.C[s] = ""
            cost, self.uncover = check(self.G, self.C, weighted=False, uncovered=True)
            if cost == 0:
                self.update_dscore()
                break
        sortedVertices = list(dscore_sorted.keys())
        for i in range(len(sortedVertices)):
            if not edges:
                break
            tempVertex = sortedVertices[i]
            output.append(tempVertex)
            removeEdges(edges, tempVertex)
            del copyGraph[tempVertex]
        return output
            
        
    def update_dscore(self):
        self.dscore = {}
        for v in self.G.keys():
            C_temp = self.C.copy()
            if v in C_temp:
                del C_temp[v]
                self.dscore[v] = check(self.G, self.C, False) - check(self.G, C_temp, False)
            else:
                C_temp[v] = ""
                self.dscore[v] = check(self.G, self.C, False) - check(self.G, C_temp, False)
        return self.dscore
    
    def simulated_annealing(self):
        """Peforms simulated annealing to find a solution"""
        initial_temp = 1000
        final_temp = .0001
        alpha = 0.9999

        current_temp = initial_temp

        # Start by initializing the current state with the initial state
        initial_state = self.initialization()
        C = initial_state

        t1 = time()
        # print(t1,"1")
        cutoff = self.cut_off
        trace = []
        while current_temp > final_temp:
            t3 = time()
            t_eclipse = t3-t1
            if(t_eclipse > cutoff):
                break
            
            trace.append((format(t_eclipse, '.2f'),len(C)))
            curr_cost = computeCost(self.G, C)
            newC = get_neighbors(C,self.G)
            # Check if neighbor is best so far
            new_cost = computeCost(self.G, newC)
            cost_diff = curr_cost - new_cost

            # if the new solution is better, accept it
            if cost_diff > 0:
                C = newC
                curr_cost = new_cost
            # if the new solution is not better, accept it with a probability of e^(-cost/temp)
            else:
                if random.uniform(0, 1) < math.exp(cost_diff / current_temp):
                    C = newC
                    curr_cost = new_cost
            # decrement the temperature 
            current_temp *= alpha # current_temp = alpha * current_temp
        t2 = time()
        print("total time:",t2-t1)
        return C,trace
