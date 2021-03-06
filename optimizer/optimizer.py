# Python modules
import numpy as np
import sys
import os
# My modules
from MMS.io.read_input_file     import make_dictionary
from MMS.system.make_system     import System
from MMS.solver.make_matrices   import make_left_hand_side_fq_fqfmu
from MMS.solver.make_matrices   import make_right_hand_side_fq_fqfmu
from MMS.observable.observables import interaction_energy
from MMS.solver.solvers         import inversion
# Optimization modules
import inspyred
from random import Random
from time import time
from time import sleep
from inspyred import ec
from inspyred.ec import terminators
import argparse




parser = argparse.ArgumentParser(description='Generate structures.')
parser.add_argument("-p", dest="paramfile", required=False, default="param.csv",
                    help="Name of parameters file.", type=str)
parser.add_argument("-p_min", dest="param_min", required=False, default=1.0e-08,
                    help="Lower bound.", type=float)
parser.add_argument("-p_max", dest="param_max", required=False, default=1.0,
                    help="Higher bound.", type=float)
parser.add_argument("-o", dest="outfile", required=False, default="output.txt",
                    help="Name of the output file.", type=str)
parser.add_argument("-m", dest="molecule", required=True, default="water",
                    help="""Choose the name of the molecule to parameterize:
                    water acetonitrile benzene methanol.""", type=str)
parser.add_argument("-of", dest="outfolder", required=False, default="out/",
                    help="Name of the output folder.", type=str)
parser.add_argument("-wt", dest="wtype", required=True,
                    help="Weights type. 1 1/r", type=str)
#
# TODO
# Prendi come input una lista di stringhe che corrispondono a folder_list
# Prendi come input una stringa che corrisponde al prefisso delle geometrie
pop_size = 100

args = parser.parse_args()


 # Make the output directory
if args.outfolder[-1] != "/":
    args.outfolder += "/"
try:
    os.makedirs(args.outfolder)
except:
    pass

molecule = args.molecule.lower()
if molecule == "water":
    prefix  = "water_d"
    nparams = 4
    folder_list = ["water_plane_H",
                   "water_plane_O",
                   "water_scan_H-O-H_bisec",
                   "water_scan_H-O-H_bisec_ext",
                   "water_scan_O-H"]
elif molecule == "acetonitrile":
    prefix = "acetonitrile_d"
    nparams = 8
    folder_list = ["acetonitrile_scan_C-C",
                   "acetonitrile_scan_C-H",
                   "acetonitrile_scan_C-N"]
elif molecule == "acetonitrile_no_at":
    prefix = "acetonitrile_d"
    nparams = 6
    folder_list = ["acetonitrile_scan_C-C",
                   "acetonitrile_scan_C-H",
                   "acetonitrile_scan_C-N"]
elif molecule == "methanol":
    prefix = "methanol_d"
    nparams = 8
    folder_list = ["methanol_scan_C-H_1",
                   "methanol_scan_C-H_2",
                   "methanol_scan_C-O",
                   "methanol_scan_O-C",
                   "methanol_scan_O-H"]
elif molecule == "methanol_no_at":
    prefix = "methanol_d"
    nparams = 6
    folder_list = ["methanol_scan_C-H_1",
                   "methanol_scan_C-H_2",
                   "methanol_scan_C-O",
                   "methanol_scan_O-C",
                   "methanol_scan_O-H"]
elif molecule == "benzene":
    prefix = "benzene_d"
    nparams = 4
    folder_list = ["benzene_plane_C",
                   "benzene_plane_H",
                   "benzene_scan_C-H"]

outputfile = args.outfolder + args.outfile
paramfile  = args.outfolder + args.paramfile
if os.path.exists(outputfile) or os.path.exists(paramfile):
    print("The output file already exist, exit...")
    sys.exit(0)
param_min  = args.param_min
param_max  = args.param_max

global offspring
offspring = 1

w_type = args.wtype


# EVALUATOR
def cost(params, args):


    global offspring

    # Input parameters
    paramfile  = args.get('paramfile',  'param.csv')
    outputfile = args.get('outputfile', 'output.txt')
    dmin  = args.get('dmin',  2.5)
    dmax  = args.get('dmax',  10.25)
    dstep = args.get('dstep', 0.25)
    prefix = args.get('prefix')

    # Initialize the cost function
    cost_list = []

    # Initialize dictionary for MMS
    in_file_dict = {}
    in_file_dict["system_name"]     = molecule
    in_file_dict["out_folder"]      = "results/"
    in_file_dict["model"]           = "fq"
    in_file_dict["kernel"]          = "ohno"
    in_file_dict["try_guess"]       = False
    in_file_dict["parameters_file"] = paramfile
    in_file_dict["werbosity"]       = 1


    # Print iteration number
    print("Offspring number ", offspring)

    # Run over the parameters list
    for parameters in params:

        # Initialize some list
        comp_list = []
        ref_list  = []
        w_list    = []

        # Initialize some parameter
        N = 0

        # TODO Rendilo piu' generico, prendi in input gli atom types
        # Generate input file
        f = open(paramfile,"w")
        f.write("# atom_type   chi                 eta      a.u.\n")
        if molecule == "water":
            f.write("H  {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
            f.write("O  {:>12.8f} {:>12.8f}\n".format(parameters[2],parameters[3]))
        elif molecule == "acetonitrile":
            f.write("CH3 {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
            f.write("CN  {:>12.8f} {:>12.8f}\n".format(parameters[2],parameters[3]))
            f.write("N   {:>12.8f} {:>12.8f}\n".format(parameters[4],parameters[5]))
            f.write("H   {:>12.8f} {:>12.8f}\n".format(parameters[6],parameters[7]))
        elif molecule == "acetonitrile_no_at":
            f.write("CH3 {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
            f.write("CN  {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
            f.write("N   {:>12.8f} {:>12.8f}\n".format(parameters[2],parameters[3]))
            f.write("H   {:>12.8f} {:>12.8f}\n".format(parameters[4],parameters[5]))
        elif molecule == "methanol":
            f.write("CH3 {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
            f.write("H3C {:>12.8f} {:>12.8f}\n".format(parameters[2],parameters[3]))
            f.write("OH  {:>12.8f} {:>12.8f}\n".format(parameters[4],parameters[5]))
            f.write("HO  {:>12.8f} {:>12.8f}\n".format(parameters[6],parameters[7]))
        elif molecule == "methanol_no_at":
            f.write("CH3 {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
            f.write("H3C {:>12.8f} {:>12.8f}\n".format(parameters[2],parameters[3]))
            f.write("OH  {:>12.8f} {:>12.8f}\n".format(parameters[4],parameters[5]))
            f.write("HO  {:>12.8f} {:>12.8f}\n".format(parameters[2],parameters[3]))
        elif molecule == "benzene":
            f.write("H  {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
            f.write("C  {:>12.8f} {:>12.8f}\n".format(parameters[2],parameters[3]))
        f.write("Po {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
        f.write("Ne {:>12.8f} {:>12.8f}\n".format(parameters[0],parameters[1]))
        f.close()

        # Run over several folders
        for folder in folder_list:

            # Run over the geometries
            for dist in np.arange(dmin, dmax, dstep):

                # Initialize the system
                in_file_dict["out_file_name"]   = "results/out.log"
                in_file_dict["geometry_file"]   = "../dataset/examples/{}/{}{:.2f}.xyz".format(folder,prefix,dist)

                # Make the system object
                system = System(in_file_dict)

                # Get the geomtry of the system
                geom_prefix = in_file_dict["geometry_file"].split(".xyz")[0].split("/")[-1]
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


                try:
                    # Solve the Ax=b problem and get the atomic charges
                    q  = inversion(LHS, RHS, System=system)

                    # Interaction energy
                    Eint = interaction_energy(system, q=q[0:system.NumAtoms], mu=q[system.NumAtoms+system.NumGroups:])

                    # Get the reference value of a specific geometry
                    ref  = float(os.popen("grep 'QM/MM Electrostatic Energy:' ../dataset/examples/{}/eT/{}{:.2f}.out".format(folder,prefix,dist)).read().split()[-1])

                    # Get the interaction energy 1-2 and 1-3 and convert it to kcal/mol 
                    comp = (Eint[0,1]+Eint[0,2])*627.509
                except:
                    # Get the reference value of a specific geometry
                    ref  = float(os.popen("grep 'QM/MM Electrostatic Energy:' ../dataset/examples/{}/eT/{}{:.2f}.out".format(folder,prefix,dist)).read().split()[-1])

                    # Set the interaction energy to an high value
                    comp = 1.0e10

                # Add to the list of observables
                # for a specific parameters set
                comp_list.append(comp)
                ref_list.append(ref)

                # Weights
                if w_type == "1/r":
                    w_list.append(dmin/dist)
                elif w_type == "1":
                    w_list.append(1.0)

                # Accumulate the total number of geometries used
                N += 1

        # Add to the cost function list
        cost_list.append(np.sum(np.asarray(w_list)*np.square(np.asarray(ref_list) - np.asarray(comp_list)))/N)
        o = open(outputfile,"a+")
        o.write("{:>15.8e} ".format(cost_list[-1]))
        for param_i in parameters:
            o.write("{:>15.8f} ".format(param_i))
        o.write("\n")
        o.close()

    # Update offspring value
    offspring += 1

    # Rimuovo il log perche' ci appende roba e fa un casino!
    os.system("rm {}".format(in_file_dict["out_file_name"]))

    return cost_list



# Generate initial parameters
# GENERATOR
def generate_parameters(random, args):
    size = args.get('num_inputs', 10)
    return [random.uniform(param_min, param_max) for i in range(size)]



# Initialize the output file
o = open(outputfile,"w")
o.write("#Cost                Parameters\n")
o.close()

rand = Random()
rand.seed(int(time()+np.random.randint(1,10e10)))
es = ec.ES(rand)
sleep(1)

# TERMINATOR
es.terminator = terminators.evaluation_termination

# Start optimization
final_pop = es.evolve(generator=generate_parameters,
                      evaluator=cost,
                      pop_size=pop_size,
                      maximize=False,
                      bounder=ec.Bounder(param_min, param_max),
                      max_evaluations=pop_size*500,
                      mutation_rate=0.25,
                      num_inputs=nparams,
                      outputfile=outputfile,
                      paramfile=paramfile,
                      prefix=prefix,
                      folder_list=folder_list
                      )

# Sort and print the best individual, who will be at index 0.
final_pop.sort(reverse=True)
#print(final_pop[0])

os.system("rm {}".format(paramfile))
