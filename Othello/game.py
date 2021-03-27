import const
import Buttons
import asset_manager
import board
#
import pygame
import PySimpleGUI as sg

class Othello():
	""" Logic of game Reversi. """
	def __init__(self):
		self.game_board = board.Board()
		self.assets = asset_manager.Asset_manager()
		self.buttons = {}
		self.message = {const.WHITE : "White player won", const.BLACK : "Black player won", const.DRAW : "Draw"}
		self.computer_player = None
		self.done = False
		self.playing = False
		self.re_playing = False
		self.screen = None
		self.clock = None
		#
		self.myFont = None
		self.counts = [None, None]

	# Determines who won.
	def winner(self) -> str:
		white_count = self.game_board.pieces_count[const.WHITE]
		black_count = self.game_board.pieces_count[const.BLACK]
		if (white_count > black_count):
			return self.message[const.WHITE]
		elif (white_count == black_count):
			return self.message[const.DRAW]
		else:
			return self.message[const.BLACK]

	# Initializes images, variables necessary for start.
	def init(self) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode(const.WINDOW_SIZE)
		pygame.display.set_caption("Othello")
		self.clock = pygame.time.Clock()
		self.myFont = pygame.font.SysFont("Times New Roman", 80)
		# Load images.
		if not self.assets.load_images():
			self.quit_game()

		# ------------ Buttons ------------ 
		# Play button.
		self.buttons["play"] = (True, Buttons.Button(pygame.Rect(const.BOARD_SIZE, 
			0, const.BUTTON_WIDTH, const.BUTTON_HEIGHT), self.play,
				self.assets.play_button[self.assets.IDLE], self.assets.play_button[self.assets.HOVER]))

		# Back button.
		self.buttons["back"] = (False, Buttons.Button(pygame.Rect(const.BOARD_SIZE, 
			0, const.BUTTON_WIDTH, const.BUTTON_HEIGHT), self.back,
				self.assets.back_button[self.assets.IDLE], self.assets.back_button[self.assets.HOVER]))

		# Save button.
		self.buttons["save"] = (True, Buttons.Button(pygame.Rect(const.BOARD_SIZE,
			const.BUTTON_HEIGHT+3, const.BUTTON_WIDTH, const.BUTTON_HEIGHT), self.game_board.save_game,
				self.assets.save_button[self.assets.IDLE], self.assets.save_button[self.assets.HOVER]))

		# Load button.
		self.buttons["load"] = (True, Buttons.Button(pygame.Rect(const.BOARD_SIZE,
			const.BUTTON_HEIGHT*2+6, const.BUTTON_WIDTH, const.BUTTON_HEIGHT), self.game_board.load_game,
				self.assets.load_button[self.assets.IDLE], self.assets.load_button[self.assets.HOVER]))

		# Left arrow button.
		self.buttons["left_arrow"] = (False, Buttons.Button(pygame.Rect(const.BOARD_SIZE,
			const.BUTTON_HEIGHT*3+3, 154, const.BUTTON_HEIGHT), self.game_board.previous_board,
				 self.assets.left_arrow[self.assets.IDLE], self.assets.left_arrow[self.assets.HOVER]))

		# Right arrow button.
		self.buttons["right_arrow"] = (False, Buttons.Button(pygame.Rect(const.BOARD_SIZE+154, 
			const.BUTTON_HEIGHT*3+3, 154, const.BUTTON_HEIGHT), self.game_board.next_board,
				self.assets.right_arrow[self.assets.IDLE], self.assets.right_arrow[self.assets.HOVER]))

		# Replay button.
		self.buttons["replay"] = (True, Buttons.Button(pygame.Rect(const.BOARD_SIZE,
			const.BOARD_SIZE-(const.BUTTON_HEIGHT*2)-6, const.BUTTON_WIDTH, const.BUTTON_HEIGHT), self.replay,
				self.assets.replay_button[self.assets.IDLE], self.assets.replay_button[self.assets.HOVER]))

		# Quit button.
		self.buttons["quit"] = (True, Buttons.Button(pygame.Rect(const.BOARD_SIZE,
			const.BOARD_SIZE-const.BUTTON_HEIGHT-3, const.BUTTON_WIDTH, const.BUTTON_HEIGHT), self.quit_game,
				self.assets.quit_button[self.assets.IDLE], self.assets.quit_button[self.assets.HOVER]))
		
	# Draws board and pieces on it.
	def draw_board(self) -> None:
		self.screen.blit(self.assets.gameBoard_img, (0, 0))
		white_board = self.game_board.boards[const.WHITE]
		black_board = self.game_board.boards[const.BLACK]
		for row in range(const.ROW):
			for col in range(const.COLUMN):
				shift = (1 << (63 - (col + const.ROW*row)))
				# White pieces.
				if (shift & white_board):
					self.screen.blit(self.assets.pieces_type[const.WHITE], 
						(const.PIECE_WIDTH*col+2, const.PIECE_HEIGHT*row+2))
				# Black pieces.
				if (shift & black_board):
					self.screen.blit(self.assets.pieces_type[const.BLACK], 
						(const.PIECE_WIDTH*col+2, const.PIECE_HEIGHT*row+2))

	# Draws count of white and black pieces.
	def draw_counts(self) -> None:
		white_count = self.myFont.render(
			str(self.game_board.pieces_count[const.WHITE]), 1, const.COLORS[const.GREY])
		self.screen.blit(white_count, (const.BOARD_SIZE, 390))
		self.screen.blit(self.assets.pieces_type[const.WHITE], 
			(const.BOARD_SIZE+75, 400))
		black_count = self.myFont.render(
			str(self.game_board.pieces_count[const.BLACK]), 1, const.COLORS[const.GREY])
		self.screen.blit(black_count, (const.BOARD_SIZE+150, 390))
		self.screen.blit(self.assets.pieces_type[const.BLACK], 
			(const.BOARD_SIZE+160+70, 400))

	# --------- Main program loop --------- 

	# Starts the game loop.
	def run(self) -> None:
		self.init()
		while not self.done:
			self.render()
			self.events()
		self.quit_game()

	# Renders everything on screen.
	def render(self) -> None:
		self.screen.fill(const.COLORS[const.BLACK])
		self.draw_board()
		self.draw_counts()
		for to_show, button in self.buttons.values():
			if to_show:
				button.display(self.screen)
		pygame.display.update()
		self.clock.tick(30)

	# Takes care of events.
	def events(self) -> None:
		for event in pygame.event.get():
			pos = pygame.mouse.get_pos() 
			if event.type == pygame.QUIT:
				self.quit_game()
			elif event.type == pygame.MOUSEBUTTONDOWN and self.playing:
				# User clicks the mouse. Get the position
				try:
					# Change the x / y screen coordinates to grid coordinates
					row, column = const.row_col_pos(*pos)
					# Placed the piece where user click, if position is valid
					if const.valid_pos(row, column) and self.playing:
						print("Clicked")
						if (self.game_board.check_move(row, column)):
							if (self.game_board.check_win()):
								self.render()
								print(self.winner())
								self.ask_restart()
				except AttributeError:
					print("AttributeError")

			for to_show, button in self.buttons.values():
				if to_show:
					if (button.handle_event(event, *pos)):
						return

	# ----------- Button functions ----------- 

	# Hides button from screen.
	def hide_button(self, button_name: str) -> None:
		button_tuple = self.buttons.get(button_name)
		if button_tuple: # Is not None.
			self.buttons.update({button_name : (False, button_tuple[1])})
		else:
			print(f"Button {button_name} does not exists.")

	# Shows button on screen.
	def show_button(self, button_name: str) -> None:
		button_tuple = self.buttons.get(button_name)
		if button_tuple: # Is not None.
			self.buttons.update({button_name : (True, button_tuple[1])})
		else:
			print(f"Button {button_name} does not exists.")
		
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
					self.game_board.set_players(const.WHITE)
					print("Starting as White")
				else:
					self.game_board.set_players(const.BLACK)
					print("Starting as Black")
			#self.move_gen.generate_moves(self.boards[self.current_player], self.boards[self.opponent])
		else:
			sg.popup_cancel("User aborted")

	# Takes user to replay state.
	def replay(self) -> None:
		self.re_playing = True
		# Show back button, hide replay, play button.
		self.hide_button("play")
		self.show_button("back")
		self.hide_button("replay")
		# Show arrow buttons.
		self.show_button("left_arrow")
		self.show_button("right_arrow")
		
	# Takes user back to starting screen.
	def back(self) -> None:
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
			self.game_board.init()
			# Change first button
			self.computer_player = None
			self.playing = False
			self.hide_button("back")
			self.show_button("play")
			self.show_button("replay")
		else:
			self.quit_game()

	# Exits the game.
	def quit_game(self) -> None:
		pygame.quit()
		quit()


if __name__ == '__main__':
	othello = Othello()
	othello.run()



		