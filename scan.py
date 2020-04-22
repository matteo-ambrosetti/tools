import MDAnalysis
import directions
import numpy as np
import os

# Reference geometry
filename   = "benzene.xyz"

# Output geometry prefix
out_folder = "scan_plane_C/"
d_min  = 2.5
d_max  = 10.0
d_step = 0.25
dipole_len = 1.0
indxA  = 6
indxB  = 0
indxC  = 1
scan_type = 2

# Make the output directory
try:
    os.mkdir(out_folder)
except:
    pass

# Load the reference geometry
u = MDAnalysis.Universe(filename)

# Choose the scan type
if scan_type == 1:
    # Define the position of the reference atoms
    posA  = u.atoms.positions[indxA]
    posB  = u.atoms.positions[indxB]
    # Scan along a direction defined by the
    # vector pointing from atom A to atom B
    direction = directions.versor(posA, posB)
elif scan_type == 2:
    # Define the position of the reference atoms
    posA  = u.atoms.positions[indxA]
    posB  = u.atoms.positions[indxB]
    posC  = u.atoms.positions[indxC]
    # Scan along a direction defined by the
    # vector perpendicular to the plane defined
    # by three points: A, B and C
    direction = directions.versor_perp_plane(posA,posB,posC)

# Write out files
out_prefix  = out_folder + filename.split(".xyz")[0]
out_prefixs = out_folder + filename.split(".xyz")[0] + "s"
a = open("{}.xyz".format(out_prefixs), "w")
for dist in np.arange(d_min, d_max, d_step):
    f = open("{}_d{:.2f}.xyz".format(out_prefix, dist), "w")
    f.write("{}\n".format(u.atoms.n_atoms+2))
    a.write("{}\n".format(u.atoms.n_atoms+2))
    f.write("scan along indxA:{} --> indxB{} - dist:{}\n".format(indxA, indxB,dist))
    a.write("scan along indxA:{} --> indxB{} - dist:{}\n".format(indxA, indxB,dist))
    q_1 = posB + dist*direction
    q_2 = q_1  + dipole_len*direction
    for i in range(u.atoms.n_atoms):
        f.write("{:<2} ".format(u.atoms.names[i]))
        a.write("{:<2} ".format(u.atoms.names[i]))
        for j in range(3):
            f.write("{:>12.6f} ".format(u.atoms.positions[i,j]))
            a.write("{:>12.6f} ".format(u.atoms.positions[i,j]))
        f.write("\n")
        a.write("\n")
    f.write("{:<2} {:>12.6f} {:>12.6f} {:>12.6f}\n".format("Po", q_1[0], q_1[1], q_1[2]))
    a.write("{:<2} {:>12.6f} {:>12.6f} {:>12.6f}\n".format("Po", q_1[0], q_1[1], q_1[2]))
    f.write("{:<2} {:>12.6f} {:>12.6f} {:>12.6f}\n".format("Ne", q_2[0], q_2[1], q_2[2]))
    a.write("{:<2} {:>12.6f} {:>12.6f} {:>12.6f}\n".format("Ne", q_2[0], q_2[1], q_2[2]))
    f.close()
a.close()
