import warnings

from deap import creator

from publication.operators.inicialization.bpg_sq_tel_individual_ratio import sq_bpg_50x50_tel_bgp_strict_ir
from publication.operators.inicialization.bpg_sq_tel_population_ratio import sq_bpg_50x50_tel_bgp_strict_pr
from publication.operators.inicialization.bpg_sq_tel_probability_product import bpg_sq_tel_pp
from publication.operators.inicialization.population_guess import spg
from publication.operators.inicialization.sq_bpg import sq_bpg
from publication.operators.inicialization.tel_bpg import tel_bgp_wide, tel_bpg_strict, tel_bpg_p10, tel_bpg_p25

def register_initialization(initialization_name, toolbox, filename_areal, filename_sq, int_quantity, n_pop):
    if initialization_name == "spg":
        register_initialization_spg(toolbox, filename_areal, int_quantity, n_pop)

    elif initialization_name == "tel_bpg_strict":
        register_initialization_tel_bpg_strict(toolbox, filename_areal, int_quantity, n_pop)

    elif initialization_name == "tel_bgp_wide":
        register_initialization_tel_bgp_wide(toolbox, filename_areal, int_quantity, n_pop)

    elif initialization_name == "tel_bpg_p10":
        register_initialization_tel_bpg_p10(toolbox, filename_areal, int_quantity, n_pop)

    elif initialization_name == "tel_bpg_p25":
        register_initialization_tel_bpg_p25(toolbox, filename_areal, int_quantity, n_pop)

    elif initialization_name == "sq_bpg":
        register_initialization_sq_bpg(toolbox, filename_areal, filename_sq, int_quantity, n_pop)

    elif initialization_name == "bpg_sq_tel_pp":
        register_initialization_bpg_sq_tel_pp(toolbox, filename_areal, filename_sq, int_quantity, n_pop)

    elif initialization_name == "sq_bpg_50x50_tel_bgp_strict_pr":
        register_sq_bpg_50x50_tel_bgp_strict_pr(toolbox, filename_areal, filename_sq, int_quantity, n_pop)

    elif initialization_name == "sq_bpg_50x50_tel_bgp_strict_ir":
        register_sq_bpg_50x50_tel_bgp_strict_ir(toolbox, filename_areal, filename_sq, int_quantity, n_pop)

    else:
        warnings.warn("Unknown initialization: None registered")


def register_initialization_spg(toolbox, filename_areal, int_quantity, n_pop):
    toolbox.register("population_guess", spg, list, creator.Individual, filename_areal, int_quantity, n_pop)


def register_initialization_tel_bpg_strict(toolbox, filename_areal, int_quantity, n_pop):
    toolbox.register("population_guess", tel_bpg_strict, list, creator.Individual, filename_areal, int_quantity, n_pop)


def register_initialization_tel_bgp_wide(toolbox, filename_areal, int_quantity, n_pop):
    toolbox.register("population_guess", tel_bgp_wide, list, creator.Individual, filename_areal, int_quantity, n_pop)


def register_initialization_tel_bpg_p10(toolbox, filename_areal, int_quantity, n_pop):
    toolbox.register("population_guess", tel_bpg_p10, list, creator.Individual, filename_areal, int_quantity, n_pop)


def register_initialization_tel_bpg_p25(toolbox, filename_areal, int_quantity, n_pop):
    toolbox.register("population_guess", tel_bpg_p25, list, creator.Individual, filename_areal, int_quantity, n_pop)


def register_initialization_sq_bpg(toolbox, filename_areal, filename_sq, int_quantity, n_pop):
    toolbox.register("population_guess", sq_bpg, list, creator.Individual, filename_areal, filename_sq, int_quantity, n_pop)


def register_initialization_bpg_sq_tel_pp(toolbox, filename_areal, filename_sq, int_quantity, n_pop):
    toolbox.register("population_guess", bpg_sq_tel_pp, list, creator.Individual, filename_areal, filename_sq, int_quantity, n_pop)


def register_sq_bpg_50x50_tel_bgp_strict_pr(toolbox, filename_areal, filename_sq, int_quantity, n_pop):
    toolbox.register("population_guess", sq_bpg_50x50_tel_bgp_strict_pr, list, creator.Individual, filename_areal,
                     filename_sq, int_quantity, n_pop)


def register_sq_bpg_50x50_tel_bgp_strict_ir(toolbox, filename_areal, filename_sq, int_quantity, n_pop):
    toolbox.register("population_guess", sq_bpg_50x50_tel_bgp_strict_ir, list, creator.Individual, filename_areal,
                     filename_sq, int_quantity, n_pop)
