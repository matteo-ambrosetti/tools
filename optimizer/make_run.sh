#!/bin/bash


## Water
#for i in $(seq 1 20)
#do
#	python optimizer.py -p "param_"$i".csv" -p_min 1.0e-08 -p_max 1.0 -wt "1/r" -m water -o "output_"$i".txt" -of "examples/water/out_w1.0_over_r_int0.0-1.0_1" & 
#done

## Acetonitrile
#for i in $(seq 1 20)
#do
#	python optimizer.py -p "param_"$i".csv" -p_min 1.0e-08 -p_max 1.0 -wt "1/r" -m acetonitrile_no_at -o "output_"$i".txt" -of "examples/acetonitrile/out_w1.0_over_r_int0.0-1.0_no_at_1" & 
#done


# Methanol
for i in $(seq 1 20)
do
	python optimizer.py -p "param_"$i".csv" -p_min 1.0e-08 -p_max 1.0 -wt "1/r" -m methanol_no_at -o "output_"$i".txt" -of "examples/methanol/out_w1.0_over_r_int0.0-1.0_no_at_3" & 
done


