import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController



class Monster(Entity):
    def __init__(self,node,pacman=None,blinky=None):
        Entity.__init__(self,node)
        self.name = MONSTER
        self.points =200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def update(self,dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self,dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self,node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnNode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)


class Blinky(Monster):
    def __init__(self,node,pacman=None,blinky=None):
        Monster.__init__(self,node,pacman,blinky)
        self.name = BLINKY
        self.color = RED

class Pinky(Monster):
    def __init__(self,node,pacman=None, blinky=None):
        Monster.__init__(self,node,pacman,blinky)
        self.name = PINK
        self.color = PINK

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS,0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH *4

class Inky(Monster):
    def __init__(self,node,pacman=None,blinky=None):
        Monster.__init__(self,node,pacman,blinky)
        self.name = INKY
        self.color = TEAL

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS,TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] *TILEWIDTH *2
        vec2 = (vec1-self.blinky.position) *2
        self.goal = self.blinky.position +vec2


class Clyde(Monster):
    def __init__(self,node,pacman=None,blinky=None):
        Monster.__init__(self,node,pacman,blinky)
        self.name = CLYDE
        self.color = ORANGE

    def scatter(self):
        self.goal = Vector2(0,TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH*8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction]*TILEWIDTH*4



class MonsterGroup(object):
    def __init__(self,node,pacman):
        self.blinky = Blinky(node,pacman)
        self.pinky = Pinky(node,pacman)
        self.inky = Inky(node,pacman)
        self.clyde = Clyde(node,pacman)
        self.monsters = [self.blinky,self.inky,self.clyde]

    def __iter__(self):
        return iter(self.monsters)

    def update(self,dt):
        for monster in self:
            monster.update(dt)

    def startFreight(self):
        for monster in self:
            monster.startFreight()
        self.resetPoints()

    def setSpawnNode(self,node):
        for monster in self:
            monster.setSpawnNode(node)

    def updatePoints(self):
        for monster in self:
            monster.points *=2

    def resetPoints(self):
        for monster in self:
            monster.points = 200

    def reset(self):
        for monster in self:
            monster.reset()
    def hide(self):
        for monster in self:
            monster.visible = False
    def show(self):
        for monster in self:
            monster.visible = True

    def render(self,screen):
        for monster in self:
            monster.render(screen)


