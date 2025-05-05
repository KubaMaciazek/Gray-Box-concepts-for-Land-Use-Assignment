# ############################################################################################ ###########################################################################################
# BRM (Biased repair mutation) ~SCHWAAB
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import scipy
import numpy
from scipy import ndimage
import scipy.signal
import scipy.stats


def BRM(individual, current_landuse,quantity, power_BRM, power_inverse_BRM):
    sum_urban = numpy.sum(numpy.array(individual==1))
    sum_total = numpy.sum(numpy.array(current_landuse==1)) + quantity #numpy.sum(areal[areal==1])
    # print("BRM: ", str(sum_urban-sum_total))
    count=0

    if sum_urban > sum_total:

        # print("BRM >")
        original_copy = numpy.copy(current_landuse)
        original_copy[individual==1] = 1 #in der original copy ist also der patch auch geloescht
        original_copy_labeling = numpy.copy(original_copy)
        original_copy_labeling[original_copy_labeling!=1]=0
        indices = numpy.where(numpy.array(current_landuse==2) & numpy.array(individual == 1))
        coords = zip(indices[0], indices[1])
        struct = scipy.ndimage.generate_binary_structure(2,1)
        struct_mask = numpy.zeros(struct.shape)
        struct_mask[struct]=1 #2
        neighbours = scipy.ndimage.filters.convolve(original_copy_labeling, struct_mask, mode='constant')
        neighbours[numpy.logical_not(numpy.array(current_landuse==2) & numpy.array(individual == 1))] = 0
        probabilities = neighbours[numpy.array(current_landuse==2) & numpy.array(individual == 1)]
        probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
        probabilities = probabilities#**power_attach_by_prob

        inverse_probabilities = numpy.max(probabilities/probabilities.sum())  + numpy.min(probabilities/probabilities.sum())   -probabilities/probabilities.sum()
        inverse_probabilities = inverse_probabilities**power_inverse_BRM
        #inverse_probabilities=(1-probabilities/probabilities.sum())/numpy.sum((1-probabilities/probabilities.sum()))

        #or
        #inverse_probabilities=(1-probabilities/probabilities.sum())/numpy.sum((1-probabilities/probabilities.sum()))
        #or uniform
        #inverse_probabilities[inverse_probabilities >=0]=1.

##        newvalue = a * value + b
##        a = (max'-min')/(max-min)
##        b = max - a * max
##        a = (0.1-0.01)/ (numpy.max(inverse_probabilities) - numpy.min(inverse_probabilities))
##        b = 0.1 - a * numpy.max(inverse_probabilities)
##        new = a * inverse_probabilities + b

        coords_list = list(coords)
        i = numpy.random.choice(len(coords_list), int(sum_urban-sum_total), replace=False, p=inverse_probabilities/numpy.sum(inverse_probabilities))
        #rn = numpy.random.choice(range(0, len(indices_x)-1), int(sum_urban-sum_total), replace=False) #tatsaechlich random
        for j in i:
            individual[coords_list[j]]=2


    if sum_urban < sum_total:


        # print("BRM <")
        original_copy = numpy.copy(current_landuse)
        original_copy[individual==1] = 1 #in der original copy ist also der patch auch geloescht # [K]:in the original copy the patch is also deleted
        original_copy_labeling = numpy.copy(original_copy)
        original_copy_labeling[original_copy_labeling!=1]=0
        indices = numpy.where(numpy.array(current_landuse==2) & numpy.array(individual == 2))
        coords = zip(indices[0], indices[1])
        # print("nr of choices: ", str(len(indices[0])))
        struct = scipy.ndimage.generate_binary_structure(2,1)
        struct_mask = numpy.zeros(struct.shape)
        struct_mask[struct]=1 #2
        neighbours = scipy.ndimage.filters.convolve(original_copy_labeling, struct_mask, mode='constant')
        neighbours[numpy.logical_not(numpy.array(current_landuse==2) & numpy.array(individual == 2))] = 0
        probabilities = neighbours[numpy.array(current_landuse==2) & numpy.array(individual == 2)]
        probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
        probabilities = probabilities**power_BRM
        # # [KUBA]: Python 2>3 compatibility
        # i = numpy.random.choice(len(coords), int(sum_total-sum_urban), replace=False, p=probabilities/probabilities.sum())
        coords_list = list(coords)
        # print(coords_list)
        i = numpy.random.choice(len(coords_list), int(sum_total-sum_urban), replace=False, p=probabilities/probabilities.sum())
        # print("i: ", str(i))
        # print(i)
        # print(len(coords_list))
        # print(coords_list)
        #rn = numpy.random.choice(range(0, len(indices_x)-1), int(sum_urban-sum_total), replace=False) #tatsaechlich random

        for j in i:
            # print(coords_list[j])
            # print(individual[coords_list[j]])
            individual[coords_list[j]]=1

#    print "numpy.sum(numpy.array(individual==1)): %d" %numpy.sum(numpy.array(individual==1))
    return individual
    # return individual,
