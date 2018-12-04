import pygame
import math

DISPLAY_WIDTH = 30
DISPLAY_HEIGHT = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)


class Ship:

    def __init__(self, x, y, velocity, max_vel):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.vel = velocity
        self.max_vel = max_vel

    def move(self, angle, wrap=False):

        if (wrap == False) and ((self.x > DISPLAY_WIDTH - 20) or (self.y > DISPLAY_HEIGHT - 40)):
            self.vel = 0

        self.x += self.vel * math.cos(math.radians(angle))
        self.y += self.vel * math.sin(math.radians(angle))

        if wrap == True:
            self.x %= DISPLAY_WIDTH
            self.y %= DISPLAY_HEIGHT

    def render(self, display):
        pygame.draw.circle(display, (0, 255, 0), (self.x, self.y), 10)