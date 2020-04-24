#!/bin/bash


for i in $(seq 1 10)
do
	python optimizer.py -p "param_"$i".csv" -p_min 1.0e-08 -p_max 1.0 -o "output_"$i".txt" -of "examples/water/out_w1.0_int0.0-1.0_1" & 
done
