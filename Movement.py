import pygame
import math
from Army import *
import Path


def calcDistance(x1,y1,x2,y2):
    val = (x2-x1)**2
    val += (y2-y1)**2
    dist = math.sqrt(val)
    return dist

def seek(x, y, mx, my, mvel):
    # avoiding oscilation at target arrival this will make it land at the target
    if calcDistance(x, y, mx, my) <= mvel:
        return x - mx, y - my

    if (x - mx) == 0:
        if (y - my) > 0:
            theta = math.radians(90)
        elif (y - my) < 0:
            theta = math.radians(-90)
        else:
            theta = math.radians(0)

    else:

        tanVal = (y - my) / (x - mx)
        theta = (math.atan(tanVal))

    # right half :
    if (mx > x):
        mon_vel_x = mvel * math.cos(theta) * -1
        mon_vel_y = mvel * math.sin(theta) * -1

    # left half
    else:

        mon_vel_x = mvel * math.cos(theta)
        mon_vel_y = mvel * math.sin(theta)

    return mon_vel_x, mon_vel_y


# Just like seek, but here it just takes in the target object and the chasing object
# and makes changes to the chasing object

def object_seek(target, player, vel):

    # avoiding oscilation at target arrival this will make it land at the target
    if calcDistance(target.x, target.y, player.x, player.y) <= vel:
        player.x= target.x
        player.y = target.y
        return True

    
    if (target.x - player.x) == 0:
        if (target.y - player.y) > 0:
            theta = math.radians(90)
        elif (target.y - player.y) < 0:
            theta = math.radians(-90)
        else:
            theta = math.radians(0)

    else:

        tanVal = (target.y - player.y) / (target.x - player.x)
        theta = (math.atan(tanVal))

    # right half :
    if (player.x > target.x):
        mon_vel_x = vel * math.cos(theta) * -1
        mon_vel_y = vel * math.sin(theta) * -1

    # left half
    else:

        mon_vel_x = vel * math.cos(theta)
        mon_vel_y = vel * math.sin(theta)

    player.x+=int(mon_vel_x)
    player.y+=int(mon_vel_y)

    return False

#platoon seek is a seek for the entire platoon
#The entire platoon moves towards the target object at (seek_x, seek_y)
def platoon_seek(platform, platoon_number, seek_x, seek_y, team):

    i = 0
    sx=seek_x
    sy=seek_y

    # if we make all the soldiers seek the the same locations, they will all overlap
    # hence we define 6 positions around the original seek cordinates
    # A platooon can have a max of 6 soldiers
    # hence we define 6 positions and make the soldiers seek to 6 separate cordinates
    
    positions = [(seek_x,seek_y),(seek_x + 15 ,seek_y), (seek_x,seek_y+15),(seek_x,seek_y-15),(seek_x-15,seek_y),(seek_x+15,seek_y+15)]

    if team == 'player':

        for character in platform.playerArmy:
            if character.platoon == platoon_number:
                done = object_seek(Soldier(positions[i][0], positions[i][1], 1, 'player'), character, 5)
                i+=1

    elif team == 'enemy':

        for character in platform.enemyArmy:
            if character.platoon == platoon_number:
                done = object_seek(Soldier(positions[i][0], positions[i][1], 1, 'player'), character, 5)
                i+=1

    return done



















