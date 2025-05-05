import warnings

import numpy as np

from publication.operators.mutations.rbm_rcm_brm_bcpm import RBM_RCM_BRM_BCPM, RBM_RCM_BRM_BCPM_NRII, \
    RBM_RCM_BRM_BCPM_WRI


def register_mutation(mutation_name, toolbox, int_quantity, areal):
    if mutation_name == "rbm_rcm_brm_bcpm":
        register_mutation_rbm_rcm_brm_bcpm(toolbox, int_quantity, areal)
    elif mutation_name == "rbm_rcm_brm_bcpm_wri":
        register_mutation_rbm_rcm_brm_bcpm_wri(toolbox, int_quantity, areal)
    elif mutation_name == "rbm_rcm_brm_bcpm_nrii":
        register_mutation_rbm_rcm_brm_bcpm_nrii(toolbox, int_quantity, areal)
    else:
        warnings.warn("Unknown mutation: None registered")


"""
rbm_rcm_brm_bcpm
"""

indpb = 0.1
indpb_clustering = 0.1  # 0.2 0.1
indpb_patch = 0.1
power_BCPM = 1  # 1
power_patch_BCPM = 1  # 1
power_patch_inverse_BCPM = 1  # 1
power_BRM = 1  # 1 #value between 0 and 1 (decrease differences), value > 1 (increase differences), 0 means uniform probabilities
power_inverse_BRM = 1  # 1


def register_mutation_rbm_rcm_brm_bcpm(toolbox, int_quantity, areal):
    count_max = round(1. / float(int_quantity) * float(int_quantity))

    toolbox.register("mutate", RBM_RCM_BRM_BCPM,
                     current_landuse=np.copy(areal),
                     quantity=float(int_quantity),
                     indpb=indpb,
                     indpb_clustering=indpb_clustering,
                     indpb_patch=indpb_patch,
                     count_max=count_max,
                     power_BCPM=power_BCPM,
                     power_patch_BCPM=power_patch_BCPM,
                     power_patch_inverse_BCPM=power_patch_inverse_BCPM,
                     power_BRM=power_BRM,
                     power_inverse_BRM=power_inverse_BRM)


def register_mutation_rbm_rcm_brm_bcpm_wri(toolbox, int_quantity, areal):
    count_max = round(1. / float(int_quantity) * float(int_quantity))

    toolbox.register("mutate", RBM_RCM_BRM_BCPM_WRI,
                     current_landuse=np.copy(areal),
                     quantity=float(int_quantity),
                     indpb=indpb,
                     indpb_clustering=indpb_clustering,
                     indpb_patch=indpb_patch,
                     count_max=count_max,
                     power_BCPM=power_BCPM,
                     power_patch_BCPM=power_patch_BCPM,
                     power_patch_inverse_BCPM=power_patch_inverse_BCPM,
                     power_BRM=power_BRM,
                     power_inverse_BRM=power_inverse_BRM)


def register_mutation_rbm_rcm_brm_bcpm_nrii(toolbox, int_quantity, areal):
    count_max = round(1. / float(int_quantity) * float(int_quantity))

    toolbox.register("mutate", RBM_RCM_BRM_BCPM_NRII,
                     current_landuse=np.copy(areal),
                     quantity=float(int_quantity),
                     indpb=indpb,
                     indpb_clustering=indpb_clustering,
                     indpb_patch=indpb_patch,
                     count_max=count_max,
                     power_BCPM=power_BCPM,
                     power_patch_BCPM=power_patch_BCPM,
                     power_patch_inverse_BCPM=power_patch_inverse_BCPM,
                     power_BRM=power_BRM,
                     power_inverse_BRM=power_inverse_BRM)
