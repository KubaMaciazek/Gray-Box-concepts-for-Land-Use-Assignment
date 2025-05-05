# ############################################################################################ ###########################################################################################
# BCPM (Biased Cells Patch Mutation ) ~SCHWAAB
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import random
import scipy
import numpy
from scipy import ndimage
import skimage
import scipy.signal
import scipy.stats

from publication.operators.mutations.brm import BRM
from publication.operators.mutations.schwaab_mutation_help_functions_2016_08_12 import f_ccl


def BCPM(individual, current_landuse, quantity, indpb_patch, power_BCPM, power_patch_BCPM, power_patch_inverse_BCPM, power_BRM, power_inverse_BRM):

    # individual = BRM(individual,current_landuse,quantity, power_BRM, power_inverse_BRM)[0] #do the repair! then do the single pixel mutation
    individual = BRM(individual, current_landuse, quantity, power_BRM, power_inverse_BRM)  # do the repair! then do the single pixel mutation

    if random.random() < indpb_patch:


        original = numpy.copy(current_landuse)

        #I decided to not use a combination of original and individual, but only the individual, makes things easier (maybe somehow good and not so good)
        individual_new_urban = numpy.zeros_like(individual)
        individual_new_urban[numpy.array(current_landuse==2) & numpy.array(individual == 1)] = 1 #only new urban pixels
        labeled_array, numpatches = f_ccl(individual_new_urban, [2,1])

        #here an if condition for the number of patches
        if numpatches > 2:

            #calculate sizes of patches
            sizes = ndimage.sum(individual_new_urban, labeled_array, range(numpatches + 1))
            sizes = sizes[sizes!=0] # remove zeros

            #instead of selecting min_size, select size according to probability
            #devide size, so that the differences between the municipalities becomes smaller

            inverse_probabilities = numpy.max(sizes/numpy.sum(sizes))  + numpy.min(sizes/numpy.sum(sizes))   - sizes/numpy.sum(sizes)
            #inverse_probabilities = inverse_probabilities * (1-inverse_probabilities)
            #inverse_probabilities = inverse_probabilities ** power
            #inverse_probabilities[inverse_probabilities>=0]=1.
            inverse_probabilities = inverse_probabilities ** power_patch_inverse_BCPM
            #inverse_probabilities=(1-(sizes/numpy.sum(sizes)))/numpy.sum(1-(sizes/numpy.sum(sizes)))

            min_size = numpy.random.choice(sizes, 1, p=inverse_probabilities/numpy.sum(inverse_probabilities)) # #or p=(1-(sizes/numpy.sum(sizes)))/numpy.sum(1-(sizes/numpy.sum(sizes)))
            mask_size = numpy.where(sizes==min_size)
            mask_size = mask_size[0] +1
            #randomly select one of these patches that are equal or smaller 2 in size

            a_index = random.choice(mask_size)

            #delete this patch in the individual_new_urban #maybe the whole thing could be done using some of the image functions, e.g. for removing noise (erosion?)
            sum_deleted = numpy.sum(labeled_array==a_index)
            individual_new_urban[labeled_array==a_index] = 0

            #print "sum_deleted: %d" %sum_deleted


            #if attach_by_prob:
            tmp_bool=False
            if random.random() < 0:
                #print "test_01"
                tmp_bool=True

                original_copy = numpy.copy(original)
                original_copy[individual_new_urban==1] = 1 #in der original copy ist also der patch auch geloescht

                original_copy_labeling = numpy.copy(original_copy)
                original_copy_labeling[original_copy_labeling!=1]=0
    ##            labeled_array, numpatches = f_ccl(original_copy_labeling, [2,1])

                #assign the amount of pixels (belonging to the deleted patch), assign to the largest patch? or to a random patch? to the patches of the individual_new_urban or a combination of the individual_new_urban and the original?

                #first version: to the largest patch of the individual_new_urban (makes maybe even more sense: I do not want to assign new areas to existing farms, which are often the single pixels in the original)
    ##            range_numpatches = numpy.array(range(1, numpatches+1))
    ##            range_numpatches= range_numpatches[range_numpatches != a_index]

    ##            if max_patch:
    ##                patch_number = numpy.max(range_numpatches)
    ##            else:
    ##                patch_number = random.choice(range_numpatches)

    ##            labeled_array_copy = numpy.copy(labeled_array)
    ##            labeled_array_copy[labeled_array != patch_number] = 0
    ##            bool_outer_edge=skimage.segmentation.find_boundaries(labeled_array_copy, mode="outer") #, connectivity=1, mode='thick', background=0)

                bool_agri = original_copy==2
    ##            sum_true = numpy.sum(bool_outer_edge & bool_agri)

    ##            if sum_true >= sum_deleted:
                arrays_indices = numpy.where(bool_agri)
                coords = zip(arrays_indices[0], arrays_indices[1])

                #use varying neighborhood sizes
    ###########################################################
    ##            increase_struct = random.randint(1,math.trunc(math.sqrt((min(original_copy.shape))))) #random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #maybe quantity isn't the right indicator here, maybe rather edge length
    ##            #print(increase_struct)
    ##            struct = scipy.ndimage.generate_binary_structure(2,1)
    ##            big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)
    ##            struct_mask = numpy.zeros(big_struct.shape)
    ##            struct_mask[big_struct]=1 #2
    ###########################################################
                #this does not work well, because he counts the number of neighbors, however, it should count the number of neighbors only for agricultural pixels -> a filter seems more appropriate
                struct = scipy.ndimage.generate_binary_structure(2,1)
                struct_mask = numpy.zeros(struct.shape)
                struct_mask[struct]=1 #2

                #original_copy[original_copy!=1] = 0 #2
                #neighbours = scipy.ndimage.filters.convolve(original_copy, struct_mask, mode='constant') #/4
                #neighbours = scipy.signal.convolve2d(original_copy, struct_mask, mode='same')
                neighbours = scipy.ndimage.filters.convolve(original_copy_labeling, struct_mask, mode='constant')


    ##            import arcpy
    ##            prel_pr_exp = neighbours
    ##            name_gemeinde = "Uster"
    ##            extent_raster = arcpy.Raster("D:/doktorarbeit/optimization/data_gemeinden_zuerich/" + str(name_gemeinde) + "/areal_4_09.tif")
    ##            extent = extent_raster.extent
    ##            myRaster = arcpy.NumPyArrayToRaster(prel_pr_exp, lower_left_corner = arcpy.Point(extent.XMin,extent.YMin), x_cell_size=100, y_cell_size=100, value_to_nodata=0)
    ##            myRaster.save("D:/doktorarbeit/optimization/tmp/neighbours_new.tif")

                #filter
    #########################################################################################################################
                neighbours[numpy.logical_not(bool_agri)] = 0

                #increase_struct = random.randint(1,math.trunc(math.sqrt((min(original_copy.shape))))) #random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #maybe quantity isn't the right indicator here, maybe rather edge length
                ##print(increase_struct)
                #struct = scipy.ndimage.generate_binary_structure(2,1)
                #big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)
                #struct_mask = numpy.zeros(big_struct.shape)
                #struct_mask[big_struct]=1 #2

                #filtered = scipy.ndimage.filters.convolve(neighbours, struct_mask, mode='constant')

    ##            import cv2
    ##            filtered = cv2.GaussianBlur(neighbours,(5,5),0)
                ##filtered = numpy.array(filters.gaussian_filter(current_landuse, sigma=1))
                ##filtered = scipy.ndimage.filters.gaussian_filter(neighbours, sigma=10)
                ##scipy.ndimage.filters.gaussian_filter(input=current_landuse, sigma=0.1)
                ##filtered = gaussian_kde(neighbours)

    ##            import arcpy
    ##            prel_pr_exp = filtered
    ##            name_gemeinde = "Uster"
    ##            extent_raster = arcpy.Raster("D:/doktorarbeit/optimization/data_gemeinden_zuerich/" + str(name_gemeinde) + "/areal_4_09.tif")
    ##            extent = extent_raster.extent
    ##            myRaster = arcpy.NumPyArrayToRaster(prel_pr_exp, lower_left_corner = arcpy.Point(extent.XMin,extent.YMin), x_cell_size=100, y_cell_size=100, value_to_nodata=0)
    ##            myRaster.save("D:/doktorarbeit/optimization/tmp/filtered.tif")

                #if random.random() < 0.5:
                #    probabilities = filtered[bool_agri]
                #else:
                probabilities = neighbours[bool_agri]


                probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
                probabilities = probabilities**power_BCPM


                #print probabilities
                #print probabilities/probabilities.sum()**power_attach_by_prob
                i = numpy.random.choice(len(coords), sum_deleted, replace=False, p=probabilities/probabilities.sum())
                #print i

                for j in i:
                    individual_new_urban[coords[j]]=1

                individual[current_landuse==2]=2
                individual[individual_new_urban==1]=1



            #elif attach_overall:
            elif tmp_bool==False:
                #print "test_02"
                original_copy = numpy.copy(original)
                original_copy[individual_new_urban==1] = 1 #in der original copy ist also der patch auch geloescht

                original_copy_labeling = numpy.copy(original_copy)
                original_copy_labeling[original_copy_labeling!=1]=0
                labeled_array, numpatches = f_ccl(original_copy_labeling, [2,1])

    ##            import arcpy
    ##            prel_pr_exp = labeled_array
    ##            name_gemeinde = "Uster"
    ##            extent_raster = arcpy.Raster("D:/doktorarbeit/optimization/data_gemeinden_zuerich/" + str(name_gemeinde) + "/areal_4_09.tif")
    ##            extent = extent_raster.extent
    ##            myRaster = arcpy.NumPyArrayToRaster(prel_pr_exp, lower_left_corner = arcpy.Point(extent.XMin,extent.YMin), x_cell_size=100, y_cell_size=100, value_to_nodata=0)
    ##            myRaster.save("D:/doktorarbeit/optimization/tmp/labeled_array.tif")


                sizes = ndimage.sum(original_copy_labeling, labeled_array, range(numpatches + 1))
                sizes = sizes[sizes!=0] # remove zeros
                #assign the amount of pixels (belonging to the deleted patch), assign to the largest patch? or to a random patch? to the patches of the individual_new_urban or a combination of the individual_new_urban and the original?

                #first version: to the largest patch of the individual_new_urban (makes maybe even more sense: I do not want to assign new areas to existing farms, which are often the single pixels in the original)
                range_numpatches = numpy.array(range(1, numpatches+1))
    ##            range_numpatches= range_numpatches[range_numpatches != a_index]

                #calculate probabilities
                struct = scipy.ndimage.generate_binary_structure(2,1)
                struct_mask = numpy.zeros(struct.shape)
                struct_mask[struct]=1 #2
                neighbours = scipy.ndimage.filters.convolve(original_copy_labeling, struct_mask, mode='constant')

                bool_agri = original_copy==2
                arrays_indices = numpy.where(bool_agri)
                coords = zip(arrays_indices[0], arrays_indices[1])
                neighbours[numpy.logical_not(bool_agri)] = 0


                ###########################################################
                #if max_patch:
    ##            if random.random()<0.5:
    ##                patch_number = numpy.max(range_numpatches)
    ##            else:
    ##                patch_number = random.choice(range_numpatches)

                ###########################################################
                #select patch by probability proportional to patch size

                probabilities = sizes/numpy.sum(sizes)
                probabilities = probabilities**power_patch_BCPM

                patch_number = numpy.random.choice(range_numpatches, p=probabilities/numpy.sum(probabilities))

                labeled_array_copy = numpy.copy(labeled_array)
                labeled_array_copy[labeled_array != patch_number] = 0
                bool_outer_edge=skimage.segmentation.find_boundaries(labeled_array_copy, mode="outer") #, connectivity=1, mode='thick', background=0)

                sum_true = numpy.sum(bool_outer_edge & bool_agri)

                probabilities = neighbours[bool_agri & bool_outer_edge]
                probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
                probabilities = probabilities**power_BCPM


                if sum_true >= sum_deleted:
                        arrays_indices = numpy.where(bool_outer_edge & bool_agri)

                        # [KUBA]: Python 2.7 to 3.4
                        # coords = zip(arrays_indices[0], arrays_indices[1])
                        coords = list(zip(arrays_indices[0], arrays_indices[1]))

                        for i in numpy.random.choice(len(coords), sum_deleted, replace=False, p=probabilities/probabilities.sum()):
                            individual_new_urban[coords[i]]=1


                if sum_true < sum_deleted:

                        if sum_true > 0:
                            arrays_indices = numpy.where(bool_outer_edge & bool_agri)

                            # [KUBA]: Python 2.7 to 3.4
                            # coords = zip(arrays_indices[0], arrays_indices[1])
                            coords = list(zip(arrays_indices[0], arrays_indices[1]))

                            for i in numpy.random.choice(len(coords), sum_true, replace=False, p=probabilities/probabilities.sum()):
                                individual_new_urban[coords[i]]=1

                        #and randomly pick some new pixels according to the difference of the pixels available around the edge and the "ones" which have been deleted
                        arrays_indices = numpy.where([individual_new_urban==0] & bool_agri)

                        # [KUBA]: Python 2.7 to 3.4
                        # coords = zip(arrays_indices[1], arrays_indices[2])
                        coords = list(zip(arrays_indices[1], arrays_indices[2]))

                        #new probabilities
                        probabilities = neighbours[(individual_new_urban==0) & bool_agri]
                        probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
                        probabilities = probabilities**power_BCPM

                        for i in numpy.random.choice(len(coords), sum_deleted-sum_true, replace=False, p=probabilities/probabilities.sum()):
                            individual_new_urban[coords[i]]=1

                individual[current_landuse==2]=2
                individual[individual_new_urban==1]=1



            else:

                #assign the amount of pixels (belonging to the deleted patch), assign to the largest patch? or to a random patch? to the patches of the individual_new_urban or a combination of the individual_new_urban and the original?
                #print "test"
                #first version: to the largest patch of the individual_new_urban (makes maybe even more sense: I do not want to assign new areas to existing farms, which are often the single pixels in the original)
                range_numpatches = numpy.array(range(1, numpatches+1))
                range_numpatches= range_numpatches[range_numpatches != a_index]

##                if max_patch:
##                    patch_number = numpy.max(range_numpatches)
##                else:
                patch_number = random.choice(range_numpatches)

                labeled_array_copy = numpy.copy(labeled_array)
                labeled_array_copy[labeled_array != patch_number] = 0
                bool_outer_edge=skimage.segmentation.find_boundaries(labeled_array_copy, mode="outer") #, connectivity=1, mode='thick', background=0)

                bool_agri = original==2
                sum_true = numpy.sum(bool_outer_edge & bool_agri)

                if sum_true >= sum_deleted:
                        arrays_indices = numpy.where(bool_outer_edge & bool_agri)
                        coords = list(zip(arrays_indices[0], arrays_indices[1])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                        for i in numpy.random.choice(len(coords), sum_deleted, replace=False):
                            individual_new_urban[coords[i]]=1


                if sum_true < sum_deleted:

                        if sum_true > 0:
                            arrays_indices = numpy.where(bool_outer_edge & bool_agri)
                            coords = list(zip(arrays_indices[0], arrays_indices[1])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                            for i in numpy.random.choice(len(coords), sum_true, replace=False):
                                individual_new_urban[coords[i]]=1

                #and randomly pick some new pixels according to the difference of the pixels available around the edge and the "ones" which have been deleted

                        arrays_indices = numpy.where([individual_new_urban==0] & bool_agri)
                        coords = list(zip(arrays_indices[1], arrays_indices[2])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                        for i in numpy.random.choice(len(coords), sum_deleted-sum_true, replace=False):
                            individual_new_urban[coords[i]]=1

                individual[current_landuse==2]=2
                individual[individual_new_urban==1]=1
                            #print individual_new_urban

    return individual,






def BCPM_without_repair(individual, current_landuse, quantity, indpb_patch, power_BCPM, power_patch_BCPM, power_patch_inverse_BCPM, power_BRM, power_inverse_BRM):


    #individual = BRM(individual,current_landuse,quantity, power_BRM, power_inverse_BRM)[0] #do the repair! then do the single pixel mutation

##    print "enter function"
    if random.random() < indpb_patch:

##        print(indpb_patch)
##        print "enter if"
        original = numpy.copy(current_landuse)

        #I decided to not use a combination of original and individual, but only the individual, makes things easier (maybe somehow good and not so good)
        individual_new_urban = numpy.zeros_like(individual)
        individual_new_urban[numpy.array(current_landuse==2) & numpy.array(individual == 1)] = 1 #only new urban pixels
        labeled_array, numpatches = f_ccl(individual_new_urban, [2,1])

        #here an if condition for the number of patches
        if numpatches > 2:

            #calculate sizes of patches
            sizes = ndimage.sum(individual_new_urban, labeled_array, range(numpatches + 1))
            sizes = sizes[sizes!=0] # remove zeros

            #instead of selecting min_size, select size according to probability
            #devide size, so that the differences between the municipalities becomes smaller

            inverse_probabilities = numpy.max(sizes/numpy.sum(sizes))  + numpy.min(sizes/numpy.sum(sizes))   - sizes/numpy.sum(sizes)
            #inverse_probabilities = inverse_probabilities * (1-inverse_probabilities)
            #inverse_probabilities = inverse_probabilities ** power
            #inverse_probabilities[inverse_probabilities>=0]=1.
            inverse_probabilities = inverse_probabilities ** power_patch_inverse_BCPM
            #inverse_probabilities=(1-(sizes/numpy.sum(sizes)))/numpy.sum(1-(sizes/numpy.sum(sizes)))

            min_size = numpy.random.choice(sizes, 1, p=inverse_probabilities/numpy.sum(inverse_probabilities)) # #or p=(1-(sizes/numpy.sum(sizes)))/numpy.sum(1-(sizes/numpy.sum(sizes)))
            mask_size = numpy.where(sizes==min_size)
            mask_size = mask_size[0] +1
            #randomly select one of these patches that are equal or smaller 2 in size

            a_index = random.choice(mask_size)

            #delete this patch in the individual_new_urban #maybe the whole thing could be done using some of the image functions, e.g. for removing noise (erosion?)
            sum_deleted = numpy.sum(labeled_array==a_index)
            individual_new_urban[labeled_array==a_index] = 0

            #print "sum_deleted: %d" %sum_deleted


            #if attach_by_prob:
            tmp_bool=False
            if random.random() < 0:
                print("here not")
                tmp_bool=True

                original_copy = numpy.copy(original)
                original_copy[individual_new_urban==1] = 1 #in der original copy ist also der patch auch geloescht

                original_copy_labeling = numpy.copy(original_copy)
                original_copy_labeling[original_copy_labeling!=1]=0
    ##            labeled_array, numpatches = f_ccl(original_copy_labeling, [2,1])

                #assign the amount of pixels (belonging to the deleted patch), assign to the largest patch? or to a random patch? to the patches of the individual_new_urban or a combination of the individual_new_urban and the original?

                #first version: to the largest patch of the individual_new_urban (makes maybe even more sense: I do not want to assign new areas to existing farms, which are often the single pixels in the original)
    ##            range_numpatches = numpy.array(range(1, numpatches+1))
    ##            range_numpatches= range_numpatches[range_numpatches != a_index]

    ##            if max_patch:
    ##                patch_number = numpy.max(range_numpatches)
    ##            else:
    ##                patch_number = random.choice(range_numpatches)

    ##            labeled_array_copy = numpy.copy(labeled_array)
    ##            labeled_array_copy[labeled_array != patch_number] = 0
    ##            bool_outer_edge=skimage.segmentation.find_boundaries(labeled_array_copy, mode="outer") #, connectivity=1, mode='thick', background=0)

                bool_agri = original_copy==2
    ##            sum_true = numpy.sum(bool_outer_edge & bool_agri)

    ##            if sum_true >= sum_deleted:
                arrays_indices = numpy.where(bool_agri)
                coords = zip(arrays_indices[0], arrays_indices[1])

                #use varying neighborhood sizes
    ###########################################################
    ##            increase_struct = random.randint(1,math.trunc(math.sqrt((min(original_copy.shape))))) #random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #maybe quantity isn't the right indicator here, maybe rather edge length
    ##            #print(increase_struct)
    ##            struct = scipy.ndimage.generate_binary_structure(2,1)
    ##            big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)
    ##            struct_mask = numpy.zeros(big_struct.shape)
    ##            struct_mask[big_struct]=1 #2
    ###########################################################
                #this does not work well, because he counts the number of neighbors, however, it should count the number of neighbors only for agricultural pixels -> a filter seems more appropriate
                struct = scipy.ndimage.generate_binary_structure(2,1)
                struct_mask = numpy.zeros(struct.shape)
                struct_mask[struct]=1 #2

                #original_copy[original_copy!=1] = 0 #2
                #neighbours = scipy.ndimage.filters.convolve(original_copy, struct_mask, mode='constant') #/4
                #neighbours = scipy.signal.convolve2d(original_copy, struct_mask, mode='same')
                neighbours = scipy.ndimage.filters.convolve(original_copy_labeling, struct_mask, mode='constant')


    ##            import arcpy
    ##            prel_pr_exp = neighbours
    ##            name_gemeinde = "Uster"
    ##            extent_raster = arcpy.Raster("D:/doktorarbeit/optimization/data_gemeinden_zuerich/" + str(name_gemeinde) + "/areal_4_09.tif")
    ##            extent = extent_raster.extent
    ##            myRaster = arcpy.NumPyArrayToRaster(prel_pr_exp, lower_left_corner = arcpy.Point(extent.XMin,extent.YMin), x_cell_size=100, y_cell_size=100, value_to_nodata=0)
    ##            myRaster.save("D:/doktorarbeit/optimization/tmp/neighbours_new.tif")

                #filter
    #########################################################################################################################
                neighbours[numpy.logical_not(bool_agri)] = 0

                #increase_struct = random.randint(1,math.trunc(math.sqrt((min(original_copy.shape))))) #random.randint(1,math.trunc(math.sqrt(quantity)/2.)) #maybe quantity isn't the right indicator here, maybe rather edge length
                ##print(increase_struct)
                #struct = scipy.ndimage.generate_binary_structure(2,1)
                #big_struct = scipy.ndimage.iterate_structure(struct, increase_struct)
                #struct_mask = numpy.zeros(big_struct.shape)
                #struct_mask[big_struct]=1 #2

                #filtered = scipy.ndimage.filters.convolve(neighbours, struct_mask, mode='constant')

    ##            import cv2
    ##            filtered = cv2.GaussianBlur(neighbours,(5,5),0)
                ##filtered = numpy.array(filters.gaussian_filter(current_landuse, sigma=1))
                ##filtered = scipy.ndimage.filters.gaussian_filter(neighbours, sigma=10)
                ##scipy.ndimage.filters.gaussian_filter(input=current_landuse, sigma=0.1)
                ##filtered = gaussian_kde(neighbours)

    ##            import arcpy
    ##            prel_pr_exp = filtered
    ##            name_gemeinde = "Uster"
    ##            extent_raster = arcpy.Raster("D:/doktorarbeit/optimization/data_gemeinden_zuerich/" + str(name_gemeinde) + "/areal_4_09.tif")
    ##            extent = extent_raster.extent
    ##            myRaster = arcpy.NumPyArrayToRaster(prel_pr_exp, lower_left_corner = arcpy.Point(extent.XMin,extent.YMin), x_cell_size=100, y_cell_size=100, value_to_nodata=0)
    ##            myRaster.save("D:/doktorarbeit/optimization/tmp/filtered.tif")

                #if random.random() < 0.5:
                #    probabilities = filtered[bool_agri]
                #else:
                probabilities = neighbours[bool_agri]


                probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
                probabilities = probabilities**power_BCPM


                #print probabilities
                #print probabilities/probabilities.sum()**power_attach_by_prob
                i = numpy.random.choice(len(coords), sum_deleted, replace=False, p=probabilities/probabilities.sum())
                #print i

                for j in i:
                    individual_new_urban[coords[j]]=1

                individual[current_landuse==2]=2
                individual[individual_new_urban==1]=1



            #elif attach_overall:
            elif tmp_bool==False:
                #print "here good"
                original_copy = numpy.copy(original)
                original_copy[individual_new_urban==1] = 1 #in der original copy ist also der patch auch geloescht

                original_copy_labeling = numpy.copy(original_copy)
                original_copy_labeling[original_copy_labeling!=1]=0
                labeled_array, numpatches = f_ccl(original_copy_labeling, [2,1])

    ##            import arcpy
    ##            prel_pr_exp = labeled_array
    ##            name_gemeinde = "Uster"
    ##            extent_raster = arcpy.Raster("D:/doktorarbeit/optimization/data_gemeinden_zuerich/" + str(name_gemeinde) + "/areal_4_09.tif")
    ##            extent = extent_raster.extent
    ##            myRaster = arcpy.NumPyArrayToRaster(prel_pr_exp, lower_left_corner = arcpy.Point(extent.XMin,extent.YMin), x_cell_size=100, y_cell_size=100, value_to_nodata=0)
    ##            myRaster.save("D:/doktorarbeit/optimization/tmp/labeled_array.tif")


                sizes = ndimage.sum(original_copy_labeling, labeled_array, range(numpatches + 1))
                sizes = sizes[sizes!=0] # remove zeros
                #assign the amount of pixels (belonging to the deleted patch), assign to the largest patch? or to a random patch? to the patches of the individual_new_urban or a combination of the individual_new_urban and the original?

                #first version: to the largest patch of the individual_new_urban (makes maybe even more sense: I do not want to assign new areas to existing farms, which are often the single pixels in the original)
                range_numpatches = numpy.array(range(1, numpatches+1))
    ##            range_numpatches= range_numpatches[range_numpatches != a_index]

                #calculate probabilities
                struct = scipy.ndimage.generate_binary_structure(2,1)
                struct_mask = numpy.zeros(struct.shape)
                struct_mask[struct]=1 #2
                neighbours = scipy.ndimage.filters.convolve(original_copy_labeling, struct_mask, mode='constant')

                bool_agri = original_copy==2
                arrays_indices = numpy.where(bool_agri)
                coords = zip(arrays_indices[0], arrays_indices[1])
                neighbours[numpy.logical_not(bool_agri)] = 0


                ###########################################################
                #if max_patch:
    ##            if random.random()<0.5:
    ##                patch_number = numpy.max(range_numpatches)
    ##            else:
    ##                patch_number = random.choice(range_numpatches)

                ###########################################################
                #select patch by probability proportional to patch size

                probabilities = sizes/numpy.sum(sizes)
                probabilities = probabilities**power_patch_BCPM

                patch_number = numpy.random.choice(range_numpatches, p=probabilities) #probabilities/numpy.sum(probabilities))

                labeled_array_copy = numpy.copy(labeled_array)
                labeled_array_copy[labeled_array != patch_number] = 0
                bool_outer_edge=skimage.segmentation.find_boundaries(labeled_array_copy, mode="outer") #, connectivity=1, mode='thick', background=0)

                sum_true = numpy.sum(bool_outer_edge & bool_agri)

                probabilities = neighbours[bool_agri & bool_outer_edge]
                probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
                probabilities = probabilities**power_BCPM


                if sum_true >= sum_deleted:
                        arrays_indices = numpy.where(bool_outer_edge & bool_agri)

                        # [KUBA][!!!]: python 2.7 to 3.4 conversion
                        # Zip returns an iterator, which means we can only use it once, later it is exhausted.
                        # But here I need to use it twice. Once for length, once to get specific element.
                        # Python 3.4 can't do that, so we need conversion to list, which is memeory consyming.
                        # Best to find alternative for later time.
                        # coords = zip(arrays_indices[0], arrays_indices[1])
                        coords = list(zip(arrays_indices[0], arrays_indices[1])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                        # [KUBA]: python 2.7 to 3.4 conversion - Nope, not here. General for zip iterator
                        # https://stackoverflow.com/questions/31011631/python-2-3-object-of-type-zip-has-no-len
                        for i in numpy.random.choice(len(coords), sum_deleted, replace=False, p=probabilities/probabilities.sum()):
                        # for i in numpy.random.choice(sum(1 for _ in coords), sum_deleted, replace=False, p=probabilities/probabilities.sum()): # Fix undone
                            individual_new_urban[coords[i]]=1 # [KUBA]: Python 2.7 to 3.4 -> Nope, fix list(cords)[i] reversed


                if sum_true < sum_deleted:

                        if sum_true > 0:
                            arrays_indices = numpy.where(bool_outer_edge & bool_agri)
                            coords = list(zip(arrays_indices[0], arrays_indices[1])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                            for i in numpy.random.choice(len(coords), sum_true, replace=False, p=probabilities/probabilities.sum()):
                                individual_new_urban[coords[i]]=1

                        #and randomly pick some new pixels according to the difference of the pixels available around the edge and the "ones" which have been deleted
                        arrays_indices = numpy.where([individual_new_urban==0] & bool_agri)
                        coords = list(zip(arrays_indices[1], arrays_indices[2])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                        #new probabilities
                        probabilities = neighbours[(individual_new_urban==0) & bool_agri]
                        probabilities = probabilities.astype(float) #only necessary if choosing scipy.ndimage.filters.convolve instead of scipy.signal.convolve2d
                        probabilities = probabilities**power_BCPM

                        for i in numpy.random.choice(len(coords), sum_deleted-sum_true, replace=False, p=probabilities/probabilities.sum()):
                            individual_new_urban[coords[i]]=1

                individual[current_landuse==2]=2
                individual[individual_new_urban==1]=1



            else:

                print("here not")
                #assign the amount of pixels (belonging to the deleted patch), assign to the largest patch? or to a random patch? to the patches of the individual_new_urban or a combination of the individual_new_urban and the original?
                #print "test"
                #first version: to the largest patch of the individual_new_urban (makes maybe even more sense: I do not want to assign new areas to existing farms, which are often the single pixels in the original)
                range_numpatches = numpy.array(range(1, numpatches+1))
                range_numpatches= range_numpatches[range_numpatches != a_index]

##                if max_patch:
##                    patch_number = numpy.max(range_numpatches)
##                else:
                patch_number = random.choice(range_numpatches)

                labeled_array_copy = numpy.copy(labeled_array)
                labeled_array_copy[labeled_array != patch_number] = 0
                bool_outer_edge=skimage.segmentation.find_boundaries(labeled_array_copy, mode="outer") #, connectivity=1, mode='thick', background=0)

                bool_agri = original==2
                sum_true = numpy.sum(bool_outer_edge & bool_agri)

                if sum_true >= sum_deleted:
                        arrays_indices = numpy.where(bool_outer_edge & bool_agri)
                        coords = list(zip(arrays_indices[0], arrays_indices[1]))  # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                        for i in numpy.random.choice(len(coords), sum_deleted, replace=False):
                            individual_new_urban[coords[i]]=1


                if sum_true < sum_deleted:

                        if sum_true > 0:
                            arrays_indices = numpy.where(bool_outer_edge & bool_agri)
                            coords = list(zip(arrays_indices[0], arrays_indices[1])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                            for i in numpy.random.choice(len(coords), sum_true, replace=False):
                                individual_new_urban[coords[i]]=1

                #and randomly pick some new pixels according to the difference of the pixels available around the edge and the "ones" which have been deleted

                        arrays_indices = numpy.where([individual_new_urban==0] & bool_agri)
                        coords = list(zip(arrays_indices[1], arrays_indices[2])) # [KUBA]: Python 2.7 to 3.4, list(zip(...)), list added

                        for i in numpy.random.choice(len(coords), sum_deleted-sum_true, replace=False):
                            individual_new_urban[coords[i]]=1

                individual[current_landuse==2]=2
                individual[individual_new_urban==1]=1
                            #print individual_new_urban

    return individual,
