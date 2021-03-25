import pygame

class Button(object):
	""" Button class. """
	def __init__(self, rect, callback, image_up, image_down = None):
		self.rect = rect
		self.img_up = image_up
		self.img_down = (image_up if image_down == None else image_down)
		self.callback = callback
		self.display_hover = False

	# Handle events that get passed from the event loop. 
	def handle_event(self, event, x: int, y: int) -> bool:
		if self.rect.collidepoint((x, y)):
			self.display_hover = True	
			if event.type == pygame.MOUSEBUTTONDOWN:
				print('Button pressed.')
				self.callback()
				return True
			return False
		else:
			self.display_hover = False
			return False

	# Display button image, depeding on mouse position.
	def display(self, screen) -> None:
		if self.display_hover:
			screen.blit(self.img_up, (self.rect[0], self.rect[1]))
		else:
			screen.blit(self.img_down, (self.rect[0], self.rect[1]))


		