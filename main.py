import segment
import player
import mymap
import math_functions as mf

import pygame as pg
import numpy as np
import math
import time
import sys


PI_DIV_180 = math.pi / 180


def keySortSegment(elem):
	return min(math.dist(elem[0].p1, elem[1]), math.dist(elem[0].p2, elem[1]))


class Game:
	def __init__(self):
		"""
		This method define all variables needed by the program
		"""
		pg.init() # Start of pygame

		infoObject = pg.display.Info() # We get the screen size of the computer
		self.winSize = ((infoObject.current_w, infoObject.current_h - 63)) # We remove the toolbar of the window's height
		self.win  = pg.display.set_mode(self.winSize, pg.RESIZABLE) # We create the window

		self.clock = pg.time.Clock() # The clock be used to limit our fps
		self.fps = 60

		self.last = time.time()

		self.minimap = False
		self.waitMinimap = 0

		self.textureN = pg.image.load("imgs/N.png").convert_alpha()
		self.textureS = pg.image.load("imgs/S.png").convert_alpha()
		self.textureE = pg.image.load("imgs/E.png").convert_alpha()
		self.textureW = pg.image.load("imgs/W.png").convert_alpha()

		self.segments = mymap.getSegmentFromMap()

		pos, orientation = mymap.getPlayerPosFromMap()

		self.player = player.Player(pos, orientation)

		self.halfwinW = self.winSize[0] // 2
		self.halfwinH = self.winSize[1] // 2
		self.screenDist =  (self.halfwinW * 0.7) / math.tan(self.player.halfFov)

		self.ceilBox = (0, 0, self.winSize[0], self.winSize[1] / 2)
		self.floorBox = (0, self.winSize[1] / 2, self.winSize[0], self.winSize[1])

		self.nbRays = 1920 // 2
		self.rays = []

		self.intersections = []

		self.runMainLoop = True


	def run(self):
		"""
		This method is the main loop of the game
		"""
		while self.runMainLoop: # Game loop
			self.input()
			self.tick()
			self.render()
			self.clock.tick(self.fps)


	def input(self):
		"""
		The method catch user's inputs, as key presse or a mouse click
		"""
		for event in pg.event.get(): # We check each event
			if event.type == pg.QUIT: # If the event it a click on the top right cross, we quit the game
				self.quit()

		self.keyboardState = pg.key.get_pressed()
		self.mouseState = pg.mouse.get_pressed()
		self.mousePos = pg.mouse.get_pos()

		# Press espace to quit
		if self.keyboardState[pg.K_ESCAPE]:
			self.quit()

		# Press Z/W to go front and S to go back
		if self.keyboardState[pg.K_z] or self.keyboardState[pg.K_w]:
			self.player.move('f', self.segments)
		elif self.keyboardState[pg.K_s]:
			self.player.move('b', self.segments)

		# Press Q/A to go left and D to go right
		if self.keyboardState[pg.K_q] or self.keyboardState[pg.K_a]:
			self.player.move('l', self.segments)
		elif self.keyboardState[pg.K_d]:
			self.player.move('r', self.segments)

		# Press left arrow to rotate left or right arrow to rotate right
		if self.keyboardState[pg.K_LEFT]:
			self.player.rotate('l')
		elif self.keyboardState[pg.K_RIGHT]:
			self.player.rotate('r')

		# Make player run if left shift is press
		if self.keyboardState[pg.K_LSHIFT]:
			self.player.setRun(True)
		else:
			self.player.setRun(False)

		# If tab press, enable / disable minimap
		if self.waitMinimap == 0 and self.keyboardState[pg.K_TAB]:
			self.minimap = not self.minimap
			self.waitMinimap = 0.5


	def tick(self):
		"""
		This is the method where all calculations will be done
		"""
		tmp = time.time()
		delta = tmp - self.last
		self.last = tmp

		if self.waitMinimap > 0:
			self.waitMinimap -= delta
			if self.waitMinimap < 0:
				self.waitMinimap = 0

		self.rays = self.player.getRays(self.nbRays)

		self.intersections = []

		playerDir = mf.orientationToVec(self.player.orientation)
		segmentsToTest = []
		for seg in self.segments:
			if seg.normal.dot(playerDir) <= self.player.fovRatio:
				segmentsToTest.append((seg, self.player.pos))

		segmentsToTest.sort(key=keySortSegment)

		for ray in self.rays:
			best = (-1, None, None, None)
			for seg,_ in segmentsToTest:
				test = ray.collid(seg)
				if (0 <= test[0] and (best[0] == -1 or test[0] < best[0])):
					best = test
					break
			self.intersections.append(best)

		pg.display.set_caption(str(self.clock.get_fps()))


	def render(self):
		"""
		This is the method where all graphic update will be done
		"""

		# Render of '3d' view
		if not self.minimap:
			pg.draw.rect(self.win, mymap.CEIL_COLOR, self.ceilBox)
			pg.draw.rect(self.win, mymap.FLOOR_COLOR, self.floorBox)
			large = (self.winSize[0] // self.nbRays)
			for i in range(len(self.intersections)):
				dist, inter, xRatio, face = self.intersections[i]
				if 0 <= dist:
					ray = self.rays[i]

					diffRot = mf.vecToOrientation(ray.vec) - self.player.orientation
					radDiffRot = diffRot * PI_DIV_180
					dist *= math.cos(radDiffRot)

					dist /= mymap.WALL_SIZE
					size = self.screenDist / (dist + 0.00001)

					topY = self.halfwinH - (size / 2)

					if face == 'N':
						self.drawLineTexture(self.textureN, i * large, xRatio, large, topY, size)
					elif face == 'S':
						self.drawLineTexture(self.textureS, i * large, xRatio, large, topY, size)
					elif face == 'E':
						self.drawLineTexture(self.textureE, i * large, xRatio, large, topY, size)
					elif face == 'W':
						self.drawLineTexture(self.textureW, i * large, xRatio, large, topY, size)

					# if face == 'N':
					# 	color = (255, 0, 0)
					# elif face == 'S':
					# 	color = (255, 255, 0)
					# elif face == 'E':
					# 	color = (255, 0, 255)
					# elif face == 'W':
					# 	color = (0, 255, 255)
					# else:
					# 	color = (100, 100, 100)
					# pg.draw.rect(self.win, color, (i * large, topY, large, size))

		# Render of minimap
		else:
			self.win.fill((0, 0, 0)) # We clean our screen with one color
			toMove = np.array((self.winSize)) / 2 - self.player.pos

			for i in range(len(self.intersections)):
				inter = self.intersections[i]
				ray = self.rays[i]
				if 0 <= inter[0]:
					startPos = ray.origin + toMove
					endPos = inter[1] + toMove
					pg.draw.line(self.win, (100, 100, 100), startPos, endPos)
				else:
					p = mf.movePoint(ray.origin, ray.vec, 1000)
					startPos = ray.origin + toMove
					endPos = p + toMove
					pg.draw.line(self.win, (100, 100, 100), startPos, endPos)

			for seg in self.segments:
				seg.drawMinimap(self.win, toMove)

			self.player.drawMinimap(self.win, toMove)

		pg.display.update() # We update the drawing. Before the function call, any changes will be not visible


	def quit(self):
		"""
		This is the quit method
		"""
		pg.quit() # Pygame quit
		sys.exit()


	def drawLineTexture(self, texture, winX, xRatio, large, startY, size):
		x = int(xRatio * texture.get_width())

		if x == texture.get_width():
			x -= 1

		wall = texture.subsurface((x, 0, 1, texture.get_height()))

		wall = pg.transform.scale(wall, (large, size))

		self.win.blit(wall, (winX, startY))

Game().run() # Start game
