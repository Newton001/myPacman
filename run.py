import pygame
from pygame.locals import *
from constants import *
from pacman import *
from nodes import *
from pellets import PelletGroup
from monsters import MonsterGroup
from fruit import Fruit
from pauser import Pause

class GameController(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE,0,32)
        self.background = None
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.monsters.reset()
        self.fruit = None

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()

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
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("maze2.txt")
        self.monsters = MonsterGroup(self.nodes.getStartTempNode(),self.pacman)
        self.monsters.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5,0+14))
        self.monsters.pinky.setStartNode(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
        self.monsters.inky.setStartNode(self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14))
        self.monsters.clyde.setStartNode(self.nodes.getNodeFromTiles(4 + 11.5, 3 + 14))
        self.monsters.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5,3+14))
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.monsters)
        self.nodes.denyAccessList(2 + 11.5, 3 + 14, LEFT, self.monsters)
        self.nodes.denyAccessList(2 + 11.5, 3 + 14, RIGHT, self.monsters)
        self.monsters.inky.startNode.denyAccess(RIGHT, self.monsters.inky)
        self.monsters.clyde.startNode.denyAccess(LEFT, self.monsters.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.monsters)
        self.nodes.denyAccessList(15, 14, UP, self.monsters)
        self.nodes.denyAccessList(12, 26, UP, self.monsters)
        self.nodes.denyAccessList(15, 26, UP, self.monsters)

    def update(self):
        dt = self.clock.tick(30)/1000
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            self.monsters.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkMonsterEvents()
            self.checkFruitEvents()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkMonsterEvents(self):
        for monster in self.monsters:
            if self.pacman.collideMonster(monster):
                if monster.mode.current is FREIGHT:
                    self.pacman.visible = False
                    monster.visible = False
                    self.pause.setPause(pauseTime=1,func=self.showEntities)
                    monster.startSpawn()
                    self.nodes.allowHomeAccess(monster)
                elif monster.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.pacman.die()
                        self.monsters.hide()
                        if self.lives <= 0:
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def showEntities(self):
        self.pacman.visible = True
        self.monsters.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.monsters.hide()

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None



    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.showEntities()
                        else:
                            self.hideEntities()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.monsters.render(self.screen)
        pygame.display.update()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten +=1
            if self.pellets.numEaten == 30:
                self.monsters.inky.startNode.allowAccess(RIGHT, self.monsters.inky)
            if self.pellets.numEaten == 70:
                self.monsters.clyde.startNode.allowAccess(LEFT, self.monsters.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name is POWERPELLET:
                self.monsters.startFreight()
            if self.pellets.isEmpty():
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)




if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()