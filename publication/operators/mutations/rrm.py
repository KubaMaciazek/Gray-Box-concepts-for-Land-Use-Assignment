# ############################################################################################ ###########################################################################################
# RRM (Random repair mutation)  ~ SCHWAAB
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import numpy

##current_landuse = numpy.array([[1,2,2,2,3,3],[2,2,2,2,3,3],[1,2,3,2,1,1],[4,2,2,2,4,2]])
##individual = numpy.array([[1,1,2,2,2,0],[0,2,1,1,0,2],[0,2,0,2,2,0],[0,2,2,2,1,1]])
##quantity = 5


def RRM(individual, current_landuse, quantity):

    sum_urban = numpy.sum(numpy.array(individual==1))
    sum_total = numpy.sum(numpy.array(current_landuse==1)) + quantity #numpy.sum(areal[areal==1])
    count=0
    if sum_urban > sum_total:

        indices = numpy.where(numpy.array(current_landuse==2) & numpy.array(individual == 1))
        indices_x = indices[0]
        indices_y = indices[1]
        rn = numpy.random.choice(range(0, len(indices_x)-1), int(sum_urban-sum_total), replace=False) #tatsaechlich random

        individual[[indices_x[rn]],[indices_y[rn]]] = 2

        indices_x = numpy.delete(indices_x,rn)
        indices_y = numpy.delete(indices_y,rn)

        sum_urban = numpy.sum(numpy.array(individual==1))
        count = count + 1


    if sum_urban < sum_total:

        indices = numpy.where(numpy.array(current_landuse==2) & numpy.array(individual == 2))
        indices_x = indices[0]
        indices_y = indices[1]

        rn = numpy.random.choice(range(0, len(indices_x)-1), int(sum_total-sum_urban), replace=False) #tatsaechlich random
        individual[[indices_x[rn]],[indices_y[rn]]] = 1

        indices_x = numpy.delete(indices_x,rn)
        indices_y = numpy.delete(indices_y,rn)

        sum_urban = numpy.sum(numpy.array(individual==1))
        count=count+1
#    print "numpy.sum(numpy.array(individual==1)): %d" %numpy.sum(numpy.array(individual==1))
    return individual
