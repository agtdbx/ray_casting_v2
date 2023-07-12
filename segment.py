import math_functions as mf

import pygame as pg
import numpy as np


class Segment:
	def __init__(self, p1, p2, face):
		self.p1 = np.array(p1)
		self.p2 = np.array(p2)
		self.vec = self.p2 - self.p1
		dx = self.p2[0] - self.p1[0]
		dy = self.p2[1] - self.p1[1]
		self.normal = np.array((-dy, dx))
		self.normal = self.normal / np.linalg.norm(self.normal)
		self.color = (255, 100, 100)
		self.face = face


	def draw(self, win):
		pg.draw.line(win, self.color, self.p1, self.p2)


	def drawMinimap(self, win, move):
		pg.draw.line(win, self.color, self.p1 + move, self.p2 + move)
