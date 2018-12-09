import pygame

import Door
import Goal
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
    gate = None
    goal = None

    def __init__(self):
        self.wall_list = []
        self.cannon_list = []
        self.landmine_list = []
        self.aquamine_list = []
        self.ship_list = []
        self.playerArmy = []
        self.enemyArmy = []
        self.ship_paths = []
        self.island_nodes = []
        self.all_sprites_list = []
        self.playerPlatoons = []
        self.enemyPlatoons = []

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


def find_route(pos, dest, node_list):
    """ Given the initial position of a land unit, find a path from its position to an end position """

    # Variable to hold the result path
    result_path = []

    # Get start position
    x1 = pos[0]
    y1 = pos[1]

    # Initialize variables for loop
    closest_node = None
    distance = 2000  # Arbitrary large distance that can't exist between values for this display size

    # Find closest start node
    for node in node_list:
        distance_from_start = calcDistance(x1, y1, node.point.x, node.point.y)
        if (distance_from_start < distance):
            distance = distance_from_start
            closest_node = node
    result_path.append(closest_node)
    # print("start node #: ", closest_node.number)
    source = closest_node.number

    # Count nodes going forward (clockwise)
    forward_list = []
    # print("forward loop")
    # Determine starting index
    start = source
    if source == len(node_list) - 1:
        start = 0
    # print("starting at node: ", start)
    # Look for nodes
    for i in range(start, len(node_list)):
        if node_list[i].number == dest:
            forward_list.append(node_list[i])
            # print("appended node ", node_list[i].number)
            break
        forward_list.append(node_list[i])
        # print("appended node ", node_list[i].number)
        if i + 1 == len(node_list):
            for j in range(0, start):
                if node_list[j].number == dest:
                    forward_list.append(node_list[i])
                    # print("appended node ", node_list[j].number)
                    break
                forward_list.append(node_list[j])
                # print("appended node ", node_list[j].number)

    # Count nodes going backward (counter clockwise)
    backward_list = []
    # print("backward loop")
    # Determine the starting index
    if source == 0:
        backward_list.append(node_list[source])
        source = len(node_list) - 1
    for i in range(source, 0, -1):
        if node_list[i].number == dest:
            backward_list.append(node_list[i])
            # print("appended node ", node_list[i].number)
            break
        backward_list.append(node_list[i])
        # print("appended node ", node_list[i].number)
        if i == 0:
            for j in range(len(node_list), source, -1):
                if node_list[j].number == source or node_list[j].number == dest:
                    backward_list.append(node_list[i])
                    # print("appended node ", node_list[j].number)
                    break
                backward_list.append(node_list[j])
                # print("appended node ", node_list[j].number)

    # Compare which path is shorter
    # print("length of forward: ", len(forward_list))
    # print("length of backward: ", len(backward_list))

    if len(forward_list) < len(backward_list):
        return forward_list
    else:
        return backward_list

if __name__ == '__main__':

    # --- Mouse set up
    pygame.mouse.set_visible(True)
    cursor_type = 'green'

    # --- Set up game platform
    platform = GamePlatform()
    bb= Blackboard(platform)

    # --- Populating the Game Platform
    platform.all_sprites_list = pygame.sprite.Group()
    # Create 2 cannons, left and right
    platform.cannon_list = [Cannon(540, 410, RADIUS, LCANNON_IMG), Cannon(800, 390, RADIUS, RCANNON_IMG)]
    platform.all_sprites_list.add(platform.cannon_list[0])
    platform.all_sprites_list.add(platform.cannon_list[1])
    # Create gate to siege
    platform.gate = Door.Door(661, 525)
    platform.all_sprites_list.add(platform.gate)
    # Create goal for enemies
    platform.goal = Goal.Goal(711, 444, 10, 10)

    # --- Creating Player Armies

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

    # --- Determine routes for ships that will be used randomly for ships
    g1 = Graph.Graph()
    g2 = Graph.Graph()

    # Adjacency list in the form of a matrix
    graph1 = [[0, 5, 0, 0, 0, 10, 0, 0],
              [0, 0, 5, 0, 0, 0, 0, 0],
              [0, 0, 0, 5, 0, 0, 0, 0],
              [0, 0, 0, 0, 5, 0, 0, 0],
              [0, 0, 0, 5, 0, 0, 0, 30],
              [0, 0, 0, 0, 0, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 10],
              [0, 0, 0, 0, 0, 0, 0, 0]]
    graph2 = [[0, 5, 0],
              [0, 0, 5],
              [0, 0, 0]]

    # Node mapping and creates the shortest path from source to destination via graph 1
    node0 = Path.Node(0, Path.Point(70, 55))
    node1 = Path.Node(1, Path.Point(174, 287))
    node2 = Path.Node(2, Path.Point(160, 720))
    node3 = Path.Node(3, Path.Point(556, 779))
    node4 = Path.Node(4, Path.Point(1007, 672))
    node5 = Path.Node(5, Path.Point(678, 73))
    node6 = Path.Node(6, Path.Point(1092, 204))
    node7 = Path.Node(7, Path.Point(1224, 447))
    nodearray1 = [node0, node1, node2, node3, node4, node5, node6, node7]
    path_ship_1 = g1.dijkstra(graph1, 0, 1)
    path_ship_2 = g1.dijkstra(graph1, 0, 4)

    # Node mapping and creates the shortest path from source to destination via graph 1
    node_one = Path.Node(0, Path.Point(70, 55))
    node_two = Path.Node(1, Path.Point(678, 73))
    node_three = Path.Node(2, Path.Point(1092, 204))
    nodearray2 = [node_one, node_two, node_three]
    path_ship_3 = g2.dijkstra(graph2, 0, 2)

    # Converts the result path to one with nodes from the node array
    result_path_1 = g1.convertpath(path_ship_1, nodearray1)
    result_path_2 = g1.convertpath(path_ship_2, nodearray1)
    result_path_3 = g2.convertpath(path_ship_3, nodearray2)

    # Add these possible paths to the list
    platform.ship_paths.append(result_path_1)
    platform.ship_paths.append(result_path_2)
    platform.ship_paths.append(result_path_3)

    # Creates a path object and a path from the shortest path found
    # path_1_object = Path.Path().createpath(result_path_1)
    # print(path_1_object)
    # path_2_object = Path.Path().createpath(result_path_2)
    # path_3_object = Path.Path().createpath(result_path_3)

    # Create 3 ships
    platform.ship_list.append(Ship.Ship(100, 100, 0, 10, platform.ship_paths))
    platform.ship_list.append(Ship.Ship(100, 100, 0, 10, platform.ship_paths))
    platform.ship_list.append(Ship.Ship(100, 100, 0, 10, platform.ship_paths))
    for ship in platform.ship_list:
        platform.all_sprites_list.add(ship)

    # --- Determine routes for soldiers once they reach the island
    platform.island_nodes.append(Path.Node(0, Path.Point(466, 348)))
    platform.island_nodes.append(Path.Node(1, Path.Point(630, 239)))
    platform.island_nodes.append(Path.Node(2, Path.Point(805, 259)))
    platform.island_nodes.append(Path.Node(3, Path.Point(916, 484)))
    platform.island_nodes.append(Path.Node(4, Path.Point(800, 579)))
    platform.island_nodes.append(Path.Node(5, Path.Point(555, 560)))

    # --- Testing paths
    # ex_pos1 = [355, 418]
    # ex_pos1 = [875, 682]
    # onepath = find_route(ex_pos1, 4, platform.island_nodes)
    # onepath = find_route(ex_pos1, 2, platform.island_nodes)
    # print(onepath)

    pos = pygame.mouse.get_pos()

    # --- GAME LOOP --- #
    while not done:

        # Checking if cannons are in range to select color of crosshair
        pos = pygame.mouse.get_pos()
        if not InCannonRange(platform, pos[0], pos[1], 200):
            cursor_type = 'red'
        else:
            cursor_type = 'green'

        # Checking for mouse clicks and key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                print("Click ", pos, status)
            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so adjust speed.
                if event.key == pygame.K_m:
                    status = "Create Mine"
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

        if status == "Create Mine":
            x1, y1 = pos
            x2, y2 = island_circle.center
            distance = math.hypot(x1 - x2, y1 - y2)

            if distance <= ISLAND_RADIUS:
            # If the mouse is colliding with the land circle, create a landmine
                land_mine = LandMine.LandMine(pos[0] - 15, pos[1] - 15, RADIUS)
                platform.landmine_list.append(land_mine)
                platform.all_sprites_list.add(land_mine)
            # Else create an aquatic mine
            else:
                aquamine = AquaticMine.AquaticMine(pos[0] - 15, pos[1] - 15, RADIUS)
                platform.aquamine_list.append(aquamine)
                platform.all_sprites_list.add(aquamine)

            status = "None"
        elif status == "Fire Cannon":
            print(fire_cannon(pos[0], pos[1], platform)[0])

        #------------ CHECKING FOR CONTACT WITH MINES--------------------

        for platoon in platform.playerPlatoons:
            for mine in platform.landmine_list:
                d=calcDistance(mine.x, mine.y, platoon.avg_coord[0],platoon.avg_coord[1])
                if d < 30:
                    destroyPlatoon(platoon)
                    platform.landmine_list.remove(mine)
                    platform.all_sprites_list.remove(mine)

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
        # path_1_object.draw(gameDisplay, path_1_object.path)

        # random tests ------------------------

        # testing platoon update
        # for plat in platform.platoons:
        #     plat.update()
        #     print(plat.total_health)

        #testing ATTACK
        # Attack(platform.playerPlatoons[0], platform.enemyPlatoons[0])

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

        # Check if an enemy soldier is at the gate or the goal
        for platoon in platform.enemyPlatoons:
            for enemy in platoon:
                # Get the position of the enemy player
                pos = [enemy.x, enemy.y]

                # Check if this enemy is at the gate
                if platform.gate.rect.collidepoint(pos):
                    platform.gate.tagged = platform.gate.tagged + 1

                    #

                # Checking enemies at the goal
                if platform.goal.rect.collidepoint(pos):
                    platform.goal.tagged = platform.goal.tagged + 1

                    # If 5 enemies have reached the goal, the game is over


        # rendering the soldiers on the game screen
        for character in platform.playerArmy:
            character.render(gameDisplay)
        for character in platform.enemyArmy:
            character.render(gameDisplay)


        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
        clock.tick(25)