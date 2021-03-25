import numpy
import matplotlib.pyplot as plt
import random
from queue import LifoQueue
# -------- Randomized depth-first search -------
random.seed(42)
size = 16
visits = numpy.zeros((size, size), dtype=bool)
stack = LifoQueue()
class Cell(object):
	"""docstring for Cell"""
	def __init__(self):
					#  x  y -> upp,  right,     	left,      		down        
		self.walls = {(0, 1): True, (1, 0): True, (-1, 0): True, (0, -1): True}
	def remove_wall(self, direction: tuple) -> None:
		self.walls[direction] = False
		
grid = [[Cell() for i in range(size)] for i in range(size)]
show = False
movement = [(0, 1), (1, 0), (-1, 0), (0, -1)]
inverter = {(0, 1): (0, -1), (1, 0): (-1, 0), (-1, 0): (1, 0), (0, -1): (0, 1)}

def has_neighbours(x: int, y: int) -> list:
	neighbours = []
	for i,j in movement:
		coord_x = x+i
		coord_y = y+j
		if ((coord_x >= 0 and coord_x < size) and (coord_y >= 0 and coord_y < size)):
			if not visits[coord_x, coord_y]: # if wasnt visited
				neighbours.append((i, j))
	return neighbours

"""
Choose the initial cell, mark it as visited and push it to the stack
While the stack is not empty
	Pop a cell from the stack and make it a current cell
	If the current cell has any neighbours which have not been visited
		Push the current cell to the stack
		Choose one of the unvisited neighbours
		Remove the wall between the current cell and the chosen cell
		Mark the chosen cell as visited and push it to the stack
"""
def algo(start_x: int, start_y: int) -> None:
	visits[start_x, start_y] = 1 # Visited
	stack.put((start_x, start_y))
	while not stack.empty():
		curr_x, curr_y = stack.get() # Pop
		neighbours = has_neighbours(curr_x, curr_y) # list of neighbours coords
		if neighbours: # not empty
			stack.put((curr_x, curr_y)) # push the current cell to stack -> backtracing
			neighbour_x, neighbour_y = random.choice(neighbours) # choose one of the neighbours at random
			visits[curr_x+neighbour_x, curr_y+neighbour_y] = 1 # visited neighbour
			grid[curr_x+neighbour_x][curr_y+neighbour_y].remove_wall(inverter[(neighbour_x, neighbour_y)]) # remove wall from neighbour
			grid[curr_x][curr_y].remove_wall((neighbour_x, neighbour_y)) # remove wall from current cell
			stack.put((curr_x+neighbour_x, curr_y+neighbour_y)) # push
algo(0, 0)
show = True

def plot_maze(maze: list, size: int) -> None:
	for i in range(size):
		for j in range(size):
			cell = maze[i][j]
			if cell.walls[(0, 1)]:  # North walls
				plt.plot([i, i+1], [j+1, j+1], 'b-')
			if cell.walls[(1, 0)]:  # West walls
				plt.plot([i+1, i+1], [j, j+1], 'b-')
			if cell.walls[(0, -1)]: # South walls
				plt.plot([i, i+1], [j, j], 'b-')
			if cell.walls[(-1, 0)]: # East walls
				plt.plot([i, i], [j, j+1], 'b-')
			
	plt.show()





























