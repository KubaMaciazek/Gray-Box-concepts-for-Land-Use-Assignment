# ############################################################################################ ###########################################################################################
# RCM (Random cell mutation) ~SCHWAAB
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import numpy
import random

from publication.operators.mutations.rrm import RRM


def RCM(individual, current_landuse, quantity, indpb, count_max):

##    print individual
##    print numpy.sum(individual==2)

    individual = RRM(individual,current_landuse,quantity) #do the repair! then do the single pixel mutation
    # individual = RRM(individual,current_landuse,quantity)[0] #do the repair! then do the single pixel mutation

##    print individual
##    print numpy.sum(individual==2)

##    print "entered function"
    if random.random() < indpb:

##        print "entered if"
##        print indpb
        indices_agri = numpy.where(numpy.array(individual == 2)) #dauert das zu lange?
        indices_agri_x = indices_agri[0]
        indices_agri_y = indices_agri[1]
        indices_urban = numpy.where(numpy.array(current_landuse==2) & numpy.array(individual == 1)) #dauert das zu lange?
        indices_urban_x = indices_urban[0]
        indices_urban_y = indices_urban[1]
        rn = numpy.random.choice(range(0, len(indices_agri_x)-1), count_max, replace=False) #tatsaechlich random
        individual[[indices_agri_x[rn]],[indices_agri_y[rn]]] = 1
        rn = numpy.random.choice(range(0, len(indices_urban_x)-1), count_max, replace=False) #tatsaechlich random
        individual[[indices_urban_x[rn]],[indices_urban_y[rn]]] = 2

    return individual,


def RCM_without_repair(individual, current_landuse, quantity, indpb, count_max):

##    print individual
##    print numpy.sum(individual==2)

    #individual = RRM(individual,current_landuse,quantity)[0] #do the repair! then do the single pixel mutation

##    print individual
##    print numpy.sum(individual==2)
    #print "enter function"
    #print(indpb)

    if random.random() < indpb:

        #print(indpb)
        #print "enter if"
        #print "RCM_without_repair"
        indices_agri = numpy.where(numpy.array(individual == 2)) #dauert das zu lange?
        indices_agri_x = indices_agri[0]
        indices_agri_y = indices_agri[1]
        indices_urban = numpy.where(numpy.array(current_landuse==2) & numpy.array(individual == 1)) #dauert das zu lange?
        indices_urban_x = indices_urban[0]
        indices_urban_y = indices_urban[1]
        rn = numpy.random.choice(range(0, len(indices_agri_x)-1), count_max, replace=False) #tatsaechlich random
        individual[[indices_agri_x[rn]],[indices_agri_y[rn]]] = 1
        rn = numpy.random.choice(range(0, len(indices_urban_x)-1), count_max, replace=False) #tatsaechlich random
        individual[[indices_urban_x[rn]],[indices_urban_y[rn]]] = 2

    return individual,