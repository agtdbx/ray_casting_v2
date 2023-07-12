import segment
import math_functions as mf

import pygame as pg
import numpy as np
from numba import njit

# Dot product beetween 2D vectors
@njit(fastmath=True)
def dot(v1, v2):
	return (v1[0] * v2[0]) + (v1[1] * v2[1])


# Cross product beetween 2D vectors
@njit(fastmath=True)
def cross(v1, v2):
	return (v1[0] * v2[1]) - (v1[1] * v2[0])


# Function to do the intersection beetween a ray and a segment
# The decorate defore def is to speedup the function
@njit(fastmath=True)
def makeCollid(rayOrigin, rayDir, segNormal, segDir, segP1):
	if 0 <= dot(rayDir, segNormal):
		return (-1, -1)

	v1 = rayOrigin - segP1
	v2 = segDir
	v3 = np.array((-rayDir[1], rayDir[0]))

	subpart = dot(v2, v3)
	if subpart == 0:
		return (-1, -1)

	t1 = cross(v2, v1) / subpart
	if (t1 < 0):
		return (-1, -1)

	t2 = dot(v1, v3) / subpart
	if (t2 < 0 or 1 < t2):
		return (-1, -1)

	return (t1, t2)


class Ray:
	def __init__(self, origin, vec):
		self.origin = origin
		self.vec = vec

	# The collid method of ray with a segment
	def collid(self, seg):
		dist, xRatio = makeCollid(self.origin, self.vec, seg.normal, seg.vec, seg.p1)

		if dist < 0:
			return (-1, None, None, None)

		return (dist, mf.movePoint(self.origin, self.vec, dist), xRatio, seg.face)
