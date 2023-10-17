import pygame
from pygame.locals import *
from constants import *
from pacman import *
from nodes import *
from pellets import PelletGroup
from monsters import Monster

class GameController(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE,0,32)
        self.background = None

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("maze2.txt")
        self.nodes.setPortalPair((0,17),(27,17))
        homekey = self.nodes.creatHomeNodes(11.5,14)
        self.nodes.connectHomeNodes(homekey,(12,14),LEFT)
        self.nodes.connectHomeNodes(homekey,(15,14),RIGHT)
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.pellets = PelletGroup("maze2.txt")
        self.monster = Monster(self.nodes.getStartTempNode(),self.pacman)

    def update(self):
        dt = self.clock.tick(30)/1000
        self.pacman.update(dt)
        self.monster.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.monster.render(self.screen)
        pygame.display.update()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten +=1
            self.pellets.pelletList.remove(pellet)




if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()