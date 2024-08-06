from Generator import *

class Maze(object):
	"""docstring for Maze"""
	def __init__(self, size: np.array, algorithm=None):
		print(f"Initializing maze with size:{size}")
		self.size = size
		self.algorithm = algorithm
		self.grid = (self.empty_grid() if algorithm == None else algorithm.generate(size))

	def empty_grid(self) -> list:
		return [[Cell() for j in range(int(self.size[0]))] for i in range(int(self.size[1]))]

	def render(self, screen):
		if self.algorithm != None:
			self.algorithm.generate(screen, self.size)
		else: # Empty maze
			for y in range(int(self.size[1])):
				y_shift = y * CELL_SIZE
				for x in range(int(self.size[0])):
					pygame.draw.rect(
						screen, # Display
						WHITE,  # Color 
						pygame.Rect(CELL_SIZE*x, y_shift, CELL_SIZE, CELL_SIZE), # Rect
						1 # Width 
					)
					pygame.display.update()


if __name__ == "__main__":
	maze = Maze(np.array((10, 10), dtype=int))

		