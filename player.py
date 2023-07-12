import ray
import math_functions as mf
import define

import pygame as pg
import numpy as np
import math


class Player:
	def __init__(self, pos, orientation):
		self.pos = np.array(pos)
		self.orientation = self.checkOrientation(orientation)
		self.moveSpeed = define.PLAYER_MOVEMENT_SPEED
		self.rotateSpeed = define.PLAYER_ROTATION_SPEED
		self.fov = define.PLAYER_FOV
		self.halfFov = self.fov / 2
		self.fovRatio = self.fov / 360 * 3
		self.run = False
		self.computeVec()


	# Method to have degrees always in range [0, 359]
	def checkOrientation(self, orientation):
		while orientation < 0:
			orientation += 360
		while orientation >= 360:
			orientation -= 360
		return orientation


	# Method to compute the vec of the player used for movement
	def computeVec(self):
		# Front vector
		self.vecFront = mf.orientationToVec(self.orientation)
		# Back vector
		self.vecBack = np.array((-self.vecFront[0], -self.vecFront[1]))
		# Left vector
		self.vecLeft = np.array((self.vecFront[1], -self.vecFront[0]))
		# Right vector
		self.vecRight = np.array((-self.vecFront[1], self.vecFront[0]))


	def draw(self, win):
		p1 = mf.movePoint(self.pos, self.vecLeft, 15)
		p2 = mf.movePoint(self.pos, self.vecFront, 45)
		p3 = mf.movePoint(self.pos, self.vecRight, 15)

		p1 = mf.movePoint(p1, self.vecBack, 20)
		p2 = mf.movePoint(p2, self.vecBack, 20)
		p3 = mf.movePoint(p3, self.vecBack, 20)

		pg.draw.polygon(win, (100, 255, 100), [p1, p2, p3])


	def drawMinimap(self, win, move):
		p1 = mf.movePoint(self.pos, self.vecLeft, 15)
		p2 = mf.movePoint(self.pos, self.vecFront, 45)
		p3 = mf.movePoint(self.pos, self.vecRight, 15)

		p1 = mf.movePoint(p1, self.vecBack, 20) + move
		p2 = mf.movePoint(p2, self.vecBack, 20) + move
		p3 = mf.movePoint(p3, self.vecBack, 20) + move

		pg.draw.polygon(win, (100, 255, 100), [p1, p2, p3])


	# The collid method to kwon if the player can move
	def collid(self, pos, segments):
		radius = 25

		for seg in segments:
			distOP = math.dist(pos, seg.p1)
			distOQ = math.dist(pos, seg.p2)
			distPQ = math.dist(seg.p1, seg.p2)

			vecOP = seg.p1 - pos
			vecOQ = seg.p2 - pos

			vecPQ = seg.vec
			vecQP = seg.p1 - seg.p2

			minDist = 2000000000
			maxDist = max(distOP, distOQ)

			if vecOP.dot(vecQP) > 0 and vecOQ.dot(vecPQ) > 0:
				minDist = (2 * mf.computeTriangleArea(pos, seg.p1, seg.p2)) / distPQ
			else:
				minDist = min(distOP, distOQ)

			if minDist <= radius and maxDist >= radius:
				return True

		return False


	def move(self, direction, segments):
		if self.run:
			speed = self.moveSpeed * 2
		else:
			speed = self.moveSpeed

		if direction == 'f':
			pos = mf.movePoint(self.pos, self.vecFront, speed)
			move = True
		elif direction == 'b':
			pos = mf.movePoint(self.pos, self.vecBack, speed)
			move = True
		elif direction == 'l':
			pos = mf.movePoint(self.pos, self.vecLeft, speed)
			move = True
		elif direction == 'r':
			pos = mf.movePoint(self.pos, self.vecRight, speed)
			move = True
		else:
			move = False

		if move:
			if not self.collid(pos, segments):
				self.pos = pos


	def rotate(self, rot):
		if rot == 'l':
			self.orientation -= self.rotateSpeed
			self.orientation = self.checkOrientation(self.orientation)
			self.computeVec()
		elif rot == 'r':
			self.orientation += self.rotateSpeed
			self.orientation = self.checkOrientation(self.orientation)
			self.computeVec()


	def setRun(self, run):
		self.run = run


	# The method to get the ray used for raycasting
	def getRays(self, nbRay):
		rays = []
		startOrientation = self.checkOrientation(self.orientation - self.halfFov)
		toAddOrientation = self.fov / nbRay

		for i in range(nbRay):
			orientation = startOrientation + (toAddOrientation * i)
			orientation = self.checkOrientation(orientation)
			vec = mf.orientationToVec(orientation)
			vec = vec / np.linalg.norm(vec)
			rays.append(ray.Ray(self.pos, vec))
		return rays
