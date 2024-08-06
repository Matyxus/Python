from maze import *
import pygame


class Launcher(object):
	""" Launcher for GUI """
	def __init__(self):
		self.size = np.array(MAZE_WINDOW/CELL_SIZE, dtype=float)
		self.maze = Maze(self.size)
		self.UI = None
		# init pygame
		self.buttons : list = []
		self.running = True
		self.screen = None

	def run(self):
		print(f"Maze_display {MAZE_WINDOW}")
		self.buttons = self.create_buttons()
		pygame.init()
		self.screen = pygame.display.set_mode(WINDOW_SIZE)
		pygame.display.set_caption("Maze")
		clock = pygame.time.Clock()
		# Main loop
		self.maze.render(self.screen)
		while self.running:
			self.events()
			clock.tick(60)
		self.exit()

	# Takes care of events.
	def events(self) -> None:
		for event in pygame.event.get():
			pos = pygame.mouse.get_pos() 
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# User clicks the mouse. Get the position
				try:
					print(f"Clicked at {pos}")
				except AttributeError:
					pass
			# Events passed in buttons.
			"""
			for button in self.buttons:
				if (button.handle_event(event, pos)):
					return
			"""

	def create_buttons(self):
		pass

	def render_maze(self):
		for y in range(self.maze.size[1]):
			for x in range(self.maze.size[0]):
				cell = self.maze.grid[y][x]
				"""
				if cell.walls[UP.tobytes()]:    # North walls
					pygame.draw.line(self.screen, WHITE, (i, j), (i*10+10, j))
				if cell.walls[RIGHT.tobytes()]: # West walls
					pygame.draw.line(self.screen, WHITE, (i*10+10, j), (i*10+10, j*10+10))
				if cell.walls[DOWN.tobytes()]:  # South walls
					pygame.draw.line(self.screen, WHITE, (i, j*10+10), (i*10+10, j*10+10))
				"""
				"""
				if cell.walls[LEFT.tobytes()]:  # East walls
					pygame.draw.line(self.screen, WHITE, (x, y), (x, y*10+10))
				"""
				pygame.display.update()
		pygame.display.update()


	def set_size(size: np.array):
		
		self.size = np.array(MAZE_WINDOW/CELL_SIZE, dtype=float)

	def exit(self):
		print("Exiting...")
		quit()



if __name__ == "__main__":
	launch = Launcher()
	launch.run()