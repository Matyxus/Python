import numpy as np
import matplotlib.pyplot as plt
import random
import time
import pygame
from Cell import *


class Generator(object):
	""" Base class for algorithms that generate mazes """
	def __init__(self):
		self.seed : int = 42
		self.grid : list
		self.visited : np.array
		self.size : tuple

	def in_bounds(self, pos: np.array) -> bool:
		return ((0 <= pos[0] < self.size[0]) and (0 <= pos[1] < self.size[1]))

	def generate(self, size: tuple, start: tuple, screen):
		pass

	def plot_maze(self) -> None:
		pass

	def time_in_sec(self, amount : float):
		return (round((amount / (10**9)), 3))

		