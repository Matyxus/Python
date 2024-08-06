from const import *

class Cell(object):

	def __init__(self):      
		self.walls : dict = {
			UP.tobytes(): True, 
			DOWN.tobytes(): True, 
			RIGHT.tobytes(): True, 
			LEFT.tobytes(): True
		}

	def remove_wall(self, direction : array) -> None:
		self.walls[direction.tobytes()] = False

	def __str__(self) -> str:
		return "Not implemented yet"

if __name__ == "__main__":
	cell = Cell()
	cell.remove_wall(DOWN)
	print(cell.walls)
