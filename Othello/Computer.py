import move_generator
import patterns as pt

class Player(object):
	""" Computer player for Othello. """
	def __init__(self, player: int, opponent: int):
		self.player = player
		self.opponent = opponent
		self.depth = 8 # Maximal search depth
		self.move_gen = move_generator.MoveGenerator()
		self.deep_round = 0
		self.cut_off = 0
		self.ordered = 0
		self.cache_hits = 0
		self.curr_round = 0
		self.evaluate = None # Evaluation function.
		# Score rewarding full patern, based on disc count.
		self.rows_cols_count = [0, 0, 0, 0, 1, 2, 5, 7, 10]
		self.side_to_move = 0
		

	# Returns move found by Min-Max, if no move was found, returns 0.
	def move(self, my_board: int, opp_board: int) -> int:
		self.curr_round += 1 # Current round count
		# Clear hash_table every two rounds.
		if self.curr_round%2 == 0:
			self.move_gen.hash_gen.cache.clear()
		self.deep_round = 0
		pieces_count = bin(my_board | opp_board).count("1")
		# Choose evaluation function based on current state of game.
		if pieces_count < 12:
			self.evaluate = self.early_eval
		elif pieces_count >= 12 and pieces_count < 50:
			self.evaluate = self.middle_eval
			self.depth = 6
		else:
			self.depth = 8
			self.evaluate = self.end_eval
		score, move = self.NegaMax(my_board, opp_board, self.depth, float("-inf"), float("inf"), 1)
		return move

	# Simple getter.
	def get_player(self) -> int:
		return self.player

	# -------- Evaluation Helpers -------- 

	# Returns score for pieces, that are adjacents to other same colored pieces.
	def adjacent(self, curr_board: int) -> int:
		score = 0
		# ------ Adjacent Disc ------ 
		# North & South
		north_adjacent = self.move_gen.North(curr_board) & curr_board
		south_adjacent = self.move_gen.South(curr_board) & curr_board
		ns_adjacent = (north_adjacent >> 8) & (south_adjacent << 8)
		score += bin(ns_adjacent).count("1")
		# West & East
		west_adjacent = self.move_gen.West(curr_board) & curr_board
		east_adjacent = self.move_gen.East(curr_board) & curr_board
		we_adjacent = (west_adjacent >> 1) & (east_adjacent << 1)
		score += bin(we_adjacent).count("1")
		# North West & South East
		north_west_adjacent = self.move_gen.NorthWest(curr_board) & curr_board
		south_east_adjacent = self.move_gen.SouthEast(curr_board) & curr_board 
		nw_se_adjacent = (north_west_adjacent >> 9) & (south_east_adjacent << 9)
		score += bin(nw_se_adjacent).count("1")
		# North East & South West
		north_east_adjacent = self.move_gen.NorthEast(curr_board) & curr_board
		south_west_adjacent = self.move_gen.SouthWest(curr_board) & curr_board
		ne_sw_adjacent = ((north_east_adjacent << 1) >> 8) & ((south_west_adjacent >> 1) << 8)
		score += bin(ne_sw_adjacent).count("1")
		# All directions
		all_dir_adjacent = (ns_adjacent & we_adjacent & nw_se_adjacent & ne_sw_adjacent)
		score += bin(all_dir_adjacent).count("1") * 5
		# Pieces that are not adjacent in two directions
		all_adjacent = (ns_adjacent | we_adjacent | nw_se_adjacent | ne_sw_adjacent)
		score -= bin(curr_board^all_adjacent).count("1")
		return score 

	# Check patterns in all directions.
	def patterns(self, board: int) -> int:
		score = 0
		# Pieces that are in full paters of either row/col/diag,
		# add bonus points for being in more than 1 pattern.
		pieces_in_patterns = 0 
		for row, col in zip(pt.row_patterns, pt.col_patterns):
			count = bin(board & row).count("1")
			score += self.rows_cols_count[count]
			count = bin(board & col).count("1")
			score += self.rows_cols_count[count]
			# Full pattern.
			if board & row == row: 
				pieces_in_patterns |= row
			if board & col == col:
				score += bin(col & pieces_in_patterns).count("1")*3
				pieces_in_patterns |= col
		# Left diagonals.
		for diag in pt.diag_patterns:
			count = bin(board & diag).count("1")
			score += self.rows_cols_count[count]
			# Full pattern.
			if board & diag == diag:
				score += bin(diag).count("1")*2
				score += bin(diag & pieces_in_patterns).count("1")
				pieces_in_patterns |= diag
		# Right diagonals.
		for diag in pt.diag2_pattern:
			count = bin(board & diag).count("1")
			score += self.rows_cols_count[count]
			# Full pattern.
			if board & diag == diag:
				score += bin(diag).count("1")*2
				score += bin(diag & pieces_in_patterns).count("1")
		return score

	# Check if there are any discs alone on rows or cols, 
	# in future moves.
	def frontiers(self, board: int, moves: int) -> int:
		score = 0
		while moves:
			move = self.move_gen.bit_scan(moves)
			moves ^= (1 << move)
			x = (7-move//8)
			y = 7-move%8
			row = pt.row_patterns[x] & ((1 << move) | board)
			col = pt.col_patterns[y] & ((1 << move) | board)
			if row == 0:
				score -= 1
			if col == 0:
				score -= 1
			if col == 0 and row == 0:
				score -= 2
		return score

	# Check if moves are adjacent to edges, and
	# if player controls adjacent to edges with edge.
	def edges(self, board: int, moves: int) -> int:
		score = 0
		# Check if moves are adjacent to edges without controling it
		for i in range(4):
			# Moving adjacent to corner and not controling it
			if (pt.corners_adjacent[i] & moves != 0):
				if (pt.corners_alone[i] & board == 0):
					score -= 3
			# Controling corner and pieces adjacent to it.
			if ((pt.corners_adjacent[i] | pt.corners_alone[i]) & board) != 0:
				score += 5
		return score

	# -------- Evaluation Functions -------- 

	# Early game evaluation
	def early_eval(self, curr_board: int, opp_board: int, my_moves: int) -> int:
		score = 0
		opp_moves = self.move_gen.generate_moves(opp_board, curr_board)
		# No moves case.
		if my_moves == 0:
			score -= 7
		if opp_moves == 0:
			score += 7
		my_pieces_count = bin(curr_board).count("1")
		opp_pieces_count = bin(opp_board).count("1")
		# winning, losing case
		if my_moves == 0 and opp_moves == 0:
			if my_pieces_count > opp_pieces_count:
				return 1000000
			elif my_pieces_count == opp_pieces_count:
				return 0
			else:
				return -1000000

		score += bin(curr_board & pt.corners).count("1") * 50
		score -= bin(opp_board & pt.corners).count("1") * 50
		# ------ Center board ------ 
		# Make opponent play outside of center 16.
		score += bin(pt.center & curr_board).count("1")
		score -= bin(pt.center & opp_board).count("1")
		score += bin(pt.center & my_moves).count("1")
		score -= bin(pt.center & opp_moves).count("1")
		# Outer edges of center 16.
		score -= bin(pt.inner_edges & curr_board).count("1")
		score += bin(pt.inner_edges & opp_board).count("1")
		score -= bin(pt.inner_edges & my_moves).count("1")
		score += bin(pt.inner_edges & opp_moves).count("1")
		# ------ Future Moves ------ 
		# Number of moves.
		score += bin(my_moves).count("1")*2
		score -= bin(opp_moves).count("1")*2
		# Moves played on edges.
		score += bin(my_moves & pt.edges).count("1")*3
		score -= bin(opp_moves & pt.edges).count("1")*3
		# Moves on corners.
		score += bin(my_moves & pt.corners).count("1") * 50
		score -= bin(opp_moves & pt.corners).count("1") * 50
		# Adjacent
		score += self.adjacent(curr_board)*2
		score -= self.adjacent(opp_board)*2
		return score

	# Middle game evaluation.
	def middle_eval(self, curr_board: int, opp_board: int, my_moves: int) -> int:
		score = 0
		opp_moves = self.move_gen.generate_moves(opp_board, curr_board)
		my_pieces_count = bin(curr_board).count("1")
		opp_pieces_count = bin(opp_board).count("1")
		# No moves case.
		if my_moves == 0:
			score -= 10
		if opp_moves == 0:
			score += 10
		# Winning, losing, draw case.
		if my_moves == 0 and opp_moves == 0:
			if my_pieces_count > opp_pieces_count:
				return 1000000
			elif my_pieces_count == opp_pieces_count:
				return 0
			else:
				return -1000000
		# ------ Current Board ------ 
		score += (my_pieces_count - opp_pieces_count) * 0.5
		# Corners.
		score += bin(curr_board & pt.corners).count("1") * 50
		score -= bin(opp_board & pt.corners).count("1") * 50
		# Adjacent.
		score += self.adjacent(curr_board) * 0.5
		score -= self.adjacent(opp_board) * 0.5
		# Patterns.
		score += self.patterns(curr_board)
		score -= self.patterns(opp_board)
		# ------ Future Moves ------ 
		# Number of moves.
		score += bin(my_moves).count("1")
		score -= bin(opp_moves).count("1")
		# Moves played on edges.
		score += bin(my_moves & pt.edges).count("1") * 4
		score -= bin(opp_moves & pt.edges).count("1") * 4
		# Moves on corners.
		score += bin(my_moves & pt.corners).count("1") * 50
		score -= bin(opp_moves & pt.corners).count("1") * 50
		# Frontier discs.
		score += self.frontiers(curr_board, my_moves)
		score -= self.frontiers(opp_board, opp_moves)
		# Corners with edges.
		score += self.edges(curr_board, my_moves)
		score -= self.edges(opp_board, opp_moves)
		return score

	# End game evaluaton, prioritize having more discs on board,
	# force opponent to make moves that flip less, call when there is
	# only ~12 empty spaces on board, to find all boards.
	def end_eval(self, curr_board: int, opp_board: int, my_moves: int) -> int:
		score = 0
		opp_moves = self.move_gen.generate_moves(opp_board, curr_board)
		my_pieces_count = bin(curr_board).count("1")
		opp_pieces_count = bin(opp_board).count("1")
		# No moves case.
		if my_moves == 0:
			score -= 30
		if opp_moves == 0:
			score += 30
		# Winning, losing, draw case.
		if my_moves == 0 and opp_moves == 0:
			if my_pieces_count > opp_pieces_count:
				return 1000000
			elif my_pieces_count == opp_pieces_count:
				return 0
			else:
				return -1000000
		# Difference between pieces.
		score += (my_pieces_count - opp_pieces_count)
		# Difference between number of moves.
		my_moves_count = bin(my_moves).count("1")
		opp_moves_count = bin(opp_moves).count("1")
		score += (my_moves_count-opp_moves_count)
		# Check how many pieces can opponent flip.
		opp_flip = 0
		while opp_moves:
			move = (1 << self.move_gen.bit_scan(opp_moves))
			opp_moves ^= move
			opp_flip |= self.move_gen.generate_flipped(opp_board, curr_board, move)
		# Check how many can i flip.
		my_flip = 0
		while my_moves:
			move = (1 << self.move_gen.bit_scan(my_moves))
			my_moves ^= move
			my_flip |= self.move_gen.generate_flipped(curr_board, opp_board, move)
		# Add score based on number of possible flips.
		opp_flip = bin(opp_flip).count("1")
		my_flip = bin(my_flip).count("1")
		score += my_flip
		score -= opp_flip
		# Compare flip counts with number of moves.
		if my_flip >= opp_flip:
			score += 5
			# Bonus score if i can flip more with less moves.
			if my_moves_count <= opp_moves_count:
				score += 15
			else: # Adjust score based on number of moves.
				score -= (opp_moves_count-my_moves_count)
		else: # Less
			score -= 5
			# Adjust score based on number of moves.
			if my_moves_count <= opp_moves_count:
				score += (my_moves_count-opp_moves_count)
			else: # Minus score if i cant flip more with more moves.
				score -= 15
		return score

	#  -------- Search Functions -------- 

	# Orders move from highest scoring to lowest scoring, does by 
	# performing search to depth 2 and evaluating resulting boards, 
	# speeds up search.
	def move_ordering(self, curr_board: int, opp_board: int, my_moves: list) -> list:
		moves = []
		for move in my_moves:
			new_curr_board, new_opp_board = self.move_gen.place_piece(curr_board, opp_board, 1 << move)
			score = self.shallow_search(new_curr_board, new_opp_board, 2, False)
			moves.append((move, score))
		moves = sorted(moves, key=lambda x: x[1], reverse=True)
		return [i[0] for i in moves]

	# Performs shallow search, returns only score.
	def shallow_search(self, curr_board: int, opp_board: int, depth: int, maximizingPlayer: bool) -> int:
		moves_list = self.move_gen.generate_moves(curr_board, opp_board)
		if (depth == 0 or moves_list == 0):
			return self.evaluate(curr_board, opp_board, moves_list)
		# Maximizing player.
		if maximizingPlayer:
			score = float("-inf")
			while moves_list:
					move = (1 << self.move_gen.bit_scan(moves_list))
					moves_list ^= move
					new_curr_board, new_opp_board = self.move_gen.place_piece(curr_board, opp_board, move)
					score = max(score, self.shallow_search(opp_board, curr_board, depth-1, False))
			return score
		# Minimzing player.
		else:
			score = float("inf")
			while moves_list:
					move = (1 << self.move_gen.bit_scan(moves_list))
					moves_list ^= move
					new_curr_board, new_opp_board = self.move_gen.place_piece(curr_board, opp_board, move)
					score = min(score, self.shallow_search(opp_board, curr_board, depth-1, True))
			return score

	# NegaMax algorithm with alpha, beta cut-off.
	def NegaMax(self, curr_board: int, opp_board: int, 
			  	depth: int, alpha: float, beta: float, side_to_move: int) -> tuple:

		self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.sides[self.side_to_move]
		
		# Check if board is in hash cache.
		result = self.move_gen.hash_gen.cache.get(self.move_gen.hash_gen.hash)
		if result and result[2] == depth:
			#self.cache_hits += 1
			return (result[0], result[1])

		moves_list = self.move_gen.generate_moves(curr_board, opp_board)
		best_move = 0
		# End of search, return evaluation.
		if (depth == 0 or moves_list == 0):
			#self.deep_round += 1
			best_score = self.evaluate(curr_board, opp_board, moves_list)
			self.move_gen.hash_gen.cache[self.move_gen.hash_gen.hash] = (side_to_move*best_score, best_move, depth)
			return (side_to_move*best_score, best_move)
		
		score = float("-inf")
		# Creates moves in list, so they can be sorted.
		moves = []
		while moves_list:
			move = self.move_gen.bit_scan(moves_list)
			moves_list ^= (1 << move)
			moves.append(move)
		# Shallow search if depth is > 6, to order moves.
		if depth >= self.depth-2:
			#self.ordered += 1
			moves = self.move_ordering(curr_board, opp_board, moves)

		for move in moves:
			# hash
			new_curr_board, new_opp_board = self.move_gen.place_piece(curr_board, opp_board, (1 << move))
			# Added / Removed pieces on both sides.
			swaped = (opp_board ^ new_opp_board)
			# ------ Hash Change -------
			temp = swaped
			while temp:
				temp_move = self.move_gen.bit_scan(temp)
				temp ^= (1 << temp_move)
				# This pieces was added for one side, removed for other
				self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.hash_table[0][temp_move]
				self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.hash_table[1][temp_move]
			self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.hash_table[self.side_to_move][move]
			# ------ Hash Changed -------
			# Change player
			self.side_to_move = ((self.side_to_move +1) & 1)
			the_score, the_move = self.NegaMax(new_opp_board, new_curr_board, depth-1, -beta, -alpha, -side_to_move)
			# Score comparison.
			if score < -the_score:
				best_move = (1 << move)
				score = -the_score
			# ------ Reverse Hash -------
			# Remove opponent hash
			self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.sides[self.side_to_move]
			while swaped:
				temp_move = self.move_gen.bit_scan(swaped)
				swaped ^= (1 << temp_move)
				# This pieces was added for one side, removed for other
				self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.hash_table[0][temp_move]
				self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.hash_table[1][temp_move]
			# Change player
			self.side_to_move = ((self.side_to_move +1) & 1)
			# Add back the placed one
			self.move_gen.hash_gen.hash ^= self.move_gen.hash_gen.hash_table[self.side_to_move][move]
			# ------ Reversed Hash -------
			# Cut-off.
			alpha = max(alpha, score)
			if alpha >= beta:
				#self.cut_off += 1
				break
		# Insert hash to cache
		self.move_gen.hash_gen.cache[self.move_gen.hash_gen.hash] = (score, best_move, depth)
		return score, best_move

if __name__ == '__main__':
	from timeit import default_timer as timer
	player = Player(0, 1)
	black = 0x810000000
	white = 0x1008000000
	start = timer()
	move = player.move(white, black)
	end = timer()
	# Cache_hits, ordered, cut_off, deep_round are commented out.
	print(f"Calculation took {end-start} seconds.")
	print(f"Number of evaluated nodes: {player.deep_round}")
	print(f"Number of cut-offs: {player.cut_off}")
	print(f"Ordered moves: {player.ordered} times")
	print(f"Hash hits: {player.cache_hits}")
		
