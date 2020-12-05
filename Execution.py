import argparse
from helper import *
from Local_search1 import *
from Local_search2 import *
from Branch_and_Bound import *
from Approximation import *


if __name__ == '__main__':
    # Required Arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-inst', required=True, type=str, default="dummy1.graph")
    parser.add_argument('-alg', required=True, type=str, choices=["BnB", "Approx", "LS1", "LS2"], default="LS2")
    parser.add_argument('-time', type=int, default=2)
    parser.add_argument('-seed', type=int, default=1)

    # Optional Arguments
    #LS1
    parser.add_argument('-gamma', required=False, type=int)
    parser.add_argument('-rho', required=False, type=int)

    # Parse Arguments
    args = parser.parse_args()
    inst = args.inst.split(".")[0]
    alg = args.alg
    time = args.time
    seed = args.seed

    # Creat output path
    out_path = "_".join(str(e) for e in [inst, alg, time, seed])

    # Parse Graph
    G, V, E = build_graph("./DATA/" + args.inst)

    # Run algorithm
    print("Run %s on %s with cutoff %s and random seed %s" % (inst, alg, time, seed))
    if args.alg == "BnB":
        BnB = BnB(G, cut_off=args.time, seed=args.seed)
        opt, trace = BnB.search()
        write_out(opt, trace, "./OUT/BnB_out/" + out_path)

    elif args.alg == "Approx":
        App = Approx(G, cut_off=args.time, seed=args.seed)
        opt, trace = App.search()
        write_out(opt, trace, "./OUT/App_out/" + out_path)

    elif args.alg == "LS1":
        LS = LS1(G, V, E, cut_off=args.time, seed=args.seed, gamma=args.gamma, rho=args.rho)
        opt, trace = LS.search()
        write_out(opt, trace, "./OUT/LS1_out/" + out_path)

    elif args.alg == "LS2":
        G,E = build_graph2("./DATA/" + args.inst)
        #print(G,1111,E)
        LS = LocalSearch2(G, E, cut_off=args.time, seed=args.seed)
        sol,trace = LS.simulated_annealing()
        write_out(sol, trace, "./OUT/LS2_out/" + out_path)
