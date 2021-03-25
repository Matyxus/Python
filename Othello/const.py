# constantss
WINDOW_SIZE = [948, 640]
WHITE = 0
BLACK = 1
DRAW = 2
COLORS = [(255, 255, 255), (0, 0, 0)]
ROW = COLUMN = 8
WIDTH = 20
HEIGHT = 20
THICKNESS = 1
piece_width = 40*2
piece_height = 40*2
# start of the game
black_start_board = 0x810000000
white_start_board = 0x1008000000

# Center mouse positon to grid coordinates.
def row_col_pos(pos_x: int, pos_y: int) -> tuple:
	#print(WIDTH, HEIGHT)
	row = pos_x // (WIDTH + THICKNESS)
	column = pos_y // (HEIGHT + THICKNESS)
	return (row, column)

# Check if the position is on board.
def valid_pos(x: int, y: int) -> bool:
	return ((x >= 0 and x < ROW) and (y >= 0 and y < COLUMN))

