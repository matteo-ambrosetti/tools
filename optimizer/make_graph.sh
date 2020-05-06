#!/bin/bash


## Water
#path_data="/home/m.ambrosetti/dataset_dipole_scan/tools/optimizer/examples/water/"
#path_geom="/home/m.ambrosetti/dataset_dipole_scan/tools/dataset/examples/"
#
#for folder in "water_plane_H" "water_plane_O" "water_scan_H-O-H_bisec" "water_scan_H-O-H_bisec_ext" "water_scan_O-H"
#do
#    python graphs.py -uat -ifp $path_data"out_w1.0_int0.0-1.0/" -ifg $path_geom$folder -p "water_d" -n 10 -nb 1
#done
#
#for folder in "water_plane_H" "water_plane_O" "water_scan_H-O-H_bisec" "water_scan_H-O-H_bisec_ext" "water_scan_O-H"
#do
#    python graphs.py -uat -ifp $path_data"out_w1.0_int0.0-1.0_1/" -ifg $path_geom$folder -p "water_d" -n 10 -nb 1
#done
#
#for folder in "water_plane_H" "water_plane_O" "water_scan_H-O-H_bisec" "water_scan_H-O-H_bisec_ext" "water_scan_O-H"
#do
#    python graphs.py -uat -ifp $path_data"out_w1.0_int0.0-1.0_2/" -ifg $path_geom$folder -p "water_d" -n 10 -nb 1
#done




# Acetonitrile 
#path_data="/home/m.ambrosetti/dataset_dipole_scan/tools/optimizer/examples/acetonitrile/"
#path_geom="/home/m.ambrosetti/dataset_dipole_scan/tools/dataset/examples/"

#for folder in "acetonitrile_scan_C-C" "acetonitrile_scan_C-H" "acetonitrile_scan_C-N" "acetonitrile_plane_N"
#do
#    python graphs.py -uat -ifp $path_data"out_w1.0_int0.0-1.0_1/" -ifg $path_geom$folder -p "acetonitrile_d" -n 10 -nb 1
#done

#for folder in "acetonitrile_scan_C-C" "acetonitrile_scan_C-H" "acetonitrile_scan_C-N" "acetonitrile_plane_N"
#do
#    python graphs.py -uat -ifp $path_data"out_w1.0_int0.0-1.0_2/" -ifg $path_geom$folder -p "acetonitrile_d" -n 20 -nb 1
#done

#for folder in "acetonitrile_scan_C-C" "acetonitrile_scan_C-H" "acetonitrile_scan_C-N" "acetonitrile_plane_N"
#do
#    python graphs.py -uat -ifp $path_data"out_w1.0_over_r_int0.0-1.0_1/" -ifg $path_geom$folder -p "acetonitrile_d" -n 20 -nb 1
#done

#for folder in "acetonitrile_scan_C-C" "acetonitrile_scan_C-H" "acetonitrile_scan_C-N" "acetonitrile_plane_N"
#do
#    python graphs.py -ifp $path_data"out_w1.0_over_r_int0.0-1.0_no_at_1/" -ifg $path_geom$folder -p "acetonitrile_d" -n 20 -nb 1
#done


# Methanol
path_data="/home/m.ambrosetti/dataset_dipole_scan/tools/optimizer/examples/methanol/"
path_geom="/home/m.ambrosetti/dataset_dipole_scan/tools/dataset/examples/"

for folder in "methanol_scan_C-H_1" "methanol_scan_C-H_2" "methanol_scan_C-O" "methanol_scan_O-C" "methanol_scan_O-H"
do
    python graphs.py -uat -ifp $path_data"out_w1.0_over_r_int0.0-1.0_1/" -ifg $path_geom$folder -p "methanol_d" -n 20 -nb 1
done


