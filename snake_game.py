from pygame.locals import *
from random import randint
import pygame
import time
import math

from GameHelperFunctions import *
from gameobjects import *

 
class App:
    PixelBreite = 21 
    def __init__(self, initObject):
        self.SpielfeldBreite = initObject.spielfeldgöße[0] + 2
        self.SpielfeldHöhe = initObject.spielfeldgöße[1] + 2
        self.windowWidth = self.PixelBreite * self.SpielfeldBreite
        self.windowHeight = self.PixelBreite * self.SpielfeldHöhe
        self._running = True
        self._exit = False
        self._display_surf = None
        self._snake_surf = None
        self._apple_surf = None
        self._wall_surf = None
        self.game = Game()
        self.player = Player(initObject.originalSnakeLength, self.PixelBreite) 
        self.apple = Apple(randint(1,self.SpielfeldBreite-2),randint(1,self.SpielfeldHöhe-2), self.PixelBreite, self.SpielfeldHöhe, self.SpielfeldBreite)
        self.wall = Wall(self.PixelBreite, self.SpielfeldHöhe, self.SpielfeldBreite)
        self.wallhit = 0
        self.appleHit = 0
        self.appleAngle = 0
        self.blocked = [0,0,0, 0,0,0,0,0,0,0] #Die ersten drei Stellen für direkte Blocks, danach sieben Stellen für die Strahlen
        self.snakedir = [0,0]
        self.appledir = getAppleDirection(self.player, self.apple)
        self.snakeCenterAngle = 0
        self.stepssurvived = 0

        self.apfelnumer = 0

        self.initObject = initObject
        if self.on_init() == False:
            self._running = False
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._snake_surf = pygame.image.load("art/snake.png").convert()
        self._apple_surf = pygame.image.load("art/apple.png").convert()
        self._wall_surf = pygame.image.load("art/wall.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()
 
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],self.PixelBreite-1):
                self.apfelnumer = self.apfelnumer + 1
                self.apple.drop(self.apfelnumer)
                self.player.length = self.player.length + 1
                self.appleHit = 1
 
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],self.PixelBreite-1):
                self._running = False
                self.wallhit = 1

        # does the snake collide with the wall?
        for i in range(2,self.wall.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.wall.x[i], self.wall.y[i],self.PixelBreite-1):
                self._running = False
                self.wallhit = 1
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._snake_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.wall.draw(self._display_surf, self._wall_surf)
    
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self, virtualKey):
        #virtualKey = 0
        
        pygame.event.pump()
        keys = pygame.key.get_pressed() 

        self.appledir = getAppleDirection(self.player, self.apple)
        self.snakedir = getCurrentDirection(self.player)
        self.appleAngle = angle_with_apple(self.snakedir, self.appledir)
        self.blocked = getBlocked(self.player, self.wall, self.PixelBreite, self.game)
        #self.snakeCenterAngle = self.getSnakeCenterAngle()

        if (keys[K_RIGHT] or virtualKey == "Right"):
            self.player.moveRight()

        if (keys[K_LEFT] or virtualKey == "Left"):
            self.player.moveLeft()

        if (keys[K_UP] or virtualKey == "Up"):
            self.player.moveUp()

        if (keys[K_DOWN] or virtualKey == "Down"):
            self.player.moveDown()

        if (keys[K_ESCAPE]):
            self._exit = True

        self.on_loop()
        self.on_render()

        if self.initObject.verzögern:
            time.sleep (self.initObject.verzögerung)
        return [self._running, self.player.length, self._exit]

    def getState(self):
        #return str((self.appleAngle, self.blocked[0], self.blocked[1], self.blocked[2], self.blocked[3], self.blocked[4], self.blocked[5], self.blocked[6],self.blocked[7], self.blocked[8], self.blocked[9], self.snakedir[0], self.snakedir[1], self.snakeCenterAngle))
        return str((self.appleAngle, self.blocked[0], self.blocked[1], self.blocked[2], self.snakedir[0], self.snakedir[1]))

    def getResult(self):
        appleZw = self.appleHit
        wallZw = self.wallhit
        self.appleHit = 0
        self.wallhit = 0
        return [appleZw, wallZw]

    def getAppleDis(self):
        return (math.sqrt(self.appledir[0]**2 + self.appledir[1]**2))
    
    def getSnakeCenterAngle(self):
        xCenter = 0
        yCenter = 0
        #Schwerpunkt der Schlange in x und y bestimmen (ohne Kopf):
        for i in range(1, self.player.length):
            xCenter = xCenter + self.player.x[i]
            yCenter = yCenter + self.player.y[i]
        #x- und y-Koordinaten mitteln für Schwerpunkt:
        xCenter = xCenter / (self.player.length - 1)
        yCenter = yCenter / (self.player.length - 1)
        #Berechne Richtung zum Schwerpunkt:
        centerDir = [xCenter - self.player.x[0], yCenter - self.player.y[0]]
        #Berechne Winkel:
        angle = math.atan2(centerDir[1] * self.snakedir[0] - centerDir[0] * self.snakedir[1], centerDir[1] * self.snakedir[1] + centerDir[0] * self.snakedir[0])/ math.pi
        angle = round(angle * 2) / 2
        return angle


        






