# ~Schwaab, from test_fractal_index

import numpy
from publication.objective_functions.parts import f_ccl, f_returnEdgeLength


def edge_length_urban(original, new_urban, ab):
    '''
    :param original: original lulc
    :param new_urban: indyvidual, binary matrix indicating cells for urbanization (1'ones)
    :param ab: ?
    :return: total edge length (TEL) of all urban cells pathes
    '''

    # print('edge_length_urban')  #test

##    original = numpy.array([[2,1,1,1,3,3],[2,2,2,2,3,3],[1,1,3,3,1,1],[4,4,4,1,4,2]])
##    new_urban = numpy.array([[0,0,0,0,0,0],[0,0,0,1,0,0],[0,0,0,0,0,0],[0,0,0,0,1,1]])

    area_lulcc = numpy.zeros_like(new_urban, dtype=int)
    # print('area_lulcc')
    # print(area_lulcc)  # test
    # print('new_urban')
    # print(new_urban)  # test
    # print('original')
    # print(original)  # test
    area_lulcc[(new_urban == 1) | (original == 1)] = 1  # [KUBA][!!!]: dodany OR original=1.
    # print('area_lulcc')
    # print(area_lulcc)  # test
    labeled_array, numpatches = f_ccl(area_lulcc, ab)
    # print('labeled_array')
    # print(labeled_array)  # test
    # print(numpatches)  # test

    #option 1
    '''
    To, gdyby tu dać poprustu sume orginalnych urban z indyvidualem, to by chyba wystarczyło...
    '''
    total_edge_length_urban = f_returnEdgeLength(labeled_array, 1)

    #slower or faster? the second version is slower
    #option 2
##    labeled_array = (f_setBorderZero(labeled_array))
##    labeled_array = labeled_array.astype(int)
##    bool_outer_edge=skimage.segmentation.find_boundaries(labeled_array, mode="outer")
##    total_edge_length_urban = numpy.sum(bool_outer_edge)

    return total_edge_length_urban
