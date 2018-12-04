import pygame

DISPLAY_WIDTH = 30
DISPLAY_HEIGHT = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
AQUAMINE_IMG = pygame.image.load("aquamine.png")
AQUAMINE_IMG = pygame.transform.scale(AQUAMINE_IMG, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


class AquaticMine:
    image = AQUAMINE_IMG

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def render(self, display):
        display.blit(self.image, (self.x, self.y))