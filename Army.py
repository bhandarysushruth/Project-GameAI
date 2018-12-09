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

class Platoon:
    def __init__(self,platform,platoon_number,team):

        self.platoon_number=platoon_number
        self.team = team
        self.platoon_members=[]
        self.members_alive = 6
        self.total_health = 0

        #building a platoon from the platform and platoon number
        if team == 'player':
            for member in platform.playerArmy:
                if member.platoon == platoon_number:



                    self.platoon_members.append(member)
                    self.total_health= self.total_health + member.health
        elif team == 'enemy':
            for member in platform.enemyArmy:
                if member.platoon == platoon_number:
                    self.platoon_members.append(member)
                    self.total_health+=member.health

        self.members_alive = len(self.platoon_members)
        self.avg_coord = self.avg_platoon_coord()


    def avg_platoon_coord(self):
        sum_x=0
        sum_y=0
        for member in self.platoon_members:
            sum_x+=member.x
            sum_y+=member.y
        return (int(sum_x/len(self.platoon_members)),int(sum_y/len(self.platoon_members)))



    #updates the platoon to check if any member is dead and updates members_alive count and total health
    def update(self):

        health_count=0
        for mem in self.platoon_members:
            health_count += mem.health


        for member in self.platoon_members:
            if member.health == 0:
                member.is_dead =True
                self.platoon_members.remove(member)


        self.members_alive=len(self.platoon_members)
        self.total_health = health_count

        if(len(self.platoon_members) >0):
            self.avg_coord = self.avg_platoon_coord()



def destroyPlatoon(platoon):
    for member in platoon.platoon_members:
        member.health = 0
    platoon.update()







