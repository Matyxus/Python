import Zobrist
# ----- How it Works -----




# ----- Move Generator -----
class MoveGenerator():
	""" Move generator for Othello (bit-board). """
	def __init__(self):
		self.SHIFT = 8
		self.RIGHT_SIDE = 0xFEFEFEFEFEFEFEFE
		self.LEFT_SIDE = 0x7F7F7F7F7F7F7F7F
		self.BIT_ALIGN64 = 0xFFFFFFFFFFFFFF
		self.directions = [self.North, self.South, self.East, self.West, 
						   self.NorthWest, self.NorthEast, self.SouthWest, self.SouthEast]
		self.possible_moves = 0
		self.hash_gen = Zobrist.Zobrist(0x1008000000, 0x810000000)
		self.count = 0
		self.side_to_move = 0 # White

	# From bit-board prints its binary representation.
	def print_board(self, board: int) -> None:
		# String represantion of board
		print("*"*8)
		string_board = "".join([str(((1 << i) & board) >> i) for i in range(self.SHIFT*self.SHIFT)])[::-1]
		for i in range(self.SHIFT):
			print(string_board[i*self.SHIFT:(self.SHIFT+i*self.SHIFT)])

	# Coords have to be inverted, since they start from left upper corner.
	def invertor(self, x: int, y: int) -> tuple:
		return ((abs(x-7)), abs(8*(y-7)))

	# Check if move is correct. 
	def legal_move(self, x: int, y: int) -> bool:
		x, y = self.invertor(x, y)
		return (((1 << (x+ y)) & self.possible_moves) != 0) 

	""" Directions in which pieces can move. """
	def North(self, board: int) -> int:
		return ((board & self.BIT_ALIGN64) << self.SHIFT)

	def South(self, board: int) -> int:
		return (board >> self.SHIFT)

	def East(self, board: int) -> int:
		return ((board & self.RIGHT_SIDE) >> 1)

	def West(self, board: int) -> int: 
		return ((board & self.LEFT_SIDE) << 1)

	def NorthWest(self, board: int) -> int:
		return ((((board & self.LEFT_SIDE) << 1) & self.BIT_ALIGN64) << self.SHIFT)

	def NorthEast(self, board: int) -> int:
		return ((((board & self.RIGHT_SIDE) >> 1) & self.BIT_ALIGN64) << self.SHIFT)

	def SouthWest(self, board: int) -> int: 
		return (((board & self.LEFT_SIDE) << 1) >> self.SHIFT)

	def SouthEast(self, board: int) -> int: 
		return (((board & self.RIGHT_SIDE) >> 1) >> self.SHIFT)

	# Generates all possible moves.
	# Inputs and output are 64-bit numbers (bitboards).
	def generate_moves(self, curr_board: int, enemy_board: int) -> int:
		self.possible_moves = 0
		# Empty board -> 1 if there is no piece else 0.
		empty_board = ~(curr_board | enemy_board)
		# Search in all directions. 
		for direction in self.directions:
			# Find all adjacent enemy pieces in certain direction
			targets = direction(curr_board) & enemy_board
			# Continue searching for adjacent enemy pieces
			for movement in range(5):
				targets |= direction(targets) & enemy_board
			# Check if there is empty place behind enemy ajdacent pieces
			self.possible_moves |= (direction(targets) & empty_board)
		return self.possible_moves

	# Finds all pieces that should be flipped.
	# Inputs and output are 64-bit numbers (bitboards).
	def generate_flipped(self, curr_board: int, enemy_board: int, pos: int) -> int:
		flip = 0
		# Search in all directions.
		for direction in self.directions:
			# Move the piece on placed position and search for opponent pieces in that direction.
			to_flip = direction(pos)
			# Holder.
			targets = 0
			# This loop will fail when it finds 0 -> empty space or same colored piece.
			while (to_flip & enemy_board):
				targets |= to_flip
				to_flip = direction(to_flip)
			# Check if the last shift found same-colored piece.
			if (to_flip & curr_board):
				flip |= targets
		return flip

	# Places piece, returns modified board.
	# Inputs and outputs are 64-bit numbers (bitboards).
	def place_piece(self, curr_board: int, opp_board: int, pos: int) -> tuple:
		to_swap = self.generate_flipped(curr_board, opp_board, pos)
		#assert(opp_board & to_swap == to_swap)
		opp_board ^= to_swap
		#assert(curr_board & to_swap == 0)
		curr_board |= to_swap
		curr_board |= pos
		return (curr_board, opp_board)

	# Returns least significat set (non zero) bit index.
	# Input and output is number.
	def bit_scan(self, x: int) -> int:
		return ((x&-x).bit_length()-1)

	# Performance and Correctness test with hashing.
	# Inputs are 64-bit numbers (bitboards).
	# Depth is positive integer (recommended under 11).
	def perft_hash(self, curr_board: int, opp_board: int, depth: int):
		# Check hash
		self.hash_gen.hash ^= self.hash_gen.sides[self.side_to_move]
		#hash_now = self.current_hash
		#curr_player = self.side_to_move
		result = self.hash_gen.cache.get(self.hash_gen.hash)
		if result:
			self.count += result
			return
		moves_list = self.generate_moves(curr_board, opp_board)
		count_now = self.count
		# Swap players if depth is not 1.
		if moves_list == 0: # There is only one move.
			if depth == 1: # The only move is to swap players.
				self.count += 1
				#assert(self.hash_gen.cache.get(self.hash_gen.hash) == None)
				self.hash_gen.cache[self.hash_gen.hash] = 1
				return
			else: # Switch to opponent player
				self.side_to_move = ((self.side_to_move +1) & 1)
				self.perft_hash(opp_board, curr_board, depth-1)
				# Unhash opponent
				self.hash_gen.hash ^= self.hash_gen.sides[self.side_to_move]
				#assert(self.hash_gen.hash == hash_now)
				# Switch player back.
				self.side_to_move = ((self.side_to_move +1) & 1)
				#assert(self.hash_gen.cache(self.hash_gen.hash) == None)
				self.hash_gen.cache[self.hash_gen.hash] = (self.count - count_now)
				return
		# Add number of moves and return.		
		if (depth == 1):
			self.count += bin(moves_list).count("1")
			#assert(self.hash_gen.cache.get(self.hash_gen.hash) == None)
			self.hash_gen.cache[self.hash_gen.hash] = (self.count - count_now)
			return
		# Play all possible moves.
		while moves_list:
			move = self.bit_scan(moves_list)
			moves_list ^= (1 << move)
			new_curr_board, new_opp_board = self.place_piece(curr_board, opp_board, 1 << move)
			# Added / Removed pieces on both sides.
			swaped = (opp_board ^ new_opp_board)
			#assert((swaped | curr_board | (1 << move)) == new_curr_board)
			# ------ Hash Change -------
			# Change hash for added piece on move
			self.hash_gen.hash ^= self.hash_gen.hash_table[self.side_to_move][move]
			temp = swaped
			while temp:
				temp_move = self.bit_scan(temp)
				temp ^= (1 << temp_move)
				# This pieces was added for one side, removed for other
				self.hash_gen.hash ^= self.hash_gen.hash_table[0][temp_move]
				self.hash_gen.hash ^= self.hash_gen.hash_table[1][temp_move]
			# ------ Hash Changed -------
			# Change player
			self.side_to_move = ((self.side_to_move +1) & 1)
			self.perft_hash(new_opp_board, new_curr_board, depth-1)
			# ------ Reverse Hash -------
			# Remove opponent hash
			self.hash_gen.hash ^= self.hash_gen.sides[self.side_to_move]
			while swaped:
				temp_move = self.bit_scan(swaped)
				swaped ^= (1 << temp_move)
				# This pieces was added for one side, removed for other
				self.hash_gen.hash ^= self.hash_gen.hash_table[0][temp_move]
				self.hash_gen.hash ^= self.hash_gen.hash_table[1][temp_move]
			# Change player
			self.side_to_move = ((self.side_to_move +1) & 1)
			#assert(curr_player == self.side_to_move)
			# Add back the placed one
			self.hash_gen.hash ^= self.hash_gen.hash_table[self.side_to_move][move]
			# ------ Reversed Hash -------
			#assert(self.hash_gen.hash == hash_now)
		#assert(self.hash_gen.cache.get(self.hash_gen.hash) == None)
		self.hash_gen.cache[self.hash_gen.hash] = (self.count - count_now)
		return

	# Performance and Correctness test.
	def perft(self, curr_board: int, opp_board: int, depth: int):
		moves_list = self.generate_moves(curr_board, opp_board)
		# Swap players if depth is not 1.
		if moves_list == 0: # There is only one move.
			if depth == 1: # The only move is to swap players.
				self.count += 1
				return
			else: # Switch to opponent player
				self.perft(opp_board, curr_board, depth-1)
				return
		# Add number of moves and return.		
		if (depth == 1):
			self.count += bin(moves_list).count("1")
			return
		# Play all possible moves.
		while moves_list:
			move = self.bit_scan(moves_list)
			moves_list ^= (1 << move)
			new_curr_board, new_opp_board = self.place_piece(curr_board, opp_board, 1 << move)
			self.perft(new_opp_board, new_curr_board, depth-1)
		return

# -------- Testing Move Generator -----------
# Time measured on i7-87000
# https://www.chessprogramming.org/Perft
# https://www.aartbik.com/strategy.php
# _________________________________________________________
#| DEPTH |  LEAF_NODES  	| ETA(sec.)   | ETA(sec.) Hash |
#|=======|==================|=============|================|
#|   1   |             4	|	 ~ 0  	  |		~ 0		   |
#|   2   |            12	|	 ~ 0      |		~ 0		   |
#|   3   |            56	|	 ~ 0	  |		~ 0		   |
#|   4   |           244	|	 ~ 0	  |		~ 0		   |
#|   5   |         1.396	|	 ~ 0      |		~ 0		   |
#|   6   |         8.200	|	 ~ 0	  |		~ 0		   |
#|   7   |        55.092	|	 ~ 1	  |		~ 0		   |
#|   8   |       390.216	|	 ~ 1	  |		~ 1		   |
#|   9   |     3.005.288	|	 ~ 9      |		~ 7	   	   |
#|  10   |    24.571.284	|	 ~ 70	  |		~ 50	   |
#|  11   |   212.258.800   	|	 ~ 570	  |		~ 340	   |
#|=======|==================|=============|================|
# Hash collisions can potentionally occur on depth higher
# than 11, not tested, adding depth to hash will extend
# hash space, increasing the depth at which collisions will
# inevitably happen.

if __name__ == '__main__':
	from timeit import default_timer as timer
	move_gen = MoveGenerator()
	black_start_board = 0x810000000
	white_start_board = 0x1008000000
	depth = 8
	assert(depth <= 11) # Takes too long otherwise
	print(f"Calculating number of moves on depth {depth}")
	start = timer()
	move_gen.perft_hash(white_start_board, black_start_board, depth)
	end = timer()
	print(f"Calculation took {end-start} seconds.")
	print(f"Moves found: {move_gen.count}")
	





