from pygame.locals import *
from random import randint
import pygame
import time
import math

from appleFinder import *
from gameobjects import *

 
class App:
    SpielfeldBreite = 17
    SpielfeldHöhe = 17

    PixelBreite = 21
    windowWidth = PixelBreite * SpielfeldBreite
    windowHeight = PixelBreite * SpielfeldHöhe

    spielzahl = 0
    gesamtpunkte = 0
    maxpunkte = 0
 
    def __init__(self):
        self.Data_in = []
        self.Data_out = []
        self._running = True
        self._exit = False
        self._display_surf = None
        self._snake_surf = None
        self._apple_surf = None
        self._wall_surf = None
        self.game = Game()
        self.player = Player(3, self.PixelBreite) 
        self.apple = Apple(randint(1,self.SpielfeldBreite-2),randint(1,self.SpielfeldHöhe-2), self.PixelBreite, self.SpielfeldHöhe, self.SpielfeldBreite)
        self.wall = Wall(self.PixelBreite, self.SpielfeldHöhe, self.SpielfeldBreite)
        App.spielzahl = App.spielzahl + 1
        self.wallhit = 0
        self.appleHit = 0
        self.appleAngle = 0
        self.blocked = [0,0,0]
        self.snakedir = [0,0]
        self.appledir = getAppleDirection(self.player, self.apple)
        self.snakeCenterAngle = 0
        self.directionsBlocked = [0,0,0,0,0,0,0]
        

        self.stepssurvived = 0


 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._snake_surf = pygame.image.load("art/snake.png").convert()
        self._apple_surf = pygame.image.load("art/apple.png").convert()
        self._wall_surf = pygame.image.load("art/wall.png").convert()

    def text_typer(self,text) :
        self.font = pygame.font.SysFont("arial", 25)
        self.text = self.font.render(text, True, (255, 255, 255))

        self.textrect = self.text.get_rect()
        self.textrect.centerx = self._display_surf.get_rect().centerx
        self.textrect.centery = self._display_surf.get_rect().centery

 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()
 
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],self.PixelBreite-1):
                self.apple.drop(self.player)
                self.player.length = self.player.length + 1
                App.gesamtpunkte = App.gesamtpunkte + 1
                if self.player.length-3 > App.maxpunkte:
                    App.maxpunkte = self.player.length-3

                self.appleHit = 1
 
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],self.PixelBreite-1):
                #print("You lose! Collision with snake: ")
                #print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                #print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                self._running = False
                self.wallhit = 1

        # does the snake collide with the wall?
        for i in range(2,self.wall.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.wall.x[i], self.wall.y[i],self.PixelBreite-1):
                #print("You lose! Collision with wall: ")
                #print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                #print("x[" + str(i) + "] (" + str(self.wall.x[i]) + "," + str(self.wall.y[i]) + ")")
                self._running = False
                self.wallhit = 1
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._snake_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.wall.draw(self._display_surf, self._wall_surf)
        self._display_surf.blit(self.text, self.textrect)
    
        #pygame.display.update() 
        pygame.display.flip()
 
    def on_cleanup(self):
        file2write=open("input.txt",'a')
        file2write.write(str(self.Data_in))
        file2write.close()
        file2write=open("output.txt",'a')
        file2write.write(str(self.Data_out))
        file2write.close()
        pygame.quit()

    def on_startup(self):
        if self.on_init() == False:
            self._running = False
    def on_execute(self, virtualKey):
        #virtualKey = 0
        
        pygame.event.pump()
        keys = pygame.key.get_pressed() 

        self.appledir = getAppleDirection(self.player, self.apple)
        self.snakedir = getCurrentDirection(self.player)
        self.appleAngle = angle_with_apple(self.snakedir, self.appledir)
        self.blocked = getBlocked(self.player, self.wall, self.PixelBreite, self.game)
        self.snakeCenterAngle = self.getSnakeCenterAngle()
        self.directionsBlocked = self.getDirectionsBlocked()

        #virtualKey = getKey(snakedir, direction(self.blocked, self.appledir, self.snakedir))
        #inData = [self.appledir[0], self.appledir[1], self.snakedir[0], self.snakedir[1], self.blocked[0], self.blocked[1], self.blocked[2]]
        
        #self.Data_in.append(inData)
        #self.Data_out.append(virtualKey)
        #print(direction(blocked, appledir, snakedir))
        #print(virtualKey)

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

        #print(direction(self.player, self.apple))
        average = int(self.gesamtpunkte / self.spielzahl)
        self.text_typer("Momentan:" + str(self.player.length-3) + "  Average:" + str(average) + "  max:" + str(self.maxpunkte))
        self.on_loop()
        self.on_render()
        time.sleep (50.0 / 1000.0)
        return [self._running, self.player.length, self._exit]

    def getState(self):
        return str((self.appleAngle, self.blocked[0], self.blocked[1], self.blocked[2], self.snakedir[0], self.snakedir[1], self.snakeCenterAngle))

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
        angle = round(angle * 8) / 8
        #print(angle)
        return angle

    def getDirectionsBlocked(self):
        directionsBlocked = [0,0,0,0,0,0,0]
        






