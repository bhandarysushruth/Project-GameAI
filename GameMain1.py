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
import Door
import Goal



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
background = pygame.image.load("background_1.png")
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
PAUSE_IMG = pygame.image.load("pause.png")
PAUSE_IMG = pygame.transform.scale(PAUSE_IMG, (1440, 878))
WIN_IMG = pygame.image.load("win_image.png")
WIN_IMG = pygame.transform.scale(WIN_IMG, (350, 200))
LOST_IMG = pygame.image.load("lost_image.png")
LOST_IMG = pygame.transform.scale(LOST_IMG, (300, 180))


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


# GLOBAL VARIABLE
status = ""
cannon_range = 400
cannon_blast_radius = 40
cannon_count = 0
cannon_limit = 10
is_paused = False
enemy_seek_location = (689,565)
mine_limit = 5
mine_count = 0
has_won = False
has_lost = False

# Defining main classes
class Blackboard:

    def __init__(self, platform):
        self.platform = platform
        self.platoon_seek_active = False
        self.enemy_platoon_seek_active = False
        #contains a list of all the active platoon_seeks
        #each entry in the list is a set which contains the platoon number, target cordinates, team, path
        #for example, if you want the player platoon number 1 to move to (100,100), you do
        # active_platoon_seeks.append((1, 100, 100, 'player', path_list))
        #the path is calculated by the find route function to make sure that 
        # if the the seek is on the other side of the wall, it circumnavigates the walls
        self.active_platoon_seeks = []
        self.enemy_active_platoon_seeks = []
    
    def update(self):
        if self.platoon_seek_active:
            for seeks in self.active_platoon_seeks:
                if len(seeks[4]) > 0:
                    seek_done = platoon_seek(self.platform, seeks[0], seeks[4][0].point.x, seeks[4][0].point.y, seeks[3])
                    if seek_done:
                        del seeks[4][0]
                else:
                    seek_done = platoon_seek(self.platform, seeks[0], seeks[1], seeks[2], seeks[3])
                    if seek_done:
                        self.active_platoon_seeks.remove(seeks)

            if len(self.active_platoon_seeks) == 0:
                platoon_seek_active = False
    
    def updateEnemy(self):
        if self.enemy_platoon_seek_active:
            for seeks in self.enemy_active_platoon_seeks:
                if len(seeks[4]) > 0:
                    seek_done = platoon_seek(self.platform, seeks[0], seeks[4][0].point.x, seeks[4][0].point.y, seeks[3])
                    if seek_done:
                        del seeks[4][0]
                else:
                    seek_done = platoon_seek(self.platform, seeks[0], seeks[1], seeks[2], seeks[3])
                    if seek_done:
                        self.enemy_active_platoon_seeks.remove(seeks)

            if len(self.enemy_active_platoon_seeks) == 0:
                platoon_seek_active = False    

class GamePlatform:

    #gate = None
    #goal = None
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
        self.ship_paths = []
        self.island_nodes = []
        self.water_nodes = []
        self.disembarking_points = []
        self.gate = None
        self.goal = None

# ------------------- FUCNTION TO FIND A ROUTE ----------------

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

# ------------------- /FUCNTION TO FIND A ROUTE ----------------

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
    # Create gate to siege
    platform.gate = Door.Door(661, 525)
    # print(platform.gate)
    # print("avadvv------")
    platform.all_sprites_list.add(platform.gate)
    # Create goal for enemies
    platform.goal = Goal.Goal(711, 444)


    # Creating Player Armies

    #platoon1
    
    platform.playerArmy.append(Soldier(525,600, 1, 'player'))
    platform.playerArmy.append(Soldier(510,600, 1, 'player'))
    platform.playerArmy.append(Soldier(510,615, 1, 'player'))
    platform.playerArmy.append(Soldier(525,615, 1, 'player'))
    platform.playerArmy.append(Knight(540,600, 1, 'player'))
    platform.playerArmy.append(Knight(540,615, 1, 'player'))
    
    

    #creating a platoon object with all the members of platoon1 and adding it to platform
    platform.playerPlatoons.append(Platoon(platform,1,'player'))


    #platoon 2
    platform.playerArmy.append(Knight(730,630, 2, 'player'))
    platform.playerArmy.append(Soldier(715,630, 2, 'player'))
    platform.playerArmy.append(Soldier(715,645, 2, 'player'))
    platform.playerArmy.append(Soldier(730,645, 2, 'player'))
    platform.playerArmy.append(Knight(745,630, 2, 'player'))
    platform.playerArmy.append(Soldier(745,645, 2, 'player'))
    
        
    platform.playerPlatoons.append(Platoon(platform,2,'player'))

    #platoon 3
    platform.playerArmy.append(Knight(900,600, 3, 'player'))
    platform.playerArmy.append(Soldier(900,585, 3, 'player'))
    platform.playerArmy.append(Soldier(915,600, 3, 'player'))
    platform.playerArmy.append(Soldier(915,585, 3, 'player'))
    platform.playerArmy.append(Knight(930,600, 3, 'player'))
    platform.playerArmy.append(Soldier(930,585, 3, 'player'))
    
        
    platform.playerPlatoons.append(Platoon(platform,3,'player'))



    # enemy platoon 1
    platform.enemyArmy.append(Knight(400,320, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(400,305, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(415,320, 1, 'enemy'))
    platform.enemyArmy.append(Knight(415,305, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(385,320, 1, 'enemy'))
    platform.enemyArmy.append(Soldier(385,305, 1, 'enemy'))

    platform.enemyPlatoons.append(Platoon(platform,1,'enemy'))

    #enemy platoon 2
    platform.enemyArmy.append(Knight(900,345, 2, 'enemy'))
    platform.enemyArmy.append(Soldier(900,320, 2, 'enemy'))
    platform.enemyArmy.append(Soldier(915,345, 2, 'enemy'))
    platform.enemyArmy.append(Knight(915,320, 2, 'enemy'))
    platform.enemyArmy.append(Soldier(930,345, 2, 'enemy'))
    platform.enemyArmy.append(Soldier(930,320, 2, 'enemy'))

    platform.enemyPlatoons.append(Platoon(platform,2,'enemy'))





    disembark0 = [(350,450),(350,435),(350,415),(365,450),(365,435),(365,415)]
    disembark1 = [(850, 660),(865, 660),(880, 660),(850, 645),(865, 645),(880, 645)]
    disembark2 = [(1020, 305),(1005, 305),(990, 305),(1020, 330),(1005, 330),(990, 330)]
    disembarks = [disembark0,disembark1,disembark2]
    platform.disembarking_points = disembarks


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
    # node0 = Path.Node(0, Path.Point(100, 55))
    # node1 = Path.Node(1, Path.Point(174, 287))
    # node2 = Path.Node(2, Path.Point(160, 720))
    # node3 = Path.Node(3, Path.Point(556, 779))
    # node4 = Path.Node(4, Path.Point(1007, 672))
    # node5 = Path.Node(5, Path.Point(678, 73))
    # node6 = Path.Node(6, Path.Point(1092, 204))
    # node7 = Path.Node(7, Path.Point(1224, 447))
    # nodearray1 = [node0, node1, node2, node3, node4, node5, node6, node7]
    # platform.water_nodes = nodearray1

    node0=(100,100)
    node1=(124,420)
    node2=(265,758)
    node3=(602,809)
    node4=(898,758)
    node5=(1090,251)
    node6=(700,25)
    node_array=[node0,node1,node2,node3,node4,node5,node6]
    platform.water_nodes = node_array



    # path_ship_1 = g1.dijkstra(graph1, 0, 1)
    path_ship_1 = [1]
    # path_ship_2 = g1.dijkstra(graph1, 0, 4)
    path_ship_2 = [6,5]
    # path_ship_3 = [0, 5, 6]
    path_ship_3 = [1,2,3,4]

    #debugging :
    # print("here")
    print(path_ship_1, path_ship_2, path_ship_3)

    # Node mapping and creates the shortest path from source to destination via graph 1
    node_one = Path.Node(0, Path.Point(70, 55))
    node_two = Path.Node(1, Path.Point(678, 73))
    node_three = Path.Node(2, Path.Point(1092, 204))
    nodearray2 = [node_one, node_two, node_three]
    

    # Converts the result path to one with nodes from the node array
    # result_path_1 = g1.convertpath(path_ship_1, nodearray1)
    # result_path_2 = g1.convertpath(path_ship_2, nodearray1)
    # result_path_3 = g2.convertpath(path_ship_3, nodearray2)

    # Add these possible paths to the list
    platform.ship_paths.append(path_ship_1)
    platform.ship_paths.append(path_ship_2)
    platform.ship_paths.append(path_ship_3)

    # Create 3 ships
    platform.ship_list.append(Ship.Ship(100, 100, 5, 15, platform.ship_paths, 1, 2))
    platform.ship_list.append(Ship.Ship(100, 110, 5, 15, platform.ship_paths, 2, 1))
    platform.ship_list.append(Ship.Ship(101, 101, 5, 15, platform.ship_paths, 0,0))
    
    # for ship in platform.ship_list:
    #     platform.all_sprites_list.add(ship)

    # --- Determine routes for soldiers once they reach the island
    platform.island_nodes.append(Path.Node(0, Path.Point(410, 348)))
    platform.island_nodes.append(Path.Node(1, Path.Point(630, 200)))
    platform.island_nodes.append(Path.Node(2, Path.Point(805, 220)))
    platform.island_nodes.append(Path.Node(3, Path.Point(935, 484)))
    platform.island_nodes.append(Path.Node(4, Path.Point(800, 590)))
    platform.island_nodes.append(Path.Node(5, Path.Point(530, 580)))
    # ex_pos1 = [355, 418]
    ex_pos1 = [435, 607]
    # onepath = find_route(ex_pos1, 4, platform.island_nodes)
    onepath = find_route(ex_pos1, 3, platform.island_nodes)

    print("testing island nodes")
    for n in onepath:
        print(n.number)



    pos = pygame.mouse.get_pos()


    #---------------- ENEMY PLATOONS SEEKING DOOR ------------------------
    #finding the closest node to door. (Right now seeking a random coord at (722,214))
    closest_enemy_dest_node = Path.closest_node(platform, enemy_seek_location[0], enemy_seek_location[1])

    for plat in platform.enemyPlatoons:
        plat_x = plat.avg_coord[0]
        plat_y = plat.avg_coord[1]
        land_path = find_route([plat_x,plat_y], closest_enemy_dest_node, platform.island_nodes)

        bb.enemy_platoon_seek_active = True
        bb.enemy_active_platoon_seeks.append((plat.platoon_number,enemy_seek_location[0], enemy_seek_location[1], 'enemy', land_path))


    #---------------- //ENEMY PLATOONS SEEKING DOOR ------------------------



    # --- GAME LOOP --- #
    
    while not done:

        if not is_paused:

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
                        mine_count+=1
                        if mine_count <= mine_limit:
                            status = "Create Mine"
                    # if event.key == pygame.K_l:
                    #     status = "Create Land Mine"
                    # elif event.key == pygame.K_a:
                    #     status = "Create Aquatic Mine"
                    elif event.key == pygame.K_f:
                        status = "Fire Cannon"
                    elif event.key == pygame.K_n:
                        status = "None"
                    elif event.key == pygame.K_p:
                        is_paused = True

                    elif event.key == pygame.K_1:
                        if calcDistance(pos[0],pos[1],703,406) < ISLAND_RADIUS:
                            #calculating path
                            closest_dest_node_num = Path.closest_node(platform,pos[0],pos[1])
                            platoon_x = platform.playerPlatoons[0].avg_coord[0]
                            platoon_y = platform.playerPlatoons[0].avg_coord[1]
                            inland_path = find_route([platoon_x,platoon_y], closest_dest_node_num, platform.island_nodes)

                            #implementing seek
                            bb.platoon_seek_active = True
                            bb.active_platoon_seeks.append((1,pos[0],pos[1],'player',inland_path))
                    
                    elif event.key == pygame.K_2:
                        if calcDistance(pos[0],pos[1],703,406) < ISLAND_RADIUS:
                            #calculating path
                            closest_dest_node_num = Path.closest_node(platform,pos[0],pos[1])
                            platoon_x = platform.playerPlatoons[1].avg_coord[0]
                            platoon_y = platform.playerPlatoons[1].avg_coord[1]
                            inland_path = find_route([platoon_x,platoon_y], closest_dest_node_num, platform.island_nodes)


                            bb.platoon_seek_active = True
                            bb.active_platoon_seeks.append((2,pos[0],pos[1],'player', inland_path))

                    elif event.key == pygame.K_3:
                        if calcDistance(pos[0],pos[1],703,406) < ISLAND_RADIUS:
                            #calculating path
                            closest_dest_node_num = Path.closest_node(platform,pos[0],pos[1])
                            platoon_x = platform.playerPlatoons[2].avg_coord[0]
                            platoon_y = platform.playerPlatoons[2].avg_coord[1]
                            inland_path = find_route([platoon_x,platoon_y], closest_dest_node_num, platform.island_nodes)


                            bb.platoon_seek_active = True
                            bb.active_platoon_seeks.append((3,pos[0],pos[1],'player', inland_path))
                   
                    elif event.key == pygame.K_c:
                        if cannon_count <=cannon_limit:
                            if InCannonRange(platform,pos[0],pos[1],cannon_range):
                                cannon_count+=1
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

            #------------ / checking for contact of ships with Aquatic Mines --------

            for ship in platform.ship_list:
                for mine in platform.aquamine_list:
                    d=calcDistance(mine.x, mine.y, ship.x, ship.y)
                    if d < 50:
                        #print("ship hit")
                        ship.enemies_on_board-= 3
                        platform.aquamine_list.remove(mine)
                        platform.all_sprites_list.remove(mine)


            #------------checking for contact of ships with Aquatic Mines --------

            #------------ CANNON FIRING ------------------------------

            if len(platform.activeCannonBalls) > 0:
                for cannon_ball in platform.activeCannonBalls:
                    reached_dest = cannon_ball.update()
                    cannon_ball.render(gameDisplay)
                    if reached_dest:
                        destroy(platform, cannon_ball.destination, cannon_blast_radius)
                        platform.activeCannonBalls.remove(cannon_ball)

            #------------ /CANNON FIRING ------------------------------

            #------------ SHIP MOVEMENTS ------------------------------

            for ship in platform.ship_list:
                ship.updateShip(platform)
                if ship.is_destroyed:
                    platform.ship_list.remove(ship)
                elif ship.reached_pier:
                    platform.ship_list.remove(ship)

                    #making the disembarked platoon move towards the door
                    plat = platform.enemyPlatoons[-1]
                    plat_x = plat.avg_coord[0]
                    plat_y = plat.avg_coord[1]
                    land_path = find_route([plat_x,plat_y], closest_enemy_dest_node, platform.island_nodes)
                    bb.enemy_platoon_seek_active = True
                    bb.enemy_active_platoon_seeks.append((plat.platoon_number,enemy_seek_location[0], enemy_seek_location[1], 'enemy', land_path))


                else:
                    ship.render(gameDisplay)

            #------------ /SHIP MOVEMENTS ------------------------------

    # for plat in platform.enemyPlatoons:
    #     plat_x = plat.avg_coord[0]
    #     plat_y = plat.avg_coord[1]
    #     land_path = find_route([plat_x,plat_y], closest_enemy_dest_node, platform.island_nodes)

    #     bb.enemy_platoon_seek_active = True
    #     bb.enemy_active_platoon_seeks.append((plat.platoon_number,enemy_seek_location[0], enemy_seek_location[1], 'enemy', land_path))




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
            bb.updateEnemy()
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

            # --- Checking if anyone has won or lost the game
            gate_target = pygame.Rect(661, 525, 60,60)
            goal_target = pygame.Rect(platform.goal.rect.x, platform.goal.rect.y, 70,170)
            total_enemies_remaining = 0
            for platoon in platform.enemyPlatoons:
                # Get the number of enemies remaining
                total_enemies_remaining += platoon.members_alive

                # Check how many enemies are at the gate
                if gate_target.collidepoint(platoon.avg_coord[0], platoon.avg_coord[1]):
                    #print("collision with door")
                    # Check how many soldiers are in this platoon
                    if platoon.members_alive >= 5:
                        # The gate is destroyed
                        #print("drop gate")
                        platform.all_sprites_list.remove(platform.gate)
                        has_lost = True
                        is_paused = True

                # Check how many enemies are at the goal
                if platform.goal.rect.collidepoint(pos):
                    # Check how many soldiers are in this platoon
                    if platoon.members_alive >= 5:
                        has_lost = True
                        # The player loses
                        print("You lose!")
                        is_paused =True


            if total_enemies_remaining <= 0:
                has_won = True
                # The player wins
                print("You win!")
                is_paused = True
    
    # # PAUSE SCREEN
        else:
            # if has_won and is_paused:
            #     gameDisplay.blit(WIN_IMG,(0,0))
            #     pygame.display.update()
            # elif has_lost:
            #     gameDisplay.blit(PAUSE_IMG,(0,0))
            #     pygame.display.update()
            # else:
            if has_won:
                gameDisplay.blit(WIN_IMG,(500,325))
            elif has_lost:
                gameDisplay.blit(LOST_IMG,(500,325))
            else:
                gameDisplay.blit(PAUSE_IMG,(0,0))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    # Figure out if it was an arrow key. If so adjust speed.
                    if event.key == pygame.K_p:
                        is_paused = False




















