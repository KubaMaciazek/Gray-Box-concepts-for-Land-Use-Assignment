import itertools

import numpy as np
from deap import algorithms
from deap.tools._hypervolume import pyhv as hv

from publication.common.select_elements_with_probability import select_elements_with_probability


def nsgaii_optimization_ffe(population, nffe, n_pop, toolbox, cxpb, mutpb, hof, ref_point_convergence):
    fits_hof_all = []
    hvs = []
    ffe_condition = False
    curr_nr_of_evals = 0

    for gen in itertools.count():
        # # Log evaluations
        # if divmod(gen, 100)[1] == 0: print(str((float(curr_nr_of_evals) / nffe) * 100) + "% of evaluations")

        # 1) Deep copy population
        population_copy = [toolbox.clone(ind) for ind in population]

        # [CROSSOVER]
        # 2) Select individuals for crossover
        selected_for_cross, discarded_from_cross = select_elements_with_probability(population_copy, cxpb)
        # 3) Apply crossover on selected
        # selected_for_cross = algorithms.varAnd(selected_for_cross, toolbox, cxpb=1, mutpb=0)
        for i in range(1, len(selected_for_cross), 2):
            selected_for_cross[i - 1], selected_for_cross[i] = toolbox.mate(selected_for_cross[i - 1], selected_for_cross[i])
            del selected_for_cross[i - 1].fitness.values, selected_for_cross[i].fitness.values

        # [MUTATION]
        # 4) Select individuals for mutation
        crossed_selected_for_mutation, crossed_discarded_from_mutation = select_elements_with_probability(selected_for_cross, mutpb)
        not_crossed_selected_for_mutation, discarded_from_either = select_elements_with_probability(discarded_from_cross, mutpb)
        selected_for_mutation = crossed_selected_for_mutation + not_crossed_selected_for_mutation
        # 5) Apply mutation
        for i in range(len(selected_for_mutation)):
            selected_for_mutation[i], = toolbox.mutate(selected_for_mutation[i])
            del selected_for_mutation[i].fitness.values

        offspring = crossed_discarded_from_mutation + selected_for_mutation

        # [REPAIR]
        # 6) Apply repair mechanism to all manipulated individuals
        # ToDo: Implenet repair mechanism registration
        offspring = list(map(toolbox.repair, offspring))

        # [EVALUATE]
        # 7) Evaluate offspring and assign its fitnesses
        fits = list(toolbox.map(toolbox.evaluate, offspring))
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit

        # [FFE CHECK]
        # 8) Check for end condition
        curr_nr_of_evals += len(offspring)
        if curr_nr_of_evals >= nffe:
            # 8.a.1) Set loop breaker
            ffe_condition = True
            # 8.a.2) Discard offspring over ffe limit
            # ToDo: check if works with 0
            offspring = offspring[:-(curr_nr_of_evals - nffe)]

        # [SELECTION]
        # 9) Apply NSGA-II selection
        population = toolbox.select(offspring + population, k=n_pop)
        hof.update(population)

        # # [DATA GATHERING]
        # # 10) Save data in each 100th generation
        # if divmod(gen, 100)[1] == 0:
        #     fits_hof_all.append(list(toolbox.map(toolbox.evaluate, hof)))
        #
        #     convergence_hof = toolbox.map(toolbox.evaluate, hof)
        #     convergence_hof = set(convergence_hof)
        #     convergence_hof_array = np.array(list(convergence_hof))
        #     hyper_volume = hv.hypervolume(pointset=convergence_hof_array, ref=ref_point_convergence)
        #     hvs.append(hyper_volume)

        # [END]
        # 11) Brake if final condition met
        if ffe_condition:
            # 11.1) Save data of final iteration
            fits_hof_all.append(list(toolbox.map(toolbox.evaluate, hof)))

            convergence_hof = toolbox.map(toolbox.evaluate, hof)
            convergence_hof = set(convergence_hof)
            convergence_hof_array = np.array(list(convergence_hof))
            hyper_volume = hv.hypervolume(pointset=convergence_hof_array, ref=ref_point_convergence)
            hvs.append(hyper_volume)

            break

    return hvs, fits_hof_all
