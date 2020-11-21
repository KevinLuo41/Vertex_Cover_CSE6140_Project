import argparse
from graph import *
from Local_search1 import *
from Local_search2 import *
from Branch_and_Bound import *
from Approximation import *
import os
import shutil


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-inst', required=True, type=str,default="dummy1.graph")
    parser.add_argument('-alg', required=True, type=str, choices=["BnB","Approx","LS1","LS2"],default="LS1")

    parser.add_argument('-time', type=int,default=2)
    parser.add_argument('-seed', type=int, default=1)

    parser.add_argument('-gamma', required=False, type=int)
    parser.add_argument('-rho', required=False, type=int)


    args = parser.parse_args()
    inst = args.inst.split(".")[0]
    alg = args.alg
    time = args.time
    seed = args.seed
    out_path = "_".join(str(e) for e in [inst,alg,time,seed])

    G, V, E = build_graph("./DATA/"+args.inst)
    print("Run %s on %s with cutoff %s and random seed %s" %(inst,alg,time,seed) )
    if args.alg == "BnB":
        pass

    elif args.alg == "Approx":
        pass

    elif args.alg == "LS1":
        LS = LS1(G, V, E,cut_off = args.time, seed = args.seed,gamma=args.gamma,rho=args.rho)
        opt, trace= LS.search()
        write_out(opt, trace, "./OUT/LS1_out/"+out_path)


    elif args.alg == "LS2":
        pass







