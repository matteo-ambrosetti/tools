import MDAnalysis
import argparse
import os

parser = argparse.ArgumentParser(description='Generate eT input files.')
parser.add_argument("-suf", dest="suffix", required=True,  help="Suffix.", type=str)
parser.add_argument("-n",   dest="name",   required=False, help="Molecule name.",
                    default="", type=str)
parser.add_argument("-if", dest="inputfolder", required=True,
                    help="Input folder path.", type=str)
parser.add_argument("-of", dest="outputfolder", required=True,
                    help="Output folder path.", type=str)
parser.add_argument("-fun", dest="functional", required=False, default="hf",
                    help="Functional.", type=str)
parser.add_argument("-bas", dest="basis_set", required=False, default="6-311++g**",
                    help="Basis set.", type=str)
args = parser.parse_args()

# Add / to the folder name if needed
if args.inputfolder[-1] != "/":
    args.inputfolder += "/"
if args.outputfolder[-1] != "/":
    args.outputfolder += "/"

functional = args.functional
basis_set  = args.basis_set
in_folder  = args.inputfolder
out_folder = args.outputfolder
suffix     = args.suffix
molecule_name = args.name
try:
    os.makedirs(out_folder)
except:
    pass




def write_eT(infile, outfile, comment, functional, basis_set):

    # Read input geometry
    u = MDAnalysis.Universe(infile)

    # Open output file
    f = open(outfile,"w")

    # Write the output
    f.write("system\n")
    f.write("   name: {}\n".format(comment))
    f.write("   charge: 0\n")
    f.write("end system\n\n")

    f.write("do\n")
    f.write("  ground state\n")
    f.write("end do\n\n")

    f.write("memory\n")
    f.write("   available: 8\n")
    f.write("end memory\n\n")

    f.write("solver scf\n")
    f.write("   algorithm: scf-diis\n")
    f.write("end solver scf\n\n")

    f.write("molecular mechanics\n")
    f.write("   forcefield: non-polarizable\n")
    f.write("end molecular mechanics\n\n")

    f.write("method\n")
    f.write("   hf\n".format(functional))
    f.write("end method\n\n")

    f.write("geometry\n")
    f.write("basis: {}\n".format(basis_set))
    for i in range(u.atoms.n_atoms):
        if u.atoms.names[i] != "Po" and u.atoms.names[i] != "Ne":
            f.write("{:<2} ".format(u.atoms.names[i]))
            for j in range(3):
                f.write("{:>12.6f} ".format(u.atoms.positions[i,j]))
            f.write("\n")
    f.write(" --\n")
    for i in range(u.atoms.n_atoms):
        if u.atoms.names[i] == "Po" or u.atoms.names[i] == "Ne":
            f.write("H [IMol=1] ".format(u.atoms.names[i]))
            for j in range(3):
                f.write("{:>12.6f} ".format(u.atoms.positions[i,j]))
            if u.atoms.names[i] == "Po":
                f.write("[q=+1.0]\n".format(u.atoms.names[i]))
            elif u.atoms.names[i] == "Ne":
                f.write("[q=-1.0]\n".format(u.atoms.names[i]))
    f.write("end geometry")
    f.close()


subfile = out_folder + "sub_eT.sh"
f = open(subfile,"w")
f.write("#!/bin/bash\n")
f.write("eT=/home/m.ambrosetti//eT/build_mlhf_opt_new/./eT_launch\n")
for name in os.listdir(in_folder):
    if name.startswith(suffix):
        suff = name.split(".xyz")[0]
        dist = suff.split("_d")[-1]
        comment = "{} scan {}".format(molecule_name, dist)
        infile  = in_folder  + name
        outfile = out_folder + suff + ".inp"
        write_eT(infile, outfile, comment, functional, basis_set)
        f.write("$eT {}\n".format(suff + ".inp"))
        f.write("wait\n")
f.close()
os.system("chmod +x {}".format(subfile))
