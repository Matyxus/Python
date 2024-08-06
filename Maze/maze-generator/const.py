# ---------- Directions  ----------
from numpy import array
UP    = array([0, 1], dtype=int)  # 1
DOWN  = array([0, -1], dtype=int) # 3
LEFT  = array([-1, 0], dtype=int) # 5
RIGHT = array([1, 0], dtype=int)  # 7
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
INVERTER  : dict = {
	UP.tobytes()    : DOWN,
	DOWN.tobytes()  : UP,
	LEFT.tobytes()  : RIGHT,
	RIGHT.tobytes() : LEFT
}
# ---------- Window --------------
WINDOW_SIZE = array([1024, 768], dtype=int)
BUTTON_SIZE = array([128, 64], dtype=int)
MAZE_WINDOW = array([1024-128, 768], dtype=int)
CELL_SIZE = 64
# ---------- Colors --------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



"""
CELL_ASCII : dict = {
	#   UP DOWN LEFT RIGHT
	#	0	0	0	0
	0 : "   \n   \n",
	#	0	0	0	1
	1  : "   \n  |\n",
	#	0	0	1	0
	2  : "   \n|  \n",
	#	0	0	1	1
	3  : "   \n| |\n",
	#	0	1	0	0
	4  : "   \n___\n",
	#	0	1	0	1
	5  : "   \n__|\n",
	#	0	1	1	0
	6  : "   \n|__\n",
	#	0	1	1	1
	7  : "   \n|_|\n",
	#	1	0	0	0
	8  : "___\n   \n",
	#	1	0	0	1
	9  : "___\n  |\n",
	#	1	0	1	0
	10 : "___\n|  \n",
	#	1	0	1	1
	11 : "___\n| |\n",
	#	1	1	0	0
	12 : "___\n___\n",
	#	1	1	0	1
	13 : "___\n__|\n",
	#	1	1	1	0
	14 : "___\n|__\n",
	#	1	1	1	1
	15 : "___\n|_|\n",
}
"""
if __name__ == "__main__":
	pass
