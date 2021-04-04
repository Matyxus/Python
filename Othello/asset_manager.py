import pygame
import const

class Asset_manager(object):
	""" Holder of images. """
	def __init__(self):
		self.pieces_type = []
		self.play_button = []
		self.quit_button = []
		self.save_button = []
		self.load_button = []
		self.left_arrow = []
		self.right_arrow = []
		self.replay_button = []
		self.back_button = []
		self.gameBoard_img = None
		self.HOVER = 1
		self.IDLE = 0

	# Loads images, returns true on success else false.
	def load_images(self) -> bool:
		try:
			# Pieces.
			self.pieces_type.append(pygame.image.load("Images/whitePiece.png"))
			self.pieces_type.append(pygame.image.load("Images/blackPiece.png"))
			# Gameboard.
			self.gameBoard_img = pygame.image.load("Images/board.png")
			# Play button.
			self.play_button.append(pygame.image.load("Images/startButton.png"))
			self.play_button.append(pygame.image.load("Images/startButton_hover.png"))
			# Quit button.
			self.quit_button.append(pygame.image.load("Images/quitButton.png"))
			self.quit_button.append(pygame.image.load("Images/quitButton_hover.png"))
			# Save button.
			self.save_button.append(pygame.image.load("Images/saveButton.png"))
			self.save_button.append(pygame.image.load("Images/saveButton_hover.png"))
			# Load button.
			self.load_button.append(pygame.image.load("Images/loadButton.png"))
			self.load_button.append(pygame.image.load("Images/loadButton_hover.png"))
			# Left arrow button.
			self.left_arrow.append(pygame.image.load("Images/leftArrow.png"))
			self.left_arrow.append(pygame.image.load("Images/leftArrow_hover.png"))
			# Right arrow button.
			self.right_arrow.append(pygame.image.load("Images/rightArrow.png"))
			self.right_arrow.append(pygame.image.load("Images/rightArrow_hover.png"))
			# Replay button.
			self.replay_button.append(pygame.image.load("Images/replayButton.png"))
			self.replay_button.append(pygame.image.load("Images/replayButton_hover.png"))
			# Back button.
			self.back_button.append(pygame.image.load("Images/backButton.png"))
			self.back_button.append(pygame.image.load("Images/backButton_hover.png"))
			# Setup constants.
			self.set_constants()
		except Exception as e:
			print("Coudnt find images, make sure to not change the name of files or directory.")
			return False
		return True

	# Sets constatns, such as board width etc.
	def set_constants(self) -> None:
		const.WIDTH = self.gameBoard_img.get_width() // const.ROW
		const.HEIGHT = self.gameBoard_img.get_height() // const.COLUMN
		const.PIECE_WIDTH = self.pieces_type[const.WHITE].get_width() + 4
		const.PIECE_HEIGHT = self.pieces_type[const.WHITE].get_height() + 4
		const.BOARD_SIZE = self.gameBoard_img.get_width()
		const.BUTTON_WIDTH = self.play_button[0].get_width()
		const.BUTTON_HEIGHT = self.play_button[0].get_height()

# Check if images can be loaded without error.
if __name__ == '__main__':
	pygame.init()
	man = Asset_manager()
	man.load_images()
	pygame.quit()
	