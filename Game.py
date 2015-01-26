import math
from life import Node
class Game:

	def __init__(self, positions):
		params = Game.getParameters(positions)
		self._node = Game.nodeBuilder(params[1], params[0], positions)
		self._view = [params[0][0], params[0][2]]

	@classmethod
	def getParameters(cls, positions):
		maximum_x = max(map(lambda a: a[0], positions))
		minimum_x = min(map(lambda a: a[0], positions))
		width = maximum_x - minimum_x + 1
		maximum_y = max(map(lambda a: a[1], positions))
		minimum_y = min(map(lambda a: a[1], positions))
		height = maximum_y - minimum_y + 1
		center_x = (maximum_x + minimum_x)//2
		center_y = (maximum_y + minimum_y)//2
		largest_dimension = max(width, height)
		#level = int(math.ceil(math.log((largest_dimension), 2))) + 1 #this also works
		level = max(1, int(math.ceil(math.log(largest_dimension, 2))))
		size = 2**level
		return [(center_x - size//2 + 1, center_x + size//2,
			center_y - size//2 + 1, center_y + size//2), level]

	@classmethod
	def nodeBuilder(self, level, params, positions):
		if level == 1:
			ul = 1 if (params[0], params[2]) in positions else 0
			ur = 1 if (params[1], params[2]) in positions else 0
			bl = 1 if (params[0], params[3]) in positions else 0
			br = 1 if (params[1], params[3]) in positions else 0
			return Node(ul ,ur, bl, br, 1)
		else:
			offset = 2**(level - 1)
			ul = (params[0], params[1] - offset,
				params[2], params[3] - offset)
			ur = (params[0] + offset, params[1],
				params[2], params[3] - offset)
			bl = (params[0], params[1] - offset,
				params[2] + offset, params[3])
			br = (params[0] + offset, params[1],
				params[2] + offset, params[3])
			return Node(Game.nodeBuilder(level - 1, ul, positions),
				Game.nodeBuilder(level - 1, ur, positions),
				Game.nodeBuilder(level - 1, bl, positions),
				Game.nodeBuilder(level - 1, br, positions), level)

	def Draw(self, size, canvas, shift = 0):
		self._view = [self._view[0] - shift, self._view[1] - shift]
		self._node.Draw(size, canvas, self._view)