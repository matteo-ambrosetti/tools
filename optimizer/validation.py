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
parser.add_argument("-m", dest="molecule", required=True, default="water",
                    help="""Choose the name of the molecule to parameterize:\n
                    water\n acetonitrile\n benzene\n methanol.""", type=str)
parser.add_argument("-ifp", dest="inputfolderparams", required=True,
                    help="Input folder where parameters output files are stored.", type=str)
parser.add_argument("-ifg", dest="inputfoldergeoms", required=True,
                    help="Input folder where geometry files are stored.", type=str)
parser.add_argument("-ifl", dest="inputfolderlogs", required=True,
                    help="Input folder where reference files are stored.", type=str)
parser.add_argument("-uat", dest="useatomtype", action='store_true',
                    help="Choose to use atom types or not, see optimizer.py.")


rmin=2.0
rmax=5.0
rstep=1.0
nframes=100
nbest=1
nruns=20

args = parser.parse_args()


molecule = args.molecule.lower()
inputfolderparams = args.inputfolderparams
inputfoldergeoms  = args.inputfoldergeoms #"/home/m.ambrosetti/dataset_dipole_scan/test_bulk_polar_mu/xyz"
inputfolderlogs   = args.inputfolderlogs  #"/home/m.ambrosetti/dataset_dipole_scan/test_bulk_polar_mu/com_water_tip3p_polar"
use_at = args.useatomtype
paramfile = "opt_param.csv"


o = open("validation_{}.csv".format(molecule),"w")


for run in range(1,nruns+1):
    # Reference data    <<------<<<<<- DEVE RESTARE QUI PERCHE' ridefinisco ref_*
    if molecule == "water":
        geomfile  = "../dataset/water.xyz"
        ref_mu    = np.array([0.0, 0.0, 0.73285])
        ref_iso   = 9.26401
        ref_aniso = 0.838698
    elif molecule == "acetonitrile":
        geomfile  = "../dataset/acetonitrile.xyz"
        ref_mu    = np.array([-1.55842, 0.0, 1.93018e-05])
        ref_iso   = 28.5891
        ref_aniso = 14.5023
    elif molecule == "methanol":
        geomfile  = "../dataset/methanol.xyz"
        ref_mu    = np.array([0.393081, 0.468925, 0.26685])
        ref_iso   = 20.6071
        ref_aniso = 3.17240
    elif molecule == "benzene":
        geomfile  = "../dataset/benzene.xyz"
        ref_mu     = np.array([-0.135469e-04, 0.0, 0.0])
        ref_iso    = 65.0206
        ref_aniso  = 36.0713

    # Run number
    o.write("# Run {}\n".format(run))

    # Load parameters of a specific run
    A = np.loadtxt("{}/output_{}.txt".format(inputfolderparams,run))

    # Take the first nbest parameters of the run
    BestN  = sorted(A,key=lambda x: x[0])[0:nbest]
    cost   = np.asarray([i[0] for i in BestN])
    params = np.asarray([i[1:] for i in BestN])

    # Initialize the index of the parameters
    indx = 1
    for param in params:
        # Write the header
        if molecule == "water":
            o.write("#           ChiH            EtaH            ChiO            EtaO\n")
            o.write("#")
            for param_i in param:
                o.write(" {:>15.4e}".format(param_i))
            o.write("\n")
            o.write("#            Cost    Isopol_error  Anisopol_error  Dipole_error_x  Dipole_error_y  Dipole_error_z            ChiH            EtaH            ChiO            EtaO\n")
        elif molecule == "acetonitrile":
            if use_at == True:
                o.write("#            Cost    Isopol_error  Anisopol_error  Dipole_error_x  Dipole_error_y  Dipole_error_z" + \
                        "          ChiCH3          EtaCH3           ChiCN           EtaCN            ChiN            EtaN            ChiH            EtaH\n")
            elif use_at == False:
                o.write("#            Cost    Isopol_error  Anisopol_error  Dipole_error_x  Dipole_error_y  Dipole_error_z" + \
                        "          ChiC            EtaC             ChiN            EtaN            ChiH            EtaH\n")
        elif molecule == "methanol":
            o.write("#            Cost    Isopol_error  Anisopol_error  Dipole_error_x  Dipole_error_y  Dipole_error_z" + \
                    "          ChiCH3          EtaCH3          ChiH3C          EtaH3C           ChiOH           EtaOH           ChiHO           EtaHO\n")
        elif molecule == "benzene":
            o.write("#            Cost    Isopol_error  Anisopol_error  Dipole_error_x  Dipole_error_y  Dipole_error_z            ChiH            EtaH            ChiC            EtaC\n")

        # Write the param file
        f = open(paramfile,"w")
        f.write("# atom_type   chi                 eta      a.u.\n")
        if molecule == "water":
            f.write("H {} {}\n".format(param[0],param[1]))
            f.write("O {} {}\n".format(param[2],param[3]))
        if molecule == "acetonitrile":
            if use_at == True:
                f.write("CH3 {} {}\n".format(param[0],param[1]))
                f.write("CN  {} {}\n".format(param[2],param[3]))
                f.write("N   {} {}\n".format(param[4],param[5]))
                f.write("H   {} {}\n".format(param[6],param[7]))
            elif use_at == False:
                f.write("CH3 {} {}\n".format(param[0],param[1]))
                f.write("CN  {} {}\n".format(param[0],param[1]))
                f.write("N   {} {}\n".format(param[2],param[3]))
                f.write("H   {} {}\n".format(param[4],param[5]))
        if molecule == "methanol":
            f.write("CH3 {:>12.8f} {:>12.8f}\n".format(param[0],param[1]))
            f.write("H3C {:>12.8f} {:>12.8f}\n".format(param[2],param[3]))
            f.write("OH  {:>12.8f} {:>12.8f}\n".format(param[4],param[5]))
            f.write("HO  {:>12.8f} {:>12.8f}\n".format(param[6],param[7]))
        if molecule == "benzene":
            f.write("H {} {}\n".format(param[0],param[1]))
            f.write("C {} {}\n".format(param[2],param[3]))
        f.close()

        # SINGLE MOLECULE
        o.write("# Single molecule validation\n")

        # Initialize the input dictionary
        in_file_dict = {}
        in_file_dict["system_name"]     = molecule
        in_file_dict["out_folder"]      = "results_opt/"
        in_file_dict["out_file_name"]   = "results_opt/mms_{}.log".format(run)
        in_file_dict["model"]           = "fq"
        in_file_dict["kernel"]          = "ohno"
        in_file_dict["try_guess"]       = True
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

        # Build the RHS matrix
        RHS = make_right_hand_side_fq_fqfmu(system)

        # Solve the Ax=b problem and get the atomic charges
        q  = inversion(LHS, RHS, System=system)

        # Polarizability
        polar = polarizability(system,LHS,RHS)

        # Dipole Moment
        mu = dipole_moment(system, q[0:system.NumAtoms])

        # Interaction Energy
        Eint = interaction_energy(system, q=q[0:system.NumAtoms], mu=q[system.NumAtoms+system.NumGroups:])

        o.write("  {:>15.5e} {:>15.4f} {:>15.4f}".format(cost[0], 100*(ref_iso-polar[1])/ref_iso, 100*(ref_aniso-polar[2])/ref_aniso))
        for mu_i in (100*(ref_mu-mu[0][0])/ref_mu):
            o.write(" {:>15.4f}".format(mu_i))
        for param_i in param:
            o.write(" {:>15.4e}".format(param_i))
        o.write("\n")

        #print("Run index                          : ", run)
        #print("Parameters                         : ", param)
        #print("Cost                               : ", cost)
        #print("Parameter index                    : ", indx)
        #print("Charges                            : ", q[0:3])
        #print("Isotropic Polarizability   (error) : ", polar[1], "(", ref_iso - polar[1], ")")
        #print("Anisotropic Polarizability (error) : ", polar[2], "(", ref_aniso - polar[2], ")")
        #print("Dipole moment              (error) : ", mu[0][0], "(", ref_mu - mu[0][0], ")")
        #print("Energy                             : ", Eint[0])
        #print("\n")
        indx += 1


        # BULK
        o.write("# Bulk validation\n")
        iso_error = []
        aniso_error = []
        mu_error = []
        # Run over the sphere of different radius
        for r in np.arange(rmin,rmax,rstep):
            # Run over the frames from which the spheres are extracted
            for fr in range(nframes):
                # Set the new input file
                in_file_dict["geometry_file"] = "{}/sphere_r{}_fr{}.xyz".format(inputfoldergeoms,int(r),fr)

                # Initialize the system
                system = System(in_file_dict)

                # Get the geomtry of the system
                try:
                    system.read_xyz(in_filename=in_file_dict["geometry_file"])
                except:
                    continue

                # Get the parameters from the paramfile
                system.get_params()

                # Build the LHS matrix
                LHS = make_left_hand_side_fq_fqfmu(system)

                # Build the RHS matrix
                RHS = make_right_hand_side_fq_fqfmu(system)

                # Solve the Ax=b problem and get the atomic charges
                q  = inversion(LHS, RHS, System=system)

                # Polarizability
                polar = polarizability(system,LHS,RHS)

                # Dipole Moment
                mu = np.sum(dipole_moment(system, q[0:system.NumAtoms])[0], axis=0)

                # Get the dipole moment and the polarizability from log file
                ref_mu = []
                try:
                    # Dipole
                    a = os.popen("grep -A 6 'Electric dipole moment (input orientation):' {}/sphere_r{}_fr{}.log".format(inputfolderlogs, int(r), fr)).read()
                    char_indx = 0
                    for char in a.split():
                        if char == 'x' or char == 'y' or char == 'z':
                            ref_mu.append(float(a.split()[char_indx+1].replace("D","E")))
                        char_indx += 1
                    ref_mu = np.array(ref_mu)
                    # Polarizability
                    ref_iso   = float(os.popen("grep 'iso'   {}/sphere_r{}_fr{}.log".format(inputfolderlogs, int(r), fr)).read().split()[1].replace("D","E"))
                    ref_aniso = float(os.popen("grep 'aniso' {}/sphere_r{}_fr{}.log".format(inputfolderlogs, int(r), fr)).read().split()[1].replace("D","E"))
                    # Append the results
                    mu_error.append(abs(ref_mu - mu))
                    iso_error.append(abs(ref_iso - polar[1]))
                    aniso_error.append(abs(ref_aniso - polar[2]))
                except:
                    continue

                werbosity = 1
                if werbosity > 2:
                    o.write("{:<15} {:>15.5e} {:>15.4f} {:>15.4f}".format(geomfile.split("/")[-1].split(".xyz")[0], cost[0], 100*(ref_iso-polar[1])/ref_iso, 100*(ref_aniso-polar[2])/ref_aniso))
                    for mu_i in (100*(ref_mu-mu)/ref_mu):
                        o.write(" {:>15.4f}".format(mu_i))
                    for param_i in param:
                        o.write(" {:>15.4e}".format(param_i))
                    o.write("\n")

        o.write("Mean  isopolar error      : {:<10.4f} +/- {:<10.4f}\n".format(np.mean(iso_error),np.std(iso_error)))
        o.write("Mean  anisopolar error    : {:<10.4f} +/- {:<10.4f}\n".format(np.mean(aniso_error),np.std(aniso_error)))
        o.write("Mean  dipole moment error : {:<10.4f} +/- {:<10.4f}\n".format(np.mean(mu_error),np.std(mu_error)))
        o.write("\n")

o.close()

os.system("mv validation_{}.csv {}/".format(molecule,inputfolderparams))




### CLUSTER MOLECULE VALIDATION
#o.write("Bulk properties validation\n")
#
#for run in range(1,11):
#    o.write("Run {}\n".format(run))
#    # Load parameters of a specific run
#    A = np.loadtxt("{}/output_{}.txt".format(inputfolder,run))
#
#    paramfile = "opt_param.csv"
#    N = 1
#    BestN  = sorted(A,key=lambda x: x[0])[0:N]
#    cost   = np.asarray([i[0] for i in BestN])
#    params = np.asarray([i[1:] for i in BestN])
#
#    iso_error = []
#    aniso_error = []
#    mu_error = []
#    for r in np.arange(2.0, 5.0, 1.0):
#        for fr in range(100):
#            geomfile  = "/home/m.ambrosetti/dataset_dipole_scan/test_qmqm/sphere/xyz/sphere_r{}_fr{}.xyz".format(int(r),fr)
#            for param in params:
#                f = open(paramfile,"w")
#                f.write("# atom_type   chi                 eta      a.u.\n")
#                # Water
#                f.write("H {} {}\n".format(param[0],param[1]))
#                f.write("O {} {}\n".format(param[2],param[3]))
#                f.close()
#
#                # Initialize the input dictionary
#                in_file_dict = {}
#                in_file_dict["system_name"]     = molecule
#                in_file_dict["out_folder"]      = "results_opt/"
#                in_file_dict["out_file_name"]   = "results_opt/mms_{}.log".format(run)
#                in_file_dict["model"]           = "fq"
#                in_file_dict["kernel"]          = "ohno"
#                in_file_dict["try_guess"]       = True
#                in_file_dict["parameters_file"] = paramfile
#                in_file_dict["geometry_file"]   = geomfile
#                in_file_dict["werbosity"]       = 2
#
#                # Initialize the system
#                system = System(in_file_dict)
#
#                # Get the geomtry of the system
#                try:
#                    system.read_xyz(in_filename=in_file_dict["geometry_file"])
#                except:
#                    continue
#
#                # Get the parameters from the paramfile
#                system.get_params()
#
#                # Build the LHS matrix
#                LHS = make_left_hand_side_fq_fqfmu(system)
#
#                # Build the RHS matrix
#                RHS = make_right_hand_side_fq_fqfmu(system)
#
#                # Solve the Ax=b problem and get the atomic charges
#                q  = inversion(LHS, RHS, System=system)
#
#                # Polarizability
#                polar = polarizability(system,LHS,RHS)
#
#                # Dipole Moment
#                mu = np.sum(dipole_moment(system, q[0:system.NumAtoms])[0], axis=0)
#
#                # Get the dipole from log file
#                ref_mu = []
#                try:
#                    a = os.popen("grep -A 6 'Electric dipole moment (input orientation):' /home/m.ambrosetti/dataset_dipole_scan/test_qmqm/sphere/com_water_polar/sphere_r{}_fr{}.log".format(int(r), fr)).read()
#                    char_indx = 0
#                    for char in a.split():
#                        if char == 'x' or char == 'y' or char == 'z':
#                            ref_mu.append(float(a.split()[char_indx+1].replace("D","E")))
#                        char_indx += 1
#                    ref_mu = np.array(ref_mu)
#                    mu_error.append(abs(ref_mu - mu))
#                except:
#                    continue
#
#
#                try:
#                    ref_iso   = float(os.popen("grep 'iso' /home/m.ambrosetti/dataset_dipole_scan/test_qmqm/sphere/com_water_polar/sphere_r{}_fr{}.log".format(int(r), fr)).read().split()[1].replace("D","E"))
#                    ref_aniso = float(os.popen("grep 'iso' /home/m.ambrosetti/dataset_dipole_scan/test_qmqm/sphere/com_water_polar/sphere_r{}_fr{}.log".format(int(r), fr)).read().split()[2].replace("D","E"))
#                    iso_error.append(abs(ref_iso - polar[1]))
#                    aniso_error.append(abs(ref_aniso - polar[2]))
#                except:
#                    continue
#
#                werbosity = 1
#                if werbosity > 2:
#                    o.write("{:<15} {:>15.5e} {:>15.4f} {:>15.4f}".format(geomfile.split("/")[-1].split(".xyz")[0], cost[0], 100*(ref_iso-polar[1])/ref_iso, 100*(ref_aniso-polar[2])/ref_aniso))
#                    for mu_i in (100*(ref_mu-mu)/ref_mu):
#                        o.write(" {:>15.4f}".format(mu_i))
#                    for param_i in param:
#                        o.write(" {:>15.4e}".format(param_i))
#                    o.write("\n")
#
#    o.write("            ChiH            EtaH            ChiO            EtaO\n")
#    for param_i in param:
#        o.write(" {:>15.4e}".format(param_i))
#    o.write("\n")
#    o.write("Mean  isopolar error      : {:<10.4f} +/- {:<10.4f}\n".format(np.mean(iso_error),np.std(iso_error)))
#    o.write("Mean  anisopolar error    : {:<10.4f} +/- {:<10.4f}\n".format(np.mean(aniso_error),np.std(aniso_error)))
#    o.write("Mean  dipole moment error : {:<10.4f} +/- {:<10.4f}\n".format(np.mean(mu_error),np.std(mu_error)))
#    o.write("\n")
#o.close()
