# from graph import *
import time
import random
import sys
import copy
import networkx as nx
import networkx.algorithms.approximation.vertex_cover as mvc


def build_graph(filename):
    G = nx.Graph()
    with open(filename, 'r') as graph:
        V, E, _ = list(map(lambda x: int(x), graph.readline().split()))

        i = 1
        for line in graph:
            vertices = list(map(lambda x: int(x), line.split()))
            for v in vertices:
                G.add_edge(i, v, weight=1)
            i += 1

    return G, V, E


class LocalSearch11:
    def __init__(self, G, V, E, out_dir="./LS1_out/", cut_off=120, seed=1, gamma=None, rho=0.3):
        random.seed(seed)

        self.G = G
        self.V = V
        self.Vertex = set(range(1, V + 1))
        self.E = E

        self.cut_off = cut_off
        self.out_dir = out_dir
        self.C = {}

        self.uncover = []
        self.dscore = [0] * (self.V + 1)

        self.confChange = [1] * (self.V + 1)

        self.rho = rho
        if not gamma:
            self.gamma = V / 5

        self.output = []

    def init_sol(self):
        C = mvc.min_weighted_vertex_cover(self.G,weight="weight")
        self.C = dict(zip(C,[""]*len(C)))

        # nodes = list(self.G.nodes())
        # D = sorted(list(zip(dict(self.G.degree(nodes)).values(), nodes)), reverse=True)
        #
        # unc = set(G.edges)
        #
        # for d in D:
        #     v = d[1]
        #     self.C[v] = ""
        #     for x in G.neighbors(v):
        #         unc.discard((v, x))
        #         unc.discard((x, v))
        #         if not unc:
        #             return

    def find_vertex(self):
        maxd = -sys.maxsize
        selected = -1
        for v in self.C.keys():
            if self.dscore[v] > maxd:
                maxd = self.dscore[v]
                selected = v
        return selected

    def removeVertex(self, v):
        self.dscore[v] = -self.dscore[v]
        self.confChange[v] = 0
        for x in self.G.neighbors(v):
            self.confChange[x] = 1
            if x not in self.C.keys():
                self.uncover.extend([(v, x), (x, v)])
                # print(self.G[v][x]["weight"],"asdfadgfds")
                self.dscore[x] += self.G[v][x]["weight"]

            else:
                self.dscore[x] -= self.G[v][x]["weight"]

        del self.C[v]

    def chooseAdd(self):
        e = random.sample(self.uncover, 1)[0]
        u, v = e
        if self.confChange[u] == 1 and self.confChange[v] == 1:
            if self.dscore[u] > self.dscore[v]:
                return u
            elif self.dscore[u] < self.dscore[v]:
                return v
            else:
                return random.sample([u, v], 1)[0]

        elif self.confChange[u] == 1 and self.confChange[v] == 0:
            return u
        elif self.confChange[u] == 0 and self.confChange[v] == 1:
            return v
        else:
            raise ValueError("Two vertices of the selected edge cannot be zero simultaneously")

    def addVertex(self, v):
        self.dscore[v] = -self.dscore[v]
        for x in self.G.neighbors(v):
            self.confChange[x] = 1
            if x not in self.C.keys():
                self.uncover.remove((v, x))
                self.uncover.remove((x, v))

                self.dscore[x] -= self.G[v][x]["weight"]
            else:
                self.dscore[x] += self.G[v][x]["weight"]

        self.C[v] = ""

    def search(self):
        self.init_sol()
        elapse_time = 0
        tik = time.time()

        while elapse_time < self.cut_off:

            if not self.uncover:
                C_opt = self.C.copy()
                h = self.find_vertex()
                self.removeVertex(h)

                print(len(C_opt))

                record = time.time()-tik
                self.output.append((round(record,2), len(list(C_opt.keys()))))

                # print(C_opt)
                continue

            u = self.find_vertex()
            self.removeVertex(u)

            v = self.chooseAdd()
            self.addVertex(v)

            # print(self.uncover)

            for p, q in self.uncover:
                self.G[p][q]["weight"] += 1
                self.dscore[p] += 1

            # print("wwwww: ",G.size(weight="weight"))
            if G.size(weight="weight") / self.E >= self.gamma:
                self.dscore = [0] * (V + 1)
                self.uncover = []
                for u, v, w in self.G.edges(data=True):
                    w["weight"] = int(self.rho * w["weight"])
                    if not (u in self.C or v in self.C):
                        self.uncover.extend([(u, v), (v, u)])
                        self.dscore[u] += self.G[u][v]["weight"]
                        self.dscore[v] += self.G[u][v]["weight"]
                    elif not (u in self.C and v in self.C):
                        if u in self.C:
                            self.dscore[u] -= self.G[u][v]["weight"]
                        else:
                            self.dscore[v] -= self.G[u][v]["weight"]

            elapse_time = time.time() - tik
        #
        # print(self.check_time)
        return C_opt

    def output(self):






if __name__ == "__main__":

    data_path = "./DATA/"

    try:
        p_path = data_path + sys.argv[1]
    except:
        p_path = data_path + "jazz.graph"

    G, V, E = build_graph(p_path)

    LS = LocalSearch11(G, V, E)

    opt = LS.search()

    print(len(list(opt.keys())))