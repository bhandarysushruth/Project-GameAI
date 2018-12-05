import pygame
import math


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

    # right half
    if (mx > x):
        mon_vel_x = mvel * math.cos(theta) * -1
        mon_vel_y = mvel * math.sin(theta) * -1

    # left half
    else:
        mon_vel_x = mvel * math.cos(theta)
        mon_vel_y = mvel * math.sin(theta)

    return mon_vel_x, mon_vel_y