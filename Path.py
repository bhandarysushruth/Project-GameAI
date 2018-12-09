import pygame
import Movement

# Define global variables
MIN_RADIUS = 5

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Point:
    """ Point class that stores x and y coordinates """
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    """ Node class that holds a node """
    number = 0
    point = Point(0, 0)


    def __init__(self, number, point):
        self.number = number
        self.point = point


class Path:
    """ Path class that contains a data structure of all the points in the path """
    path = list()
    length = 0
    radius = MIN_RADIUS

    def draw(self, screen, pathlist):
        """ Draws the path to be followed """

        length = len(pathlist)

        for i, val in enumerate(pathlist):
            # If we've reached the end of the list, stop iterating
            if i == length - 1:
                return
            pygame.draw.line(screen, RED, (pathlist[i].x, pathlist[i].y), (pathlist[i+1].x, pathlist[i+1].y), 5)

    def createpath(self, shortestpath):
        """ Convert to path object """
        for node in shortestpath:
            self.path.append(node.point)

