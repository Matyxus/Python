# Constants
WINDOW_SIZE = [800, 800]
WHITE = 0
GREEN = 1
RED = 2
BLUE = 3
BLACK = 4
ACQUA = 5
COLORS = [(255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 0, 0), (0, 255, 255)]
# Grid sizes
grid_size = 38
WIDTH = 20
HEIGHT = 20
THICKNESS = 1

# Center mouse positon to grid coordinates
def row_col_pos(pos_x: int, pos_y: int) -> tuple:
	column = pos_x // (WIDTH + THICKNESS)
	row = pos_y // (HEIGHT + THICKNESS)
	return (row, column)




