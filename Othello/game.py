import const
import Buttons
import move_generator
import asset_manager
#
import pygame
import PySimpleGUI as sg
import tkinter as tk
import os
from tkinter import filedialog

class Othello():
	""" Logic of game Othello """
	def __init__(self):
		self.current_player = const.WHITE
		self.opponent = const.BLACK
		self.move_gen = move_generator.MoveGenerator()
		self.assets = asset_manager.Asset_manager()
		self.boards = [const.white_start_board, const.black_start_board]
		self.history = [const.white_start_board, const.black_start_board]
		self.buttons = {}
		self.message = {const.WHITE : "White player won", const.BLACK : "Black player won", const.DRAW : "Draw"}
		self.computer_player = None
		self.done = False
		self.playing = False
		self.re_playing = False
		self.screen = None
		self.clock = None
		self.current_index = len(self.history)
	# Swaps players.
	def swap_players(self) -> None:
		temp = self.opponent
		self.opponent = self.current_player
		self.current_player = temp

	# Checks for validity of move, than places it, than checks for win.
	def check_move(self, x: int, y: int) -> None:
		print(f"Checking if move {x, y} is legal")
		if self.move_gen.legal_move(x, y):
			print("Is legal")
			x,y = self.move_gen.invertor(x, y)
			self.make_move(1 << (x+y))
			if (self.check_win()):
				print(self.winner())
				self.ask_restart()

	# Determines who won.
	def winner(self) -> str:
		curr_count = bin(self.boards[self.current_player]).count("1")
		opp_count = bin(self.boards[self.opponent]).count("1")
		if (curr_count > opp_count):
			return self.message[self.current_player]
		elif (curr_count == opp_count):
			return self.message[const.DRAW]
		else:
			return self.message[self.opponent]

	# Places piece and swaps pieces.
	def make_move(self, pos: int) -> None:
		self.boards[self.current_player], self.boards[self.opponent] = self.move_gen.place_piece(
			self.boards[self.current_player], self.boards[self.opponent], pos)

		self.history.append(self.boards[const.WHITE])
		self.history.append(self.boards[const.BLACK])
		self.swap_players()
		self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])

	# Checks if game ended.
	def check_win(self) -> bool:
		if (self.move_gen.possible_moves == 0):
			print("Current player cant make move, swaping")
			self.swap_players()
			self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])
			if (self.move_gen.possible_moves == 0):
				print("End of game, deciding who won")
				return True
			return False
		return False

	# Initializes images, variables necessary for start.
	def init(self) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode(const.WINDOW_SIZE)
		pygame.display.set_caption("Othello")
		self.clock = pygame.time.Clock()
		if not self.assets.load_images():
			pygame.quit()
			quit()
		const.WIDTH = self.assets.gameBoard_img.get_rect()[2]//8
		const.HEIGHT = self.assets.gameBoard_img.get_rect()[3]//8

		# Buttons.
		self.buttons["play"] = (True, Buttons.Button(pygame.Rect(640, 0, 308, 77), self.play,
			self.assets.play_button[self.assets.IDLE], self.assets.play_button[self.assets.HOVER]))

		self.buttons["save"] = (True, Buttons.Button(pygame.Rect(640, 77, 308, 77), self.save_game,
			self.assets.save_button[self.assets.IDLE], self.assets.save_button[self.assets.HOVER]))

		self.buttons["load"] = (True, Buttons.Button(pygame.Rect(640, 77*2, 308, 77), self.load_game,
			self.assets.load_button[self.assets.IDLE], self.assets.load_button[self.assets.HOVER]))

		self.buttons["quit"] = (True, Buttons.Button(pygame.Rect(640, 640-77, 308, 77), self.quit_game,
			self.assets.quit_button[self.assets.IDLE], self.assets.quit_button[self.assets.HOVER]))

		self.buttons["replay"] = (True, Buttons.Button(pygame.Rect(640, 77*4, 308, 77), self.replay,
			self.assets.replay_button[self.assets.IDLE], self.assets.replay_button[self.assets.HOVER]))

		self.buttons["left_arrow"] = (False, Buttons.Button(pygame.Rect(640, 77*5, 154, 77), 
			self.previous_board, self.assets.left_arrow[self.assets.IDLE], self.assets.left_arrow[self.assets.HOVER]))

		self.buttons["right_arrow"] = (False, Buttons.Button(pygame.Rect(640+154, 77*5, 154, 77), 
			self.next_board, self.assets.right_arrow[self.assets.IDLE], self.assets.right_arrow[self.assets.HOVER]))

		self.buttons["back"] = (False, Buttons.Button(pygame.Rect(640, 0, 308, 77), self.back,
			self.assets.back_button[self.assets.IDLE], self.assets.back_button[self.assets.HOVER]))
		

	# Draws board and pieces on it.
	def draw_board(self) -> None:
		self.screen.blit(self.assets.gameBoard_img, (0, 0))
		# blit pieces on left side and their count
		# if self.playing or self.replaying:
		#	.....
		for row in range(const.ROW):
			for col in range(const.COLUMN):
				shift = (1 << (63 - (col + const.ROW*row)))
				# White pieces.
				if (shift & self.boards[const.WHITE]):
					self.screen.blit(self.assets.pieces_type[const.WHITE], 
						(const.piece_width*col+2, const.piece_height*row+2))
				# Black pieces.
				if (shift & self.boards[const.BLACK]):
					self.screen.blit(self.assets.pieces_type[const.BLACK], 
						(const.piece_width*col+2, const.piece_height*row+2))

	# --------- Main program loop --------- 

	# Starts the game loop.
	def run(self):
		self.init()
		while not self.done:
			self.render()
			self.events()
		pygame.quit()
		quit()

	# Renders everything on screen.
	def render(self):
		self.screen.fill(const.COLORS[const.BLACK])
		self.draw_board()
		for to_show, button in self.buttons.values():
			if to_show:
				button.display(self.screen)
		pygame.display.update()
		self.clock.tick(30)

	# Takes care of events.
	def events(self):
		for event in pygame.event.get():
			pos = pygame.mouse.get_pos() 
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN and self.playing:
				# User clicks the mouse. Get the position
				try:
					# Change the x / y screen coordinates to grid coordinates
					row, column = const.row_col_pos(*pos)
					# Placed the piece where user click, if position is valid
					if const.valid_pos(row, column):
						print("Clicked")
						self.check_move(row, column)
				except AttributeError:
					print("AttributeError")

			for to_show, button in self.buttons.values():
				if to_show:
					if (button.handle_event(event, *pos)):
						return

	# ----------- Button funcitons ----------- 

	# Hides button from screen.
	def hide_button(self, button_name: str):
		button_tuple = self.buttons.get(button_name)
		if button_tuple: # Is not None.
			self.buttons.update({button_name : (False, button_tuple[1])})
		else:
			print(f"Button {button_name} does not exists.")

	# Shows button on screen.
	def show_button(self, button_name: str):
		button_tuple = self.buttons.get(button_name)
		if button_tuple: # Is not None.
			self.buttons.update({button_name : (True, button_tuple[1])})
		else:
			print(f"Button {button_name} does not exists.")
		
	# Saves the game and its history in ".txt" file.
	def save_game(self) -> None:
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
			pygame.display.update()
		else:
			print("No moves were played!")

	# Loads a game from ".txt" file.
	def load_game(self) -> None:
		root = tk.Tk()
		root.withdraw()
		s_file = filedialog.askopenfile(mode="r", filetypes = [("Text files", "*.txt")], initialdir = os.getcwd())
		if s_file:
			self.history = [int(i) for i in s_file.read().splitlines()]
			s_file.close()
			self.current_player = self.history.pop()
			self.opponent = ((self.current_player + 1) & 1)
			self.boards[const.BLACK] = self.history[-1]
			self.boards[const.WHITE] = self.history[-2]
			self.current_index = len(self.history)-2
		root.destroy()
		pygame.display.update()
		self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])

	# Asks user if he wants to play against AI, and starting color.
	def play(self) -> None:
		sg.theme("Dark Brown")
		event, values = sg.Window("Game settings", [[sg.Text("Select ->"), 
			sg.Listbox(["Vs AI", "Start as White", "Start as Black"], 
			select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, 3), key="LB")],
		    	[sg.Button("Ok"), sg.Button("Cancel")]], keep_on_top=True).read(close=True)

		if event == "Ok":
			self.playing = True
			# Add back button, hide play button.
			self.hide_button("play")
			self.hide_button("replay")
			self.show_button("back")
			sg.popup(f"You chose {values['LB']}")
			for i in values["LB"]:
				if i == "Vs AI":
					print("Playing against computer")
				elif i == "Start as White":
					self.current_player = const.WHITE
					self.opponent = const.BLACK
					print("Starting as White")
				else:
					self.current_player = const.BLACK
					self.opponent = const.WHITE
					print("Starting as Black")
			self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])
		else:
			sg.popup_cancel("User aborted")

	# Takes user to replay state.
	def replay(self):
		self.re_playing = True
		self.current_index = len(self.history)-2
		# Show back button, hide replay, play button.
		self.hide_button("play")
		self.show_button("back")
		self.hide_button("replay")
		# Show arrow buttons.
		self.show_button("left_arrow")
		self.show_button("right_arrow")
		
	
	# In replay stata, shows previous move.
	def previous_board(self):
		if self.current_index-2 >= 0:
			self.current_index -= 2
			self.boards[const.WHITE] = self.history[self.current_index]
			self.boards[const.BLACK] = self.history[self.current_index+1]

	# In replay state, shows next move.
	def next_board(self):
		if self.current_index < len(self.history)-2:
			self.current_index += 2
			self.boards[const.WHITE] = self.history[self.current_index]
			self.boards[const.BLACK] = self.history[self.current_index+1]

	# Takes user back to starting screen.
	def back(self):
		# Replace first button with "play game", last button with
		self.show_button("play")
		self.hide_button("back")
		self.show_button("replay")
		if self.re_playing:
			self.re_playing = False
			# Hide both arrow buttons.
			self.hide_button("left_arrow")
			self.hide_button("right_arrow")
		self.playing = False
		
	# Asks usert to restart the game.
	def ask_restart(self) -> None:
		sg.theme("Dark Brown")
		event = sg.PopupYesNo("Restart?", keep_on_top=True)
		# Go back to menu
		if event == "Yes":
			self.boards[const.WHITE] = const.white_start_board 
			self.boards[const.BLACK] = const.black_start_board 
			self.history = self.history[:2]
			# Change first button
			self.computer_player = None
			self.playing = False
		else:
			self.quit_game()

	# Exits the game.
	def quit_game(self) -> None:
		pygame.quit()
		quit()


if __name__ == '__main__':
	othello = Othello()
	othello.run()



		