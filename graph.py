import time
import sys
import numpy as np

import copy



def build_graph(filename):
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
        GG = np.zeros([V+1,V+1])

        i = 1
        D = {}
        for line in graph:

            vertices = list(map(lambda x: int(x), line.split()))
            # print(i)
            GG[i][vertices] = 1
            G[i] = set(vertices)
            # GGG[i] = dict(zip(vertices,[""]*(len(vertices))))
            D[i] = len(vertices)
            i += 1

    return G, D, E, GG


# def check(G, C):
#     # G = GG.copy()
#     # for s in C.keys():
#     #     G[s,:] = 0
#     #     G[:,s] = 0
#     #
#     # cost = G.sum()
#
#
#
#
#     cost = 0
#     check_time = 0
#     C = set(C.keys())
#     tt = time.time()
#     for s, slist in G.items():
#         if s not in C:
#
#
#             e = slist.difference(C)
#
#             # uncover.update(set(zip([s] * len(e), e)))
#             cost += len(e)
#     # check_time += time.time() - tt
#     # print(check_time)
#
#
#     return cost

# def check(G,C):
#     E = G.copy()
#     for v in C.keys():
#         if v not in E.keys():
#             continue
#         for u in E[v].keys():
#             del E[u][v]
#             if len(E[u]) == 0:
#                 E.pop(u, None)
#
#         E.pop(v, None)
#
#     cost = 0
#     for s, e in E.items():
#         cost+=len(e)
#     return cost

def check(GG,C):
    G = GG.copy()
    G[list(C.keys()),:] = 0
    G[:,list(C.keys())] = 0

    cost = G.sum()
    return cost