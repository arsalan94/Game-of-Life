from Tkinter import *
import ttk
from Game import Game
import time

width, height = 800, 800
size = 10

root = Tk()
root.title("Conway's Game of Life")

live = []
game = None
level = 0
paused = True

def callback(event):
	id = event.widget.find_closest(event.x, event.y)
	color = canvas.itemcget(id, "fill")
	if (color == "black"):
		live.append((event.x//size, event.y//size))
		canvas.itemconfig(id, fill = "green")
	else:
		live.remove((event.x//size, event.y//size))
		canvas.itemconfig(id, fill = 'black')

def runGame():
	global game, level, size
	canvas.delete("all")
	game = Game(live)
	game.Draw(size, canvas)
	level = game._node._level

def nextGen():
	global level, size
	game._node = game._node.evolve()
	newlevel = game._node._level
	change = newlevel - level
	shift = 0
	if level < newlevel:
		shift = 2**(level - 1)
	if level > newlevel:
		shift = - 2**(level - 2)
	level = newlevel
	canvas.delete("all")
	game.Draw(size, canvas, shift)

"""def test():
	game._node.test()"""

def runAndPause():
	global paused
	paused = False if paused else True 
	if paused:
		runButton.config(text = "run")
		return
	runButton.config(text = "pause")
	go()

def go():
	global paused
	if paused:
		return
	global level, size
	game._node = game._node.evolve()
	newlevel = game._node._level
	change = newlevel - level
	shift = 0
	if level < newlevel:
		shift = 2**(level - 1)
	if level > newlevel:
		shift = - 2**(level - 2)
	level = newlevel
	canvas.delete("all")
	game.Draw(size, canvas, shift)
	canvas.after(5, go)

def zoomOutFunction():
	global size
	size = max(1, size - 4)

def zoomInFunction():
	global size
	size = min(80, size + 4)

canvas = Canvas(root, width = width, height = height, bg = "black")
canvas.pack(side = "left")

setCoordinates = Button(root, text = "set coordinates", command = runGame)
setCoordinates.pack(side = "right")
nextGeneration = Button(root, text = "Next Generation", command = nextGen)
nextGeneration.pack(side = "right")
runButton = Button(root, text = "run", command = runAndPause)
runButton.pack(side = "right")
zoomIn = Button(root, text = "+", command = zoomInFunction)
zoomIn.pack(side = "right")
zoomOut = Button(root, text = "-", command = zoomOutFunction)
zoomOut.pack(side = "right")

for x in range (0, width//size):
	for y in range (0, height//size):
		canvas.tag_bind(
			canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill = "black", outline = "gray"),
			 "<Button-1>", callback)

root.mainloop()