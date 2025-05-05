import os

import numpy as np
from deap import creator, base

from publication.statistics.load_results import load_results


def calculate_combination_tpf(trrp, combination, pcls, ind_init):
    tpf = []

    # sample combination path
    scp = os.path.join(trrp, combination)
    # sample combination seeds results
    scsr = []

    for seedfile in os.listdir(scp):
        # print(seedfile)
        scsr.append(load_results(os.path.join(scp, seedfile)))

    # seedfiles results final pareto fronts combined (all points in one set)
    cfpf = []
    for result in scsr:
        fpf_points = result['pfs'][-1]
        for point in fpf_points:
            cfpf.append((float(point[0]), float(point[1])))

    # unique values/points = optimized cfpf
    ocfpf = list(set(cfpf))
    return ocfpf

    # # creation of deap format
    # combined_fpf = []
    # for index, fit in enumerate(ocfpf):
    #     deap_ind = ind_init(str(index) + str(combination))
    #     deap_ind.fitness.values = fit
    #     combined_fpf.append(deap_ind)
    #
    # deap_combined_pop = pcls(combined_fpf)
    #
    # return deap_combined_pop

##################################################################################################################

# def calculate_combination_tpf(trrp, combination, pcls, ind_init):
#     tpf = []
#
#     # sample combination path
#     scp = os.path.join(trrp, combination)
#     # print(scp)
#     # sample combination seeds results
#     scsr = []
#
#     for seedfile in os.listdir(scp):
#         # print(seedfile)
#         scsr.append(load_results(os.path.join(scp, seedfile)))
#
#     # final paret fronts
#     fpf = []
#     combined_fpf = []
#     for result in scsr:
#         fpf_points = result['pfs'][-1]
#         # print(fpf_points)
#
#         fpf_points_optimized = []
#         for point in fpf_points:
#             fpf_points_optimized.append((float(point[0]), float(point[1])))
#         uniq = set(fpf_points_optimized)
#         fpf_points_optimized = list(uniq)
#         # print(fpf_points_optimized)
#
#         deap_pop = []
#         for index, fit in enumerate(fpf_points_optimized):
#             # fit = (float(point[0]), float(point[1]))
#             # print(fit)
#             deap_ind = ind_init(str(index) + str(combination))
#             deap_ind.fitness.values = fit
#             deap_pop.append(deap_ind)
#             combined_fpf.append(deap_ind)
#         fpf.append(pcls(deap_pop))
#
#         # print(len(deap_pop))
#         # print(deap_pop[-1].fitness)
#         # fpf.append(result['pfs'][-1])
#
#     deap_combined_pop = pcls(combined_fpf)
#     # print([x.fitness for x in deap_combined_pop])
#     print(len([x.fitness for x in deap_combined_pop]))
#     print(list(set([x.fitness for x in deap_combined_pop])))
#     # print(len(deap_combined_pop))
#     return deap_combined_pop
