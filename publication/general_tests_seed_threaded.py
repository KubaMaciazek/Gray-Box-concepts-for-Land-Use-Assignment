import time

import numpy as np
from deap import creator, base, tools

from publication.algorithms.nsgaii.nsgaii_optimization_ffe import nsgaii_optimization_ffe
from publication.general_test.register_initialization import register_initialization
from publication.general_test.register_mutation import register_mutation
from publication.general_test.register_repair import register_repair
from publication.general_test.register_sample import register_sample
from publication.general_test.setup_individual_test_run import setup_individual_test_run
from publication.statistics.save_results import save_results

from publication.operators.crossovers.ac import ac
from publication.operators.crossovers.ppc import ppc
from publication.operators.crossovers.spc import spc
from publication.operators.crossovers.ppc_fuo import ppc_fuo


# def run_single_test(seed, sample, initialization, mutation, crossover, repair, n_pop, NFFE, cxpb, mutpb, toolbox,
#                     nr_of_tests, test_nr, starting_time, test_stamp, algorithm):
def run_single_test(algorithm,
                    n_pop, NFFE, cxpb, mutpb,
                    w1, w2,
                    seed,
                    sample,
                    initialization, mutation, crossover, repair,
                    nr_of_tests, test_nr, starting_time, test_stamp):
    print("run_single_test - nsgaii")

    creator.create("FitnessMax", base.Fitness, weights=(w1, w2))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("select", tools.selNSGA2)

    """
    Function to run a single test setup with given parameters.
    """
    # Extract relevant paths and data
    areal_raster_path, sq_raster_path, areal, sq_raster_normalized, int_quantity, ref_point_convergence \
        = register_sample(sample, toolbox)
    register_initialization(initialization, toolbox, areal_raster_path, sq_raster_path, int_quantity, n_pop)
    register_mutation(mutation, toolbox, int_quantity, areal)
    toolbox.register("mate", eval(crossover))
    register_repair(repair, toolbox, int_quantity, areal)

    test_nr, start_time, population, hof\
        = setup_individual_test_run(seed, test_nr, starting_time, nr_of_tests, toolbox, NFFE, n_pop, 0)

    # Perform NSGA-II optimization
    hvs, fits_hof_all = nsgaii_optimization_ffe(population, NFFE, n_pop, toolbox, cxpb, mutpb, hof,
                                                ref_point_convergence)

    elapsed_time = time.time() - start_time

    # Save results
    save_results(hvs, elapsed_time, fits_hof_all, test_stamp, NFFE, "n_pop",
                 f"{algorithm};{initialization};{mutation};{crossover};{repair};{n_pop};{int(cxpb*100)};{int(mutpb*100)}", seed, sample)

    return seed, hvs, fits_hof_all, elapsed_time

"""
        ------------------------------------- Old version -----------------------------------------------
"""

#
# import random
# import time
#
# import numpy as np
# from deap import creator, base, tools
#
# from publication.algorithms.nsgaii.nsgaii_optimization import nsgaii_optimization
# from publication.algorithms.nsgaii.nsgaii_optimization_ffe import nsgaii_optimization_ffe
# from publication.general_test.register_initialization import register_initialization
# from publication.general_test.register_mutation import register_mutation
# from publication.general_test.register_repair import register_repair
# from publication.general_test.register_sample import register_sample
# from publication.general_test.setup_individual_test_run import setup_individual_test_run
# from publication.general_test.tests_configs import get_general_tests_config
#
# from publication.operators.crossovers.ac import ac
# from publication.operators.crossovers.ppc import ppc
# from publication.operators.crossovers.spc import spc
# from publication.operators.crossovers.ppc_fuo import ppc_fuo
# from publication.statistics.save_results import save_results
#
#
# # FOR NOW FOR NSGA-II
#
# def general_tests_seed_threaded(algorithm,
#                                 n_pop, NFFE, cxpb, mutpb,
#                                 w1, w2,
#                                 seed,
#                                 sample_municipalities,
#                                 list_initializations, list_mutations, list_crossovers, list_repairs,
#                                 nr_of_tests, test_nr, starting_time, test_stamp,
#                                 thread_nr):
#     """
#     ------------------------------------ GENERAL TEST CONFIG ------------------------------------
#     """
#
#     # algorithm = "nsgaii"
#     # (n_pop, NFFE, cxpb, mutpb,
#     #  w1, w2,
#     #  _,
#     #  sample_municipalities,
#     #  list_initializations, list_mutations, list_crossovers, list_repairs,
#     #  nr_of_tests, test_nr, starting_time, test_stamp) = get_general_tests_config()
#     # print('Test stamp: ' + test_stamp)
#
#     # creator.create("FitnessMax", base.Fitness, weights=(w1, w2))
#     # creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)
#
#     toolbox = base.Toolbox()  # Should it be reset somewhere in the loop?
#     toolbox.register("select", tools.selNSGA2)
#
#
#     """
#         Testing purposes only
#     """
#     # NFFE = 2                           # FOR TESTING PUTPOSES ONLY !!!
#     # seeds = [11,22,33,44,55] #[seeds[0]]                # FOR TESTING PUTPOSES ONLY !!!
#     # # sample_municipalities = ["Uster"]   # FOR TESTING PUTPOSES ONLY !!!
#     # # list_crossovers = ["spc"]           # FOR TESTING PUTPOSES ONLY !!!
#     # # list_initializations = ["spg"]           # FOR TESTING PUTPOSES ONLY !!!
#     # # list_repairs = ["brm"]           # FOR TESTING PUTPOSES ONLY !!!
#     # # nr_of_tests = 1           # FOR TESTING PUTPOSES ONLY !!!
#     # # #
#     # # # # list_repairs = ["rrm", "brm"]
#     # # # # list_repairs = ["brm"]
#     # # # # mutpb = 0
#     """
#         -----
#     """
#
#     # for seed in _:
#
#     for sample in sample_municipalities:
#         areal_raster_path, sq_raster_path, areal, sq_raster_normalized, int_quantity, ref_point_convergence \
#             = register_sample(sample, toolbox)
#
#         for initialization in list_initializations:
#             register_initialization(initialization, toolbox, areal_raster_path, sq_raster_path, int_quantity, n_pop)
#
#             for mutation in list_mutations:
#                 register_mutation(mutation, toolbox, int_quantity, areal)
#
#                 for crossover in list_crossovers:
#                     toolbox.register("mate", eval(crossover))  # ac | spc | ppc | ppc_fuo
#
#                     for repair in list_repairs:
#                         register_repair(repair, toolbox, int_quantity, areal)
#
#                         '''
#                             ---------------- Actual singular test ---------------
#                         '''
#                         test_nr, start_time, population, hof = setup_individual_test_run(seed, test_nr, starting_time,
#                                                                                          nr_of_tests, toolbox, NFFE,
#                                                                                          n_pop, thread_nr)
#
#                         # (hvs, fits_hof_all) = nsgaii_optimization(
#                         #     population, NGEN, n_pop, toolbox, cxpb, mutpb, hof, ref_point_convergence)
#                         (hvs, fits_hof_all) = nsgaii_optimization_ffe(
#                             population, NFFE, n_pop, toolbox, cxpb, mutpb, hof, ref_point_convergence)
#
#                         elapsed_time = time.time() - start_time
#
#                         print(hvs, fits_hof_all)
#                         save_results(hvs, elapsed_time, fits_hof_all, test_stamp, NFFE, n_pop,
#                                      algorithm + ";" + initialization + ";" + mutation + ";" + crossover + ";" + repair,
#                                      seed, sample)
#
#                         # # print(hvs, elapsed_time, fits_hof_all)
#                         # #
#                         # # # print(hyper_volume, elapsed_time, final_fits)
#                         # # # plot_pf(final_fits)
#                         # # save_results(hvs, elapsed_time, fits_hof_all, test_stamp, NFFE, n_pop, initialization + ";" + mutation + ";" + crossover , seed, sample)
#                         # #
#                         # # # hv, t, pf = load_results(test_stamp, NFFE, n_pop, initialization + ";" + mutation + ";" + crossover, seed, sample)
#                         # # # print(hv, t, pf)
#                         # # # plot_pf(pf)
#
#
# # run