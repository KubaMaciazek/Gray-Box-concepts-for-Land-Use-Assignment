import random
import numpy as np
import scipy
from scipy import ndimage

from publication.operators.inicialization.population_guess import get_2_random_deap_uster_individuals
from publication.common.sq_vis import plot_lulc_map, plot_sq


def spc(ind1, ind2):
    '''
    Function to produce crossovers of two individuals.
    Crossover by exchange of given percentage of patches? (1 up to half?)
    :param ind1:
    :param ind2:
    :return: Crossed individuals  ind1 & ind2
    '''

    # Stwórz ponumerowaną mapę patchy urban
    urban_area = np.zeros_like(ind1, dtype=int)
    urban_area[ind1 == 1] = 1
    # plot_lulc_map(urban_area, 'urban_area')

    # labeled_urban_area, numpatches = f_ccl(urban_area, [2, 1])
    struct = scipy.ndimage.generate_binary_structure(2, 1)
    labeled_urban_area, numpatches = ndimage.label(urban_area, struct)
    # plot_sq(labeled_urban_area, 'labeled_urban_area')
    # print(range(numpatches))

    # Wylosować 50% patchy które zamieniamy
    selected_patches = random.sample(range(1, numpatches+1), numpatches//2) #//3 -> 33% | //4 -> 25%       | better results for 33%?
    # selected_patches_mask = np.zeros_like(labeled_urban_area)
    # selected_patches_mask[selected_patches_mask in selected_patches] = 1
    selected_patches_mask = np.isin(labeled_urban_area, selected_patches)
    # plot_lulc_map(selected_patches_mask, 'selected_patches_mask')

    # Exchange values based on mask
    ind1[selected_patches_mask], ind2[selected_patches_mask] = ind2[selected_patches_mask], ind1[selected_patches_mask]

    return ind1, ind2


def test_spc():
    # random.seed(12345)
    ind1, ind2 = get_2_random_deap_uster_individuals()
    plot_lulc_map(ind1, 'ind1')
    plot_lulc_map(ind2, 'ind2')
    ind1, ind2 = spc(ind1, ind2)
    plot_lulc_map(ind1, 'spc_ind1')
    plot_lulc_map(ind2, 'spc_ind2')


# TEST

# test_spc()
