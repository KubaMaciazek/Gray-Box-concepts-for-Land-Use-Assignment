import os
import time

import numpy as np
from deap import creator, base, tools

from publication.algorithms.moead.moead_optimization_ffe import moead_optimization_ffe
from publication.algorithms.nsgaii.nsgaii_optimization_ffe import nsgaii_optimization_ffe
from publication.algorithms.moead.weighted_normalized_fitness import weighted_normalized_fitness
from publication.data.get_community_data import get_community_ideal_point
from publication.general_test.register_initialization import register_initialization
from publication.general_test.register_mutation import register_mutation
from publication.general_test.register_repair import register_repair
from publication.general_test.register_sample import register_sample
from publication.general_test.setup_individual_test_run import setup_individual_test_run
from publication.statistics.load_results import load_results
from publication.statistics.save_results import save_results

from publication.operators.crossovers.ac import ac
from publication.operators.crossovers.ppc import ppc
from publication.operators.crossovers.spc import spc
from publication.operators.crossovers.ppc_fuo import ppc_fuo


def run_single_tunning_test_moead(algorithm,
                    n_pop, NFFE, cxpb, mutpb,
                    w1, w2,
                    seed,
                    sample,
                    initialization, mutation, crossover, repair,
                    nr_of_tests, test_nr, starting_time, test_stamp):


    # Check if completed:
    file_path = 'tests_results/'
    comination = f"{algorithm};{initialization};{mutation};{crossover};{repair};{n_pop};{cxpb};{mutpb}"
    final_dir = file_path + str(algorithm) + '_' + str('tunning') + '/' + test_stamp + '/' + sample + '/' + comination
    final_path = os.path.join(final_dir, str(seed) + '.txt')
    if os.path.exists(final_path):
        result = load_results(final_path)
        print(final_path)
        print(result)
        return seed, result['hvs'], result['pfs'], result['total_exec_time']


    t_neighbours = n_pop // 10

    creator.create("FitnessMax", base.Fitness, weights=(w1, w2))
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

    # Perform MOEAD optimization
    hvs, fits_hof_all = moead_optimization_ffe(population, NFFE, n_pop, toolbox, cxpb, mutpb, hof,
                                               ref_point_convergence, t_neighbours)

    elapsed_time = time.time() - start_time

    # Save results
    save_results(hvs, elapsed_time, fits_hof_all, test_stamp, algorithm, 'tunning',
                 f"{algorithm};{initialization};{mutation};{crossover};{repair};{n_pop};{cxpb};{mutpb}", seed, sample)

    return seed, hvs, fits_hof_all, elapsed_time
