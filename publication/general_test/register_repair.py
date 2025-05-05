import warnings

import numpy as np

from publication.operators.mutations.brm import BRM
from publication.operators.mutations.rrm import RRM

power_BRM = 1  # 1 #value between 0 and 1 (decrease differences), value > 1 (increase differences), 0 means uniform probabilities
power_inverse_BRM = 1  # 1


def register_repair(repair_name, toolbox, int_quantity, areal):
    if repair_name == "rrm":
        toolbox.register("repair", RRM,
                         current_landuse=np.copy(areal),
                         quantity=float(int_quantity))
    elif repair_name == "brm":
        toolbox.register("repair", BRM,
                         current_landuse=np.copy(areal),
                         quantity=float(int_quantity),
                         power_BRM=power_BRM,
                         power_inverse_BRM=power_inverse_BRM)
    else:
        warnings.warn("Unknown repair: None registered")
