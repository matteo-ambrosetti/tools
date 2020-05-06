from MMS.io.read_input_file     import make_dictionary
from MMS.system.make_system     import System
from MMS.solver.make_matrices   import make_left_hand_side_fq_fqfmu
from MMS.solver.make_matrices   import make_right_hand_side_fq_fqfmu
from MMS.observable.observables import interaction_energy
from MMS.solver.solvers         import inversion
from MMS.observable.observables import dipole_moment
from MMS.observable.observables import polarizability
import numpy as np
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Generate structures.')
parser.add_argument("-ifp", dest="inputfolderparam", required=True,
                    help="Input folder where the parameters are stored", type=str)
parser.add_argument("-ifg", dest="inputfoldergeom", required=True,
                    help="Input folder where the geometries are stored.", type=str)
parser.add_argument("-p", dest="prefix", required=True,
                    help="Input geometries prefix.", type=str)
parser.add_argument("-d_min", dest="dmin", required=False, default=2.5,
                    help="Minimum distance of the dipole from the molecule.", type=float)
parser.add_argument("-d_max", dest="dmax", required=False, default=10.0,
                    help="Maximum distance of the dipole from the molecule.", type=float)
parser.add_argument("-d_step", dest="dstep", required=False, default=0.25,
                    help="Step of the scan.", type=float)
parser.add_argument("-n", dest="nruns", required=True,
                    help="Number of optimized runs to be considered.", type=int)
parser.add_argument("-nb", dest="nbest", required=False, default=1,
                    help="Take the first nbest parameters from each run.", type=int)
parser.add_argument("-uat", dest="useatomtype", action='store_true',
                    help="Choose to use atom types or not, see optimizer.py.")
args = parser.parse_args()


runs_folder = args.inputfolderparam
geom_folder = args.inputfoldergeom
if runs_folder[-1] == "/":
    pass
else:
    runs_folder += "/"
if geom_folder[-1] == "/":
    pass
else:
    geom_folder += "/"

geom_prefix = args.prefix
nruns     = args.nruns
nbestxrun = args.nbest
d_min  = args.dmin
d_max  = args.dmax
d_step = args.dstep
use_at = args.useatomtype
paramfile = "opt_param.csv"

# Iterate over all the runs
for run in range(1,nruns+1):
    # Load all the parameters
    A = np.loadtxt(runs_folder + "output_{}.txt".format(run))
    # Take the best nbestxrun parameters and their cost function
    BestN  = sorted(A,key=lambda x: x[0])[0:nbestxrun]
    cost   = np.asarray([i[0]  for i in BestN])
    param_list = np.asarray([i[1:] for i in BestN])

    for j, param in enumerate(param_list):
        o = open("{}/graph_run{}_top{}_{}.csv".format(runs_folder,run,j+1,geom_folder.split("/")[-2]),"w")
        # Write the run number
        o.write("# Run number : {}\n".format(run))
        o.write("# Parameter set number : {}\n".format(j+1))
        o.write("# Cost function : {}\n".format(cost[j]))
        ## Water
        #o.write("#      ChiH            EtaH            ChiO            EtaO\n")
        # Acetonitrile
        #if use_at == True:
        #    o.write("#       ChiCH3          EtaCH3           ChiCN           EtaCN            ChiN            EtaN            ChiH            EtaH\n")
        #elif use_at == False:
        #    o.write("#       ChiC            EtaC             ChiN            EtaN             ChiH            EtaH\n")
        # Methanol
        if use_at == True:
            o.write("#       ChiCH3          EtaCH3          ChiH3C          EtaH3C           ChiOH           EtaOH           ChiHO           EtaHO\n")
        elif use_at == False:
            o.write("#       ChiC            EtaC            ChiH            EtaH             ChiO            EtaO\n")
        o.write("#")
        for param_i in param:
            o.write(" {:>15.4e}".format(param_i))
        o.write("\n")
        o.write("# Distance     Computed     Reference\n")

        # Write the j-th parameter set of the i-th run on the opt_param.csv file
        f = open(paramfile,"w")
        f.write("# atom_type   chi                 eta      a.u.\n")
        ## Water
        #f.write("H {} {}\n".format(param[0],param[1]))
        #f.write("O {} {}\n".format(param[2],param[3]))
        ## Acetonitrile
        #if use_at == True:
        #    f.write("CH3 {:>12.8f} {:>12.8f}\n".format(param[0],param[1]))
        #    f.write("CN  {:>12.8f} {:>12.8f}\n".format(param[2],param[3]))
        #    f.write("N   {:>12.8f} {:>12.8f}\n".format(param[4],param[5]))
        #    f.write("H   {:>12.8f} {:>12.8f}\n".format(param[6],param[7]))
        #elif use_at == False:
        #    f.write("CH3 {} {}\n".format(param[0],param[1]))
        #    f.write("CN  {} {}\n".format(param[0],param[1]))
        #    f.write("N   {} {}\n".format(param[2],param[3]))
        #    f.write("H   {} {}\n".format(param[4],param[5]))
        # Methanol
        if use_at == True:
            f.write("CH3 {:>12.8f} {:>12.8f}\n".format(param[0],param[1]))
            f.write("H3C {:>12.8f} {:>12.8f}\n".format(param[2],param[3]))
            f.write("OH  {:>12.8f} {:>12.8f}\n".format(param[4],param[5]))
            f.write("HO  {:>12.8f} {:>12.8f}\n".format(param[6],param[7]))
        elif use_at == False:
            f.write("CH3 {:>12.8f} {:>12.8f}\n".format(param[0],param[1]))
            f.write("H3C {:>12.8f} {:>12.8f}\n".format(param[2],param[3]))
            f.write("OH  {:>12.8f} {:>12.8f}\n".format(param[4],param[5]))
            f.write("HO  {:>12.8f} {:>12.8f}\n".format(param[2],param[3]))
        # Non commentare mai!
        f.write("Po {} {}\n".format(param[0],param[1]))
        f.write("Ne {} {}\n".format(param[0],param[1]))
        f.close()

        for dist in np.arange(d_min, d_max+d_step, d_step):
            geomfile = "{}/{}{:.2f}.xyz".format(geom_folder,geom_prefix,dist)

            # Initialize the input dictionary
            in_file_dict = {}
            in_file_dict["system_name"]     = "water"
            in_file_dict["out_folder"]      = "results_opt/"
            in_file_dict["out_file_name"]   = "results_opt/mms_{}.log".format(run)
            in_file_dict["model"]           = "fq"
            in_file_dict["kernel"]          = "ohno"
            in_file_dict["try_guess"]       = False
            in_file_dict["parameters_file"] = paramfile
            in_file_dict["geometry_file"]   = geomfile
            in_file_dict["werbosity"]       = 2

            # Initialize the system
            system = System(in_file_dict)

            # Get the geomtry of the system
            system.read_xyz(in_filename=in_file_dict["geometry_file"])

            # Get the parameters from the paramfile
            system.get_params()

            # Build the LHS matrix
            LHS = make_left_hand_side_fq_fqfmu(system)

            # Set the charge of each moiety
            #  1         2   3 
            # [Molecule, Po, Ne]
            system.MolCharge = [0.0, 1.0, -1.0]

            # Build the RHS matrix
            RHS = make_right_hand_side_fq_fqfmu(system)

            # Solve the Ax=b problem and get the atomic charges
            q  = inversion(LHS, RHS, System=system)

            # Interaction Energy between the molecule and the dipole
            Eint = interaction_energy(system, q=q[0:system.NumAtoms], mu=q[system.NumAtoms+system.NumGroups:])


            # Get the reference value of a specific geometry
            ref  = float(os.popen("grep 'QM/MM Electrostatic Energy:' {}/eT/{}{:.2f}.out".format(geom_folder,geom_prefix,dist)).read().split()[-1])

            # Get the interaction energy 1-2 and 1-3 and convert it to kcal/mol
            comp = (Eint[0,1]+Eint[0,2])*627.509

            o.write("  {:<12.5f} {:<12.8f} {:<12.8f}\n".format(dist, comp, ref))
        o.close()
