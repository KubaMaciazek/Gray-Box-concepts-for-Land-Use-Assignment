import numpy as np
from osgeo import gdal


def get_areal_raster(areal_file):
    areal_raster = gdal.Open(areal_file)
    nodata = areal_raster.GetRasterBand(1).GetNoDataValue()
    areal_raster = np.array(areal_raster.GetRasterBand(1).ReadAsArray())
    areal_raster[areal_raster == nodata] = 0.0
    areal_raster[np.isnan(areal_raster)] = 0.0
    return areal_raster
