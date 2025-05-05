# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Jonas Schwaab
#
# Created:     10.11.2015
# Copyright:   (c) Jonas 2015
# Licence:     <your licence>
# -------------------------------------------------------------------------------

from __future__ import division
import random
import numpy
from matplotlib.path import Path


def ac(ind1, ind2):
    """Executes a 2d crossover
    """

    gridshape = ind1.shape

    #randomly select point on y or x and then look for the point opposite to that one
    axis = random.choice(["x","y"])
    if axis=="x":
        point_row1 = random.randint(1,gridshape[1])
        point_row2 = gridshape[1] - point_row1
        point_col1 = gridshape[0]
        point_col2 = 0
        point_row3 = 0
        point_col3 = 0
        point_row4 = 0
        point_col4 = gridshape[0]
        point_row5 = point_row1
        point_col5 = point_col1
    else:
        point_col1 = random.randint(1,gridshape[0])
        point_col2 = gridshape[0] - point_col1
        point_row1 = gridshape[1]
        point_row2 = 0
        point_col3 = 0
        point_row3 = 0
        point_col4 = 0
        point_row4 = gridshape[1]
        point_row5 = point_row1
        point_col5 = point_col1


    verts = [(point_row1, point_col1),(point_row2, point_col2),(point_row3, point_col3),(point_row4, point_col4),(point_row5, point_col5)]
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO,Path.LINETO, Path.CLOSEPOLY,]
    path = Path(verts, codes)

    nx, ny = gridshape[1], gridshape[0]

    # Create vertex coordinates for each grid cell...
    # (<0,0> is at the top left of the grid in this system)
    x, y = numpy.meshgrid(numpy.arange(0.5, nx+0.5, 1), numpy.arange(0.5, ny+0.5, 1))
    x, y = x.flatten(), y.flatten()
    points = numpy.vstack((x,y)).T
    grid = Path.contains_points(path, points) #if it lies on the boundary all will be true or fals. Thus more pixels will in generally be true or false
    grid = grid.reshape((ny,nx))
    # print(grid)

    ind1[~grid], ind2[~grid] = ind2[~grid], ind1[~grid]

    return ind1, ind2
