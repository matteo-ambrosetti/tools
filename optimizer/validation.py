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

# Reference values
## Acetonitrile
#ref_mu    = np.array([-1.55842, 0.0, 1.93018e-05])
#ref_iso   = 28.5891
#ref_aniso = 14.5023
# Water
ref_mu    = np.array([0.0, 0.0, 0.73285])
ref_iso   = 9.26401
ref_aniso = 0.838698

o = open("validation.csv","w")
# Water
o.write("#            Cost    Isopol_error  Anisopol_error  Dipole_error_x  Dipole_error_y  Dipole_error_z            ChiH            EtaH            ChiO            EtaO\n")
# Acetonitrile
#o.write("#            Cost    Isopol_error  Anisopol_error  Dipole_error_x  Dipole_error_y  Dipole_error_z" + \
#        "          ChiCH3          EtaCH3           ChiCN           EtaCN            ChiN            EtaN            ChiH            EtaH\n")

for run in range(1,11):
    # Load all the parameters
    # Water
    A = np.loadtxt("examples/water/out_w1.0_int0.0-1.0_1/output_{}.txt".format(run))
    geomfile  = "../dataset/water.xyz"
    # Acetonitrile
    #A = np.loadtxt("examples/acetonitrile/out_w1.0_int0.0-1.0/output_{}.txt".format(run))
    #geomfile  = "../dataset/acetonitrile.xyz"

    paramfile = "opt_param.csv"
    N = 1

    BestN  = sorted(A,key=lambda x: x[0])[0:N]
    cost   = np.asarray([i[0] for i in BestN])
    params = np.asarray([i[1:] for i in BestN])

    indx = 1
    for param in params:
        f = open(paramfile,"w")
        f.write("# atom_type   chi                 eta      a.u.\n")
        ## Acetonitrile
        #f.write("CH3 {} {}\n".format(param[0],param[1]))
        #f.write("CN  {} {}\n".format(param[2],param[3]))
        #f.write("N   {} {}\n".format(param[4],param[5]))
        #f.write("H   {} {}\n".format(param[6],param[7]))
        # Water
        f.write("H {} {}\n".format(param[0],param[1]))
        f.write("O {} {}\n".format(param[2],param[3]))
        f.close()

        # Initialize the input dictionary
        in_file_dict = {}   #make_dictionary("input.txt")
        in_file_dict["system_name"]     = "water"
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


        print("Run index                          : ", run)
        print("Parameters                         : ", param)
        print("Cost                               : ", cost)
        print("Parameter index                    : ", indx)
        print("Charges                            : ", q[0:3])
        print("Isotropic Polarizability   (error) : ", polar[1], "(", ref_iso - polar[1], ")")
        print("Anisotropic Polarizability (error) : ", polar[2], "(", ref_aniso - polar[2], ")")
        print("Dipole moment              (error) : ", mu[0][0], "(", ref_mu - mu[0][0], ")")
        print("Energy                             : ", Eint[0])
        print("\n")
        indx += 1

o.close()
