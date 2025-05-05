# MOEAD
import concurrent.futures
import os

import numpy as np
from deap import creator, base, tools

from publication.general_test.tests_configs import get_general_tests_config
from publication.general_tests_seed_threaded import run_single_test
from publication.general_tests_threaded_moead import single_general_moead_run

tunned_source = 'tunning/tunned_parameters_dictionary_moead.txt'
# tunned_source = 'tunning/tunned_parameters_dictionary_moead_0505.txt'


def run_tests_for_tunned_best_moead():
    """
    Run all general tests in parallel using ThreadPoolExecutor.
    """
    _ = "moead"
    (_, NFFE, _, _, w1, w2, seeds, sample_municipalities, _, _,
     _, _, _, test_nr, starting_time, _) = get_general_tests_config()

    test_stamp = "1731336743_moead_tuned"
    # test_stamp = "1731336743_moead_tuned_0505"
    print('Test stamp: ' + test_stamp)
    nr_of_tests = 960

    """
        Setup confirmation
    """
    print("NFFE: ", str(NFFE))
    print("w1: ", str(w1))
    print("w2: ", str(w2))
    print("seeds: ", str(seeds))
    print("len(seeds): ", str(len(seeds)))
    print("sample_municipalities: ", str(sample_municipalities))
    """
        -----
    """

    # Prepare arguments for parallel execution
    args = []
    for seed in seeds:
        for sample in sample_municipalities:

            with open(tunned_source, 'r') as file:
                combinations = [line.strip() for line in file.readlines()]
                for combination in combinations:
                    params = combination.split(';')
                    algorithm = params[0]
                    initialization = params[1]
                    mutation = params[2]
                    crossover = params[3]
                    repair = params[4]
                    n_pop = int(params[5])
                    cxpb = float(params[6])
                    mutpb = float(params[7])

                    t_neighbours = n_pop // 10

                    args.append((
                        algorithm,
                        n_pop, NFFE, cxpb, mutpb,
                        w1, w2,
                        seed,
                        sample,
                        initialization, mutation, crossover, repair,
                        nr_of_tests, test_nr, starting_time, test_stamp,
                        t_neighbours
                    ))
                    test_nr += 1

    # Remove finished tests

    file_path = 'tests_results/'
    args_filtered = []
    for arg in args:
        (
            algorithm,
            n_pop, NFFE, cxpb, mutpb,
            w1, w2,
            seed,
            sample,
            initialization, mutation, crossover, repair,
            nr_of_tests, test_nr, starting_time, test_stamp,
            t_neighbours
        ) = arg
        comination = f"{algorithm};{initialization};{mutation};{crossover};{repair}"
        final_dir = file_path + str(NFFE) + '_' + str("n_pop") + '/' + test_stamp + '/' + sample + '/' + comination
        final_path = os.path.join(final_dir, str(seed) + '.txt')
        if not os.path.exists(final_path):
            args_filtered.append(arg)
        else:
            print(final_path)
    print('nr_of_tests:' + str(len(args_filtered)))

    # Run tests in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(single_general_moead_run, *arg) for arg in args_filtered]
        for future in concurrent.futures.as_completed(futures):
            try:
                seed, hvs, fits_hof_all, elapsed_time = future.result()
                # print(f"Seed: {seed}, HVS: {hvs}, Elapsed Time: {elapsed_time}")
            except Exception as exc:
                print(f"Generated an exception: {exc}")


# Execute the parallel test run
if __name__ == '__main__':
    run_tests_for_tunned_best_moead()
