import random
random.seed(42)
#https://en.wikipedia.org/wiki/Zobrist_hashing
class Zobrist(object):
	"""docstring for Zobrist"""
	def __init__(self, white_board: int, black_board: int):
		self.hash_table = [[random.getrandbits(64) for i in range(8*8)], 
			[random.getrandbits(64) for i in range(8*8)]]
		self.sides = [random.getrandbits(64) , random.getrandbits(64)]
		self.cache = {}
		self.hash = self.create_hash(white_board, black_board)

	def create_hash(self, white_board: int, black_board: int) -> int:
		val = 0
		board = (white_board | black_board) # Combine both boards together.
		while board:
			index = self.bit_scan(board) # Find index of some piece.
			board ^= (1 << index) # Remove it from board.
			# Do (piece_pos & black_board), it returns either 0
			# or number that is not 0, hence comparison with 0
			# we get True -> 1 or False -> 0, from that
			# we get index 0 -> White, 1 -> Black
			val ^= self.hash_table[((1 << index) & black_board) != 0][index]
		return val

	# Returns least significat bit index.	
	def bit_scan(self, x: int) -> int:
		return ((x&-x).bit_length()-1)
		