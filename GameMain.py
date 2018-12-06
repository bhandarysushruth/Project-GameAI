import pygame

import Player
import Wall
import Cannon
import LandMine
import AquaticMine
import Ship
import Movement


from Army import *

# Global variables
DISPLAY_WIDTH = 1440
DISPLAY_HEIGHT = 875
RADIUS = 25
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
LCANNON_IMG = pygame.image.load("lcannon.png")
LCANNON_IMG = pygame.transform.scale(LCANNON_IMG, (50, 50))
RCANNON_IMG = pygame.image.load("rcannon.png")
RCANNON_IMG = pygame.transform.scale(RCANNON_IMG, (50, 50))

# General game set up
pygame.init()
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('PROTECT THE CASTLE')
done = False
clock = pygame.time.Clock()

# # Create backing graph
# graph = []
# for r in range(80):
#     # Add an empty array that will hold each cell in this row
#     graph.append([])
#     for c in range(80):
#         graph[r].append(0)  # Append a cell


# Initializing game assets
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Initializing button  menu
status = ""
# wall_list = []
# cannon_list = []
# landmine_list = []
# aquamine_list = []

class Blackboard:

    def __init__(self, platform):
        self.platform = platform

class GamePlatform:

    def __init__(self):
        self.wall_list = []
        self.cannon_list = []
        self.landmine_list = []
        self.aquamine_list = []
        self.playerArmy = []
        self.enemyArmy = []
        self.all_sprites_list = []


# Some game functions
def fire_cannon(x, y, platform):
    """ Fires a cannon based on where the mouse coordinates currently are; the left side cannon fires
    if the cursor is to the left of XXX and the right side cannon fires if the cursor is to the right
    of XXX"""

    # Check which cannon's distance is closest to the seek point
    cannon_1 = platform.cannon_list[0]
    cannon_2 = platform.cannon_list[1]

    distance_1 = Movement.calcDistance(cannon_1.x, cannon_1.y, x, y)
    distance_2 = Movement.calcDistance(cannon_2.x, cannon_2.y, x, y)

    if distance_1 < distance_2:  # cannon_1 is closer to the target
        return cannon_1, distance_1  # return cannon_1 as cannon to fire from for cannon ball to seek from
    else:  # cannon_2 is closer to the target
        return cannon_2, distance_2  # return cannon_2 as cannont to fire from for cannon ball to seek from




if __name__ == '__main__':

    # Setting up mouse info
    pygame.mouse.set_visible(True)
    #all_sprites_list = pygame.sprite.Group()

    platform = GamePlatform()
    bb= Blackboard(platform)

    #populating the Game Platform

    platform.all_sprites_list = pygame.sprite.Group()
    platform.all_sprites_list.add(Player.Player())
    platform.cannon_list = [Cannon.Cannon(540, 410, RADIUS, LCANNON_IMG), Cannon.Cannon(800, 390, RADIUS, RCANNON_IMG)]
    platform.all_sprites_list.add(platform.cannon_list[0])
    platform.all_sprites_list.add(platform.cannon_list[1])

    # Creating Player Armies

    #platoon1
    platform.playerArmy.append(Soldier(450,400, 1, 'player'))
    platform.playerArmy.append(Soldier(465,400, 1, 'player'))
    platform.playerArmy.append(Soldier(450,415, 1, 'player'))
    platform.playerArmy.append(Soldier(465,415, 1, 'player'))
    platform.playerArmy.append(Knight(435,408, 1, 'player'))
    platform.playerArmy.append(Knight(480,408, 1, 'player'))

    #platoon 2
    platform.playerArmy.append(Soldier(950,400, 1, 'player'))
    platform.playerArmy.append(Soldier(965,400, 1, 'player'))
    platform.playerArmy.append(Soldier(950,415, 1, 'player'))
    platform.playerArmy.append(Soldier(965,415, 1, 'player'))
    platform.playerArmy.append(Knight(935,408, 1, 'player'))
    platform.playerArmy.append(Knight(980,408, 1, 'player'))

    pos = pygame.get_pos()

    # --- GAME LOOP --- #
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                print("Click ", pos)

                # If a menu item is selected, perform the required action
                if status == "Create Wall":
                    wall = Wall.Wall(pos[0], pos[1], RADIUS)
                    platform.wall_list.append(wall)
                elif status == "Create Land Mine":
                    land_mine = LandMine.LandMine(pos[0], pos[1], RADIUS)
                    platform.landmine_list.append(land_mine)
                elif status == "Create Aquatic Mine":
                    aquamine = AquaticMine.AquaticMine(pos[0], pos[1], RADIUS)
                    platform.aquamine_list.append(aquamine)
                elif status == "Fire Cannon":
                    print(fire_cannon(pos[0], pos[1], platform)[0])

            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so adjust speed.
                if event.key == pygame.K_l:
                    status = "Create Land Mine"
                elif event.key == pygame.K_a:
                    status = "Create Aquatic Mine"
                elif event.key == pygame.K_f:
                    status = "Fire Cannon"
                elif event.key == pygame.K_n:
                    status = "None"


        # Drawing to screen
        gameDisplay.blit(background, (0, 0))
        platform.all_sprites_list.update()
        platform.all_sprites_list.draw(gameDisplay)


        # rendering the soldiers on the game screen
        for character in platform.playerArmy:
            character.render(gameDisplay)


        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
        clock.tick(25)