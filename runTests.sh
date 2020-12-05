#!/bin/bash


graphFiles=`ls ./DATA/ | grep .graph`

for graph in ${graphFiles}
do
	echo ${graph}
	# you only need to change the last three input arguments to your own
	python Execution.py -inst ${graph} -alg Approx -time 60 -seed 1


done
