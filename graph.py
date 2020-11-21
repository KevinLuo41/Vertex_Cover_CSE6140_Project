import networkx as nx

def build_graph(filename):
    """
    Inputs:
        filename (str): graph file path
        weighed (Bool): if includes weights of edges (weights will be initialized to 1)

    Outputs:
        G: If weighted is False: A dict-dict-dict object.
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

def write_out(opt,trace,out_path):


    trace_path = out_path + ".trace"
    sol_path = out_path + ".sol"

    with open(sol_path, 'w') as file:
        file.write(str(len(opt))+"\n")
        file.write(",".join(str(v) for v in sorted(opt.keys())))


    with open(trace_path, 'w') as file:
        for t, sol in trace:
            file.write(str(t)+", "+str(sol)+"\n")



