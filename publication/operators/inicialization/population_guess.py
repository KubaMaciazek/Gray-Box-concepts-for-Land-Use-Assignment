"""
By Schwaab - from nsgaii_python_27.py

Funkcja init_population, przemianowana na spg, jako Schwaab Population Guess
"""
import random
import numpy as np
from deap import creator, base
from osgeo import gdal


def spg(pcls, ind_init, filename_areal, int_quantity, n_pop):
    """
    [KUBA]: stwórz początkową losową populację
    -> n_pop macierzy, z int_quantity wybranymi polami agriculture pod urbanizacje (wybrane pola 1, reszta 0)
    UWAGA: Jest możliwe uzyskanie 2 takich samych człnków populajcji.

    :param pcls: ?
    :param ind_init: ?
    :param filename_areal: path to file that contains information about land-use/land-cover for given test case
    :param int_quantity: number of new urban areas to be allocated | cells to be converted from agricultural to urban
    :param n_pop: ?
    :return:
    """

    areal_local = gdal.Open(filename_areal)
    nodata = areal_local.GetRasterBand(1).GetNoDataValue()
    areal_local = np.array(areal_local.GetRasterBand(1).ReadAsArray())
    areal_local[areal_local == nodata] = 0.0
    areal_local[np.isnan(areal_local)] = 0.0

    areal_new = np.zeros(areal_local.shape)

    # [KUBA]: a tuple, with 2 one-dimensional arrays. One for row indices, second for colun indices
    indices = np.where(np.array(areal_local == 2))

    pop = [areal_new] * n_pop
    for k in range(n_pop):
        areal_new = np.copy(areal_local)
        # [KUBA]: Wylosuj które pola agri wybieramy
        # -> Wylosuj int_quantity pozycji na podstawie długości listy koordynatów rzędów
        r_s = random.sample(range(len(indices[0])), int_quantity)

        # [KUBA]: Weź x'sy i y'ki wylosowanychpozucji, i zamień je na 1'dynki
        areal_new[indices[0][r_s],indices[1][r_s]] = 1
        pop[k] = areal_new

    # [KUBA]: the difference between the return value and pop is simply that an ind_init
    #   (i.e. a creator.Individual) is made from c. This means it is not just an array,
    #   but an individual with fitness as additional information (and FitnessMax function
    return pcls(ind_init(c) for c in pop)


"""
By Kuba
"""

AREAL_FILE = ("data/data_gemeinden_zuerich/Uster/areal_4_09.tif")
URBANIZATION_QUANTITY = 212


def get_deap_population(areal_file, urbanization_quantity, n_pop):
    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    return spg(list, creator.Individual, areal_file, urbanization_quantity, n_pop)


def get_n_random_deap_uster_individuals(n_pop):
    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    return spg(list, creator.Individual, AREAL_FILE, URBANIZATION_QUANTITY, n_pop)


def get_2_random_deap_uster_individuals():
    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    [ind1, ind2] = spg(list, creator.Individual, AREAL_FILE, URBANIZATION_QUANTITY, 2)
    return ind1, ind2


def get_random_deap_uster_individual():
    creator.create("FitnessMax", base.Fitness, weights=(-1, -1))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    return spg(list, creator.Individual, AREAL_FILE, URBANIZATION_QUANTITY, 1)[0]
