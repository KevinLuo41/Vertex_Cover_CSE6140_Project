#!/bin/bash


graphFiles=`ls ./DATA/ | grep .graph`

for graph in ${graphFiles}
do
	echo ${graph}
	python Excution.py -inst ${graph} -alg LS1 -time 60 -seed 1


done
