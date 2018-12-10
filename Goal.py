import pygame

WIDTH = 30
HEIGHT = 30

class Goal:
    """ Represents the touch point by the castle that the enemy soldiers need to get to to win """
    offset = WIDTH + 20

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Create a rectangle that represents the goal area
        self.image = pygame.Surface([WIDTH, HEIGHT])

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y