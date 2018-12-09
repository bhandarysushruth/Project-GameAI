import pygame
import math
from random import randint

DISPLAY_WIDTH = 124
DISPLAY_HEIGHT = 92
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
SHIP_IMG = pygame.image.load("ship.png")
SHIP_IMG = pygame.transform.scale(SHIP_IMG, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

class Ship(pygame.sprite.Sprite):
    hits = 0
    capacity = 100
    image = SHIP_IMG

    def __init__(self, x, y, velocity, max_vel, paths):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.vel = velocity
        self.max_vel = max_vel
        self.path = paths[randint(0,2)]

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, angle, wrap=False):

        if (wrap == False) and ((self.x > DISPLAY_WIDTH - 20) or (self.y > DISPLAY_HEIGHT - 40)):
            self.vel = 0

        self.x += self.vel * math.cos(math.radians(angle))
        self.y += self.vel * math.sin(math.radians(angle))

        if wrap == True:
            self.x %= DISPLAY_WIDTH
            self.y %= DISPLAY_HEIGHT
