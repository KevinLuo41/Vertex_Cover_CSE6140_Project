from graph import *
import time
import random
import sys


class LocalSearch1:
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

    def __init__(self, G, E, out_dir="./LS1_out/", cut_off=50, seed=1, rho=0.5, gamma=None):
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

        if gamma:
            self.gamma = gamma
        else:
            self.gamma = self.V / 2

        self.rho = rho

        for s, slist in self.G.items():
            self.dscore[s] = len(slist)

    def init_sol(self):
        dscore_sorted = {k: v for k, v in sorted(self.dscore.items(), key=lambda item: item[1], reverse=True)}
        # print (dscore_sorted)
        for s in dscore_sorted.keys():
            self.C[s] = ""
            # print (G)
            cost, self.uncover = check(self.G, self.C, weighted=True, uncovered=True)
            if cost == 0:
                self.update_dscore()
                break

    def update_dscore(self):
        self.dscore = {}
        for v in self.G.keys():
            C_temp = self.C.copy()
            if v in C_temp:
                del C_temp[v]
                self.dscore[v] = check(self.G, self.C, True) - check(self.G, C_temp, True)
            else:
                C_temp[v] = ""
                self.dscore[v] = check(self.G, self.C, True) - check(self.G, C_temp, True)
        return self.dscore

    def high_old(self, e=None):
        """
            self.C
            self.dscore
        """

        ### 问题在于先从C里选，再找最大的；而不是先找了最大的再开C

        if e:
            p, q = e

            if self.dscore[p] > self.dscore[q]:
                return p
            elif self.dscore[p] < self.dscore[q]:
                return q
            else:
                if random.randint(0, 1): return p
                else: return q



        else:
            # dscore_temp = {}
            maxd = -sys.maxsize
            selected = -1
            for i in self.C.keys():
                if self.dscore[i] > maxd:
                    maxd = self.dscore[i]
                    selected = i
            return selected

    def random_choose(self, e):

        u, v = e
        if self.confChange[u] == 1 and self.confChange[v] == 1:
            return self.high_old(e)
        elif self.confChange[u] == 1 and self.confChange[v] == 0:
            return u
        elif self.confChange[u] == 0 and self.confChange[v] == 1:
            return v
        else:
            raise ValueError("Two vertices of the selected edge cannot be zero simultaneously")

    def LocalSearch(self):
        self.init_sol()
        # print(self.uncover)

        C_opt = self.C.copy()

        print(len(list(C_opt.keys())))
        elapse_time = 0
        tik = time.time()

        while elapse_time < self.cut_off:
            if check(self.G, self.C, weighted=True) == 0:
                C_opt = self.C.copy()
                print(len(list(C_opt.keys())))
                print(list(C_opt.keys()))
                # print(self.high_old())
                del self.C[self.high_old()]
                self.update_dscore()
                continue

            u = self.high_old()
            del self.C[u]
            self.update_dscore()
            self.confChange[u] = 0
            for z in G[u].keys():
                self.confChange[z] = 1

            _, self.uncover = check(self.G, self.C, weighted=True, uncovered=True)
            # print(self.uncover)
            e = random.sample(self.uncover, 1)[0]
            v = self.random_choose(e)
            self.C[v] = ""
            self.update_dscore()
            for z in G[v].keys():
                self.confChange[z] = 1

            _, self.uncover = check(self.G, self.C, weighted=True, uncovered=True)

            # print(self.uncover)
            for p, q in self.uncover:
                self.G[p][q] += 1
                self.G[q][p] += 1
                self.W += 2

            if self.W / self.E >= self.gamma:
                for p, q in self.uncover:
                    self.W = self.W + 2 * int(self.rho * self.G[p][q]) - 2 * self.G[p][q]
                    self.G[p][q] = int(self.rho * self.G[p][q])
                    self.G[q][p] = int(self.rho * self.G[p][q])

            elapse_time = time.time() - tik
            # print(self.C)
        return C_opt


if __name__ == "__main__":

    data_path = "./DATA/"

    try:
        p_path = data_path + sys.argv[1]
    except:
        p_path = data_path + "dummy1.graph"

    G, E = build_graph(p_path, weighted=1)

    # print(G)

    LS = LocalSearch1(G, E)

    opt = LS.LocalSearch()
    print(len(list(opt.keys())))
