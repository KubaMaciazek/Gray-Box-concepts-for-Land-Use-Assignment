import os
from itertools import combinations

import numpy as np
from deap import creator, base, tools
from deap.tools._hypervolume import pyhv as hv

from publication.data.get_community_data import get_community_ref_point
from publication.summary.tpfs.calculate_combination_tpf import calculate_combination_tpf
from publication.summary.tpfs.save_tpf import save_tpf


def calculate_tpf_by_sample(analyzed_tests, sample, summary_path):
    """
    :param analyzed_tests: paths to results from test cases (nsgaii/moead, no_tuned/tuned_0901/tuned_0505)
    :param sample: sample for which to construct tpf
    """

    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    combined_testcase_ctpfs = []
    for test_path in analyzed_tests:
        test = test_path.split('\\')[-1]
        test_sample_path = os.path.join(test_path, sample)

        if not os.path.exists(test_sample_path):
            print('No such sample in test: ' + str(test_sample_path))
        else:
            combinations = [d for d in os.listdir(test_sample_path) if os.path.isdir(os.path.join(test_sample_path, d))]

            combined_tpfs = []
            for combination in combinations:
                # 1) Calculate TPF of a combination of a specific sample for specific test case
                print(sample + ';' + test + ';' + combination)
                combination_tpf = calculate_combination_tpf(test_sample_path, combination, list, creator.Individual)
                # 2) Add combination TPF to general set of points
                combined_tpfs.extend(combination_tpf)

            # 3) Optimize set by making it unique
            optimized_combined_tpfs = list(set(combined_tpfs))

            # 4) Add test case sample TPF to general set of points
            combined_testcase_ctpfs.extend(optimized_combined_tpfs)

    # 5) Optimize set by making it unique
    optimized_combined_testcase_ctpfs = list(set(combined_testcase_ctpfs))

    # 6) Transform to DEAP format
    combined_fpf = []
    for index, fit in enumerate(optimized_combined_testcase_ctpfs):
        deap_ind = creator.Individual(str(index))
        deap_ind.fitness.values = fit
        combined_fpf.append(deap_ind)
    deap_combined_pop = list(combined_fpf)

    # 7) Perform comparison and get True Pareto Front
    hof = tools.ParetoFront(similar=np.array_equal)
    print(len(deap_combined_pop))
    hof.update(deap_combined_pop)

    # 8) Save data
    fits_0 = [x.fitness.values for x in hof]

    uniq = set(fits_0)
    front = list(uniq)
    tpf_hv = cal_hv(front, sample)

    tpf = {}
    tpf['hv'] = tpf_hv
    tpf['pf'] = front

    # print(tpf)
    # print(len(front))

    save_tpf(sample, tpf, summary_path)


def calculate_tpf_by_sample__(trrp, sample, combinations):
    """
    :param trrp: test result sample root path
    :param sample: sample name
    :param combinations: list of operators combinations
    """

    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    hof_0 = tools.ParetoFront(similar=np.array_equal)
    hof_1 = tools.ParetoFront(similar=np.array_equal)
    hof_2 = tools.ParetoFront(similar=np.array_equal)

    # 1) calculate tpfs for all combinations
    ctps = []
    combined = []

    for combination in combinations:
        print(sample + ';' + combination)
        hof = tools.ParetoFront(similar=np.array_equal)
        comb_tpf = calculate_combination_tpf(trrp, combination, list, creator.Individual)
        hof.update(comb_tpf)
        combined.extend(hof.items)

        hof_0.update(comb_tpf)
        ctps.extend(comb_tpf)

    hof_1.update(ctps)
    hof_2.update(combined)

    # print(len(hof_0))
    # print(len(hof_1))
    # print(len(hof_2))

    # print(hof_0.items)
    # print(hof_1)
    # print(hof_2)

    # fits_0 = [tuple(float(x.fitness[0]), float(x.fitness[1])) for x in hof_0]
    fits_0 = [x.fitness.values for x in hof_0]
    tpf_hv = cal_hv(fits_0, sample)
    # print(cal_hv(fits_0))
    # fits_1 = [x.fitness.values for x in hof_1]
    # print(cal_hv(fits_1))
    # fits_2 = [x.fitness.values for x in hof_2]
    # print(cal_hv(fits_2))

    # save front

    uniq = set(fits_0)
    front = list(uniq)
    tpf_hv = cal_hv(front, sample)

    tpf = {}
    tpf['hv'] = tpf_hv
    tpf['pf'] = front

    # print(tpf)

    save_tpf(sample, tpf)

    # return fits_0

# ----------------------------------------- Utils -----------------------------------------


def cal_hv(convergence_hof, sample):
    convergence_hof = set(convergence_hof)
    convergence_hof_array = np.array(list(convergence_hof))
    # convergence_hof_array[:,0] = convergence_hof_array[:,0]*-1
    return hv.hypervolume(pointset=convergence_hof_array, ref=get_community_ref_point(sample))  # old version
