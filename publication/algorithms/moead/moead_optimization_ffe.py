import itertools
import random


import numpy as np
from deap.tools._hypervolume import pyhv as hv


def moead_optimization_ffe(population, nffe, n_pop, toolbox, cxpb, mutpb, hof, ref_point_convergence, t_neighbours):
    """
        EP == hof
        FV[i] == population[i].fitness.value
    """
    fits_hof_all = []
    hvs = []
    ffe_condition = False
    curr_nr_of_evals = 0

    # [SETUP]
    # 0.0) Create list of decomposition vectors ds
    ds = get_decomposition_vectors(n_pop)
    # 0.1) Create neighbourhoods
    neighbourhood = get_neighbourhoods(n_pop, t_neighbours)
    # 0.2) Compute FV fitnesses regarding individual vector
    decomposed_fitnesses = get_decomposed_fitnesses(population, ds, toolbox)
    # 0.3) Create z, where z[i] is best FV found so far for decomposition vector dv[i]

    for gen in itertools.count():

        # New Y's
        new_ys = []

        # For each decomposition vector in random order
        for n in np.random.permutation(n_pop):
            # 0) Check for end condition
            if curr_nr_of_evals >= nffe:
                ffe_condition = True
                break

            # [1) REPRODUCTION]
            y, evals = reproduce(population, neighbourhood[n], ds[n], toolbox, cxpb, mutpb)
            curr_nr_of_evals += evals

            # [2) Z_UPDATE]
            # Not necessary for this implementation

            # [3) NEIGHBOURHOOD UPDATE]
            update_neighbourhood(population, ds, neighbourhood[n], y, toolbox, decomposed_fitnesses)

            # [4) UPDATE HOF]
            # hof.update(population + [y])
            new_ys.append(y)

        hof.update(new_ys)
        if ffe_condition:
            break

    # 5) Save data of final iteration
    print("Save data")
    fits_hof_all.append(list(toolbox.map(toolbox.evaluate, hof)))

    convergence_hof = toolbox.map(toolbox.evaluate, hof)
    convergence_hof = set(convergence_hof)
    convergence_hof_array = np.array(list(convergence_hof))
    hyper_volume = hv.hypervolume(pointset=convergence_hof_array, ref=ref_point_convergence)
    hvs.append(hyper_volume)

    return hvs, fits_hof_all


def get_neighbourhoods(n_pop, t_neighbours):
    neighbourhood = np.zeros(n_pop)
    neighbourhood = np.array(neighbourhood, dtype=list)
    t_half = t_neighbours // 2

    for i in range(n_pop):
        if i - t_half < 0:
            neighbourhood[i] = range(0, t_neighbours)
        elif i + t_half >= n_pop:
            neighbourhood[i] = range(n_pop-t_neighbours, n_pop)
        else:
            neighbourhood[i] = range(i-t_half, i+t_half+1)

    return neighbourhood


def get_decomposition_vectors(n_pop):
    # step = 100//n_pop
    # xs = list(range(step/2, n_pop-(step/2), step))
    # xs = list(range(step, 101, step))
    # xs = [s - step/2 for s in xs]
    #
    step = 1 / n_pop
    xs = np.arange(step/2, 1, step)
    ys = [1-x for x in xs]
    return list(zip(xs, ys))


def get_decomposed_fitnesses(population, ds, toolbox):
    fitnesses = np.zeros(len(population))

    for ind in range(len(population)):
        fitnesses[ind] = toolbox.evaluate_fv(population[ind], ds[ind])

    return fitnesses


def reproduce(population, neighbourhood_n, ds_n, toolbox, cxpb, mutpb):
    do_cx = random.random() <= cxpb
    do_mut = random.random() <= mutpb
    evaluations = 0

    # 1) Choose randomly 2 subjects from neighbourhood
    kl = random.sample(neighbourhood_n, 2)
    k = toolbox.clone(population[kl[0]])
    l = toolbox.clone(population[kl[1]])

    # 2) Cross them
    if do_cx:
        k, l = toolbox.mate(k, l)
        del k.fitness.values, l.fitness.values
        # del k.fit_fv, l.fit_fv
    y = random.choice([k, l])

    # 3) Mutate
    if do_mut:
        y, = toolbox.mutate(y)
        del y.fitness.values
        # del y.fit_fv

    # 4) Repair
    y = toolbox.repair(y)

    # 5) Evaluate
    if do_cx or do_mut:
        evaluations = 1
        fit = toolbox.evaluate(y)
        y.fitness.values = fit

        # fit_fv = toolbox.evaluate_fv(y, ds_n)
        # y.fit_fv = fit_fv

    return y, evaluations


def update_neighbourhood(population, ds, neighbourhood_n, y, toolbox, decomposed_fitnesses):
    # For each member of neighbourhood, compare whether y not better
    for n_index in neighbourhood_n:
        fit_fv = toolbox.evaluate_fv(y, ds[n_index])
        if fit_fv <= decomposed_fitnesses[n_index]:
            population[n_index] = toolbox.clone(y)
            decomposed_fitnesses[n_index] = fit_fv

# test

# print(get_neighbourhoods(20, 5))
# print(get_decomposition_vectors(20))
