import pygame
import math
from random import randint
from Movement import *
from Army import *

DISPLAY_WIDTH = 124
DISPLAY_HEIGHT = 92
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
SHIP_IMG = pygame.image.load("ship.png")
SHIP_IMG = pygame.transform.scale(SHIP_IMG, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

class Ship:
    
    image = SHIP_IMG

    def __init__(self, x, y, velocity, max_vel, paths,path_no,t):
        # Call the parent class (Sprite) constructor
        

        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.vel = randint(velocity, max_vel)
        self.max_vel = max_vel
        self.path = paths[path_no]
        self.target_pier = t
        self.present_seek = self.path[0]

        self.enemies_on_board = 6
        self.reached_pier = False
        self.is_destroyed = False

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    
    def updateShip(self, platform):
        if not self.reached_pier:
            #debugging
            #print("updating")
            #print("seeking : "+str(self.present_seek))
            if self.enemies_on_board == 0:
                self.is_destroyed = True

            target_x= platform.water_nodes[self.present_seek][0]
            target_y= platform.water_nodes[self.present_seek][1]

            present_seek_done = object_seek(Soldier(target_x, target_y, 1,'player'), self, self.vel)

            if present_seek_done:
                self.path.remove(self.present_seek)
                self.present_seek_done = False
                if len(self.path) > 0:
                    self.present_seek = self.path[0]
                else:
                    self.reached_pier = True
                    self.disembark(platform)

    def render(self, gameDisplay):
        # pygame.draw.circle(gameDisplay, WHITE,(self.x, self.y), 7)
        gameDisplay.blit(SHIP_IMG, (self.x, self.y))

    def disembark(self,platform):
        print("disembarking")
        disembarking_points = platform.disembarking_points[self.target_pier]
        platoon_number = len(platform.enemyPlatoons) + 1
        for i in range(self.enemies_on_board):
            x_cord=disembarking_points[i][0]
            y_cord=disembarking_points[i][1]
            platform.enemyArmy.append(Soldier(x_cord,y_cord, platoon_number, 'enemy'))
        platform.enemyPlatoons.append(Platoon(platform,platoon_number,'enemy'))
        

















