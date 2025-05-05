import random
import numpy
import math

from publication.operators.mutations.rrm import RRM


# ############################################################################################ ###########################################################################################
# RBM (Random Block Mutation) ~ SCHWAAB
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def RBM(individual, current_landuse, quantity, indpb_clustering):



    if random.random() < indpb_clustering:
        edge_length_01 = random.randint(1,math.trunc(math.sqrt(quantity)/1.5))
        #edge_length_02 = random.randint(1,math.trunc(math.sqrt(quantity)/1.5))
        big_struct = numpy.ones(shape=(edge_length_01, edge_length_01)) #square, if I take the same edge_length

##        increase_struct = random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #taking the sqrt means taking the length of the edge of a square (deviding it by 2. makes it approximately the multiplicator in scipy.ndimage.iterate_structure
##        struct = scipy.ndimage.generate_binary_structure(2,1)
##        big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)

        #pick random x and y, they have to be larger than half the length of big_struct and smaller than len(x/Y)-half the length struct
        pivot_x = random.randint(0,individual.shape[0] - (math.ceil(big_struct.shape[0])+1) ) #math.ceil rundet auf  math.ceil(big_struct.shape[0]/2.)
        pivot_y = random.randint(0,individual.shape[1] - (math.ceil(big_struct.shape[1])+1) ) #shape 0 oder 1 ist egal, wenn quadrat    math.ceil(big_struct.shape[1]/2.)
        sum_new_urban = int(numpy.sum(numpy.logical_and(big_struct, individual[pivot_x:(pivot_x+big_struct.shape[1]), pivot_y:(pivot_y+big_struct.shape[0])]==2)))
        #print sum_new_urban
        individual_copy_bool = numpy.empty_like(individual, dtype=bool)
        individual_copy_bool[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]][numpy.logical_and(big_struct, individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]]==2)] = True
        individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]][numpy.logical_and(big_struct, individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]]==2)] = 1

    individual = RRM(individual, current_landuse, quantity)  # do the repair! then do the single pixel mutation
    # individual = RRM(individual, current_landuse, quantity)[0]  # do the repair! then do the single pixel mutation
    #old way of creating a block

    return individual,


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! it is not possible to simple remove the repair here, even this version has a repair in it now
def RBM_without_repair(individual, current_landuse, quantity, indpb_clustering):

##    increase_struct = random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #taking the sqrt means taking the length of the edge of a square (deviding it by 2. makes it approximately the multiplicator in scipy.ndimage.iterate_structure
##    struct = scipy.ndimage.generate_binary_structure(2,1)
##    big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)

    if random.random() < indpb_clustering:
        edge_length_01 = random.randint(1,math.trunc(math.sqrt(quantity)/1.5))
        #edge_length_02 = random.randint(1,math.trunc(math.sqrt(quantity)/1.5))
        big_struct = numpy.ones(shape=(edge_length_01, edge_length_01)) #square, if I take the same edge_length
        #print "RBM_without_repair"

##        increase_struct = random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #taking the sqrt means taking the length of the edge of a square (deviding it by 2. makes it approximately the multiplicator in scipy.ndimage.iterate_structure
##        struct = scipy.ndimage.generate_binary_structure(2,1)
##        big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)

        #pick random x and y, they have to be larger than half the length of big_struct and smaller than len(x/Y)-half the length struct
        pivot_x = random.randint(0,individual.shape[0] - (math.ceil(big_struct.shape[0])+1) ) #math.ceil rundet auf  math.ceil(big_struct.shape[0]/2.)
        pivot_y = random.randint(0,individual.shape[1] - (math.ceil(big_struct.shape[1])+1) ) #shape 0 oder 1 ist egal, wenn quadrat    math.ceil(big_struct.shape[1]/2.)
        sum_new_urban = int(numpy.sum(numpy.logical_and(big_struct, individual[pivot_x:(pivot_x+big_struct.shape[1]), pivot_y:(pivot_y+big_struct.shape[0])]==2)))
        #print sum_new_urban
        individual_copy_bool = numpy.empty_like(individual, dtype=bool)
        individual_copy_bool[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]][numpy.logical_and(big_struct, individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]]==2)] = True
        individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]][numpy.logical_and(big_struct, individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]]==2)] = 1

    """ [KUBA]: ACTUALLY REMOVING REPAIR !!! -> commented below line to do that"""
    individual = RRM(individual,current_landuse,quantity) #do the repair! then do the single pixel mutation

    return individual,


def RBM_without_repair_TRURLY(individual, current_landuse, quantity, indpb_clustering):

##    increase_struct = random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #taking the sqrt means taking the length of the edge of a square (deviding it by 2. makes it approximately the multiplicator in scipy.ndimage.iterate_structure
##    struct = scipy.ndimage.generate_binary_structure(2,1)
##    big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)

    if random.random() < indpb_clustering:
        edge_length_01 = random.randint(1,math.trunc(math.sqrt(quantity)/1.5))
        #edge_length_02 = random.randint(1,math.trunc(math.sqrt(quantity)/1.5))
        big_struct = numpy.ones(shape=(edge_length_01, edge_length_01)) #square, if I take the same edge_length
        #print "RBM_without_repair"

##        increase_struct = random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #taking the sqrt means taking the length of the edge of a square (deviding it by 2. makes it approximately the multiplicator in scipy.ndimage.iterate_structure
##        struct = scipy.ndimage.generate_binary_structure(2,1)
##        big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)

        #pick random x and y, they have to be larger than half the length of big_struct and smaller than len(x/Y)-half the length struct
        pivot_x = random.randint(0,individual.shape[0] - (math.ceil(big_struct.shape[0])+1) ) #math.ceil rundet auf  math.ceil(big_struct.shape[0]/2.)
        pivot_y = random.randint(0,individual.shape[1] - (math.ceil(big_struct.shape[1])+1) ) #shape 0 oder 1 ist egal, wenn quadrat    math.ceil(big_struct.shape[1]/2.)
        sum_new_urban = int(numpy.sum(numpy.logical_and(big_struct, individual[pivot_x:(pivot_x+big_struct.shape[1]), pivot_y:(pivot_y+big_struct.shape[0])]==2)))
        #print sum_new_urban
        individual_copy_bool = numpy.empty_like(individual, dtype=bool)
        individual_copy_bool[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]][numpy.logical_and(big_struct, individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]]==2)] = True
        individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]][numpy.logical_and(big_struct, individual[pivot_x:pivot_x+big_struct.shape[1], pivot_y:pivot_y+big_struct.shape[0]]==2)] = 1

    """ [KUBA]: ACTUALLY REMOVING REPAIR !!! -> commented below line to do that"""
    # individual = RRM(individual,current_landuse,quantity) #do the repair! then do the single pixel mutation

    return individual,
