import pygame

import Player
import Wall
from Cannon import *
import LandMine
import AquaticMine
import Ship
from Movement import *
from Army import *

# Global variables
DISPLAY_WIDTH = 1440
DISPLAY_HEIGHT = 875
RADIUS = 25
ISLAND_RADIUS = 380
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)

# Loading images
LCANNON_IMG = pygame.image.load("lcannon.png")
LCANNON_IMG = pygame.transform.scale(LCANNON_IMG, (64, 40))
RCANNON_IMG = pygame.image.load("rcannon.png")
RCANNON_IMG = pygame.transform.scale(RCANNON_IMG, (65, 42))
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Crosshair instead of cursor
pointerImgRed = pygame.image.load('redcross.png')
pointerImgRed = pygame.transform.scale(pointerImgRed, (30,30))
pointerImgRed_rect = pointerImgRed.get_rect()
pointerImgGreen = pygame.image.load('BlackCross.png')
pointerImgGreen = pygame.transform.scale(pointerImgGreen, (30,30))
pointerImgGreen_rect = pointerImgGreen.get_rect()

# General game set up
pygame.init()
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('PROTECT THE CASTLE')
done = False
clock = pygame.time.Clock()

# Identify water areas vs land areas
island_circle = pygame.draw.circle(gameDisplay, BLACK, (703, 406), ISLAND_RADIUS, 0)

# Initializing button menu
status = ""

# Defining main classes
class Blackboard:

    def __init__(self, platform):
        self.platform = platform
        self.platoon_seek_active = False
        #contains a list of all the active platoon_seeks
        #each entry in the list is a set which contains the platoon number, target cordinates, team
        #for example, if you want the player platoon number 1 to move to (100,100), you do
        # active_platoon_seeks.append((1, 100, 100, 'player'))
        self.active_platoon_seeks = []
    
    def update(self):
        if self.platoon_seek_active:
            for seeks in self.active_platoon_seeks:
                seek_done = platoon_seek(self.platform, seeks[0], seeks[1], seeks[2], seeks[3])
                if seek_done:
                    self.active_platoon_seeks.remove(seeks)

            if len(self.active_platoon_seeks) == 0:
                platoon_seek_active = False

class GamePlatform:

    def __init__(self):
        self.wall_list = []
        self.cannon_list = []
        self.landmine_list = []
        self.aquamine_list = []
        self.ship_list = []
        self.playerArmy = []
        self.enemyArmy = []
        self.all_sprites_list = []


# Defining some game functions
def fire_cannon(x, y, platform):
    """ Fires a cannon based on where the mouse coordinates currently are; the left side cannon fires
    if the cursor is to the left of XXX and the right side cannon fires if the cursor is to the right
    of XXX"""

    # Check which cannon's distance is closest to the seek point
    cannon_1 = platform.cannon_list[0]
    cannon_2 = platform.cannon_list[1]

    distance_1 = calcDistance(cannon_1.x, cannon_1.y, x, y)
    distance_2 = calcDistance(cannon_2.x, cannon_2.y, x, y)

    if distance_1 < distance_2:  # cannon_1 is closer to the target
        return cannon_1, distance_1  # return cannon_1 as cannon to fire from for cannon ball to seek from
    else:  # cannon_2 is closer to the target
        return cannon_2, distance_2  # return cannon_2 as cannont to fire from for cannon ball to seek from


if __name__ == '__main__':

    # Setting up mouse info
    pygame.mouse.set_visible(True)
    cursor_type = 'green'
    #all_sprites_list = pygame.sprite.Group()

    platform = GamePlatform()
    bb= Blackboard(platform)

    #populating the Game Platform

    platform.all_sprites_list = pygame.sprite.Group()
    #platform.all_sprites_list.add(Player.Player())
    platform.cannon_list = [Cannon(540, 410, RADIUS, LCANNON_IMG), Cannon(800, 390, RADIUS, RCANNON_IMG)]
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
    platform.playerArmy.append(Soldier(950,400, 2, 'player'))
    platform.playerArmy.append(Soldier(965,400, 2, 'player'))
    platform.playerArmy.append(Soldier(950,415, 2, 'player'))
    platform.playerArmy.append(Soldier(965,415, 2, 'player'))
    platform.playerArmy.append(Knight(935,408, 2, 'player'))
    platform.playerArmy.append(Knight(980,408, 2, 'player'))

    #create 3 ships
    platform.ship_list.append(Ship.Ship(100, 100, 0, 10))
    platform.ship_list.append(Ship.Ship(1000, 100, 0, 10))
    platform.ship_list.append(Ship.Ship(1200, 700, 0, 10))
    for ship in platform.ship_list:
        platform.all_sprites_list.add(ship)

    pos = pygame.mouse.get_pos()

    # --- GAME LOOP --- #
    while not done:

        #checking if cannons are in range to select color of crosshair
        pos = pygame.mouse.get_pos()
        if not InCannonRange(platform, pos[0], pos[1], 200):
            cursor_type = 'red'
        else:
            cursor_type = 'green'


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                print("Click ", pos, status)

                # If a menu item is selected, perform the required action
                if status == "Create Mine":
                    x1, y1 = pos
                    x2, y2 = island_circle.center
                    distance = math.hypot(x1 - x2, y1 - y2)

                    if distance <= ISLAND_RADIUS:
                        # self.radius = self.radius // 2
                    # If the mouse is colliding with the land circle, create a landmine
                    # if island_circle.get_rect().collidepoint(pygame.mouse.get_pos()):
                        land_mine = LandMine.LandMine(pos[0] - 15, pos[1] - 15, RADIUS)
                        platform.landmine_list.append(land_mine)
                        platform.all_sprites_list.add(land_mine)
                    # Else create an aquatic mine
                    else:
                        aquamine = AquaticMine.AquaticMine(pos[0] - 15, pos[1] - 15, RADIUS)
                        platform.aquamine_list.append(aquamine)
                        platform.all_sprites_list.add(aquamine)
                # if status == "Create Land Mine":
                #     land_mine = LandMine.LandMine(pos[0]-15, pos[1]-15, RADIUS)
                #     platform.landmine_list.append(land_mine)
                #     platform.all_sprites_list.add(land_mine)
                # elif status == "Create Aquatic Mine":
                #     aquamine = AquaticMine.AquaticMine(pos[0]-15, pos[1]-15, RADIUS)
                #     platform.aquamine_list.append(aquamine)
                #     platform.all_sprites_list.add(aquamine)
                elif status == "Fire Cannon":
                    print(fire_cannon(pos[0], pos[1], platform)[0])

            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so adjust speed.
                if event.key == pygame.K_m:
                    status = "Create Mine"
                # if event.key == pygame.K_l:
                #     status = "Create Land Mine"
                # elif event.key == pygame.K_a:
                #     status = "Create Aquatic Mine"
                elif event.key == pygame.K_f:
                    status = "Fire Cannon"
                elif event.key == pygame.K_n:
                    status = "None"
                elif event.key == pygame.K_1:
                    bb.platoon_seek_active = True
                    bb.active_platoon_seeks.append((1,pos[0],pos[1],'player'))
                elif event.key == pygame.K_2:
                    bb.platoon_seek_active = True
                    bb.active_platoon_seeks.append((2,pos[0],pos[1],'player'))


        # Drawing to screen
        gameDisplay.blit(background, (0, 0))

        # displaying crosshairs
        if cursor_type == 'red':
            pointerImgRed_rect.center = pygame.mouse.get_pos()
            gameDisplay.blit(pointerImgRed, pointerImgRed_rect)
        elif cursor_type == 'green':
            pointerImgGreen_rect.center = pygame.mouse.get_pos()
            gameDisplay.blit(pointerImgGreen, pointerImgGreen_rect)

        bb.update()
        platform.all_sprites_list.update()
        platform.all_sprites_list.draw(gameDisplay)
        
        # random tests ------------------------

        # testing platoon_seek fucntion

        #moving platoon number 1
        #platoon_seek(platform, 1, 450, 600, 'player')
        #moving platoon2
        #platoon_seek(platform, 2, 950, 280, 'player')

        #-----------------------------------

        # rendering the soldiers on the game screen
        for character in platform.playerArmy:
            character.render(gameDisplay)


        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
        clock.tick(25)