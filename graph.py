import time
import sys

from heapq import *
from queue import PriorityQueue as PQ
import itertools


def build_graph(filename, weighted=False, edge=False):
    """
    Inputs:
        filename (str): graph file path
        weighed (Bool): if includes weights of edges (weights will be initialized to 1)

    Outputs:
        If weighted is False: A dict-set object like a adjacent list.{1: [2, 3], 2: [1, 3, 4]}
        If weighted is True: A dict-dict object.{1: {2: 1, 3: 1}, 2: {1: 1, 3: 1, 4: 1}}

        E: num of edges

    """
    G = {}
    with open(filename, 'r') as graph:
        V, E, _ = list(map(lambda x: int(x), graph.readline().split()))
        i = 1
        for line in graph:
            vertices = set(list(map(lambda x: int(x), line.split())))
            if weighted:
                G[i] = dict(zip(vertices, [1] * len(vertices)))
            else:
                G[i] = vertices
            i += 1

    return G if edge else G, E


def check(G, C, weighted=False, uncovered=False):
    cost = 0
    C = set(C.keys())
    uncover = set()
    for s, slist in G.items():
        if s not in C:
            if weighted:
                for e, w in slist.items():
                    if e not in C:
                        cost += w
                        uncover.add((min(s, e), max(s, e)))
            else:
                e = slist.difference(C)
                uncover.update(set(zip([s] * len(e), e)))
                cost += len(e)
    if uncovered:
        return cost, uncover

    return cost
