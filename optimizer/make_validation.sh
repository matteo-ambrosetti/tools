#!/bin/bash

# Water
python validation.py -m water -uat -ifp examples/water/out_w1.0_over_r_int0.0-1.0_1/ -ifg ../../bulk_polar_mu_qm/xyz_water_tip3p/ -ifl ../../bulk_polar_mu_qm/com_water_tip3p_polar/ &

# Acetonitrile
#python validation.py -m acetonitrile -uat -ifp examples/acetonitrile/out_w1.0_over_r_int0.0-1.0_1/ -ifg ../../bulk_polar_mu_qm/xyz_acetonitrile_cm5/ -ifl ../../bulk_polar_mu_qm/com_acetonitrile_cm5_polar/ &
#python validation.py -m acetonitrile -ifp examples/acetonitrile/out_w1.0_over_r_int0.0-1.0_no_at_1/ -ifg ../../bulk_polar_mu_qm/xyz_acetonitrile_cm5/ -ifl ../../bulk_polar_mu_qm/com_acetonitrile_cm5_polar/ &

## Methanol
#python validation.py -m methanol -uat -ifp examples/methanol/out_w1.0_over_r_int0.0-1.0_1/ -ifg ../../bulk_polar_mu_qm/xyz_methanol_cm5/ -ifl ../../bulk_polar_mu_qm/com_methanol_cm5_polar/ &
#python validation.py -m methanol -ifp examples/methanol/out_w1.0_over_r_int0.0-1.0_no_at_1/ -ifg ../../bulk_polar_mu_qm/xyz_methanol_cm5/ -ifl ../../bulk_polar_mu_qm/com_methanol_cm5_polar/ &
