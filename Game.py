import pygame

import Player
import Wall
import Cannon
import LandMine
import AquaticMine
import Ship

# Global variables
DISPLAY_WIDTH = 1440
DISPLAY_HEIGHT = 875
RADIUS = 25
CELL_WIDTH = 100
CELL_HEIGHT = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)

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
cannon_list = []
landmine_list = []
aquamine_list = []

# --- GAME LOOP --- #
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // CELL_WIDTH
            row = pos[1] // CELL_HEIGHT
            print("Click ", pos, "Grid coordinates: ", row, column)

            # If a menu item is selected, perform the required action
            if status == "Create Wall":
                wall = Wall.Wall(pos[0], pos[1], RADIUS)
                wall_list.append(wall)
            elif status == "Create Cannon":
                cannon = Cannon.Cannon(pos[0], pos[1], RADIUS)
                cannon_list = cannon
            elif status == "Create Land Mine":
                land_mine = LandMine.LandMine(pos[0], pos[1], RADIUS)
                landmine_list = land_mine
            elif status == "Create Aquatic Mine":
                aquamine = AquaticMine.AquaticMine(pos[0], pos[1], RADIUS)
                aquadmine_list = aquamine
            # elif status == "Fire Cannon":
                # If cannon in list was clicked
                # Call the fire cannon method

            # # Determine which button was clicked
            # if column == X and row == Y:        # Create wall
            #     status = "Create Wall"
            # elif column == X and row == Y:      # Create cannon
            #     status = "Create Cannon"
            # elif column == X and row == Y:      # Create land mine
            #     status = "Create Land Mine"
            # elif column == X and row == Y:      # Create aquatic mine
            #     status = "Create Aquatic Mine"
            # elif column == X and row == Y:      # Fire cannon
            #     status = "Fire Cannon"
            # elif column == X and row == Y:
            #     status = "None"


    # Drawing to screen
    gameDisplay.blit(background, (0, 0))
    all_sprites_list.update()
    all_sprites_list.draw(gameDisplay)

    clock.tick(25)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()