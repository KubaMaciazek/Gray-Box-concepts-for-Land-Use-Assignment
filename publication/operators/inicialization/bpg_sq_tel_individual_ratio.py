import copy
import random

import numpy as np
from deap import creator, base

from publication.data.get_areal_raster import get_areal_raster
from publication.data.get_sq_raster import get_normalized_sq_raster
from publication.data.local_edge_length import get_agri_lel_probabilities_6a_strict
from publication.common.sq_vis import plot_lulc_map


def sq_bpg_50x50_tel_bgp_strict_ir(pcls, ind_init, areal_file, sq_file, urbanization_quantity, n_pop):
    """
    Dla każdego osobnika połowe pól wybierz SQ_BPG, a połowę TEL_BPG_strict
    """
    # """
    # Wybierz pół populacji SQ_BPG, i pół TEL_BPG_strict
    # """

    # 1) Load normalized region soil quality (values 0-1)
    sq_raster = get_normalized_sq_raster(sq_file)

    # 2) Load initial land use land cover matrix
    original_areal = get_areal_raster(areal_file)

    # 3) Load local edge length
    original_lel_influence = get_agri_lel_probabilities_6a_strict(original_areal)  # 0.25 influence by neighbour

    # 4) Create list for new population, and placeholder for created individual,
    #    and tuple of lists of cords of agricultural cells, converted from np.arrays
    new_areal = np.zeros(original_areal.shape)
    pop = [new_areal] * n_pop
    indices = np.where(np.array(original_areal == 2))
    indices_xs = indices[0].tolist()
    indices_ys = indices[1].tolist()

    # 5) Create n_pop individuals, with urbanization_quantity new selected cells for urbanization
    for k in range(n_pop):
        new_areal = np.copy(original_areal)
        i = 0
        # available_indices = np.copy(indices)
        available_xs = copy.deepcopy(indices_xs)
        available_ys = copy.deepcopy(indices_ys)
        lel_influence = np.copy(original_lel_influence)

        # 6.1) Select half of new cells, biased by their soil quality
        half_1st = urbanization_quantity // 2
        while i < half_1st:
            selected_position = random.randint(0, len(available_xs) - 1)
            selected_position_sq = sq_raster[
                available_xs[selected_position]
            ][
                available_ys[selected_position]
            ]
            selection_probability = random.random()
            if selected_position_sq <= selection_probability:
                x = available_xs.pop(selected_position)
                y = available_ys.pop(selected_position)
                new_areal[x][y] = 1
                i = i + 1

                # Update lel_influence - just add 0.25 (or 0.2 if 6c) to all neighbours.
                # Only agri are selected anyway, so rubbish in non-agri does not matter.
                neighbor_indices = [(x + i, y + j) for i in [-1, 1] for j in [-1, 1]]
                for r, c in neighbor_indices:
                    # To avoid checking for index out of bounds, I can just add a 0 border,
                    # and modify access to acomodate that change (add +1 do both indexes)
                    if 0 <= r < lel_influence.shape[0] and 0 <= c < lel_influence.shape[1]:
                        lel_influence[r, c] += 0.25

        # 6.2) Select 2nd half of new cells, biased by their lel
        while i < urbanization_quantity:
            selected_position = random.randint(0, len(available_xs) - 1)
            selected_position_influence = lel_influence[
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
                neighbor_indices = [(x + i, y + j) for i in [-1, 1] for j in [-1, 1]]
                for r, c in neighbor_indices:
                    # To avoid checking for index out of bounds, I can just add a 0 border,
                    # and modify access to acomodate that change (add +1 do both indexes)
                    if 0 <= r < lel_influence.shape[0] and 0 <= c < lel_influence.shape[1]:
                        lel_influence[r, c] += 0.25

        pop[k] = new_areal

    # 7) Return population of DEAP individuals
    return pcls(ind_init(c) for c in pop)


def test_sq_bpg_50x50_tel_bgp_strict_ir():
    sq_file = ("data/data_gemeinden_zuerich/Uster/sq.tif")
    areal_file = ("data/data_gemeinden_zuerich/Uster/areal_4_09.tif")
    urbanization_quantity = 212
    n_pop = 1

    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    population = sq_bpg_50x50_tel_bgp_strict_ir(list, creator.Individual, areal_file, sq_file, urbanization_quantity, n_pop)
    # print(population)
    plot_lulc_map(population[0], 'individual')  # log

# Test
# test_sq_bpg_50x50_tel_bgp_strict_ir()
