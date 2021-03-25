from collections import Counter
from copy import deepcopy
import time
class Reversi():
	"""docstring for Board"""
	def __init__(self, Board):
		self.flips = 0
		self.Board = Board
		self.directions = ((1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1), (-1, 0), (0, -1))
		#self.corners = ((0, 0), (7, 7), (0, 7), (7, 0))
		self.to_flip = set()
		self.possible_moves = set()
		self.player = None
		self.opp = None
		self.recently_added = set()
		self.can_flip = {}
		self.positional_values =[[80, -26, 24, -1, -5, 28, -18, 76 ],
								[-23, -39, -18, -9, -6, -8, -39, -1],
								[46, -16, 4, 1, -3, 6, -20, 52],
								[-13, -5, 2, -1, 4, 3, -12, -2],
								[-5, -6, 1, -2, -3, 0, -9, -5],
								[48, -13, 12, 5, 0, 5, -24, 41],
								[-27, -53, -11, -1, -11, -16, -58, -15],
								[87, -25, 27, -1, 5, 36, -3, 100]]

	def play(self, x, y):
		self.x_index = x
		self.y_index = y
		self.Board[x][y] = self.player
		self.flip()

	def flip(self):
		for i in self.directions:
			x = i[0]
			y = i[1]
			if self.valid_dir(self.x_index, self.y_index, x, y) == False:
				continue
			if self.Board[self.x_index+x][self.y_index+y] == self.opp:
				self.direction(self.x_index, self.y_index, x, y)
		#List comprehension ?
		for i in self.to_flip:
			x = i[0]
			y = i[1]
			self.Board[x][y] = self.player
		#Is speed fast ? 
		self.possible_moves.clear()
		self.to_flip.clear()
		self.recently_added.clear()
		self.can_flip.clear()

	def direction(self, x_index, y_index, x, y):
		if x_index+x > 7 or x_index+x < 0 or y_index+y > 7 or y_index+y < 0:
			self.recently_added.clear()
			return None
		if self.Board[x_index+x][y_index+y] == self.opp:
			self.recently_added.add((x_index+x, y_index+y))
			return self.direction(x_index+x, y_index+y, x, y)
		elif self.Board[x_index+x][y_index+y] == self.player:
			for i in self.recently_added:
				self.to_flip.add(i)
			self.recently_added.clear()
			return 0
		elif self.Board[x_index+x][y_index+y] == -1:
			self.recently_added.clear()
			return 0

	def valid_dir(self,x_index, y_index, x, y):
		if x >= 0 and y >= 0:
			if x_index+x > 7 or y_index+y > 7:
				return False
		elif x < 0 and y >=0:
			if x_index+x < 0 or y_index+y > 7:
				 return False
		elif x >=0 and y < 0:
			if x_index+x > 7 or y_index +y < 0:
				return False
		elif x < 0 and y < 0:
			if x_index+y < 0 or y_index+y < 0:
				return False
		return True


	def get_moves(self, player, opp):
		self.possible_moves.clear()
		self.to_flip.clear()
		self.recently_added.clear()
		self.can_flip.clear()
		self.player = player
		self.opp = opp
		self.zeros = sum(row.count(0) for row in self.Board)
		for x_index,row in enumerate(self.Board):
			counter = row.count(self.player)
			if counter>0:
				for y_index, col in enumerate(row):
					if col == self.player:
						for i in self.directions:
							x = i[0]
							y = i[1]
							if self.valid_dir(x_index, y_index, x, y) == False:
								continue
							if self.Board[x_index+x][y_index+y] == self.opp:
								self.flips += 1
								self.find_moves(x_index+x, y_index+y, x, y)
							self.flips = 0
		return self.possible_moves

	def priority_moves(self):
		pushed_moves = []
		if len(self.possible_moves) != 0:
			moves = Counter(self.can_flip)
			highest = moves.most_common(4)
			for i in highest:
				pushed_moves.append(i[0]) 
			#print(self.can_flip, "can_flip")
			#print(self.pushed_moves, "pushed_moves")
			return pushed_moves
		else:
			return self.possible_moves


	def find_moves(self, x_index, y_index, x, y):
		if x_index+x > 7 or x_index+x < 0 or y_index+y > 7 or y_index+y < 0:
			self.flips = 0
			return None
		if self.Board[x_index+x][y_index+y] == self.opp:
			self.flips += 1
			return self.find_moves(x_index+x, y_index+y, x, y)
		elif self.Board[x_index+x][y_index+y] == -1:
			lengt = len(self.possible_moves)
			self.possible_moves.add((x_index+x, y_index+y))
			if len(self.possible_moves) > lengt:
				self.can_flip[(x_index+x, y_index+y)] = self.flips
			self.flips = 0
			return 0


class Smartplayer():
	"""docstring for Smartplayer"""
	def __init__(self, player, opp):
		self.player = player
		self.opp = opp
		self.positional_values =[[1000, -26, 24, -1, -5, 28, -18, 1000],
								[-23, -39, -18, -9, -6, -8, -39, -1],
								[46, -16, 4, 1, -3, 6, -20, 52],
								[-13, -5, 2, -1, 4, 3, -12, -2],
								[-5, -6, 1, -2, -3, 0, -9, -5],
								[48, -13, 12, 5, 0, 5, -24, 41],
								[-27, -53, -11, -1, -11, -16, -58, -15],
								[1000, -25, 27, -1, 5, 36, -3, 1000]]
		self.round = 0
		self.deepround = 0
		self.time_limit = 0.90
		
	def hyper_parametres(self):
		#IMPROVE !
		self.posi = 0.1*(self.round/2) # divide by something or smth
		self.enemy_posi = 0.1*(self.round/2)

		self.num_of_moves = 1*(10/self.round)
		self.num_of_enemy_moves = 1*(10/self.round)

		self.pieces = 1*(self.round/15)
		self.enemy_pieces = 1*(self.round/15)

	def move(self, Matrix):
		self.Matrix = Matrix
		self.Board = Reversi(self.Matrix)
		len_of_moves = len(self.Board.get_moves(self.player, self.opp))
		self.round += 1
		if len_of_moves <4:
			self.depth = 5
		else:
			self.depth = 4
		score, best_move = self.MiniMax(deepcopy(self.Board), self.depth, float("-inf"), float("inf"), True, 0)
		if best_move == (-1, -1):
			return None
		#print(score, "score evaluted for current move")
		return best_move

	def evaluate(self, Board):
		#Setup
		score  = 0
		self.hyper_parametres()
		my_moves = self.Board.get_moves(self.player, self.opp)
		enemy_moves = self.Board.get_moves(self.opp, self.player)
		enemy_count = sum(row.count(self.opp) for row in Board)
		my_count = sum(row.count(self.player) for row in Board)
		cols = [[row[i] for row in Board] for i in range(len(Board))]
		#Winning, losing case
		if enemy_count == 0:
			return float("inf")
		if my_count == 0:
			return float("-inf")
		#Immovable pieces
		score += (sum([1 for row in Board if row.count(self.player) == 8])*30)
		score -= (sum([1 for row in Board if row.count(self.opp) == 8])*30)
		score += (sum([1 for col in cols if col.count(self.player) == 8])*30)
		score -= (sum([1 for col in cols if col.count(self.opp) == 8])*30)
		#Posi Values
		#important mainly in mid almost mid game till few rands in end, should start growing
		score += (sum([(self.positional_values[ix][iy]) for ix, row in enumerate(Board) for iy, i in enumerate(row) if i == self.player])*self.posi)
		score -= (abs(sum([(self.positional_values[ix][iy]) for ix, row in enumerate(Board) for iy, i in enumerate(row) if i == self.opp]))*self.enemy_posi)
		#Less is More -> num of moves
		if len(enemy_moves)==0:
			score += 75
		if len(my_moves) == 0:
			score -= 75
		#Higher for rewarding mobilit in early-mid-game
		score += (len(my_moves)*self.num_of_moves)
		score -= (len(enemy_moves)*self.num_of_enemy_moves)
		#Current pos
		#Doesnt matter that much in late game -> transform as much as possible +-
		score += (sum([self.positional_values[i[0]][i[1]] for i in my_moves])*self.current_moves)
		score -= (sum([self.positional_values[i[0]][i[1]] for i in enemy_moves])*self.current_enemy_moves)
		#Num pieces
		#low in early = higher mobility, starts growing depending on round / deep round
		score += (my_count*self.pieces)
		score -= (enemy_count*self.enemy_pieces)
		#Reset deep moves
		self.deepround = 0
		#Return Score
		return score

	def MiniMax(self, Board, depth, alpha, beta, maximizingPlayer, gamma):
		if gamma > self.time_limit:
			return self.current_best
		start = time.time()
		if maximizingPlayer:
			player, opp = self.player, self.opp
		else:
			player, opp = self.opp, self.player
		moves_list = Board.get_moves(player, opp)
		best_move = (-1,-1)
		# base case
		if (depth==0 or len(moves_list) == 0):
			best_score = self.evaluate(Board.Board)
			best_move  = (-1, -1)
			return best_score, best_move
		# maximizing player
		if maximizingPlayer:
			for move in moves_list:
				new_board = deepcopy(Board)
				new_board.play(move[0], move[1])
				#print(move, "my move")
				end = time.time()
				gamma += end-start
				if gamma > self.time_limit:
					return self.current_best
				self.deepround += 1
				the_score, the_move = self.MiniMax(new_board, depth-1, alpha, beta, False, gamma)
				if (the_score > alpha):
					alpha = the_score
					best_move = move
					if move in self.Board.get_moves(self.player, self.opp):
						self.current_best = (the_score, move)
				if beta <= alpha:
					break
			return alpha, best_move
		# minimzing player
		else:
			for move in moves_list:
				new_board = deepcopy(Board)
				new_board.play(move[0], move[1])
				end = time.time()
				gamma += end-start
				if gamma > self.time_limit:
					return self.current_best
				self.deepround +=1
				the_score, the_move = self.MiniMax(new_board, depth-1, alpha, beta, True, gamma)
				if (the_score < beta):
					beta = the_score
					best_move = move
				if beta <= alpha:
					break
			return beta, best_move

if __name__=="__main__":
	Matrix = [
		[-1, -1, -1, -1, -1, -1, -1, -1 ],
		[-1, -1, -1, -1, -1, -1, -1, -1 ],
		[-1, 1, -1, 1, -1, -1, -1, -1 ],
		[-1, 0, 1, 0, 0, 0, -1, -1 ],
		[-1, -1, -1, 1, 0, -1, -1, -1 ],
		[-1, -1, -1, -1, -1, -1, -1, -1 ],
		[-1, -1, -1, -1, -1, -1, -1, -1 ],
		[-1, -1, -1, -1, -1, -1, -1, -1 ]]
	sm = Smartplayer(1, 0)
	start = time.time()
	print(sm.move(Matrix))
	#print(sm.Board.Board)
	print(sm.Board.get_moves(1, 0))
	end = time.time()
	print(f"Depth {sm.depth} took {end-start} seconds")





























