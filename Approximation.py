import time
import random



class Approx:
    def __init__(self, G,  # Graph
                 cut_off=60,  # cut off time
                 seed=1,  # random seed
                 ):
        random.seed(seed)
        self.G = G
        self.cut_off = cut_off
        self.output = []

    def search(self):
        start_time = time.time()
        i = 0
        self.C = list(self.G.nodes())
        vectics_sort = sorted(list(zip(dict(self.G.degree(self.C)).values(), self.C)))

        while (i < len(vectics_sort) and (time.time() - start_time) < self.cut_off):
            cond = True
            for x in self.G.neighbors(vectics_sort[i][1]):
                if x not in self.C:
                    cond = False
            if cond:
                self.C.remove((vectics_sort[i][1]))
                self.output.append((format(time.time() - start_time, '.2f'),len(self.C)))
            i = i + 1

        return self.C, self.output
