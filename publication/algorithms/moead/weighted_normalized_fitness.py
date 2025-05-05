import numpy as np


def weighted_normalized_fitness(individual, dv, ideal_point):
    # ToDo: 1) Retrieve fitness, 2) normalize it, 3) multiply by dv, 4) sum up, 5) return
    fitness = list(individual.fitness.values)
    # print(fitness)
    # print(ideal_point)
    normalized_fitness = [f / i for f, i in zip(fitness, ideal_point)]
    # print(normalized_fitness)

    weights = list(dv)
    # print(weights)
    weighted_fitness = [f * w for f, w in zip(normalized_fitness, weights)]
    # print(weighted_fitness)

    swf = sum(weighted_fitness)
    # print(swf)
    return swf
