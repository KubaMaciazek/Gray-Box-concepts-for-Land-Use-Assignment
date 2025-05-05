import concurrent.futures

import numpy as np
from deap import creator, base, tools

from publication.general_test.tests_configs import get_general_tests_config
from publication.general_tests_seed_threaded import run_single_test


def run_general_tests_parallel():
    """
    Run all general tests in parallel using ThreadPoolExecutor.
    """
    algorithm = "nsgaii"
    (n_pop, NFFE, cxpb, mutpb, w1, w2, seeds, sample_municipalities, list_initializations, list_mutations,
     list_crossovers, list_repairs, nr_of_tests, test_nr, starting_time, test_stamp) = get_general_tests_config()
    print('Test stamp: ' + test_stamp)

    """
        Siekanie kodu
    """
    # seeds = [seeds[19]] Done: 19-1724933155,

    """
        Setup confirmation
    """
    print("algorithm: ", str(algorithm))
    print("n_pop: ", str(n_pop))
    print("NFFE: ", str(NFFE))
    print("cxpb: ", str(cxpb))
    print("mutpb: ", str(mutpb))
    print("w1: ", str(w1))
    print("w2: ", str(w2))
    print("seeds: ", str(seeds))
    print("len(seeds): ", str(len(seeds)))
    print("sample_municipalities: ", str(sample_municipalities))
    print("list_initializations: ", str(list_initializations))
    print("list_mutations: ", str(list_mutations))
    print("list_crossovers: ", str(list_crossovers))
    print("list_repairs: ", str(list_repairs))
    """
        -----
    """

    # creator.create("FitnessMax", base.Fitness, weights=(w1, w2))
    # creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)
    #
    # toolbox = base.Toolbox()
    # toolbox.register("select", tools.selNSGA2)

    # Prepare arguments for parallel execution
    args = []
    for seed in seeds:
        for sample in sample_municipalities:
            for initialization in list_initializations:
                for mutation in list_mutations:
                    for crossover in list_crossovers:
                        for repair in list_repairs:
                            args.append((
                                algorithm,
                                n_pop, NFFE, cxpb, mutpb,
                                w1, w2,
                                seed,
                                sample,
                                initialization, mutation, crossover, repair,
                                nr_of_tests, test_nr, starting_time, test_stamp
                            ))
                            test_nr += 1

    # Run tests in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_single_test, *arg) for arg in args]
        for future in concurrent.futures.as_completed(futures):
            try:
                seed, hvs, fits_hof_all, elapsed_time = future.result()
                # print(f"Seed: {seed}, HVS: {hvs}, Elapsed Time: {elapsed_time}")
            except Exception as exc:
                print(f"Generated an exception: {exc}")


# Execute the parallel test run
if __name__ == '__main__':
    run_general_tests_parallel()


"""
        ------------------------------------- Old version -----------------------------------------------
"""

# import threading
#
# import numpy
# import numpy as np
# from deap import creator, base
#
# from publication.general_test.tests_configs import get_general_tests_config
# from publication.general_tests_seed_threaded import general_tests_seed_threaded
#
#
# def run_general_tests_seed_threaded():
#     algorithm = "nsgaii"
#     (n_pop, NFFE, cxpb, mutpb,
#      w1, w2,
#      seeds,
#      sample_municipalities,
#      list_initializations, list_mutations, list_crossovers, list_repairs,
#      nr_of_tests, test_nr, starting_time, test_stamp) = get_general_tests_config()
#     print('Test stamp: ' + test_stamp)
#
#     creator.create("FitnessMax", base.Fitness, weights=(w1, w2))
#     creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)
#
#     """
#         Setup confirmation
#     """
#     print("algorithm: ", str(algorithm))
#     print("n_pop: ", str(n_pop))
#     print("NFFE: ", str(NFFE))
#     print("cxpb: ", str(cxpb))
#     print("mutpb: ", str(mutpb))
#     print("w1: ", str(w1))
#     print("w2: ", str(w2))
#     print("seeds: ", str(seeds))
#     print("len(seeds): ", str(len(seeds)))
#     print("sample_municipalities: ", str(sample_municipalities))
#     print("list_initializations: ", str(list_initializations))
#     print("list_mutations: ", str(list_mutations))
#     print("list_crossovers: ", str(list_crossovers))
#     print("list_repairs: ", str(list_repairs))
#     """
#         -----
#     """
#
#     seed_threads = []
#     for thread_nr in range(len(seeds)):
#         seed_thread = threading.Thread(
#             target=general_tests_seed_threaded,
#             args=(algorithm,
#                   n_pop, NFFE, cxpb, mutpb,
#                   w1, w2,
#                   seeds[thread_nr],
#                   numpy.copy(sample_municipalities),
#                   numpy.copy(list_initializations), numpy.copy(list_mutations),
#                   numpy.copy(list_crossovers), numpy.copy(list_repairs),
#                   nr_of_tests/len(seeds), 0, starting_time, test_stamp,
#                   thread_nr,)
#         )
#         seed_threads.append(seed_thread)
#
#     for seed_thread in seed_threads:
#         seed_thread.start()
#
#     for seed_thread in seed_threads:
#         seed_thread.join()
#
#     print("COMPLETED: run_general_tests_seed_threaded()")
#
#
# # run
#
# run_general_tests_seed_threaded()
