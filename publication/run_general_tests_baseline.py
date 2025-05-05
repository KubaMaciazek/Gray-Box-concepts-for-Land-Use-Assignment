import concurrent.futures

from publication.general_test.tests_configs import get_general_tests_config_for_baseline_tests
from publication.general_tests_seed_threaded import run_single_test
from publication.general_tests_threaded_moead import single_general_moead_run


def run_general_tests_for_baseline_threaded():
    # FOR NSGA-II and MOEAD at once

    (algorithms,
     n_pop, NFFE, cxpb, mutpb,
     w1, w2,
     seeds,
     sample_municipalities,
     list_initializations, list_mutations, list_crossovers, list_repairs,
     nr_of_tests, test_nr, starting_time, test_stamp) = get_general_tests_config_for_baseline_tests()
    t_neighbours = n_pop // 10
    print('Test stamp: ' + test_stamp)


    """
        Setup confirmation
    """
    print("algorithm: ", str(algorithms))
    print("t_neighbours", str(t_neighbours))
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

    # Prepare arguments for parallel execution
    args = []
    for algorithm in algorithms:
        for seed in seeds:
            for sample in sample_municipalities:
                for initialization in list_initializations:
                    for mutation in list_mutations:
                        for crossover in list_crossovers:
                            for repair in list_repairs:
                                if algorithm == "nsgaii":
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
                                else:
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

    # Run tests in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                run_single_test if arg[0] == "nsgaii" else single_general_moead_run, *arg
            )
            for arg in args
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                seed, hvs, fits_hof_all, elapsed_time = future.result()
                # print(f"Seed: {seed}, HVS: {hvs}, Elapsed Time: {elapsed_time}")
            except Exception as exc:
                print(f"Generated an exception: {exc}")


# Execute the parallel test run
if __name__ == '__main__':
    run_general_tests_for_baseline_threaded()
