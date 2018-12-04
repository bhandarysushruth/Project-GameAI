import pygame

DISPLAY_WIDTH = 30
DISPLAY_HEIGHT = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
CANNONBALL_IMG = pygame.image.load("cannonball.png")
CANNONBALL_IMG = pygame.transform.scale(CANNONBALL_IMG, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


class Cannon:
    image = CANNONBALL_IMG

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def render(self, display):
        pygame.draw.circle(display, (0, 255, 0), (self.x, self.y), 10)

    def fire_cannon(self, x, y, display):
        """ Fires a cannon based on where the mouse coordinates currently are; the left side cannon fires
        if the cursor is to the left of XXX and the right side cannon fires if the cursor is to the right
        of XXX"""
        display.blit(self.image, (self.x, self.y))


