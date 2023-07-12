import segment
import define

MAP = []

# Transform list of str to list of list
for line in define.STRMAP:
	lst = []
	for c in line[0]:
		if c == '0':
			lst.append(0)
		elif c == '1':
			lst.append(1)
		elif c == 'N':
			lst.append(2)
		elif c == 'E':
			lst.append(3)
		elif c == 'S':
			lst.append(4)
		elif c == 'W':
			lst.append(5)
		else:
			lst.append(-1)
	MAP.append(lst)

MAP_H = len(MAP)

# Function du get the pos and orientation of the player
def getPlayerPosFromMap():

	for mapY in range(len(MAP)):
		for mapX in range(len(MAP[mapY])):
			if MAP[mapY][mapX] == 2: # Player look Noth
				return (mapX * define.WALL_SIZE + (define.WALL_SIZE / 2), mapY * define.WALL_SIZE + (define.WALL_SIZE / 2)), 270
			if MAP[mapY][mapX] == 3: # Player look East
				return (mapX * define.WALL_SIZE + (define.WALL_SIZE / 2), mapY * define.WALL_SIZE + (define.WALL_SIZE / 2)), 0
			if MAP[mapY][mapX] == 4: # Player look South
				return (mapX * define.WALL_SIZE + (define.WALL_SIZE / 2), mapY * define.WALL_SIZE + (define.WALL_SIZE / 2)), 90
			if MAP[mapY][mapX] == 5: # Player look West
				return (mapX * define.WALL_SIZE + (define.WALL_SIZE / 2), mapY * define.WALL_SIZE + (define.WALL_SIZE / 2)), 180

	return (100, 100), 0


# Function to create all segment usefull for a wall
# if a segment face to void or to another wall, it isn't create
def getSegmentFromWall(mapX, mapY):
	segments = []

	x1 = mapX * define.WALL_SIZE
	x2 = mapX * define.WALL_SIZE + define.WALL_SIZE
	y1 = mapY * define.WALL_SIZE
	y2 = mapY * define.WALL_SIZE + define.WALL_SIZE

	if 0 < mapY and mapX < len(MAP[mapY - 1]) - 1 and abs(MAP[mapY - 1][mapX]) != 1:
		# Add up segment
		segments.append(segment.Segment((x2, y1), (x1, y1), 'N'))
	if 0 < mapX and abs(MAP[mapY][mapX - 1]) != 1:
		# Add left segment
		segments.append(segment.Segment((x1, y1), (x1, y2), 'W'))
	if mapY < MAP_H - 1 and mapX < len(MAP[mapY + 1]) - 1 and abs(MAP[mapY + 1][mapX]) != 1:
		# Add down segment
		segments.append(segment.Segment((x1, y2), (x2, y2), 'S'))
	if mapX < len(MAP[mapY]) - 1 and abs(MAP[mapY][mapX + 1]) != 1:
		# Add right segment
		segments.append(segment.Segment((x2, y2), (x2, y1), 'E'))

	return segments


# Function to get all segment of the map
def getSegmentFromMap():
	segments = []

	for mapY in range(MAP_H):
		for mapX in range(len(MAP[mapY])):
			if MAP[mapY][mapX] == 1:
				segs = getSegmentFromWall(mapX, mapY)
				segments.extend(segs)

	return segments

