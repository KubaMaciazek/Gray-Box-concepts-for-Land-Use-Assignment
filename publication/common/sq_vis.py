import numpy as np
import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from osgeo import gdal
import sys

from maciazek.main.tools_parts.get_areal_raster import get_areal_raster

data_gemeinden_zuerich_KUBA_PATH = "data/data_gemeinden_zuerich/"
areal_zuerich_KUBA_PATH = "data/data_gemeinden_zuerich/canton_zuerich/areal_zuerich"

# [KUBA]: Land-use/land-cover map visualization
def plot_lulc_map(data, title):
    colors = ['white', 'red', 'yellow', 'green', 'blue']
    cmap = plt.matplotlib.colors.ListedColormap(colors)

    # Areal dla całego cantonu przyjmuje wartość -1 dla braku wartości, dlatego aby mieć uniwersalną funkcję do plottowania,
    # trzeba zakres białego koloru ustawić zarówno na -1 (kanton) jak i 0 (poszczególne municipalities). Inaczej źle koloruje kanton

    # Define the bounds for the colormap
    bounds = [-1.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    # Create a colormap normalization instance
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    plt.matshow(data, cmap=cmap, norm=norm)
    plt.title(title)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.colorbar(ticks=[0, 1, 2, 3, 4])
    cbar = plt.colorbar(ticks=[0, 1, 2, 3, 4])
    cbar.ax.set_yticklabels(["", "Miasto", "Pola", "Las", "Woda"])
    # ["Brak danych", "Miasto", "Pola", "Las", "Woda"]
    plt.show()

# [KUBA]: Soil-quality map visualization
def plot_sq(data, title):
    # Plot the grid map with a grayscale colormap
    plt.matshow(data/np.max(data), cmap='YlOrBr')
    # Add a title
    plt.title(title)
    # Show color bar legend
    plt.colorbar()
    plt.show()


# [KUBA]: Test visualizations for Uster
def uster_vis_test():
    name_gemeinde="Uster"

    # Areal
    areal = gdal.Open(data_gemeinden_zuerich_KUBA_PATH + str(name_gemeinde) + "/areal_4_09.tif")
    # areal = gdal.Open(data_gemeinden_zuerich_KUBA_PATH + str(name_gemeinde) + "/areal_4_09_majfilter.tif")
    nodata = areal.GetRasterBand(1).GetNoDataValue()
    areal = numpy.array(areal.GetRasterBand(1).ReadAsArray());
    areal[areal == nodata] = 0.0

    print(np.unique(areal))
    plot_lulc_map(areal, "Uster: pokrycie terenu (LULC)")

    # Soil quality
    areal = gdal.Open(data_gemeinden_zuerich_KUBA_PATH + str(name_gemeinde) + "/sq.tif")
    nodata = areal.GetRasterBand(1).GetNoDataValue()
    areal = numpy.array(areal.GetRasterBand(1).ReadAsArray());
    areal[areal == nodata] = 0.0

    print(np.unique(areal))
    print(np.unique(areal).size)
    numpy.set_printoptions(threshold=sys.maxsize)
    print(areal.shape)
    # print(areal)
    plot_sq(areal, "Uster: jakość gleby (SQ)")


# [KUBA]: Test visualizations for all municipalities, and large sample of combined four.
# All except "Wetzikon (ZH)", as it does not have majfilter
# Crushes because too many plots, and FPUV does not have a majfilter.
def all_vis_test():
    all_communities_plus_FPUV = ["Uster", "Dübendorf", "Meilen", "Hedingen","Volketswil", "Bassersdorf","Oberglatt","Pfäffikon", "Bülach", "Nürensdorf", "Fehraltorf", "Rümlang", "Wetzikon (ZH)", "four_muni_FPUV"] #"Wetzikon (ZH)",

    for community in all_communities_plus_FPUV:

        print(community)

        # Areal
        areal = gdal.Open(data_gemeinden_zuerich_KUBA_PATH + community + "/areal_4_09.tif")
        nodata = areal.GetRasterBand(1).GetNoDataValue()
        areal = numpy.array(areal.GetRasterBand(1).ReadAsArray())
        areal[areal == nodata] = 0.0

        print("Areal values: " + str(np.unique(areal)))
        plot_lulc_map(areal, community + "/areal_4_09.tif")

        # # Areal filtered
        # areal = gdal.Open(data_gemeinden_zuerich_KUBA_PATH + community + "/areal_4_09_majfilter.tif")
        # nodata = areal.GetRasterBand(1).GetNoDataValue()
        # areal = numpy.array(areal.GetRasterBand(1).ReadAsArray())
        # areal[areal == nodata] = 0.0
        #
        # print("Areal filtered values: " + str(np.unique(areal)))
        # plot_lulc_map(areal, community + "/areal_4_09_majfilter.tif")

        # Soil quality
        areal = gdal.Open(data_gemeinden_zuerich_KUBA_PATH + community + "/sq.tif")
        nodata = areal.GetRasterBand(1).GetNoDataValue()
        areal = numpy.array(areal.GetRasterBand(1).ReadAsArray())
        areal[areal == nodata] = 0.0

        # print("Soil quality values: " + str(np.unique(areal)))
        print("Soil quality nr of uniq values: " + str(np.unique(areal).size))
        plot_sq(areal, community + "/sq.tif")


# [KUBA]: visualization test for canton
def canton_vis_test():
    areal_zuerich_KUBA_PATH = "data/data_gemeinden_zuerich/canton_zuerich/areal_zuerich"
    sq_zuerich_KUBA_PATH = "data/data_gemeinden_zuerich/canton_zuerich/sq"
    sq_idw_KUBA_PATH = "data/data_gemeinden_zuerich/canton_zuerich/sq_idw"

    # Areal
    areal = gdal.Open(areal_zuerich_KUBA_PATH)
    nodata = areal.GetRasterBand(1).GetNoDataValue()
    areal = numpy.array(areal.GetRasterBand(1).ReadAsArray())
    areal[areal == nodata] = 0.0

    print("Areal values: " + str(np.unique(areal)))
    plot_lulc_map(areal, "canton_zuerich/areal_zuerich")

    # Soil quality
    areal = gdal.Open(sq_zuerich_KUBA_PATH)
    nodata = areal.GetRasterBand(1).GetNoDataValue()
    areal = numpy.array(areal.GetRasterBand(1).ReadAsArray())
    areal[areal == nodata] = 0.0

    # print("Soil quality values: " + str(np.unique(areal)))
    print("Soil quality nr of uniq values: " + str(np.unique(areal).size))
    plot_sq(areal, "canton_zuerich/sq")

    # Soil quality idw
    areal = gdal.Open(sq_idw_KUBA_PATH)
    nodata = areal.GetRasterBand(1).GetNoDataValue()
    areal = numpy.array(areal.GetRasterBand(1).ReadAsArray())
    areal[areal == nodata] = 0.0

    # print("Soil quality values: " + str(np.unique(areal)))
    print("Soil quality idw nr of uniq values: " + str(np.unique(areal).size))
    plot_sq(areal, "canton_zuerich/sq_idw")


def count_rular_entities():
    # Communitites
    all_communities_plus_FPUV = ["Uster", "Dübendorf", "Meilen", "Hedingen", "Volketswil", "Bassersdorf", "Oberglatt",
                                 "Pfäffikon", "Bülach", "Nürensdorf", "Fehraltorf", "Rümlang", "Wetzikon (ZH)",
                                 "four_muni_FPUV"]

    for community in all_communities_plus_FPUV:
        path = data_gemeinden_zuerich_KUBA_PATH + community + "/areal_4_09.tif"
        areal = get_areal_raster(path)

        rular_mask = np.zeros(areal.shape)
        rular_mask[areal == 2] = 1
        print(str(community) + ":" + str(np.sum(rular_mask)))
        plot_lulc_map(areal, community + ":areal_4_09.tif")
        plot_lulc_map(rular_mask, community + ":rular_mask")

    # Kanton
    areal_zuerich_KUBA_PATH = "data/data_gemeinden_zuerich/canton_zuerich/areal_zuerich"
    areal = get_areal_raster(areal_zuerich_KUBA_PATH)
    rular_mask = np.zeros(areal.shape)
    rular_mask[areal == 2] = 1
    print(str("Kanton Zuerrich") + ":" + str(np.sum(rular_mask)))
    plot_lulc_map(areal, "Kanton Zuerrich" + ":areal_4_09.tif")
    plot_lulc_map(rular_mask, "Kanton Zuerrich" + ":rular_mask")




# ################################# TESTS ######################################

# uster_vis_test()
# all_vis_test() # will crash as described -> NO, as majority filter not included
# canton_vis_test()
# count_rular_entities()
