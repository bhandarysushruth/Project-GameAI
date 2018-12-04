import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
LANDMINE_IMG = pygame.image.load("landmine.png")
LANDMINE_IMG = pygame.transform.scale(LANDMINE_IMG, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

class LandMine:
    image = LANDMINE_IMG

    def __init__(self, x, y, radius, ):
        self.x = x
        self.y = y
        self.radius = radius

    def render(self, display):
        display.blit(self.image, (self.x, self.y))