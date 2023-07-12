import segment

# strmap = [
# 	["1111111111"],
# 	["1011000001"],
# 	["10000001011"],
# 	["10000011001"],
# 	["1N000011011"],
# 	["1000000001"],
# 	["1111111111"]
# ]

strmap = [
	["1111111111               111"],
	["1000010001               101"],
	["1000010011               101"],
	["1001110001111    1111    101"],
	["1001110000001    101111 1101"],
	["1011000001101111 100001 1001"],
	["1010001111100001111010111011"],
	["1010001   10000001001000001"],
	["1010011   11111011011010101"],
	["101011        1011011000101"],
	["101001111111111000011111101"],
	["101100000000000000111111001"],
	["10000011111111111000000001"],
	["1111101         1111111111"],
	["    101"],
	["    101111111111111"],
	["    100000000000001"],
	["    100000000000001"],
	["    10000000000N001"],
	["    111111111111111"],
]

MAP = []

for line in strmap:
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

WALL_SIZE = 100

CEIL_COLOR = (100, 100, 200)
FLOOR_COLOR = (50, 100, 50)

def getPlayerPosFromMap():

	for mapY in range(len(MAP)):
		for mapX in range(len(MAP[mapY])):
			if MAP[mapY][mapX] == 2: # Player look Noth
				return (mapX * WALL_SIZE + (WALL_SIZE / 2), mapY * WALL_SIZE + (WALL_SIZE / 2)), 270
			if MAP[mapY][mapX] == 3: # Player look East
				return (mapX * WALL_SIZE + (WALL_SIZE / 2), mapY * WALL_SIZE + (WALL_SIZE / 2)), 0
			if MAP[mapY][mapX] == 4: # Player look South
				return (mapX * WALL_SIZE + (WALL_SIZE / 2), mapY * WALL_SIZE + (WALL_SIZE / 2)), 90
			if MAP[mapY][mapX] == 5: # Player look West
				return (mapX * WALL_SIZE + (WALL_SIZE / 2), mapY * WALL_SIZE + (WALL_SIZE / 2)), 180

	return (100, 100), 0


def getSegmentFromWall(mapX, mapY):
	segments = []

	x1 = mapX * WALL_SIZE
	x2 = mapX * WALL_SIZE + WALL_SIZE
	y1 = mapY * WALL_SIZE
	y2 = mapY * WALL_SIZE + WALL_SIZE

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


def getSegmentFromMap():
	segments = []

	for mapY in range(MAP_H):
		for mapX in range(len(MAP[mapY])):
			if MAP[mapY][mapX] == 1:
				segs = getSegmentFromWall(mapX, mapY)
				segments.extend(segs)

	return segments

