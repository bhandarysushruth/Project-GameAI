import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)


class Player(pygame.sprite.Sprite):
    """ Player class that controls actions using the mouse"""

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Variables to hold the height and width of the block
        width = 15
        height = 15

        # Create an image of the player, and fill it with a color.
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

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