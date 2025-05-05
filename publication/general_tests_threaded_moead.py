import time

import numpy as np
from deap import creator, base

# from publication.algorithms.moead.custom_deap_moead_individual import CustomDeapMoeadIndividual
from publication.algorithms.moead.moead_optimization_ffe import moead_optimization_ffe
from publication.algorithms.moead.weighted_normalized_fitness import weighted_normalized_fitness
from publication.data.get_community_data import get_community_ideal_point
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

def single_general_moead_run(algorithm,
                             n_pop, NFFE, cxpb, mutpb,
                             w1, w2,
                             seed,
                             sample,
                             initialization, mutation, crossover, repair,
                             nr_of_tests, test_nr, starting_time, test_stamp,
                             t_neighbours):
    print("run_single_test - moead")

    creator.create("FitnessMax", base.Fitness, weights=(w1, w2))
    # creator.create("Individual", CustomDeapMoeadIndividual, fitness=creator.FitnessMax)
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

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

    test_nr, start_time, population, hof \
        = setup_individual_test_run(seed, test_nr, starting_time, nr_of_tests, toolbox, NFFE, n_pop, 0)

    ideal_point = get_community_ideal_point(sample)
    toolbox.register("evaluate_fv", weighted_normalized_fitness, ideal_point=ideal_point)

    # Perform NSGA-II optimization
    hvs, fits_hof_all = moead_optimization_ffe(population, NFFE, n_pop, toolbox, cxpb, mutpb, hof,
                                                ref_point_convergence, t_neighbours)

    elapsed_time = time.time() - start_time

    # Save results
    save_results(hvs, elapsed_time, fits_hof_all, test_stamp, NFFE, "n_pop",
                 f"{algorithm};{initialization};{mutation};{crossover};{repair};{n_pop};{int(cxpb*100)};{int(mutpb*100)}", seed, sample)
    # print(f"Time: {elapsed_time}; HV: {hvs}")

    return seed, hvs, fits_hof_all, elapsed_time
