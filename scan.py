import os
import argparse
import MDAnalysis
import directions
import numpy as np


parser = argparse.ArgumentParser(description='Generate structures.')
parser.add_argument("-f", dest="filename", required=True,
                    help="Input filename (only .xyz supported)", type=str)
parser.add_argument("-of", dest="outfolder", required=True,
                    help="Define the output folder name.", type=str)
parser.add_argument("-d_min", dest="dmin", required=False, default=2.5,
                    help="Minimum distance of the dipole from the molecule.", type=float)
parser.add_argument("-d_max", dest="dmax", required=False, default=10.0,
                    help="Maximum distance of the dipole from the molecule.", type=float)
parser.add_argument("-d_step", dest="dstep", required=False, default=0.25,
                    help="Step of the scan.", type=float)
parser.add_argument("-mu_len", dest="mulen", required=False, default=1.0,
                    help="Length of the dipole.", type=float)
parser.add_argument("-s", dest="scantype", required=False, default=1,
                    help="""Type of the scan performed:\n
                          1 --> Define two points. Scan along the vector joining
                                those two points. The increment is defined from
                                the second atom:   A ----> B |--step--| (+)<----(-).\n
                          2 --> Define three points. Scan along the vector perpendicular
                                to the plane defined by the three points. The increment
                                is defined for the vector passing through the second atom:
                                       (-)
                                        |
                                        |
                                        v
                                       (+)

                                        ^
                                        |
                                        |
                                A ----> B
                               /        |
                              /         |
                             /
                            v
                            C
                    """, type=int)
parser.add_argument("-id", dest="atomindex", required=True, nargs="+",
                    help="Atomic index which define the atoms used.", type=int)
args = parser.parse_args()

# Reference geometry
filename   = args.filename

# Output geometry prefix
if args.outfolder[-1] != "/":
    args.outfolder += "/"
out_folder = args.outfolder
d_min  = args.dmin
d_max  = args.dmax
d_step = args.dstep
dipole_len = args.mulen
scan_type  = args.scantype
# Get the atom index
if scan_type == 1:
    indxA, indxB = args.atomindex
elif scan_type == 2:
    indxA, indxB, indxC = args.atomindex

# Make the output directory
try:
    os.makedirs(out_folder)
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
for dist in np.arange(d_min, d_max+d_step, d_step):
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
