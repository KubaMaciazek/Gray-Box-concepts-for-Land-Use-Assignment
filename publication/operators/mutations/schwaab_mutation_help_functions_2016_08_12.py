import scipy
import numpy
from scipy import ndimage
import scipy.signal
import scipy.stats

#help-functions ~SCHWAAB
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Returns the given matrix with a zero border coloumn and row around
def f_setBorderZero(matrix):
    heightFP,widthFP = matrix.shape #define hight and width of input matrix
    withBorders = numpy.ones((heightFP+(2*1),widthFP+(2*1)))*0 # set the border to borderValue
    withBorders[1:heightFP+1,1:widthFP+1]=matrix # set the interior region to the input matrix
    return withBorders

# Connected component labeling function
def f_ccl(cl_array, ab):
    #ab=[2,2]
    # Binary structure
    struct = scipy.ndimage.generate_binary_structure(ab[0],ab[1])
    labeled_array, numpatches = ndimage.label(cl_array,struct) #ndimage.measurements.label(cl_array,struct)
    return labeled_array, numpatches

#es kann nur 0 oder 1 ?bergeben werden, das heisst, dass fuer jede Klasse ein 0/1 Raster/Array erzeugt werden muss
# Returns total Edge length
def f_returnEdgeLength(labeled_array, cellsize):
    TotalEdgeLength = f_returnPatchPerimeter(labeled_array)
    return TotalEdgeLength * cellsize

# Returns sum of patches perimeter
def f_returnPatchPerimeter(labeled_array):
    labeled_array = f_setBorderZero(labeled_array) # make a border with zeroes
    TotalPerimeter = numpy.sum(labeled_array[:,1:] != labeled_array[:,:-1]) + numpy.sum(labeled_array[1:,:] != labeled_array[:-1,:])
    return TotalPerimeter

def f_returnPatch(labeled_array,patch):
    # Make an array of zeros the same shape as `a`.
    feature = numpy.zeros_like(labeled_array, dtype=int)
    feature[labeled_array == patch] = 1
    return feature

# Return the total area for the given class
def f_returnArea(labeled_array, cellsize_2):
    #sizes = scipy.ndimage.sum(array, labeled_array, range(numpatches + 1)).astype(labeled_array.dtype)
    area = numpy.sum(labeled_array != 0) * cellsize_2
    return area
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
