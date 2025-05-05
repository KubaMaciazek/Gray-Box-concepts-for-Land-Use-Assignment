# def nsgaii_execution_nostats(population, ngen, n_pop, toolbox, cxpb, mutpb, hof, ref_point_convergence):
import numpy as np
from deap import algorithms
from deap.tools._hypervolume import pyhv as hv  # hv nawet w dokumentacji oznaczony że nie działa...?


def nsgaii_optimization(population, ngen, n_pop, toolbox, cxpb, mutpb, hof, ref_point_convergence):
    fits_hof_all = []
    hvs = []

    # start_time = time.time()

    # check = True

    for gen in range(ngen):
        # print("pop_size:" + str(len(population)) + ";" + "hof_size: " + str(len(hof)))
        if divmod(gen, 100)[1] == 0: print(str((float(gen) / ngen) * 100) + "% of generation")

        # [CROSSOVER][MUTATION]
        # https://deap.readthedocs.io/en/master/api/algo.html#deap.algorithms.varAnd
        # : apply (or not -> probability) crossover and mutation, return independent offspring
        offspring = algorithms.varAnd(population, toolbox, cxpb=cxpb, mutpb=mutpb)

        # [EVALUATION]
        fits = list(toolbox.map(toolbox.evaluate, offspring))
        # [KUBA]: #population and offspring are lists that contain the objects Individual, so population[1] is an Individual, with ind I can iterate over it and assign new fitness values
        for fit, ind in zip(fits,
                            offspring):  # population und offspring sind Listen, die die Objekte Individual, also population[1] ist ein Individual, mit ind kann ich darueber iterieren und neue fitness values zuordnen
            ind.fitness.values = fit
            # if divmod(gen, 10)[1] == 0:  # due to memory errors only every 10
            #     fit_gesamt[gen // 10] = fits  # [KUBA]: inteeger division

        # [SELECTION]
        # https://deap.readthedocs.io/en/master/api/tools.html#selection
        # Apply NSGA-II selection operator on the individuals. k – The number of individuals to select.
        population = toolbox.select(offspring + population, k=n_pop)
        hof.update(population)

        if divmod(gen+1, 100)[1] == 0:  # due to memory errors only every 10
            # print(gen)
            fits_hof_all.append(list(toolbox.map(toolbox.evaluate, hof)))

            convergence_hof = toolbox.map(toolbox.evaluate, hof)
            convergence_hof = set(convergence_hof)
            convergence_hof_array = np.array(list(convergence_hof))
            hyper_volume = hv.hypervolume(pointset=convergence_hof_array, ref=ref_point_convergence)  # old version
            hvs.append(hyper_volume)


        # # [LOGBOOK]
        # record = stats.compile(hof)
        # logbook.record(gen=gen, **record)   # record given statistics for HOF for each iteration

        # # [HYPER-VOLUME / CONVERGENCE CALCULATIONS]
        # # [KUBA]: #hv_hypervolume has problems if there are 2 points in the pareto front that have exactly the same fitness, what can happen see support.py for the update function, if the same fitness occurs twice but different landscapes, solution: the hypervolume function a " "adjusted Pareto Front".
        # # hv_hypervolume hat Probleme, wenn 2 Punkte in der pareto front sind, die exakt diesselbe fitness haben, was passieren kann siehe support.py fuer die update funktion, wennn 2 mal diesselbe fitness, aber unterschiedliche Landscaften vorkommen, Loesung: der hypervolume funktion eine "bereinigte Pareto Front" uebergeben
        # if (w1 != 0 and w2 != 0):
        #     convergence_hof = toolbox.map(toolbox.evaluate, hof)
        #     convergence_hof = set(convergence_hof)
        #     convergence_hof_array = np.array(list(convergence_hof))
        #     # convergence_hof_array[:,0] = convergence_hof_array[:,0]*-1
        #     convergence_metric[gen] = hv.hypervolume(pointset=convergence_hof_array,
        #                                              ref=ref_point_convergence)  # old version
        # ##            convergence_hof_array = np.array(list(convergence_hof))
        # ##            convergence_hof_array[:,0] = convergence_hof_array[:,0]*-1
        # ##            convergence_hof_array[:,1] = convergence_hof_array[:,1]
        # ##            convergence_metric[gen] = hyperVolume.compute(convergence_hof)
        #
        # # [KUBA]: takes about 14 minutes with 100,000 generations and 2 static objectives (e.g. lp and gr).
        # # convergence_metric[gen] = convergence_euclidean_dist(hof_0, hof)
        # # hof_0.update(population)

        # check = False

    # elapsed_time = time.time() - start_time
    # print('elapsed_time: ' + str(elapsed_time) + '\'s')  # 10 generations approximately 133 seconds
    # # type(population)
    #
    # # [PRINT-STATISTICS]
    # print_execution_statistics(fit_gesamt, hof, fits_hof_all, population, toolbox, convergence_metric)
    #
    # # [LOGBOOK]
    # manage_logbook(logbook) # Ekhm, można coś ambitniejszego być może...
    #
    # # the logbook variable makes everything extremely slow (occupying a lot of memory) -> delete if unnecessary
    # logbook.clear()
    # # logbook = []

    # print("pop_size:" + str(len(population)) + ";" + "hof_size: " + str(len(hof)))
    # final_fits = list(toolbox.map(toolbox.evaluate, hof))
    # fits_hof_all.append([])
    # fits_hof_all[len(fits_hof_all) - 1].append(final_fits)
    # sq_meds, tel_meds = zip(*logbook.select("median"))
    # sq_min, tel_min = zip(*logbook.select("min"))

    return hvs, fits_hof_all     #, np.copy(hof)
