import math
import time

n_pop = 100  # number of individuals / population size
# NGEN = 1000  # number of generations / iterations -> unused -> replaced with FFE
NFFE = 100000 # number of fitness function evaluations
cxpb = 0.5  # probability that two individuals cross during creating offspring in varAnd()
mutpb = 0.5 #1  # probability that individual mutates during varAnd()
#               mutpb = 1 this theoretically guarantees that the repair actually takes place
#               and that the same number of new pixels are always added
#               IMPORTANT IF CROSSOVER DOES NOT FIX OUTCOME SAMPLE ITSELF -> not actual -> repair added

w1 = -1  # sq objective function weight
w2 = -1  # tot_edge_len objective function weight
#           -1 for minimalization of both with equall importance

seeds20 = [1939165643, 1595794013, 3133665394, 3181000657, 2194989013, 3238441240, 3534643812, 2220046226, 673201361, 451147359, 2869651061, 1567599280, 2396077065, 3766233533, 3634474126, 2033958569, 2097258941, 867154026, 2331360844, 2490353467]

sample_municipalities = ["Hedingen", "Uster", "four_muni_FPUV"]
list_initializations = ["spg", "tel_bpg_strict", "tel_bgp_wide", "tel_bpg_p10", "tel_bpg_p25", "sq_bpg",
                        "bpg_sq_tel_pp", "sq_bpg_50x50_tel_bgp_strict_pr", "sq_bpg_50x50_tel_bgp_strict_ir"]
list_mutations = ["rbm_rcm_brm_bcpm_wri", "rbm_rcm_brm_bcpm_nrii"] # ["rbm_rcm_brm_bcpm"]
list_crossovers = ["ac", "spc", "ppc", "ppc_fuo"]
list_repairs = ["rrm", "brm"]


def get_general_tests_config():
    nr_of_tests, test_nr, starting_time, test_stamp = technical_configuration()
    return (n_pop, NFFE, cxpb, mutpb,
            w1, w2,
            seeds20,
            sample_municipalities,
            list_initializations, list_mutations, list_crossovers, list_repairs,
            nr_of_tests, test_nr, starting_time, test_stamp)


def technical_configuration():
    nr_of_tests = (len(seeds20) * len(sample_municipalities) * len(list_initializations) * len(list_mutations) *
                   len(list_crossovers) * len(list_repairs))
    test_nr = 0
    starting_time = time.time()
    test_stamp = str(math.trunc(starting_time))
    return nr_of_tests, test_nr, starting_time, test_stamp


def get_nsgaii_tunning_config():
    algorithm = "nsgaii"
    seeds5 = seeds20[:5]
    n_pop = 100
    cxpb = 0.5 #0.9
    mutpb = 0.5 #0.1
    list_initializations = ["sq_bpg", "sq_bpg_50x50_tel_bgp_strict_pr"]
    list_mutations = ["rbm_rcm_brm_bcpm_wri", "rbm_rcm_brm_bcpm_nrii"]
    list_crossovers = ["ppc", "ppc_fuo"]
    list_repairs = ["rrm", "brm"]

    _, test_nr, starting_time, test_stamp = technical_configuration()
    nr_of_tests = (len(seeds5) * len([sample_municipalities[1]]) * len(list_initializations) * len(list_mutations) *
                   len(list_crossovers) * len(list_repairs))
    return (algorithm,
            n_pop, NFFE, cxpb, mutpb,
            w1, w2,
            seeds5,
            [sample_municipalities[1]],
            list_initializations, list_mutations, list_crossovers, list_repairs,
            nr_of_tests, test_nr, starting_time, test_stamp)


def get_moead_tunning_config():
    algorithm = "moead"
    seeds5 = seeds20[:5]
    n_pop = 100
    cxpb = 0.5 #0.9
    mutpb = 0.5 #0.1
    list_initializations = ["sq_bpg", "sq_bpg_50x50_tel_bgp_strict_pr"]
    list_mutations = ["rbm_rcm_brm_bcpm_wri", "rbm_rcm_brm_bcpm_nrii"]
    list_crossovers = ["ppc", "ppc_fuo"]
    list_repairs = ["rrm", "brm"]

    _, test_nr, starting_time, test_stamp = technical_configuration()
    nr_of_tests = (len(seeds5) * len([sample_municipalities[1]]) * len(list_initializations) * len(list_mutations) *
                   len(list_crossovers) * len(list_repairs))
    return (algorithm,
            n_pop, NFFE, cxpb, mutpb,
            w1, w2,
            seeds5,
            [sample_municipalities[1]],
            list_initializations, list_mutations, list_crossovers, list_repairs,
            nr_of_tests, test_nr, starting_time, test_stamp)

def get_general_tests_config_for_baseline_tests():
    algorithm = ["nsgaii", "moead"]
    cxpb = 0.5
    mutpb = 1.0
    list_initializations = ["spg"]
    list_mutations = ["rbm_rcm_brm_bcpm_wri"]
    list_crossovers = ["ac"]
    list_repairs = ["rrm", "brm"] # shouldn't matter

    _, test_nr, starting_time, test_stamp = technical_configuration()
    nr_of_tests = (len(algorithm) * len(seeds20) * len(sample_municipalities) * len(list_initializations) * len(list_mutations) *
                   len(list_crossovers) * len(list_repairs))
    return (algorithm,
            n_pop, NFFE, cxpb, mutpb,
            w1, w2,
            seeds20,
            sample_municipalities,
            list_initializations, list_mutations, list_crossovers, list_repairs,
            nr_of_tests, test_nr, starting_time, test_stamp)


def get_final_tests_config():
    # BEST ONES
    # combDef = ["alg", "init", "mut", "cross", "repair", "n_pop", "cxpb", "mutpb"]

    moead1st = ["moead", "sq_bpg", "rbm_rcm_brm_bcpm_nrii", "ppc", "rrm", 100, 0.5, 0.5]
    moead2nd = ["moead", "tel_bpg_strict", "rbm_rcm_brm_bcpm_nrii", "ppc", "rrm", 100, 0.5, 0.5]
    moead3rd = ["moead", "sq_bpg", "rbm_rcm_brm_bcpm_nrii", "ppc", "rrm", 110, 0.5,
                0.6]  # moead;sq_bpg;rbm_rcm_brm_bcpm_nrii;ppc;rrm;110;0.5;0.6

    moead6thExtra = ["moead", "bpg_sq_tel_pp", "rbm_rcm_brm_bcpm_wri", "ppc", "rrm", 100, 0.5, 0.5]

    # nsgaii|sq_bpg_50x50_tel_bgp_strict_pr|rbm_rcm_brm_bcpm_wri|ppc_fuo|brm
    # nsgaii;sq_bpg_50x50_tel_bgp_strict_pr;rbm_rcm_brm_bcpm_wri;ppc_fuo;brm;340;1.0;0.1
    nsgaii1st = ["nsgaii", "sq_bpg_50x50_tel_bgp_strict_pr", "rbm_rcm_brm_bcpm_wri", "ppc_fuo", "brm", 340, 1.0, 0.1]

    # nsgaii|sq_bpg_50x50_tel_bgp_strict_pr|rbm_rcm_brm_bcpm_nrii|ppc|brm
    # nsgaii;sq_bpg_50x50_tel_bgp_strict_pr;rbm_rcm_brm_bcpm_nrii;ppc;brm;300;1.0;0.1
    nsgaii2nd = ["nsgaii", "sq_bpg_50x50_tel_bgp_strict_pr", "rbm_rcm_brm_bcpm_nrii", "ppc", "brm", 300, 1.0, 0.1]

    # nsgaii|sq_bpg_50x50_tel_bgp_strict_pr|rbm_rcm_brm_bcpm_nrii|ppc|rrm
    nsgaii3rd = ["nsgaii", "sq_bpg_50x50_tel_bgp_strict_pr", "rbm_rcm_brm_bcpm_nrii", "ppc", "rrm", 100, 0.5, 0.5]

    # nsgaii|sq_bpg|rbm_rcm_brm_bcpm_nrii|ppc|rrm
    # nsgaii;sq_bpg;rbm_rcm_brm_bcpm_nrii;ppc;rrm;120;0.9;0.5
    nsgaii7thExtra = ["nsgaii", "sq_bpg", "rbm_rcm_brm_bcpm_nrii", "ppc", "rrm", 120, 0.9, 0.5]

    # BASELINE
    moeadBaseline = ["moead", "spg", "rbm_rcm_brm_bcpm_wri", "ac", "rrm", 100, 0.5, 1.0]
    nsgaiiBaseline = ["nsgaii", "spg", "rbm_rcm_brm_bcpm_wri", "ac", "rrm", 100, 0.5, 1.0]

    # bestCombinationsAndBaseline = [moead1st, moead2nd, moead3rd, nsgaii1st, nsgaii2nd, nsgaii3rd, moeadBaseline,
    #                                nsgaiiBaseline]
    bestCombinationsAndBaseline = [moead1st, moead2nd, moead3rd, moead6thExtra, nsgaii1st, nsgaii2nd, nsgaii3rd, nsgaii7thExtra, moeadBaseline, nsgaiiBaseline]

    # ###########
    # All municipaliteis + remaining:
    remamining_sample_municipalities = ["Dübendorf", "Meilen", "Volketswil", "Bassersdorf", "Oberglatt", "Pfäffikon", "Bülach", "Nürensdorf", "Fehraltorf", "Rümlang", "Wetzikon (ZH)", "Hedingen", "Uster", "four_muni_FPUV"]

    _, test_nr, starting_time, test_stamp = technical_configuration()
    nr_of_tests = (len(bestCombinationsAndBaseline) * len(seeds20) * len(remamining_sample_municipalities))

    return (bestCombinationsAndBaseline,
            NFFE,
            w1, w2,
            seeds20,
            remamining_sample_municipalities,
            nr_of_tests, test_nr, starting_time, test_stamp)
