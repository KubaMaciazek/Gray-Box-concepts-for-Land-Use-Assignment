import numpy as np
from osgeo import gdal


def get_sq_raster(sq_file):
    sq_raster = gdal.Open(sq_file)
    nodata = sq_raster.GetRasterBand(1).GetNoDataValue()
    sq_raster = np.array(sq_raster.GetRasterBand(1).ReadAsArray())
    sq_raster[sq_raster == nodata] = 0.0
    sq_raster[np.isnan(sq_raster)] = 0.0
    return sq_raster


def get_normalized_sq_raster(sq_raster):
    sq_raster = get_sq_raster(sq_raster)
    return sq_raster / float(np.max(sq_raster))
