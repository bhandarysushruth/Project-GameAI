import pygame

import Player
import Wall
import Cannon
import LandMine
import AquaticMine
import Ship
import Movement

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
RCROSSHAIR = pygame.image.load("redcross.png")
RCROSSHAIR = pygame.transform.scale(RCROSSHAIR, (15, 15))

# General game set up
pygame.init()
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('PROTECT THE CASTLE')
done = False
clock = pygame.time.Clock()

# Setting up mouse info
pygame.mouse.set_visible(True)
all_sprites_list = pygame.sprite.Group()
player = Player.Player()
all_sprites_list.add(player)

# Initializing game assets
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Initializing button  menu
status = ""
wall_list = []
cannon_list = [Cannon.Cannon(540, 410, RADIUS, LCANNON_IMG), Cannon.Cannon(800, 390, RADIUS, RCANNON_IMG)]
all_sprites_list.add(cannon_list[0])
all_sprites_list.add(cannon_list[1])
landmine_list = []
aquamine_list = []

# Some game functions
def fire_cannon(x, y, cannon_list):
    """ Fires a cannon based on where the mouse coordinates currently are; the left side cannon fires
    if the cursor is to the left of XXX and the right side cannon fires if the cursor is to the right
    of XXX"""

    # Check which cannon's distance is closest to the seek point
    cannon_1 = cannon_list[0]
    cannon_2 = cannon_list[1]

    distance_1 = Movement.calcDistance(cannon_1.x, cannon_1.y, x, y)
    distance_2 = Movement.calcDistance(cannon_2.x, cannon_2.y, x, y)

    if distance_1 < distance_2:  # cannon_1 is closer to the target
        return cannon_1, distance_1  # return cannon_1 as cannon to fire from for cannon ball to seek from
    else:  # cannon_2 is closer to the target
        return cannon_2, distance_2  # return cannon_2 as cannont to fire from for cannon ball to seek from


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
                wall_list.append(wall)
            elif status == "Create Land Mine":
                land_mine = LandMine.LandMine(pos[0], pos[1], RADIUS)
                landmine_list = land_mine
            elif status == "Create Aquatic Mine":
                aquamine = AquaticMine.AquaticMine(pos[0], pos[1], RADIUS)
                aquamine_list = aquamine
            elif status == "Fire Cannon":
                results = fire_cannon(pos[0], pos[1], cannon_list)
                print(results[0])
                print(results[1])
                # Determine if range is valid and update crosshair colour to green
                if (results[1] <= 450):
                    player.image = GCROSSHAIR
                else:
                    player.image = RCROSSHAIR
                # Pass in the appropriate cannon's coordinates to seek from and shoot the cannon


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
    all_sprites_list.update()
    all_sprites_list.draw(gameDisplay)

    clock.tick(25)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()