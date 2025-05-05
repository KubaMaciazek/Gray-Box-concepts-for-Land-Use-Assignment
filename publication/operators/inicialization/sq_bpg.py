"""
By Kuba, based on Schwaab spg from population_guess
"""
import copy
import random

import numpy as np
from deap import creator, base
from osgeo import gdal

from publication.common.sq_vis import plot_sq, plot_lulc_map


def sq_bpg(pcls, ind_init, areal_file, sq_file, urbanization_quantity, n_pop):
    '''
    Function to create biased population.
    Bias: wylosuj pole, a potem dodaj je z prawdopodobieństwem równym odwrotności/dopełnienia żyznosci gleby.
    :param pcls: list to create DEAP population
    :param ind_init: DEAP creator to create DEAP individual
    :param areal_file: file with lulc raster for given area
    :param sq_file: file with sq raster for given area
    :param urbanization_quantity: numer of cells to be selected for each ind to be urbanized
    :param n_pop: population size == number of individuals to be generated
    :return: population - list of DEAP individuals
    '''

    # 0) Load region soil quality and fill NAN values with 0, then ?normalize? values
    sq_raster = gdal.Open(sq_file)
    nodata = sq_raster.GetRasterBand(1).GetNoDataValue()
    sq_raster = np.array(sq_raster.GetRasterBand(1).ReadAsArray())
    sq_raster[sq_raster == nodata] = 0.0
    sq_raster[np.isnan(sq_raster)] = 0.0

    sq_raster = sq_raster / float(np.max(sq_raster))

    # plot_sq(sq_raster, 'sq_raster')     # log

    # 1) Load initial land use land cover matrix and fill NAN values with 0
    original_areal = gdal.Open(areal_file)
    nodata = original_areal.GetRasterBand(1).GetNoDataValue()
    original_areal = np.array(original_areal.GetRasterBand(1).ReadAsArray())
    original_areal[original_areal == nodata] = 0.0
    original_areal[np.isnan(original_areal)] = 0.0

    # plot_lulc_map(original_areal, 'original_areal')     # log

    # 2) Create list for new population, and placeholder for created individual,
    #    and tuple of lists of cords of agricultural cells, converted from np.arrays
    new_areal = np.zeros(original_areal.shape)
    pop = [new_areal] * n_pop
    indices = np.where(np.array(original_areal == 2))
    indices_xs = indices[0].tolist()
    indices_ys = indices[1].tolist()

    # 3) Create n_pop individuals, with urbanization_quantity new selected cells for urbanization
    for k in range(n_pop):
        new_areal = np.copy(original_areal)
        i = 0
        # available_indices = np.copy(indices)
        available_xs = copy.deepcopy(indices_xs)
        available_ys = copy.deepcopy(indices_ys)

        # 4) Select new cells, biased by their soil quality
        while i < urbanization_quantity:
            selected_position = random.randint(0, len(available_xs) - 1)
            selected_position_sq = sq_raster[
                available_xs[selected_position]
            ][
                available_ys[selected_position]
            ]
            selection_probability = random.random()
            # print(str(i) + "\t" + str(selected_position_sq) + "\t" + str(selection_probability))  # log
            if selected_position_sq <= selection_probability:
                new_areal[
                    available_xs.pop(selected_position)
                ][
                    available_ys.pop(selected_position)
                ] = 1
                i = i + 1

        pop[k] = new_areal

    # 4) Return population of DEAP individuals
    return pcls(ind_init(c) for c in pop)


def test_bpg():
    sq_file = ("data/data_gemeinden_zuerich/Uster/sq.tif")
    areal_file = ("data/data_gemeinden_zuerich/Uster/areal_4_09.tif")
    urbanization_quantity = 212
    n_pop = 1

    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    population = sq_bpg(list, creator.Individual, areal_file, sq_file, urbanization_quantity, n_pop)
    # print(population)
    plot_lulc_map(population[0], 'individual')     # log


# Test
# test_bpg()
