#  Obtain Tunning for the best combination
#  .
#  For each sample
#   Create folder
#   For each operators combination > run in threads
#       1) Tune population
#           1.1) Do optimization for 5 seeds for initial parameters saving results
#           1.2) Calculate avg HV
#           1.3) For i in range(10)
#               Change population by step in comparison to best optimization so far
#                   Check if it was already checked, if so, divide step in half, and compute new population again
#               Do optimization
#               Calculate statistics
#               > If better result
#                   Set current population and avg_HV as best
#               > If worse result
#                   Reverse step change
#                   If it was negative, divide step change in half
import os
import concurrent.futures

from publication.general_test.tests_configs import get_moead_tunning_config
from publication.tunning.single_combination_tunning_moead import single_combination_tunning_moead


def run_tunning_moead():
    (algorithm, n_pop, NFFE, cxpb, mutpb, w1, w2, seeds, sample_municipalities, list_initializations, list_mutations,
     list_crossovers, list_repairs, nr_of_tests, test_nr, starting_time, test_stamp) = get_moead_tunning_config()

    # test_stamp = "1729266974_mt_0901" #original moead tunning
    print('Tunning & test stamp: ' + test_stamp)

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

    for sample in sample_municipalities:
        file_path = 'tests_results/'
        final_dir = file_path + str(algorithm) + '_' + str('tunning') + '/' + test_stamp + '/' + sample
        os.makedirs(final_dir, exist_ok=True)

        # Prepare arguments for parallel execution
        args = []
        for initialization in list_initializations:
            for mutation in list_mutations:
                for crossover in list_crossovers:
                    for repair in list_repairs:
                        args.append((
                            algorithm,
                            n_pop, NFFE, cxpb, mutpb,
                            w1, w2,
                            seeds,
                            sample,
                            initialization, mutation, crossover, repair,
                            nr_of_tests, test_nr, starting_time, test_stamp
                        ))
                        test_nr += 1

        # Exclude completed tunnings for repeats
        args_filtered = []

        for arg in args:
            (
                algorithm,
                n_pop, NFFE, cxpb, mutpb,
                w1, w2,
                seeds,
                sample,
                initialization, mutation, crossover, repair,
                nr_of_tests, test_nr, starting_time, test_stamp
            ) = arg
            comination = f"{algorithm};{initialization};{mutation};{crossover};{repair}"
            final_path = os.path.join(final_dir, comination + '.txt')
            if not os.path.exists(final_path):
                args_filtered.append(arg)
                print(final_path)
            else:
                # print(final_path)
                pass
        print('nr_of_tests:' + str(len(args_filtered)))


        # Run tests in parallel
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(single_combination_tunning_moead, *arg) for arg in args_filtered]
            for future in concurrent.futures.as_completed(futures):
                try:
                    _ = future.result()
                except Exception as exc:
                    print(f"Generated an exception: {exc}")


if __name__ == '__main__':
    run_tunning_moead()
