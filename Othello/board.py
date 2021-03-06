import tkinter as tk
import os
from tkinter import filedialog
#
import const
import move_generator
import Computer

class Board(object):
	""" Board of Reversi. """
	def __init__(self):
		self.boards = None
		self.history = None
		self.current_index = None
		self.pieces_count = None
		self.current_player = None
		self.opponent = None
		self.move_gen = move_generator.MoveGenerator()
		self.computer_player = None
		self.init()

	# Checks validity of a move, than places it.
	def check_move(self, x: int, y: int) -> bool:
		if self.move_gen.legal_move(x, y):
			x,y = self.move_gen.invertor(x, y)
			self.make_move(1 << (x+y))
			return True
		return False

	# Places piece and swaps pieces.
	def make_move(self, pos: int) -> None:
		self.boards[self.current_player], self.boards[self.opponent] = self.move_gen.place_piece(
			self.boards[self.current_player], self.boards[self.opponent], pos)

		self.history.append(self.boards[const.WHITE])
		self.history.append(self.boards[const.BLACK])
		self.swap_players()
		self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])
		self.current_index += 2
		self.count_pieces()

	# Check if there is computer player, and if its his turns, plays move found by it.
	def check_computer(self) -> None:
		if self.computer_player != None:
			if self.current_player == self.computer_player.get_player():
				move = self.computer_player.move(self.boards[self.current_player], self.boards[self.opponent])
				self.make_move(move)

	# Checks if game ended.
	def check_win(self) -> bool:
		if (self.move_gen.possible_moves == 0):
			self.swap_players()
			self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])
			# Both players cant move, end of game.
			if (self.move_gen.possible_moves == 0):
				return True
			return False
		return False

	# Sets variables to default values.
	def init(self) -> None:
		self.remove_computer()
		self.boards = [const.white_start_board, const.black_start_board]
		self.history = [const.white_start_board, const.black_start_board]
		self.current_index = 0
		self.count_pieces()
		self.current_player = const.WHITE
		self.opponent = const.BLACK
		self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])

	# --------- Button functions --------- 

	# In replay state, shows previous move.
	def previous_board(self) -> None:
		if self.current_index-2 >= 0:
			self.current_index -= 2
			self.boards[const.WHITE] = self.history[self.current_index]
			self.boards[const.BLACK] = self.history[self.current_index+1]
			self.count_pieces()
			self.swap_players()

	# In replay state, shows next move.
	def next_board(self) -> None:
		if self.current_index < len(self.history)-2:
			self.current_index += 2
			self.boards[const.WHITE] = self.history[self.current_index]
			self.boards[const.BLACK] = self.history[self.current_index+1]
			self.count_pieces()
			self.swap_players()

	# Saves the game and its history in ".txt" file.
	def save_game(self) -> None:
		# If any moves were played.
		if len(self.history) > 2:
			root = tk.Tk()
			root.withdraw()
			s_file = filedialog.asksaveasfile(initialdir = os.getcwd(), defaultextension = ".txt")
			if s_file:
				for position in self.history:
					s_file.write(str(position)+"\n")
				s_file.write(str(self.current_player))
				s_file.close()
			root.destroy()

	# Loads a game from ".txt" file.
	def load_game(self) -> None:
		root = tk.Tk()
		root.withdraw()
		s_file = filedialog.askopenfile(mode="r", 
			filetypes = [("Text files", "*.txt")], initialdir = os.getcwd())
		if s_file:
			self.history = [int(i) for i in s_file.read().splitlines()]
			s_file.close()
			self.current_player = self.history.pop()
			self.opponent = ((self.current_player + 1) & 1)
			self.boards[const.BLACK] = self.history[-1]
			self.boards[const.WHITE] = self.history[-2]
			self.current_index = len(self.history)-2
			self.count_pieces()
			self.remove_computer()
		root.destroy()
		self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])

	# --------- Utility functions --------- 
	
	# Counts number of pieces for players.
	def count_pieces(self):
		self.pieces_count = []
		self.pieces_count.append(bin(self.boards[const.WHITE]).count("1"))
		self.pieces_count.append(bin(self.boards[const.BLACK]).count("1"))

	# Swaps players.
	def swap_players(self) -> None:
		self.current_player = ((self.current_player + 1) & 1)
		self.opponent = ((self.opponent + 1) & 1)

	# Sets opponent and current player.
	def set_players(self, starting_player):
		self.current_player = starting_player
		self.opponent = ((self.current_player + 1) & 1)
		self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])

	# Adds computer player.
	def start_computer(self, color: int) -> None:
		self.computer_player = Computer.Player(color, (color+1) & 1)

	# Removes computer player.
	def remove_computer(self) -> None:
		self.computer_player = None


if __name__ == '__main__':
	board = Board()
	board.init()
