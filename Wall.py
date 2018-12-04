import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)


class Wall:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def render(self, display):
        pygame.draw.circle(display, (0, 255, 0), (self.x, self.y), 10)