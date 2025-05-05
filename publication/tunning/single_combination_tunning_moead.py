import os

import numpy as np

from publication.tunning.run_single_tunning_test_moead import run_single_tunning_test_moead


def single_combination_tunning_moead(algorithm,
                    n_pop_, NFFE, cxpb_, mutpb_,
                    w1, w2,
                    seeds,
                    sample,
                    initialization, mutation, crossover, repair,
                    nr_of_tests, test_nr, starting_time, test_stamp):

    n_pop = int(n_pop_)
    cxpb = float(cxpb_)
    mutpb = float(mutpb_)

    best_pop = n_pop
    best_cxpb = cxpb
    best_mutpb = mutpb
    best_avg_HV = 0

    # 1) Tune population
    # 1.1) Do initial tests
    hvs = []
    for seed in seeds:
        _, hv, _, _ = run_single_tunning_test_moead(algorithm,
                                n_pop, NFFE, cxpb, mutpb,
                                w1, w2,
                                seed,
                                sample,
                                initialization, mutation, crossover, repair,
                                nr_of_tests, test_nr, starting_time, test_stamp)
        hvs.append(hv[-1])

    # 1.2) Calculate initial HV
    best_avg_HV = np.average(hvs)

    # 1.3) Do tunning
    pop_step = 40
    modif = 1
    checked_pop = []
    checked_pop.append(n_pop)

    for i in range(10):
        # New population
        n_pop = n_pop + (pop_step * modif)

        if n_pop < 20:
            modif = modif * (-1)
            n_pop = n_pop + (pop_step * modif)
            pop_step = pop_step // 2
            n_pop = n_pop + (pop_step * modif)
        # while n_pop < 20:
        #     pop_step = pop_step // 2
        #     if pop_step <= 0:
        #         pop_step = 1
        #     n_pop = n_pop + pop_step

        if n_pop in checked_pop:
            pop_step = pop_step // 2
            n_pop = n_pop - (pop_step * modif)
        checked_pop.append(n_pop)

        # Do optimization
        hvs = []
        for seed in seeds:
            _, hv, _, _ = run_single_tunning_test_moead(algorithm,
                                                  n_pop, NFFE, cxpb, mutpb,
                                                  w1, w2,
                                                  seed,
                                                  sample,
                                                  initialization, mutation, crossover, repair,
                                                  nr_of_tests, test_nr, starting_time, test_stamp)
            hvs.append(hv[-1])

        # Calculate avg HV
        avg_HV = np.average(hvs)

        # Switch if better
        if avg_HV > best_avg_HV:
            best_avg_HV = avg_HV
            best_pop = n_pop
        else:
            modif = modif * (-1)
            n_pop = best_pop
            if modif > 0:
                pop_step = pop_step // 2

    #
    # 2) ToDo: Tune crossover

    # 2.1) Initial is last from n_pop tuning

    # 2.2) Do tunning
    cxpb_step = 0.05
    modif = 1
    checked_cxpb = []
    checked_cxpb.append(cxpb)

    for i in range(10):
        # New cxpb
        cxpb = cxpb + (cxpb_step * modif)
        cxpb = float(f"{cxpb:.5f}")
        if cxpb in checked_cxpb:
            cxpb_step = cxpb_step / 2
            cxpb = cxpb - (cxpb_step * modif)
        if cxpb > 1:
            cxpb_step = cxpb_step / 2
            cxpb = 1 - cxpb_step
            modif = modif * (-1)
        if cxpb < 0:
            cxpb_step = cxpb_step / 2
            cxpb = cxpb_step
            modif = modif * (-1)
        cxpb = float(f"{cxpb:.5f}")
        checked_cxpb.append(cxpb)

        # Do optimization
        hvs = []
        for seed in seeds:
            _, hv, _, _ = run_single_tunning_test_moead(algorithm,
                                                  n_pop, NFFE, cxpb, mutpb,
                                                  w1, w2,
                                                  seed,
                                                  sample,
                                                  initialization, mutation, crossover, repair,
                                                  nr_of_tests, test_nr, starting_time, test_stamp)
            hvs.append(hv[-1])

        # Calculate avg HV
        avg_HV = np.average(hvs)

        # Switch if better
        if avg_HV > best_avg_HV:
            best_avg_HV = avg_HV
            best_cxpb = cxpb
        else:
            modif = modif * (-1)
            cxpb = best_cxpb
            if modif > 0:
                cxpb_step = cxpb_step / 2

    #
    # 3) ToDo: Tune mutation

    # 3.1) Initial is last from cxpb tuning

    # 3.2) Do tunning
    mutpb_step = 0.05
    modif = 1
    checked_mutpb = []
    checked_mutpb.append(mutpb)

    for i in range(10):
        # New mutpb
        mutpb = mutpb + (mutpb_step * modif)
        mutpb = float(f"{mutpb:.5f}")
        if mutpb in checked_mutpb:
            mutpb_step = mutpb_step / 2
            mutpb = mutpb - (mutpb_step * modif)
        if mutpb > 1:
            mutpb_step = mutpb_step / 2
            mutpb = 1 - mutpb_step
            modif = modif * (-1)
        if mutpb < 0:
            mutpb_step = mutpb_step / 2
            mutpb = mutpb_step
            modif = modif * (-1)
        mutpb = float(f"{mutpb:.5f}")
        checked_mutpb.append(mutpb)

        # Do optimization
        hvs = []
        for seed in seeds:
            _, hv, _, _ = run_single_tunning_test_moead(algorithm,
                                                  n_pop, NFFE, cxpb, mutpb,
                                                  w1, w2,
                                                  seed,
                                                  sample,
                                                  initialization, mutation, crossover, repair,
                                                  nr_of_tests, test_nr, starting_time, test_stamp)
            hvs.append(hv[-1])

        # Calculate avg HV
        avg_HV = np.average(hvs)

        # Switch if better
        if avg_HV > best_avg_HV:
            best_avg_HV = avg_HV
            best_mutpb = mutpb
        else:
            modif = modif * (-1)
            mutpb = best_mutpb
            if modif > 0:
                mutpb_step = mutpb_step / 2

    #
    # 4) ToDo: Save best combination

    # 'tests_results/nsgaii_tunning/1727447903/Hedingen'
    # sample_dir = 'tests_results/' + str(algorithm) + '_' + str('tunning') + '/' + test_stamp + '/' + sample
    sample_dir = os.path.join('tests_results', str(algorithm) + '_' + str('tunning'), test_stamp, sample)
    combination = f"{algorithm};{initialization};{mutation};{crossover};{repair}"
    tunning_result_path = os.path.join(sample_dir, combination + '.txt')

    with open(tunning_result_path, 'w') as file:
        file.write(f"{best_pop}\n")
        file.write(f"{best_cxpb}\n")
        file.write(f"{best_mutpb}\n")
        file.write(f"{best_avg_HV}\n")
