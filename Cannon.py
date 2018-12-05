import pygame
import Movement

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

    def fire_cannon(self, x, y, cannon_list, display):
        """ Fires a cannon based on where the mouse coordinates currently are; the left side cannon fires
        if the cursor is to the left of XXX and the right side cannon fires if the cursor is to the right
        of XXX """

        # Check which cannon's distance is closest to the seek point
        cannon_1 = cannon_list[0]
        cannon_2 = cannon_list[1]

        distance_1 = Movement.calcDistance()
        distance_2 = Movement.calcDistance()
        display.blit(self.image, (self.x, self.y))




