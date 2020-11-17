import time
import sys

from heapq import *
from queue import PriorityQueue as PQ
import itertools



def build_graph(filename):
    # Write this function to parse edges from graph file to create your graph object
    G = {}
    with open(filename, 'r') as graph:
        V,E,_ = list(map(lambda x: int(x), graph.readline().split()))
        i = 1 
        for line in graph:
            vertices = list(map(lambda x: int(x), line.split()))
            G[i] = vertices
            i+=1

    # print(G)
    return G



