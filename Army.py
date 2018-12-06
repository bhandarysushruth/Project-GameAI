import pygame

yellow = (255,255,0)
red = (255,25,25)
blue = (25,25,255)

class Soldier:
    def __init__(self,x,y,platoon,team):
        self.x = x
        self.y = y
        self.health = 1
        self.platoon = platoon
        self.is_dead = False
        if team == 'player' :
            self.color = yellow
        elif team == 'enemy':
            self.color = red

    def render(self, gameDisplay):
        if not self.is_dead:
            pygame.draw.circle(gameDisplay, self.color,(self.x, self.y), 7)


class Knight:
    def __init__(self,x,y,platoon,team):
        self.x = x
        self.y = y
        self.health = 2
        self.is_dead = False
        self.platoon = platoon
        if team == 'player' :
            self.color = yellow
        elif team == 'enemy':
            self.color = red

    def render(self, gameDisplay):
        if not self.is_dead:
            pygame.draw.circle(gameDisplay, self.color,(self.x, self.y), 7)
            pygame.draw.circle(gameDisplay, self.color,(self.x, self.y), 9,1)