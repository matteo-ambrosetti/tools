#!/bin/bash


# Benzene
python scan.py -f benzene.xyz -of examples/benzene_scan_C-H/ -id 0 6   -s 1 -d_min 2.0
python make_eT.py -s benzene_d -n benzene -if examples/benzene_scan_C-H/ -of examples/benzene_scan_C-H/eT/

python scan.py -f benzene.xyz -of examples/benzene_plane_H/  -id 0 6 1 -s 2 -d_min 2.0
python make_eT.py -s benzene_d -n benzene -if examples/benzene_plane_H/ -of examples/benzene_plane_H/eT/

python scan.py -f benzene.xyz -of examples/benzene_plane_C/  -id 6 0 1 -s 2 -d_min 2.0
python make_eT.py -s benzene_d -n benzene -if examples/benzene_plane_C/ -of examples/benzene_plane_C/eT/


# Water
python scan.py -f water.xyz   -of examples/water_scan_O-H/   -id 0 1   -s 1 -d_min 2.0
python make_eT.py -s water_d -n water -if examples/water_scan_O-H/ -of examples/water_scan_O-H/eT/

python scan.py -f water.xyz   -of examples/water_plane_H/    -id 0 1 2 -s 2 -d_min 2.0
python make_eT.py -s water_d -n water -if examples/water_plane_H/ -of examples/water_plane_H/eT/

python scan.py -f water.xyz   -of examples/water_plane_O/    -id 1 0 2 -s 2 -d_min 2.0
python make_eT.py -s water_d -n water -if examples/water_plane_O/ -of examples/water_plane_O/eT/
