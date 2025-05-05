import copy
import random

import numpy as np
from deap import creator, base

from publication.data.get_areal_raster import get_areal_raster
from publication.data.local_edge_length import get_agri_lel_probabilities_6a_strict, \
    get_agri_lel_probabilities_6c_wide
from publication.common.sq_vis import plot_lulc_map


def tel_bpg(pcls, ind_init, areal_file, urbanization_quantity, n_pop, get_agri_lel_probabilities, prob_factor):
    areal_raster = get_areal_raster(areal_file)
    # plot_lulc_map(areal_raster, 'areal_raster')  # log
    # agri_probies = get_agri_lel_probabilities_6a_strict(areal_raster)
    original_agri_probies = get_agri_lel_probabilities(areal_raster)

    # 2) Create list for new population, and placeholder for created individual,
    #    and tuple of lists of cords of agricultural cells, converted from np.arrays
    new_areal = np.zeros(areal_raster.shape)
    pop = [new_areal] * n_pop
    indices = np.where(np.array(areal_raster == 2))
    indices_xs = indices[0].tolist()
    indices_ys = indices[1].tolist()

    # 3) Create n_pop individuals, with urbanization_quantity new selected cells for urbanization
    for k in range(n_pop):
        new_areal = np.copy(areal_raster)
        i = 0
        available_xs = copy.deepcopy(indices_xs)
        available_ys = copy.deepcopy(indices_ys)
        agri_probies = np.copy(original_agri_probies)

        # 4) Select new agri cells, biased by the number of their urban neighbours
        while i < urbanization_quantity:
            selected_position = random.randint(0, len(available_xs) - 1)
            selected_position_influence = agri_probies[
                available_xs[selected_position]
            ][
                available_ys[selected_position]
            ]
            selection_probability = random.random()
            if selected_position_influence > selection_probability:
                x = available_xs.pop(selected_position)
                y = available_ys.pop(selected_position)
                new_areal[x][y] = 1
                i = i + 1

                # Update agri_probies - just add 0.25 (or 0.2 if 6c) to all neighbours.
                # Only agri are selected anyway, so rubbish in non-agri does not matter.
                neighbor_indices = [(x + i, y + j) for i in [-1,1] for j in [-1,1]]
                for r, c in neighbor_indices:
                    # To avoid checking for index out of bounds, I can just add a 0 border,
                    # and modify access to acomodate that change (add +1 do both indexes)
                    if 0 <= r < agri_probies.shape[0] and 0 <= c < agri_probies.shape[1]:
                        # agri_probies[r, c] += 0.25
                        agri_probies[r, c] += prob_factor

        pop[k] = new_areal

    # 4) Return population of DEAP individuals
    return pcls(ind_init(c) for c in pop)


def tel_bpg_progressive(pcls, ind_init, areal_file, urbanization_quantity, n_pop, get_agri_lel_probabilities, prob_factor, leniency_step):
    areal_raster = get_areal_raster(areal_file)
    # plot_lulc_map(areal_raster, 'areal_raster')  # log
    # agri_probies = get_agri_lel_probabilities_6a_strict(areal_raster)
    original_agri_probies = get_agri_lel_probabilities(areal_raster)

    # 2) Create list for new population, and placeholder for created individual,
    #    and tuple of lists of cords of agricultural cells, converted from np.arrays
    new_areal = np.zeros(areal_raster.shape)
    pop = [new_areal] * n_pop
    indices = np.where(np.array(areal_raster == 2))
    indices_xs = indices[0].tolist()
    indices_ys = indices[1].tolist()

    # 3) Create n_pop individuals, with urbanization_quantity new selected cells for urbanization
    for k in range(n_pop):
        new_areal = np.copy(areal_raster)
        i = 0
        available_xs = copy.deepcopy(indices_xs)
        available_ys = copy.deepcopy(indices_ys)
        agri_probies = np.copy(original_agri_probies)

        leniency = 0
        # 4) Select new agri cells, biased by the number of their urban neighbours
        while i < urbanization_quantity:
            selected_position = random.randint(0, len(available_xs) - 1)
            selected_position_influence = agri_probies[
                available_xs[selected_position]
            ][
                available_ys[selected_position]
            ]
            selection_probability = random.random()
            if selected_position_influence + leniency > selection_probability:
                x = available_xs.pop(selected_position)
                y = available_ys.pop(selected_position)
                new_areal[x][y] = 1
                i = i + 1

                # Update agri_probies - just add 0.25 (or 0.2 if 6c) to all neighbours.
                # Only agri are selected anyway, so rubbish in non-agri does not matter.
                neighbor_indices = [(x + i, y + j) for i in [-1,1] for j in [-1,1]]
                for r, c in neighbor_indices:
                    # To avoid checking for index out of bounds, I can just add a 0 border,
                    # and modify access to acomodate that change (add +1 do both indexes)
                    if 0 <= r < agri_probies.shape[0] and 0 <= c < agri_probies.shape[1]:
                        # agri_probies[r, c] += 0.25
                        agri_probies[r, c] += prob_factor
                leniency = 0
            else:
                leniency = leniency + leniency_step

        pop[k] = new_areal

    # 4) Return population of DEAP individuals
    return pcls(ind_init(c) for c in pop)


def tel_bpg_strict(pcls, ind_init, areal_file, urbanization_quantity, n_pop):
    # areal_raster = get_areal_raster(areal_file)
    # agri_probies = get_agri_lel_probabilities_6a_strict(areal_raster)
    return tel_bpg(pcls, ind_init, areal_file, urbanization_quantity, n_pop, get_agri_lel_probabilities_6a_strict, 0.25)


def tel_bgp_wide(pcls, ind_init, areal_file, urbanization_quantity, n_pop):
    # areal_raster = get_areal_raster(areal_file)
    # agri_probies = get_agri_lel_probabilities_6c_wide(areal_raster)
    return tel_bpg(pcls, ind_init, areal_file, urbanization_quantity, n_pop, get_agri_lel_probabilities_6c_wide, 0.2)


def tel_bpg_p10(pcls, ind_init, areal_file, urbanization_quantity, n_pop):
    return tel_bpg_progressive(pcls, ind_init, areal_file, urbanization_quantity, n_pop, get_agri_lel_probabilities_6a_strict, 0.25, 0.1)


def tel_bpg_p25(pcls, ind_init, areal_file, urbanization_quantity, n_pop):
    return tel_bpg_progressive(pcls, ind_init, areal_file, urbanization_quantity, n_pop, get_agri_lel_probabilities_6a_strict, 0.25, 0.25)


def test_tel_bpg():
    areal_file = ("data/data_gemeinden_zuerich/Uster/areal_4_09.tif")
    urbanization_quantity = 212
    n_pop = 100

    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    population = tel_bpg_strict(list, creator.Individual, areal_file, urbanization_quantity, n_pop)
    # population = tel_bgp_wide(list, creator.Individual, areal_file, urbanization_quantity, n_pop)
    # population = tel_bpg_p10(list, creator.Individual, areal_file, urbanization_quantity, n_pop)
    # population = tel_bpg_p25(list, creator.Individual, areal_file, urbanization_quantity, n_pop)
    # print(population)
    plot_lulc_map(population[0], 'first individual')  # log
    plot_lulc_map(population[99], 'last individual')  # log


# Test
# test_tel_bpg()
