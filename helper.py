import networkx as nx


def build_graph(filename):
    """
    Inputs:
        filename (str): graph file path
        weighed (Bool): if includes weights of edges (weights will be initialized to 1)

    Outputs:
        G: A nx.Graph object: A dict-dict-dict structure, initialize as follow
            {1 : {2 : {”weight” : 1},3 : {”weight” : 1}},2 : {1 : {”weight” : 1}},3 : {1 : {”weight” : 1}}}
        V: num of vertices
        E: num of edges
    """

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


def write_out(opt, trace, out_path):
    """
    Inputs:
        opt (list of vertices): Final solution of MVC e.g. [1,2,4,5,6]
        trace: (list of tuple): trace of the search, e.g. [(0.00,956),(0.01,932),...]
                Note: please remember to limit the time to 2-digit.
        output path (str): output filename of instance, e.g. "./OUT/LS1_out/dummy1_LS1_2_1"
                Note: No need to add suffixes.
    """

    trace_path = out_path + ".trace"
    sol_path = out_path + ".sol"

    with open(sol_path, 'w') as file:
        file.write(str(len(opt)) + "\n")
        file.write(",".join(str(v) for v in sorted(opt)))

    with open(trace_path, 'w') as file:
        for t, sol in trace:
            file.write(str(t) + ", " + str(sol) + "\n")
