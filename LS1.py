from graph import *
import time
import random
import sys
import copy

# def check(G, C):
#     cost = 0
#     C = set(C.keys())
#     # uncover = set()
#     for s, slist in G.items():
#         if s not in C:
#             e = slist.difference(C)
#             # uncover.update(set(zip([s] * len(e), e)))
#             cost += len(e)
#     return cost

class LocalSearch0:
    """
    Inputs:
        G (dict): Unidirected Graph, Like a Adjacent Linked List
            For example: {1: [2, 3], 2: [1, 3], 3: [1, 2]}
            Keys: Vertices
            Values: the list of adjacencies for corresponing key.

        out_dir: Path of output dir

    Outputs:
        A .sol file:
            File name: < instance >_< method >_< cutoff >_< randSeed > ∗.sol,
            e.g. jazz_BnB_600.sol, jazz_LS1_600_4.sol Note that as in the example
            above, randSeed is only applicable when the method of choice is
            randomized (e.g. local search). When the method is deterministic
            (e.g. branch-and-bound), randSeed is omitted from the solution file’s
            name.

            Format:
            (a) line 1: quality of best solution found (integer)
            (b) lines 2: list of vertex IDs of the vertex cover (comma-separated):
                v1,v2,...,vn
            2. Solution trace files:

        Trace File:
            File name: < instance > < method > < cutoff > < randSeed > ∗.trace,
            e.g. jazz_BnB_600.trace, jazz_LS1_600_4.trace. Note that randSeed is
            used as in the solution files.

            File format: each line has two values (comma-separated):
            (a) A timestamp in seconds (double)
            (b) Quality of the best found solution at that point in time (integer).
                Note that to produce these lines, you should record every time a
                new improved solution is found. Example:
                3.45, 102
                7.94, 95
    """

    def __init__(self, G, D, E,GG, out_dir="./LS1_out/", cut_off=5, seed=1, p = 0.1):
        random.seed(seed)

        self.G = G
        # self.E = G
        self.GG = GG
        self.D = D
        self.V = set(self.G.keys())
        self.numE = E

        self.cut_off = cut_off
        self.out_dir = out_dir
        self.C = dict()

        self.p = p

        self.check_time = 0

    def init_sol(self):
        V = {k: v for k, v in sorted(self.D.items(), key=lambda item: item[1],reverse=True)}
        E = self.G.copy()

        # for v in V.keys():
        #     if v not in E.keys():
        #         continue
        #     self.C[v]=""
        #     for u in E[v].keys():
        #         del E[u][v]
        #         if len(E[u]) == 0:
        #             E.pop(u,None)
        #
        #     E.pop(v,None)
        #
        #     if len(E) == 0:
        #         break

        for v in V.keys():
            if v not in E.keys():
                continue
            self.C[v]=""
            for u in E[v]:
                E[u].remove(v)
                if len(E[u]) == 0:
                    E.pop(u,None)

            E.pop(v,None)

            if len(E) == 0:
                break

        # print("???",len(self.C))


    def find_vertex(self):
        # self.dscore = {}

        maxd = -sys.maxsize
        selected = -1
        for v in list(self.C.keys()):
            C_temp = self.C.copy()
            del C_temp[v]

            tt = time.time()
            dscore = check(self.GG, self.C) - check(self.GG, C_temp)
            self.check_time += time.time() - tt

            if dscore > maxd:
                maxd = dscore
                selected = v



        return selected



    def search(self):
        self.init_sol()
        elapse_time = 0
        tik = time.time()


        i = 0
        while elapse_time<self.cut_off:
            i+=1
            print(i)

            if check(self.GG,self.C)==0:


                C_opt = self.C.copy()

                h = self.find_vertex()

                del self.C[h]
                print(len(C_opt))
                print(C_opt)


            u = self.find_vertex()

            del self.C[u]

            nonC = self.V.difference(self.C)

            if random.random() < self.p:
                v = random.sample(nonC,1)[0]

            else:
                v = self.find_vertex()

            self.C[v] = ""

            elapse_time = time.time() - tik
        #
        print(self.check_time)
        return C_opt


if __name__ == "__main__":

    data_path = "./DATA/"

    try:
        p_path = data_path + sys.argv[1]
    except:
        p_path = data_path + "email.graph"

    G, D, E,GG = build_graph(p_path)
    # print(GGG)

    # print(G)

    LS = LocalSearch0(G,D, E,GG)

    opt = LS.search()

    print(len(list(opt.keys())))

