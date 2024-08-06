# Randomized depth first search
# https://en.wikipedia.org/wiki/Maze_generation_algorithm
from queue import LifoQueue
from Generator import *

class Rdfs(Generator):
	
	def __init__(self):
		super().__init__()
		self.stack = LifoQueue()

	def generate(self, size: tuple, start: tuple, screen):
		random.seed(self.seed)
		self.grid = [[Cell()for j in range(size[0])] for i in range(size[1])]
		self.visited = np.zeros(size, dtype=bool)
		self.size = size
		self.algo(start, screen)

	# Returns direction of neighbours which havent been visited yet
	def get_neighbours(self, pos: np.array) -> list:
		neighbours = []
		for dir in DIRECTIONS:
			new_pos = pos + dir
			if (super().in_bounds(new_pos) and (not self.visited[new_pos[0], new_pos[1]])):
				neighbours.append(dir)
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
	def algo(self, start: tuple, screen) -> None:
		self.visited[start[0], start[1]] = True # Visited
		self.stack.put(np.array(start, dtype=int))
		start = time.time()
		while not self.stack.empty():
			pos = self.stack.get() # Pop
			neighbours = self.get_neighbours(pos) # list of neighbours coords
			if neighbours: # Not empty
				self.stack.put(pos) # push the current cell to stack -> backtracing
				direction = random.choice(neighbours) # choose one of the neighbours at random
				neigh_pos = pos + direction # neighbour position
				self.grid[neigh_pos[0]][neigh_pos[1]].remove_wall(INVERTER[direction.tobytes()]) # remove wall from neighbour
				self.grid[pos[0]][pos[1]].remove_wall(direction) # remove wall from current cell
				self.visited[neigh_pos[0], neigh_pos[1]] = True # visited neighbour
				self.stack.put(neigh_pos) # push
		end = time.time()
		print(f"Time taken: {super().time_in_sec(end-start)}sec.")


	def plot_maze(self) -> None:
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				cell = self.grid[i][j]
				if cell.walls[UP.tobytes()]:    # North walls
					plt.plot([i, i+1], [j+1, j+1], 'b-')
				if cell.walls[RIGHT.tobytes()]: # West walls
					plt.plot([i+1, i+1], [j, j+1], 'b-')
				if cell.walls[DOWN.tobytes()]:  # South walls
					plt.plot([i, i+1], [j, j], 'b-')
				if cell.walls[LEFT.tobytes()]:  # East walls
					plt.plot([i, i], [j, j+1], 'b-')
		plt.show()

	def draw_maze(self) -> None:
		result : str = ("__"*self.size[0]+"\n")
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				cell = self.grid[i][j]
				now = result
				# print left and down
				if cell.walls[LEFT.tobytes()]:  # East walls
					result += "|"
				if cell.walls[DOWN.tobytes()]:  # South walls
					result += "_"
				if result == now:
					result += "  "
			result += "\n"
		print(result)
		print("__"*self.size[0])
		

if __name__ == "__main__":
	rdfs = Rdfs()
	rdfs.generate((16, 16), (0, 0))
	#rdfs.draw_maze()
	#rdfs.plot_maze()

