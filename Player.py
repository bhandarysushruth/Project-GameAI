import pygame

DISPLAY_WIDTH = 15
DISPLAY_HEIGHT = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
CROSSHAIR = pygame.image.load("redcross.png")
CROSSHAIR = pygame.transform.scale(CROSSHAIR, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

class Player(pygame.sprite.Sprite):
    """ Player class that controls actions using the mouse"""

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set the crosshair image
        self.image = CROSSHAIR

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    def update(self):
        # Get the current mouse position.
        pos = pygame.mouse.get_pos()

        # Fetch the x and y out of the list
        x = pos[0]
        y = pos[1]

        # Set the attribute for the top left corner where this object is located
        self.rect.x = x
        self.rect.y = y