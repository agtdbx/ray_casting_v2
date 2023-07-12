import numpy as np

import math
from numba import njit


def orientationToVec(rot):
	radians = rot * (math.pi / 180)
	return np.array((math.cos(radians), math.sin(radians)))


def vecToOrientation(vec):
	return (math.atan2(vec[1], vec[0]) * 180) / math.pi


def movePoint(point, vec, dist):
	return point + (vec * dist)


def computeTriangleArea(p1, p2, p3):
	value = abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) * 0.5

	return value
