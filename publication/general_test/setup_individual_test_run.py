import random
import time

import numpy as np

from publication.general_test.log_test_execution_progress import log_test_execution_progress
from publication.general_test.metrics import initialize_metrics


def setup_individual_test_run(seed, test_nr, starting_time, nr_of_tests, toolbox, NFFE, n_pop, thread_nr):
    random.seed(seed)
    np.random.seed(seed)

    test_nr = log_test_execution_progress(test_nr, starting_time, nr_of_tests, thread_nr)

    start_time = time.time()

    population = get_initial_population(toolbox)

    _, hof, _, _, _, _ = initialize_metrics(NFFE, n_pop)

    return test_nr, start_time, population, hof


# 1) get n indyviduals based on toolbox function
# 2) evaluate them by getting their fitnesses and assigning them to them.
def get_initial_population(toolbox):
    population = toolbox.population_guess()

    fits = toolbox.map(toolbox.evaluate, population)

    for fit, ind in zip(fits, population):
        ind.fitness.values = fit

    return population