import numpy as np
import pandas as pd
import os
import csv
import sys
import re

#This allows us to access our huge data csv
csv.field_size_limit(sys.maxsize)

#The following block is thanks to Maciej Kalisiak

#!/usr/bin/env python
#
# routine for performing the "point in polygon" inclusion test

# Copyright 2001, softSurfer (www.softsurfer.com)
# This code may be freely used and modified for any purpose
# providing that this copyright notice is included with it.
# SoftSurfer makes no warranty for this code, and cannot be held
# liable for any real or imagined damage resulting from its use.
# Users of this code must verify correctness for their application.

# translated to Python by Maciej Kalisiak <mac@dgp.toronto.edu>

#   a Point is represented as a tuple: (x,y)

#===================================================================

# is_left(): tests if a point is Left|On|Right of an infinite line.

#   Input: three points P0, P1, and P2
#   Return: >0 for P2 left of the line through P0 and P1
#           =0 for P2 on the line
#           <0 for P2 right of the line
#   See: the January 2001 Algorithm "Area of 2D and 3D Triangles and Polygons"

def is_left(P0, P1, P2):
    return (P1[0] - P0[0]) * (P2[1] - P0[1]) - (P2[0] - P0[0]) * (P1[1] - P0[1])

#===================================================================

# cn_PnPoly(): crossing number test for a point in a polygon
#     Input:  P = a point,
#             V[] = vertex points of a polygon
#     Return: 0 = outside, 1 = inside
# This code is patterned after [Franklin, 2000]

def cn_PnPoly(P, V):
    cn = 0    # the crossing number counter

    # repeat the first vertex at end
    V = tuple(V[:])+(V[0],)

    # loop through all edges of the polygon
    for i in range(len(V)-1):   # edge from V[i] to V[i+1]
        if ((V[i][1] <= P[1] and V[i+1][1] > P[1])   # an upward crossing
            or (V[i][1] > P[1] and V[i+1][1] <= P[1])):  # a downward crossing
            # compute the actual edge-ray intersect x-coordinate
            vt = (P[1] - V[i][1]) / float(V[i+1][1] - V[i][1])
            if P[0] < V[i][0] + vt * (V[i+1][0] - V[i][0]): # P[0] < intersect
                cn += 1  # a valid crossing of y=P[1] right of P[0]

    return cn % 2   # 0 if even (out), and 1 if odd (in)

#===================================================================

# wn_PnPoly(): winding number test for a point in a polygon
#     Input:  P = a point,
#             V[] = vertex points of a polygon
#     Return: wn = the winding number (=0 only if P is outside V[])

def wn_PnPoly(P, V):
    wn = 0   # the winding number counter

    # repeat the first vertex at end
    V = tuple(V[:]) + (V[0],)

    # loop through all edges of the polygon
    for i in range(len(V)-1):     # edge from V[i] to V[i+1]
        if V[i][1] <= P[1]:        # start y <= P[1]
            if V[i+1][1] > P[1]:     # an upward crossing
                if is_left(V[i], V[i+1], P) > 0: # P left of edge
                    wn += 1           # have a valid up intersect
        else:                      # start y > P[1] (no test needed)
            if V[i+1][1] <= P[1]:    # a downward crossing
                if is_left(V[i], V[i+1], P) < 0: # P right of edge
                    wn -= 1           # have a valid down intersect
    return wn

#===================================================================


#Combination of https://www.google.com/maps/d/u/0/viewer?mid=1_gsxJNfmcGZI4ZL_7LnEHj72YpvgNq-w&hl=en&ll=40.77764664018023%2C-73.9102922421289&z=12 and
#https://www.google.com/maps/d/u/0/viewer?mid=1ChYy82SQd3HfibWtRejC4_qN92k&ll=40.77106094225273%2C-73.97485224140219&z=13
#Fixes to this combination have been made my Michael N. Manta
#Manta's map can be found here https://www.google.com/maps/d/u/0/edit?mid=1k6noORbUAAseOZWpI21-L2-cVjb18any&ll=40.85241558077014%2C-73.90501683628486&z=14

coordinatesOfPlace = input("Type in the coordinates (format it as {North East}) without brackets: ")

coordinatesOfPlace = tuple(float(x) for x in coordinatesOfPlace.split(" "))[::-1]

#print(coordinatesOfPlace)

neighborhoodFinal = "Neighborhood Not Found"

if __name__ == "__main__":
    with open('neighborhooddata.csv', 'r') as neighborhoodData:
        neighborhoodCSVreader = csv.reader(neighborhoodData, delimiter=';')
        rowNum = 0
        for row in neighborhoodCSVreader:
            if rowNum == 0:
                rowNum += 1
            else:
                neighborhoodName = row[0]
                neighborhoodCoordinates = row[1]
                neighborhoodCoordinates = neighborhoodCoordinates.split(" ")
                neighborhoodCoordinates = [tuple(map(float, neighborhoodCoordinates[x].split(","))) for x in range(len(neighborhoodCoordinates) - 1)]

                #print(neighborhoodCoordinates)
                #print(rowNum, wn_PnPoly(coordinatesOfPlace, neighborhoodCoordinates))

                if wn_PnPoly(coordinatesOfPlace, neighborhoodCoordinates) != 0:
                    neighborhoodFinal = f"This location is in {neighborhoodName}."
                    break
                rowNum += 1

print(neighborhoodFinal)
