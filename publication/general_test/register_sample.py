import numpy as np

from publication.data.get_areal_raster import get_areal_raster
from publication.data.get_community_data import get_areal_and_sq_rasters_paths, get_community_ref_point
from publication.data.get_conversion_number import get_conversion_number
from publication.data.get_sq_raster import get_normalized_sq_raster
from publication.objective_functions.aggregated_objective_function import aggregated_objective_function

def register_sample(sample, toolbox):
    areal_raster_path, sq_raster_path = get_areal_and_sq_rasters_paths(sample)
    areal = get_areal_raster(areal_raster_path)
    sq_raster_normalized = get_normalized_sq_raster(sq_raster_path)

    int_quantity = get_conversion_number(sample)

    ref_point_convergence = get_community_ref_point(sample)

    toolbox.register("evaluate", aggregated_objective_function,
                     sq_raster_normalized=sq_raster_normalized,
                     areal_4kl_09=np.copy(areal))

    return areal_raster_path, sq_raster_path, areal, sq_raster_normalized, int_quantity, ref_point_convergence
