# ############################################################################################ ###########################################################################################
# RBM_RCM_BRM_BCPM ~ SCHWAAB
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

from publication.operators.mutations.bcpm import BCPM_without_repair
from publication.operators.mutations.brm import BRM
from publication.operators.mutations.rbm import RBM_without_repair, RBM_without_repair_TRURLY
from publication.operators.mutations.rcm import RCM_without_repair


def RBM_RCM_BRM_BCPM(
        individual,                     # ? indyvidual binary matrix, with ones representing cells to be converted to urban
        current_landuse,                # ? areal matrix = map of land uses
        quantity,                       # ?
        indpb_clustering,               # ?
        indpb,                          # ?
        indpb_patch,                    # ?
        count_max,                      # ?
        power_BRM,                      # ?
        power_inverse_BRM,              # ?
        power_BCPM,                     # ?
        power_patch_BCPM,               # ?
        power_patch_inverse_BCPM        # ?
):

    # [KUBA]: IT ACTUALLY IS WITH REPAIR
    individual = RBM_without_repair(individual=individual, current_landuse=current_landuse,quantity=quantity,  indpb_clustering=indpb_clustering)[0]

    individual = RCM_without_repair(individual=individual,current_landuse=current_landuse,quantity=quantity,   count_max=count_max, indpb=indpb)[0]

    # individual = BRM(individual=individual,current_landuse=current_landuse,quantity=quantity, power_BRM=power_BRM, power_inverse_BRM=power_inverse_BRM)[0] # or do the repair and then do the single pixel mutation?
    individual = BRM(individual=individual, current_landuse=current_landuse, quantity=quantity, power_BRM=power_BRM,
                     power_inverse_BRM=power_inverse_BRM)  # or do the repair and then do the single pixel mutation?

    individual = BCPM_without_repair(individual=individual,current_landuse=current_landuse,quantity=quantity, indpb_patch=indpb_patch, power_BRM=power_BRM, power_inverse_BRM=power_inverse_BRM, power_BCPM=power_BCPM, power_patch_BCPM=power_patch_BCPM, power_patch_inverse_BCPM=power_patch_inverse_BCPM)[0]

    return individual,


def RBM_RCM_BRM_BCPM_WRI(
        individual,                     # ? indyvidual binary matrix, with ones representing cells to be converted to urban
        current_landuse,                # ? areal matrix = map of land uses
        quantity,                       # ?
        indpb_clustering,               # ?
        indpb,                          # ?
        indpb_patch,                    # ?
        count_max,                      # ?
        power_BRM,                      # ?
        power_inverse_BRM,              # ?
        power_BCPM,                     # ?
        power_patch_BCPM,               # ?
        power_patch_inverse_BCPM        # ?
):

    # [KUBA]: THERE ACTUALLY IS A REPAIR
    individual = RBM_without_repair(individual=individual, current_landuse=current_landuse,quantity=quantity,  indpb_clustering=indpb_clustering)[0]

    individual = RCM_without_repair(individual=individual,current_landuse=current_landuse,quantity=quantity,   count_max=count_max, indpb=indpb)[0]

    # individual = BRM(individual=individual,current_landuse=current_landuse,quantity=quantity, power_BRM=power_BRM, power_inverse_BRM=power_inverse_BRM)[0] # or do the repair and then do the single pixel mutation?
    individual = BRM(individual=individual, current_landuse=current_landuse, quantity=quantity, power_BRM=power_BRM,
                     power_inverse_BRM=power_inverse_BRM)  # or do the repair and then do the single pixel mutation?

    individual = BCPM_without_repair(individual=individual,current_landuse=current_landuse,quantity=quantity, indpb_patch=indpb_patch, power_BRM=power_BRM, power_inverse_BRM=power_inverse_BRM, power_BCPM=power_BCPM, power_patch_BCPM=power_patch_BCPM, power_patch_inverse_BCPM=power_patch_inverse_BCPM)[0]

    return individual,


def RBM_RCM_BRM_BCPM_NRII(
        individual,                     # ? indyvidual binary matrix, with ones representing cells to be converted to urban
        current_landuse,                # ? areal matrix = map of land uses
        quantity,                       # ?
        indpb_clustering,               # ?
        indpb,                          # ?
        indpb_patch,                    # ?
        count_max,                      # ?
        power_BRM,                      # ?
        power_inverse_BRM,              # ?
        power_BCPM,                     # ?
        power_patch_BCPM,               # ?
        power_patch_inverse_BCPM        # ?
):

    # [KUBA]: THERE TRURLY IN NO REPAIR
    individual = RBM_without_repair_TRURLY(individual=individual, current_landuse=current_landuse,quantity=quantity,  indpb_clustering=indpb_clustering)[0]

    individual = RCM_without_repair(individual=individual,current_landuse=current_landuse,quantity=quantity,   count_max=count_max, indpb=indpb)[0]

    # individual = BRM(individual=individual,current_landuse=current_landuse,quantity=quantity, power_BRM=power_BRM, power_inverse_BRM=power_inverse_BRM)[0] # or do the repair and then do the single pixel mutation?
    individual = BRM(individual=individual, current_landuse=current_landuse, quantity=quantity, power_BRM=power_BRM,
                     power_inverse_BRM=power_inverse_BRM)  # or do the repair and then do the single pixel mutation?

    individual = BCPM_without_repair(individual=individual,current_landuse=current_landuse,quantity=quantity, indpb_patch=indpb_patch, power_BRM=power_BRM, power_inverse_BRM=power_inverse_BRM, power_BCPM=power_BCPM, power_patch_BCPM=power_patch_BCPM, power_patch_inverse_BCPM=power_patch_inverse_BCPM)[0]

    return individual,
