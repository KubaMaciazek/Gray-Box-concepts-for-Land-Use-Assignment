import numpy as np
from deap import tools


def get_fit_gesamt(n_gen, n_pop):
    return np.zeros((n_gen // 10, n_pop, 2))


def get_hofs(n_gen):
    hof = tools.ParetoFront(similar=np.array_equal)
    hof_0 = tools.ParetoFront(similar=np.array_equal)
    fits_hof_all = [[] for _ in range(n_gen // 10)]
    return hof, hof_0, fits_hof_all


# [KUBA]: Fits like this because I optimize sq and nump (but be careful, I have to give sq a minus
#   (in the main part) because convergence metric implicitly assumes minimization.
#   If I maximize 2 objectives, then multiply both times by -1 and e.g. for compactness and sq [-700, -8500],
#   for sq and tot_edge_len [-700 ,1700]
def get_ref_point_convergence():
    return [180, 1700]


def get_convergence_metric(n_gen):
    return np.zeros(n_gen)


def initialize_metrics(n_gen, n_pop):
    """
    Returns metrics setup for tracking evolution:
        1) fit_gesamt : aggregated_fitness - lista? wartości SQ i TEL dla każdego elementu populacji w co 10 iteracji
        2) hof : hall of fame - best individuals (non-dominated pareto front), updated in each iteration.
            -> After executions stores result of optimization -> Best ever achieved individuals.
        3) hof_0 : 
        4) fits_hof_all - list of fitness's (SQ i TEL) of hof members, in each 10th iteration
            -> 10th, therefore NOT ALL iterations, because of memory problems.
        5) ref_point_convergence - reference point for Hyper Volume calculations
        6) convergence_metric - list of Hyper Volume value calculated for each iteration
    :param n_gen: nr of evolutionary algorythym iterations
    :param n_pop: population size
    :return: metrics setup
    """
    fit_gesamt = get_fit_gesamt(n_gen, n_pop)
    hof, hof_0, fits_hof_all = get_hofs(n_gen)
    ref_point_convergence = get_ref_point_convergence()
    convergence_metric = get_convergence_metric(n_gen)
    return fit_gesamt, hof, hof_0, fits_hof_all, ref_point_convergence, convergence_metric
