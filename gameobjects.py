from random import randint

class Apple:
    x = 0
    y = 0
    step = 44
    hoehe = 0
    breite = 0
 
    def __init__(self,x,y,PixelGroese, hoehe, breite):
        self.step = PixelGroese
        self.breite = breite
        self.hoehe = hoehe
        self.x = x * self.step
        self.y = y * self.step

    def drop(self, player):
        self.x = randint(1,self.breite-2) * self.step
        self.y = randint(1,self.hoehe-2) * self.step
        game = Game()
        collision = True
        while collision:
            for i in range(0,player.length):
                if game.isCollision(self.x,self.y,player.x[i], player.y[i],self.step-1):
                    self.x = randint(1,self.breite-2) * self.step
                    self.y = randint(1,self.hoehe-2) * self.step
                else:
                    collision = False
    
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
class Player: 
    def __init__(self, length, PixelGroese):
        self.x = [3]
        self.y = [3]
        self.direction = 0
        self.length = 3    
        self.updateCountMax = 2
        self.updateCount = 0
        self.step = PixelGroese
        self.length = length
        self.x[0] = self.x[0] * self.step
        self.y[0] = self.y[0] * self.step
        for i in range(0,2000):
            self.x.append(-100)
            self.y.append(-100)
 
        # initial positions, no collision.
        self.x[1] = 1*44
        self.x[2] = 2*44
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 

class Wall:
    def __init__(self, PixelBreite, SpielfeldHöhe, SpielfeldBreite):
        self.x = []
        self.y = []
        self.length = 0
        for i in range(0,SpielfeldBreite):
            self.x.append(i * PixelBreite)
            self.x.append(i * PixelBreite)
            self.y.append(0)
            self.y.append((SpielfeldHöhe-1) * PixelBreite)
        for i in range(0, SpielfeldHöhe):
            self.x.append((SpielfeldBreite-1) * PixelBreite)
            self.x.append(0)
            self.y.append( i * PixelBreite)
            self.y.append( i * PixelBreite)
        self.length = len(self.x)

    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


