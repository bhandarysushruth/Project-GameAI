import pygame
from Movement import *
from Army import *


DISPLAY_WIDTH = 30
DISPLAY_HEIGHT = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
CANNONBALL_IMG = pygame.image.load("cannonball.png")
CANNONBALL_IMG = pygame.transform.scale(CANNONBALL_IMG, (15, 15))


class Cannon(pygame.sprite.Sprite):
    cannon_ball = CANNONBALL_IMG

    def __init__(self, x, y, radius, image):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.x = x
        self.y = y
        self.radius = radius

        # Set the image of the cannon
        self.image = image

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # def fire_cannon(self, x, y, cannon_list):
    #     """ Fires a cannon based on where the mouse coordinates currently are; the left side cannon fires
    #     if the cursor is to the left of XXX and the right side cannon fires if the cursor is to the right
    #     of XXX"""
    #
    #     # Check which cannon's distance is closest to the seek point
    #     cannon_1 = cannon_list[0]
    #     cannon_2 = cannon_list[1]
    #
    #     distance_1 = Movement.calcDistance(cannon_1.x, cannon_1.y, x, y)
    #     distance_2 = Movement.calcDistance(cannon_2.x, cannon_2.y, x, y)
    #
    #     if distance_1 < distance_2: # cannon_1 is closer to the target
    #         return cannon_1, distance_1    # return cannon_1 as cannon to fire from for cannon ball to seek from
    #     else:   # cannon_2 is closer to the target
    #         return cannon_2, distance_2    # return cannon_2 as cannont to fire from for cannon ball to seek from
    #
    # def valid_range(self, distance):
    #     """ Determines whether a target a player is trying to fire a cannon at is within range of thc closest cannon """
    #     if distance <= 450:
    #         return True
    #     else:
    #         return False


# function checks is (x,y is in the range of any cannons)

class CannonBall:
    def __init__(self,platform,cannon_number,destination):
        self.x = platform.cannon_list[cannon_number-1].x
        self.y = platform.cannon_list[cannon_number-1].y
        self.destination = destination
        #self.done = False

    def render(self,gameDisplay):
        pygame.draw.circle(gameDisplay, BLACK,(self.x, self.y), 10)

    def update(self):
        return object_seek(Soldier(self.destination[0], self.destination[1],1,'player'), self, 7)




def InCannonRange(platform, x, y, radius):

    if (calcDistance(platform.cannon_list[0].x, platform.cannon_list[0].y, x, y) < radius) or (calcDistance(platform.cannon_list[1].x, platform.cannon_list[1].y, x, y) < radius):
        return True
    else:
        return False



def selectCannon(x, y, platform):

    # Check which cannon's distance is closest to the seek point
    cannon_1 = platform.cannon_list[0]
    cannon_2 = platform.cannon_list[1]

    distance_1 = calcDistance(cannon_1.x, cannon_1.y, x, y)
    distance_2 = calcDistance(cannon_2.x, cannon_2.y, x, y)

    if distance_1 < distance_2:  # cannon_1 is closer to the target
        return 1  # return cannon_1 as cannon to fire from for cannon ball to seek from
    else:  # cannon_2 is closer to the target
        return 2  # return cannon_2 as cannont to fire from for cannon ball to seek from











