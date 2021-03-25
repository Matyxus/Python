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
				# Score, move saving.
				if (the_score > alpha):
					alpha = the_score
					best_move = move
				# Pruning.
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
				# Score, move saving.
				if (the_score < beta):
					beta = the_score
					best_move = move
				# Pruning.
				if beta <= alpha:
					self.cut_off += 1
					break
			return beta, best_move


