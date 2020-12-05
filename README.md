# Vetex_Cover_CSE6140_Project
--------------------------------------------------------------------------------
## The structure of the code:

```
.
│   runTests.sh
│   Execution.py   
│   helper.py
│   Branch_and_Bound.py
│   Approximation.py
│   Local_search1.py
│   Local_search2.py
└───DATA
│   └───*.graph
└───OUT
    └───App_out
    └───BnB_out
    └───LS1_out
    └───LS2_out
```

**runTest.sh:** shell script to run all the graph by an algorithm.
```bash
#!/bin/bash

graphFiles=`ls ./DATA/ | grep .graph`

for graph in ${graphFiles}
do
	echo ${graph}
	# you only need to change the last three input arguments to your own
	python Execution.py -inst ${graph} -alg Approx -time 60 -seed 1

done
```
**Excution.py:** Python script used to run a graph by an algorithm, receive sys.args as input. 
```bash
python Execution.py -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
```

**helper.py:** Helper functions that shared among all algorithms, include building graph, etc. 
