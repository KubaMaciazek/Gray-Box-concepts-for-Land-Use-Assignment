import concurrent.futures
import os

from publication.general_test.tests_configs import get_general_tests_config
from publication.general_tests_threaded_moead import single_general_moead_run


def run_complete_x_moead_nt_reversed_direction():
    """
        Run all general tests in parallel using ThreadPoolExecutor.
    """
    algorithm = "moead"
    (n_pop, NFFE, cxpb, mutpb, w1, w2, seeds, sample_municipalities, list_initializations, list_mutations,
     list_crossovers, list_repairs, nr_of_tests, test_nr, starting_time, test_stamp) = get_general_tests_config()
    t_neighbours = n_pop // 10

    test_stamp = 'moead_nt_reversed'
    print('Test stamp: ' + test_stamp)

    """
        Setup confirmation
    """
    print("algorithm: ", str(algorithm))
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
                                nr_of_tests, test_nr, starting_time, test_stamp,
                                t_neighbours
                            ))
                            test_nr += 1

    # Reverse and Remove finished tests -> THE TWEAK
    args.reverse()

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
        final_dir = file_path + str(NFFE) + '_' + str(n_pop) + '/' + test_stamp + '/' + sample + '/' + comination
        final_path = os.path.join(final_dir, str(seed) + '.txt')
        if not os.path.exists(final_path):
            args_filtered.append(arg)
        else:
            print(final_path)
    print('nr_of_tests:' + str(len(args_filtered)))

    # Run tests in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(single_general_moead_run, *arg) for arg in args_filtered] # for arg in args]
        for future in concurrent.futures.as_completed(futures):
            try:
                seed, hvs, fits_hof_all, elapsed_time = future.result()
                # print(f"Seed: {seed}, HVS: {hvs}, Elapsed Time: {elapsed_time}")
            except Exception as exc:
                print(f"Generated an exception: {exc}")


# Execute the parallel test run
if __name__ == '__main__':
    run_complete_x_moead_nt_reversed_direction()
