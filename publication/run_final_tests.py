import concurrent.futures

from publication.general_test.tests_configs import get_final_tests_config
from publication.general_tests_seed_threaded import run_single_test
from publication.general_tests_threaded_moead import single_general_moead_run


def run_final_tests():
    (bestCombinationsAndBaseline,
     NFFE,
     w1, w2,
     seeds,
     remamining_sample_municipalities,
     nr_of_tests, test_nr, starting_time, test_stamp) = get_final_tests_config()

    test_stamp = '1737136140_fianl_tests'

    print('Test stamp: ' + test_stamp)

    # # TEST
    # NFFE = NFFE // 100    # Test
    # seeds = [seeds[0], seeds[1]]    # Test


    # Prepare arguments for parallel execution
    args = []
    for seed in seeds:
        for sample in remamining_sample_municipalities:
            for combination in bestCombinationsAndBaseline:
                if combination[0] == "nsgaii":
                    args.append((
                        combination[0],
                        combination[5], NFFE, combination[6], combination[7],
                        w1, w2,
                        seed,
                        sample,
                        combination[1], combination[2], combination[3], combination[4],
                        nr_of_tests, test_nr, starting_time, test_stamp
                    ))
                    test_nr += 1
                else:
                    t_neighbours = combination[5] // 10
                    args.append((
                        combination[0],
                        combination[5], NFFE, combination[6], combination[7],
                        w1, w2,
                        seed,
                        sample,
                        combination[1], combination[2], combination[3], combination[4],
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


if __name__ == '__main__':
    run_final_tests()
