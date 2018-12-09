import pygame


class Goal:
    """ Represents the touch point by the castle that the enemy soldiers need to get to to win """
    tagged = 0  # After 5 tags, the player loses

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        # Create a rectangle that represents the goal area
        self.image = pygame.Surface([width, height])

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()