from Tkinter import *

hashmap = {}

"""
TODO
Canonicalization:
   implement hashmap
Memoazation:
   add _next variable
Multiple generation speed up:
   I still don't understand this... read up on it
"""

class Node:
    """Used Dr Dobbs to write the Node data structure: http://www.drdobbs.com/jvm/an-algorithm-for-compressing-space-and-t/184406478?pgno=1"""

	def __init__(self, ul, ur, bl, br, level):
		global hashmap
		self._ul = ul
		self._ur = ur
		self._bl = bl
		self._br = br
		self._level = level

	@classmethod
	def evaluate (cls, sum, val):
		if (sum == 3):
			val = 1
		if (sum != 2 and sum != 3):
			val = 0
		return val

	@classmethod
	def centeredSubnode(cls, node):
		return Node(node._ul._br, node._ur._bl, node._bl._ur, node._br._ul, node._level - 1)

	@classmethod
	def centeredHorizontal(cls, l, r):
		return Node(l._ur._br, r._ul._bl, l._br._ur, r._bl._ul, l._level - 1) 

	@classmethod
	def  centeredVertical(cls, u, b):
		return Node(u._bl._br, u._br._bl, b._ul._ur, b._ur._ul, u._level - 1)

	@classmethod
	def centeredSubSubnode(cls, node):
		return Node(node._ul._br._br, node._ur._bl._bl, node._bl._ur._ur, node._br._ul._ul, node._level - 2)

	@classmethod
	def zeroNode(cls, level, cache = []):
		if level == 0:
			return 0
		if len(cache) == 0:
			cache.append(Node(0, 0, 0, 0, 1))
		i = 1
		while i < level:
			last = cache[- 1]
			cache.append(Node(last, last, last, last, last._level + 1))
			i += 1
		return cache[level - 1]

	def __str__(self):
		return str((self._level, str(self._ul), str(self._ur), str(self._bl), str(self._br)))

	def nextGeneration(self):
		if self.isZero():
			return Node.zeroNode(self._level - 1)

		if self._level == 2:
			sum_ul = self._ul._ul + self._ul._bl + self._bl._ul + self._bl._ur + self._br._ul + self._ur._bl + self._ur._ul + self._ul._ur
			sum_ur = self._ur._ul + self._ur._ur + self._ur._br + self._br._ur + self._br._ul + self._bl._ur + self._ul._br + self._ul._ur
			sum_bl = self._bl._ul + self._ul._bl + self._ul._br + self._ur._bl + self._br._ul + self._br._bl + self._bl._br + self._bl._bl
			sum_br = self._br._ur + self._br._br + self._br._bl + self._bl._br + self._bl._ur + self._ul._br + self._ur._bl + self._ur._br

			return Node(Node.evaluate(sum_ul, self._ul._br), Node.evaluate(sum_ur, self._ur._bl), 
				Node.evaluate(sum_bl, self._bl._ur), Node.evaluate(sum_br, self._br._ul), self._level - 1);

		else:
			n00 = Node.centeredSubnode(self._ul)
			n01 = Node.centeredHorizontal(self._ul, self._ur)
			n02 = Node.centeredSubnode(self._ur)
			n10 = Node.centeredVertical(self._ul, self._bl)
			n11 = Node.centeredSubSubnode(self)
			n12 = Node.centeredVertical(self._ur, self._br)
			n20 = Node.centeredSubnode(self._bl)
			n21 = Node.centeredHorizontal(self._bl, self._br)
			n22 = Node.centeredSubnode(self._br)

			level = self._level
			return Node(Node(n00, n01, n10, n11, level - 1).nextGeneration(),
				Node(n01, n02, n11, n12, level - 1).nextGeneration(),
				Node(n10, n11, n20, n21, level - 1).nextGeneration(),
				Node(n11, n12, n21, n22, level - 1).nextGeneration(), level - 1)

	def zeroPad(self):
		zero = Node.zeroNode(self._level - 1)
		level = self._level
		return Node(Node(zero, zero, zero, self._ul, level), Node(zero, zero, self._ur, zero, level),
			Node(zero, self._bl, zero, zero, level), Node(self._br, zero, zero, zero, level), level + 1)

	def reduce(self):
		if self._level == 1:
			return self
		zero = Node.zeroNode(self._level - 2)
		node = self
		while(node._level >=2 and node._ul._ul == zero and node._ul._ur == zero and node._ul._bl == zero 
			and node._ur._ul == zero and node._ur._ur == zero and node._ur._br == zero
			and node._bl._ul == zero and node._bl._bl == zero and node._bl._br == zero 
			and node._br._ur == zero and node._br._bl == zero and node._br._br == zero):
			node = Node(node._ul._br, node._ur._bl, node._bl._ur, node._br._ul, node._level - 1)
			zero = Node.zeroNode(node._level - 2)
		return node

	def evolve(self):
		return self.zeroPad().zeroPad().nextGeneration().reduce()

	def __eq__(self, other):
		if self._level != other._level:
			return False
		if (id(self) == id(other)):
			return True
		return self._ul == other._ul and self._ur == other._ur and self._bl == other._bl and self._br == other._br

	def __hash__(self):
		return hash(id(self._ul), id(self._ur), id(self._bl), id(self._br))

	def isZero(self):
		zero = Node.zeroNode(self._level)
		return zero == self

	def getCanonical(self):
		node = hashmap.get(self)
		if node != None:
			return node
		hashmap[self] = self
		return self

	def Draw(self, size, canvas, offset=[0,0]):
		if self.isZero():
			return
		if self._level == 1:
			if self._ul:
				canvas.create_rectangle((offset[0])*size, (offset[1])*size, 
					(offset[0])*size+size, (offset[1])*size+size, fill = "green", outline = "green")
			if self._ur:
				canvas.create_rectangle((offset[0] + 1)*size, (offset[1])*size, 
					(offset[0] + 1)*size+size, (offset[1])*size+size, fill = "green", outline = "green")
			if self._bl:
				canvas.create_rectangle((offset[0])*size, (offset[1] + 1)*size, 
					(offset[0])*size+size, (offset[1] + 1)*size+size, fill = "green", outline = "green")
			if self._br:
				canvas.create_rectangle((offset[0] + 1)*size, (offset[1] + 1)*size, 
					(offset[0] + 1)*size+size, (offset[1] + 1)*size+size, fill = "green", outline = "green")
		else:
			adjust = 2**(self._level - 1)
			self._ul.Draw(size, canvas, offset)
			self._ur.Draw(size, canvas, [offset[0] + adjust, offset[1]])
			self._bl.Draw(size, canvas, [offset[0], offset[1] + adjust])
			self._br.Draw(size, canvas, [offset[0] + adjust, offset[1] + adjust])