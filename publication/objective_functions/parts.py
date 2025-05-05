# ~Schwaab, from test_fractal_index

import numpy
import scipy
from scipy import ndimage


# Returns the given matrix with a zero border coloumn and row around
def f_setBorderZero(matrix):
    # print('f_setBorderZero') # test
    # print(matrix) # test
    heightFP,widthFP = matrix.shape #define hight and width of input matrix
    withBorders = numpy.ones((heightFP+(2*1),widthFP+(2*1)))*0 # set the border to borderValue
    withBorders[1:heightFP+1,1:widthFP+1]=matrix # set the interior region to the input matrix
    # print('withBorders') # test
    # print(withBorders) # test
    return withBorders


# Connected component labeling function
def f_ccl(cl_array, ab):
    '''
    Transforms input array, by labeling its disjointed patches, and counting their number
    :param cl_array: ?binary? matrix of lulc
    :param ab: ???
    :return: matrix, where pathes are labelled: all cells of 1st patch equall 1, 2nd patch equall 2... Zeros stay 0.
        And number of disjointed patches.
    '''
    #ab=[2,2]
    # Binary structure
    struct = scipy.ndimage.generate_binary_structure(ab[0],ab[1])
    labeled_array, numpatches = ndimage.label(cl_array,struct) #ndimage.measurements.label(cl_array,struct)
    return labeled_array, numpatches

# [KUBA]: #only 0 or 1 can be passed, which means that a 0/1 grid/array must be created for each class
#es kann nur 0 oder 1 ?bergeben werden, das heisst, dass fuer jede Klasse ein 0/1 Raster/Array erzeugt werden muss

# Returns total Edge length
def f_returnEdgeLength(labeled_array, cellsize):
    TotalEdgeLength = f_returnPatchPerimeter(labeled_array)
    return TotalEdgeLength * cellsize


# Returns sum of patches perimeter
def f_returnPatchPerimeter(labeled_array):
    '''
    Calculates the total perimiter of all distinct regions
        ~divided by 2 (because each border is shared by exactly 2 regions, except map border
        , which belongs exactly to one region at a time.)
    :param labeled_array: matrix of lulc
        IF WE WANT ONLY PERIMITER OF URBAN, IT NEEDS TO BE BINARY: 1-URBAN, 0-NON-URBAN
    :return: total number of edges between different lulc cells, including border.
    '''
    labeled_array = f_setBorderZero(labeled_array) # make a border with zeroes
    TotalPerimeter = (
            numpy.sum(                          # compare horizontally
                labeled_array[:,1:]             # array without FIRST column
                != labeled_array[:,:-1]         # array without LAST column
            )                                   # ich porównanie, to efektywnie porównanie sasiadójących pól.
            + numpy.sum(
                labeled_array[1:,:]
                != labeled_array[:-1,:])        # compare vertically
    )
    return TotalPerimeter


# def f_returnPatch(labeled_array,patch):
#     # Make an array of zeros the same shape as `a`.
#     feature = numpy.zeros_like(labeled_array, dtype=int)
#     feature[labeled_array == patch] = 1
#     return feature
#
#
# # Return the total area for the given class
# def f_returnArea(labeled_array, cellsize_2):
#     #sizes = scipy.ndimage.sum(array, labeled_array, range(numpatches + 1)).astype(labeled_array.dtype)
#     area = numpy.sum(labeled_array != 0) * cellsize_2
#     return area
