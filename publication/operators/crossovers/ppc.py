import random
import numpy as np
import scipy
from scipy import ndimage

from publication.operators.inicialization.population_guess import get_2_random_deap_uster_individuals
from publication.common.sq_vis import plot_lulc_map, plot_sq


def ppc(ind1, ind2):
    # 1) Generate XOR mask for individuals
    xor_mask = np.zeros_like(ind1, dtype=int)
    xor_mask[ind1 != ind2] = 1

    # 2) Enumerate peels from the mask
    struct = scipy.ndimage.generate_binary_structure(2, 1)
    labeled_xor_mask, numpeels = ndimage.label(xor_mask, struct)

    # plot_sq(labeled_xor_mask, 'labeled_xor_mask')
    # print(range(numpeels))

    # 3) Generate crossover mask by selecting X% of random peels
    selected_peels = random.sample(range(1, numpeels + 1), numpeels // 2)   # 50%
    selected_peels_mask = np.isin(labeled_xor_mask, selected_peels)

    # plot_lulc_map(selected_peels_mask, 'selected_peels_mask')

    # 4) Do crossover
    ind1[selected_peels_mask], ind2[selected_peels_mask] = ind2[selected_peels_mask], ind1[selected_peels_mask]

    return ind1, ind2


def test_ppc():
    # random.seed(12345)
    ind1, ind2 = get_2_random_deap_uster_individuals()
    plot_lulc_map(ind1, 'ind1')
    plot_lulc_map(ind2, 'ind2')
    ind1, ind2 = ppc(ind1, ind2)
    plot_lulc_map(ind1, 'ppc_ind1')
    plot_lulc_map(ind2, 'ppc_ind2')


# TEST
# test_ppc()
