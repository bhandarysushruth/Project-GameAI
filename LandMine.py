import pygame

DISPLAY_WIDTH = 30
DISPLAY_HEIGHT = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
LANDMINE_IMG = pygame.image.load("landmine.png")
LANDMINE_IMG = pygame.transform.scale(LANDMINE_IMG, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

class LandMine(pygame.sprite.Sprite):
    image = LANDMINE_IMG

    def __init__(self, x, y, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.x = x
        self.y = y
        self.radius = radius

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
