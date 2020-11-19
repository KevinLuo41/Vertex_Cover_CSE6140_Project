from graph import *
import time
import random
import sys

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

    def __init__(self, G, out_dir="./LS1_out/", cut_off=50, seed=1, rho=0.5, gamma=None):
        random.seed(seed)

        self.G = G
        self.V = list(self.G.keys())

        self.cut_off = cut_off
        self.out_dir = out_dir
        self.C = dict()

        self.V = len(self.G)

        self.dscore = {}
        self.confChange = dict(zip(self.G.keys(), [1] * self.V))
        self.uncover = None


    def init_sol(self):



    def LS(self):
        pass



if __name__ == "__main__":

    data_path = "./DATA/"

    try:
        p_path = data_path + sys.argv[1]
    except:
        p_path = data_path + "dummy1.graph"

    G, E = build_graph(p_path)

    print(G)

    Test = LocalSearch0(G, E)

    opt = Test.LS()
    print(len(list(opt.keys())))