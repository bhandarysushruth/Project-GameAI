import pygame

import Player
import Wall
from Cannon import *
import LandMine
import AquaticMine
import Ship
from Movement import *
from Army import *
import Path
import Graph
from Strategies import *


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

# variables
status = ""
cannon_range = 400
cannon_blast_radius = 40
#cannon_fire = "deactive"

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
        self.playerPlatoons = []
        self.enemyPlatoons = []
        self.activeCannonBalls=[]



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
    
    

    #creating a platoon object with all the members of platoon1 and adding it to platform
    platform.playerPlatoons.append(Platoon(platform,1,'player'))


    #platoon 2
    platform.playerArmy.append(Knight(980,408, 2, 'player'))
    platform.playerArmy.append(Soldier(950,400, 2, 'player'))
    platform.playerArmy.append(Soldier(965,400, 2, 'player'))
    platform.playerArmy.append(Soldier(950,415, 2, 'player'))
    platform.playerArmy.append(Knight(935,408, 2, 'player'))
    platform.playerArmy.append(Soldier(965,415, 2, 'player'))
    
        
    platform.playerPlatoons.append(Platoon(platform,2,'player'))



    # enemy platoon 1
    platform.enemyArmy.append(Knight(750,610, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(765,610, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(750,625, 1, 'enemy'))
    platform.enemyArmy.append(Knight(765,625, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(735,615, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(735,630, 1, 'enemy'))

    platform.enemyPlatoons.append(Platoon(platform,1,'enemy'))

    #enemy platoon 2
    platform.enemyArmy.append(Knight(600,610, 2, 'enemy'))
    platform.enemyArmy.append(Soldier(615,610, 2, 'enemy'))
    platform.enemyArmy.append(Soldier(600,625, 2, 'enemy'))
    platform.enemyArmy.append(Knight(615,625, 2, 'enemy'))
    #platform.enemyArmy.append(Soldier(585,615, 2, 'enemy'))
    #platform.enemyArmy.append(Soldier(585,630, 2, 'enemy'))

    platform.enemyPlatoons.append(Platoon(platform,2,'enemy'))

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
        if not InCannonRange(platform, pos[0], pos[1], cannon_range):
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
                elif event.key == pygame.K_c:
                    if InCannonRange(platform,pos[0],pos[1],cannon_range):
                        cannon_number = selectCannon(pos[0],pos[1],platform)
                        platform.activeCannonBalls.append(CannonBall(platform,cannon_number,(pos[0],pos[1])))


        # Drawing to screen
        gameDisplay.blit(background, (0, 0))


        #--------------- CREATING A MINE ------

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

            status = "None"
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

        #-----------------/ CREATING A MINE------------------

        #------------ CHECKING FOR CONTACT WITH MINES--------------------

        for platoon in platform.playerPlatoons:
            for mine in platform.landmine_list:
                d=calcDistance(mine.x, mine.y, platoon.avg_coord[0],platoon.avg_coord[1])
                if d < 30:
                    destroyPlatoon(platoon)
                    platform.landmine_list.remove(mine)
                    platform.all_sprites_list.remove(mine)

        for platoon in platform.enemyPlatoons:
            for mine in platform.landmine_list:
                d=calcDistance(mine.x, mine.y, platoon.avg_coord[0],platoon.avg_coord[1])
                if d < 30:
                    destroyPlatoon(platoon)
                    platform.landmine_list.remove(mine)
                    platform.all_sprites_list.remove(mine)

        #------------ /CHECKING FOR CONTACT WITH MINES--------------------

        #------------ CANNON FIRING ------------------------------

        if len(platform.activeCannonBalls) > 0:
            for cannon_ball in platform.activeCannonBalls:
                reached_dest = cannon_ball.update()
                cannon_ball.render(gameDisplay)
                if reached_dest:
                    destroy(platform, cannon_ball.destination, cannon_blast_radius)
                    platform.activeCannonBalls.remove(cannon_ball)

        #------------ /CANNON FIRING ------------------------------




        # Drawing to screen
        #gameDisplay.blit(background, (0, 0))

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

        # testing fire cannon
        # platform.activeCannonBalls.append(CannonBall(platform,1))
        # platform.activeCannonBalls.append(CannonBall(platform,2))
        # for cannon_ball in platform.activeCannonBalls:
        #     cannon_ball.render(gameDisplay)

        #-----------------------------------

        # checking if anyone is in attacking range
        for player in platform.playerPlatoons:
            for enemy in platform.enemyPlatoons:
                player.update()
                enemy.update()
                d = calcDistance(player.avg_coord[0],player.avg_coord[1],enemy.avg_coord[0],enemy.avg_coord[1])
                #print('distance = '+str(d))
                if d < 50:
                    Attack(player,enemy)


        # rendering the soldiers on the game screen
        for character in platform.playerArmy:
            character.render(gameDisplay)
        for character in platform.enemyArmy:
            character.render(gameDisplay)


        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
        clock.tick(25)