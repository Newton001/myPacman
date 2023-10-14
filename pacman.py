import pygame
from pygame.locals import *
from vector import Vector2
from constants import *

class Pacman(object):
    def __init__(self,node):
        self.name = PACMAN
        self.directions = {STOP:Vector2(),UP:Vector2(0,-1), DOWN:Vector2(0,1),
                           LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.setPosition()

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self,dt):
        direction = self.getValidKey()
        self.direction = direction
        self.node = self.getNewTarget(direction)
        self.setPosition()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen,self.color, p,self.radius)

    def validDirection(self,direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self,direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node