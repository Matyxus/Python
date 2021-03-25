import move_generator

class Smart02(object):
	"""docstring for Smart02"""
	def __init__(self, player, opponent):
		self.player = player
		self.opponent = opponent
		self.move_gen = move_generator.MoveGenerator()
		self.deep_round = 0
		self.cut_off = 0
		self.positional_values =[80, -26, 24, -1, -5, 28, -18, 76,
								-23, -39, -18, -9, -6, -8, -39, -1,
								46, -16, 4, 1, -3, 6, -20, 52,
								-13, -5, 2, -1, 4, 3, -12, -2,
								-5, -6, 1, -2, -3, 0, -9, -5,
								48, -13, 12, 5, 0, 5, -24, 41,
								-27, -53, -11, -1, -11, -16, -58, -15,
								87, -25, 27, -1, 5, 36, -3, 100]

	# Returns move found by Min-Max, if no move was found, returns 0.
	def move(self, my_board: int, opp_board: int) -> int:
		self.deep_round = 0
		self.depth = 7
		score, move = self.search(my_board, opp_board, self.depth, float("-inf"), float("inf"), True)
		print(score)
		if (move != 0):
			self.move_gen.print_board(1 << move)
			return move
		else:
			print("No move found")
		print(f"Nodes searched: {self.deep_round}")
		print(f"Cutoffs: {self.cut_off}")
		return 0

	# Returns numerical evaluation of board.
	def evaluate(self, curr_board: int, opp_board: int) -> int:
		#self.hyper_parametres()
		return (bin(curr_board).count("1") - bin(opp_board).count("1"))

	#
	def hyper_parametres(self):
		self.pos_weight = 0.1*((self.round+self.depth)/2)
		
		self.move_count_weight = (10/(self.round+self.depth))

		self.piece_count_weight = ((self.round+self.depth)/15)

	# Min-Max algorithm with alpha, beta cut-off.
	def search(self, curr_board: int, opp_board: int, 
			  	depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> tuple:

		moves_list = self.move_gen.generate_moves(curr_board, opp_board)
		best_move = 0
		# End of search, return evaluation.
		if (depth == 0 or moves_list == 0):
			best_score = self.evaluate(curr_board, opp_board)
			return best_score, best_move
		self.deep_round += 1
		# Maximizing player.
		if maximizingPlayer:
			while moves_list:
				move = (1 << self.bit_scan(moves_list))
				moves_list ^= move
				new_curr_board, new_opp_board = self.place_piece(curr_board, opp_board, move)
				the_score, the_move = self.search(new_opp_board, new_curr_board, depth-1, alpha, beta, False)
				if (the_score > alpha):
					alpha = the_score
					best_move = move
				if beta <= alpha:
					self.cut_off += 1
					break
			return alpha, best_move
		# Minimzing player.
		else:
			while moves_list:
				move = (1 << self.bit_scan(moves_list))
				moves_list ^= move
				new_curr_board, new_opp_board = self.place_piece(curr_board, opp_board, move)
				the_score, the_move = self.search(new_opp_board, new_curr_board, depth-1, alpha, beta, True)
				if (the_score < beta):
					beta = the_score
					best_move = move
				if beta <= alpha:
					self.cut_off += 1
					break
			return beta, best_move


"""
def convert_to_array(white_board: int, black_board: int) -> list:
	board = [[-1 for i in range(8)] for j in range(8)]
	index = 64
	row = 0
	col = 0
	while white_board or black_board:
		#print(row, col)
		index -= 1
		shift = 1 << index
		assert(row <= 7 and col <= 7)
		if (shift & white_board):
			board[col][row] = const.WHITE
			white_board ^= shift
		elif (shift & black_board):
			board[col][row] = const.BLACK
			black_board ^= shift
		col += 1
		if (col == 8):
			col = 0
			row += 1
	return board

def another_perf(board, depth, player, opp) -> int:
	moves_list = board.get_moves(player, opp)
	if (depth == 0 or len(moves_list) == 0):
		return 1
	count = 0
	for move in moves_list:
		new_board = deepcopy(board)
		new_board.play(move[0], move[1])
		count += another_perf(new_board, depth-1, opp, player)
	return count

def print_board(array: list):
	for i in range(8):
		print(array[i])

def get_index(row, col):
	return (8*(8-row)-col-1)

def get_row_col(index):
	row = index%8
	col = (8-index%8)-1
	return (row, col)

def convert_moves_to_bin(moves_list):
	moves = 0
	for move in moves_list:
		moves |= (1 << get_index(*move))
	return moves


def convert_array_to_bin(array: list) -> tuple:
	white_board = 0
	black_board = 0
	row = 7
	col = 7
	for i in range(64):
		shift = (1 << i)
		assert(row >= 0 and col >= 0 and row <= 7 and col <= 7)
		if array[row][col] == const.WHITE:
			white_board |= shift
		elif array[row][col] == const.BLACK:
			black_board |= shift
		col -= 1
		if (col == -1):
			col = 7
			row -= 1
	return (white_board, black_board)
"""

