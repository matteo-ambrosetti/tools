#!/bin/bash





############
## Benzene #
############
## Scan along C-H bond
#python scan.py -f benzene.xyz -of examples/benzene_scan_C-H/ -id 0 6   -s 1 -d_min 2.0
#python make_eT.py -s benzene_d -n benzene -if examples/benzene_scan_C-H/ -of examples/benzene_scan_C-H/eT/
#
## Scan along the plane of benzene and passing through H
#python scan.py -f benzene.xyz -of examples/benzene_plane_H/  -id 0 6 1 -s 2 -d_min 2.0
#python make_eT.py -s benzene_d -n benzene -if examples/benzene_plane_H/ -of examples/benzene_plane_H/eT/
#
## Scan along the plane of benzene and passing through C
#python scan.py -f benzene.xyz -of examples/benzene_plane_C/  -id 6 0 1 -s 2 -d_min 2.0
#python make_eT.py -s benzene_d -n benzene -if examples/benzene_plane_C/ -of examples/benzene_plane_C/eT/
#
## Scan along the plane of benzene and passing through the center of mass of the molecule
#
#
##########
## Water #
##########
## Scan along O-H bond
#python scan.py -f water.xyz   -of examples/water_scan_O-H/   -id 0 1   -s 1 -d_min 2.0
#python make_eT.py -s water_d -n water -if examples/water_scan_O-H/ -of examples/water_scan_O-H/eT/
#
## Scan along rhe bisector of the H-O-H angle
#python scan.py -f water.xyz   -of examples/water_scan_H-O-H_bisec/     -p 0.0 0.0 -0.115688 0.0 0.0 0.471834  -s 1 -d_min 2.0
#python make_eT.py -s water_d -n water -if examples/water_scan_H-O-H_bisec/ -of examples/water_scan_H-O-H_bisec/eT/
#
## Scan along the external bisector of the H-O-H angle
#python scan.py -f water.xyz   -of examples/water_scan_H-O-H_bisec_ext/ -p 0.0 0.0 -0.115688 0.0 0.0 -0.115689 -s 1 -d_min 2.0
#python make_eT.py -s water_d -n water -if examples/water_scan_H-O-H_bisec_ext/ -of examples/water_scan_H-O-H_bisec_ext/eT/
#
## Scan along the plane of water and passing through H
#python scan.py -f water.xyz   -of examples/water_plane_H/    -id 0 1 2 -s 2 -d_min 2.0
#python make_eT.py -s water_d -n water -if examples/water_plane_H/ -of examples/water_plane_H/eT/
#
## Scan along the plane of water and passing through O
#python scan.py -f water.xyz   -of examples/water_plane_O/    -id 1 0 2 -s 2 -d_min 2.0
#python make_eT.py -s water_d -n water -if examples/water_plane_O/ -of examples/water_plane_O/eT/



################
# Acetonitrile #
################
# Scan along C-N bond
python scan.py -f acetonitrile.xyz   -of examples/acetonitrile_scan_C-N/   -id 1 2 -s 1 -d_min 2.0
python make_eT.py -s acetonitrile_d -n acetonitrile -if examples/acetonitrile_scan_C-N/ -of examples/acetonitrile_scan_C-N/eT/

# Scan along (N-)C-C bond
python scan.py -f acetonitrile.xyz   -of examples/acetonitrile_scan_C-C/   -id 1 0 -s 1 -d_min 2.0
python make_eT.py -s acetonitrile_d -n acetonitrile -if examples/acetonitrile_scan_C-C/ -of examples/acetonitrile_scan_C-C/eT/

# Scan along C-H bond
python scan.py -f acetonitrile.xyz   -of examples/acetonitrile_scan_C-H/   -id 0 3 -s 1 -d_min 2.0
python make_eT.py -s acetonitrile_d -n acetonitrile -if examples/acetonitrile_scan_C-H/ -of examples/acetonitrile_scan_C-H/eT/

# Scan along the plane C-N-H and passing through N
python scan.py -f acetonitrile.xyz   -of examples/acetonitrile_plane_N/    -id 0 2 3 -s 2 -d_min 2.0
python make_eT.py -s acetonitrile_d -n acetonitrile -if examples/acetonitrile_plane_N/ -of examples/acetonitrile_plane_N/eT/


#############
## Methanol #
#############
## Scan along C-O bond
#python scan.py -f methanol.xyz   -of examples/methanol_scan_C-O/   -id 0 1 -s 1 -d_min 2.0
#python make_eT.py -s methanol_d -n methanol -if examples/methanol_scan_C-O/ -of examples/methanol_scan_C-O/eT/
#
## Scan along O-C bond
#python scan.py -f methanol.xyz   -of examples/methanol_scan_O-C/   -id 1 0 -s 1 -d_min 2.0
#python make_eT.py -s methanol_d -n methanol -if examples/methanol_scan_O-C/ -of examples/methanol_scan_O-C/eT/
#
## Scan along O-H bond
#python scan.py -f methanol.xyz   -of examples/methanol_scan_O-H/   -id 1 5 -s 1 -d_min 2.0
#python make_eT.py -s methanol_d -n methanol -if examples/methanol_scan_O-H/ -of examples/methanol_scan_O-H/eT/
#
## Scan along C-H bond (this is for the two C-H into which O-H is projected as a bisector)
#python scan.py -f methanol.xyz   -of examples/methanol_scan_C-H_1/   -id 0 2 -s 1 -d_min 2.0
#python make_eT.py -s methanol_d -n methanol -if examples/methanol_scan_C-H_1/ -of examples/methanol_scan_C-H_1/eT/
#
## Scan along C-H bond
#python scan.py -f methanol.xyz   -of examples/methanol_scan_C-H_2/   -id 0 4 -s 1 -d_min 2.0
#python make_eT.py -s methanol_d -n methanol -if examples/methanol_scan_C-H_2/ -of examples/methanol_scan_C-H_2/eT/
