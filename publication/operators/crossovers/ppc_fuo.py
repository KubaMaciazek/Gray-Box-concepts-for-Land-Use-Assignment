import random
import numpy as np
import scipy
from scipy import ndimage

from publication.operators.inicialization.population_guess import get_2_random_deap_uster_individuals
from publication.common.sq_vis import plot_lulc_map, plot_sq


# Full Urban Only
def ppc_fuo(ind1, ind2):
    # 1) Generate XOR mask for individuals
    xor_mask = np.zeros_like(ind1, dtype=int)
    xor_mask[ind1 != ind2] = 1
    # plot_lulc_map(xor_mask, 'xor_mask')

    # 1.1) Reflect inconsistancies in differences continuous fields
    scraps = np.zeros_like(ind1, dtype=int)
    scraps[xor_mask == 1] = ind1[xor_mask == 1]
    # plot_lulc_map(scraps, 'scraps')

    xor_mask_u = np.zeros_like(ind1, dtype=int)
    xor_mask_u[scraps == 1] = 1
    # plot_lulc_map(xor_mask_u, 'xor_mask_u')
    xor_mask_r = np.zeros_like(ind1, dtype=int)
    xor_mask_r[scraps == 2] = 1
    # plot_lulc_map(xor_mask_r, 'xor_mask_r')


    # 2) Enumerate peels from the mask
    struct = scipy.ndimage.generate_binary_structure(2, 1)
    labeled_xor_mask_u, numpeels_u = ndimage.label(xor_mask_u, struct)
    labeled_xor_mask_r, numpeels_r = ndimage.label(xor_mask_r, struct)
    # plot_sq(labeled_xor_mask_u, 'labeled_xor_mask_u')
    # plot_sq(labeled_xor_mask_r, 'labeled_xor_mask_r')
    # print(range(numpeels_u))
    # print(range(numpeels_r))

    # # x) Test to see differences
    # plot_lulc_map(xor_mask, 'xor_mask')
    # scraps = np.zeros_like(ind1, dtype=int)
    # scraps[xor_mask == 1] = ind1[xor_mask == 1]
    # # print(np.unique(scraps))
    # # print(scraps)
    # plot_lulc_map(scraps, 'scraps')
    # plot_lulc_map(ind1, 'ind1')


    # 3) Generate crossover mask by selecting X% of random peels
    selected_peels_u = random.sample(range(1, numpeels_u + 1), numpeels_u // 2)   # 50%
    # print(selected_peels_u)
    selected_peels_mask_u = np.isin(labeled_xor_mask_u, selected_peels_u)
    # plot_lulc_map(selected_peels_mask_u, 'selected_peels_mask_u')

    selected_peels_r = random.sample(range(1, numpeels_r + 1), numpeels_r // 2)  # 50%
    # print(selected_peels_r)
    selected_peels_mask_r = np.isin(labeled_xor_mask_r, selected_peels_r)
    # plot_lulc_map(selected_peels_mask_r, 'selected_peels_mask_r')

    # 4) Do crossover
    ind1[selected_peels_mask_u], ind2[selected_peels_mask_u] = ind2[selected_peels_mask_u], ind1[selected_peels_mask_u]
    ind1[selected_peels_mask_r], ind2[selected_peels_mask_r] = ind2[selected_peels_mask_r], ind1[selected_peels_mask_r]

    return ind1, ind2


def test_ppc_fuo():
    # random.seed(12345)  # For consistent testing purposes
    ind1, ind2 = get_2_random_deap_uster_individuals()
    plot_lulc_map(ind1, 'ind1')
    plot_lulc_map(ind2, 'ind2')
    ind1, ind2 = ppc_fuo(ind1, ind2)
    plot_lulc_map(ind1, 'ppc_ind1')
    plot_lulc_map(ind2, 'ppc_ind2')


# TEST
# test_ppc_fuo()
