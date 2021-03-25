import pygame
import const
import numpy

class Grid(object):
	"""docstring for Grid"""
	def __init__(self, size):
		self.size = size
		self.grid = numpy.zeros((self.size, self.size), dtype=int)
	# Create NxN grid
	def create(self) -> None:
		assert (self.size >= 5 and self.size <= 64)
		self.grid = numpy.zeros((self.size, self.size), dtype=int) # a[15, 1] = 5
	# Takes 2 tuples as arguments
	def start_end_pos(self, start: tuple, end: tuple) -> None:
		self.grid[start] = const.GREEN
		self.grid[end] = const.ACQUA
	# Update grid colors to screen
	def grid_update(self, screen) -> None:
		i = -1
		for row in self.grid:
			i += 1
			j = -1
			for number in row:
				j += 1
				color = const.COLORS[number]
				pygame.draw.rect(screen, color,
				[(const.THICKNESS + const.WIDTH) * j + const.THICKNESS,
				(const.THICKNESS + const.HEIGHT) * i + const.THICKNESS,
				const.WIDTH, const.HEIGHT])
		pygame.display.update()
	# For debugging purposes
	def grid_print(self) -> None:
		print("Now printing grid")
		for row in self.grid:
			print(row)

