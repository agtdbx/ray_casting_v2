import numpy as np

import math
from numba import njit


# Function that take an orientation in degrees and return a vector that represent the movement for this orientation
def orientationToVec(rot):
	radians = rot * (math.pi / 180)
	return np.array((math.cos(radians), math.sin(radians)))


# Function that take a vector and return a orientation
def vecToOrientation(vec):
	return (math.atan2(vec[1], vec[0]) * 180) / math.pi


# Function that create a new point. This point begin at point param pos, and it's translate along vec param to the distance dist
def movePoint(point, vec, dist):
	return point + (vec * dist)


# Take three points and return the area of the triangle
def computeTriangleArea(p1, p2, p3):
	value = abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) * 0.5

	return value
