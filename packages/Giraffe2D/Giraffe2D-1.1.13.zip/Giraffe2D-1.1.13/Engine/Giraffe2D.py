import contextlib
import math
import os
from test.test_turtle import Vec2D

with contextlib.redirect_stdout(None):
    import pygame
    import pygame.gfxdraw
    from pygame.locals import *
    
    

print("Please Visit www.GiraffeGameEngine.com for more info")


class App():
    def __init__(self):
        pygame.init()
        
    def RenderWindow(self, width, height):
        global gameDisplay
        gameDisplay = pygame.display.set_mode((width, height))
        

    def SetAssetsFolder(self):
        self.gameFolder = os.path.dirname(__file__)
    
    
    def Update(self):
        pygame.display.update()
        pygame.display.flip()

        
    def FPS(self, amount):
        clock = pygame.time.Clock()
        clock.tick(amount)

        
    def SetTitle(self, title):
        pygame.display.set_caption(title)

        
    def Fill(self, color):
        gameDisplay.fill(color)

        
    def get_display(self):
        return gameDisplay

    def SetIcon(self, path):
        myIcon = pygame.image.load(path)
        pygame.display.set_icon(myIcon)
        
    def quit(self):
        pygame.quit()
        quit()
        
class Event():
    def __init__(self):
        pygame.init()
        self.close = False
    
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                self.close = True
    
    
    
            
class Sprite(pygame.sprite.Sprite):
    def  __init__(self, path):
        pygame.init()
        self.image = pygame.image.load(path).convert()
        self.rect = self.image.get_rect()
        

    def getPosX(self):
        return self.posX
    
    def LookAtMouse(self, spriteToRotate):
        x,y = pygame.mouse.get_pos()
        rel_x = x - self.posX
        rel_y = y - self.posY
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(spriteToRotate, angle)
        
    def LoadImage(self, path):
        pass
    
    def PlaceImage(self, x, y):
        self.x = x
        self.y = y
        pygame.Surface.blit(App.get_display(self),self.image, (self.x, self.y))

        

class Draw():
    def DrawRect(self, color, sizeX, sizeY, posX, posY):
            self.color = color
            self.sizeX = sizeX
            self.sizeY = sizeY
            self.posX = posX
            self.posY = posY
            pygame.draw.rect(App.get_display(self), self.color, [self.posX, self.posY, self.sizeX, self.sizeY])
    def DrawCircle(self):
        pass
    def DrawPolygon(self):
        pass
    def DrawTriangle(self):
        pass
    def DrawLine(self):
        pass
    

class Keyboard():
    def __init__(self):
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.moveLeft = True
        if keys[pygame.K_RIGHT]:
            self.moveRight = True
        if keys[pygame.K_UP]:
            self.moveUp = True
        if keys[pygame.K_DOWN]:
            self.moveDown = True
    def CheckKey(self, key):
        pass

class Vector2D(pygame.math.Vector2):
    def __init__(self, *args, **kwargs):
        pygame.math.Vector2.__init__(self, *args, **kwargs)
        
    
class Color():
    def __init__(self):
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
    def COLOR(self):
        pass

class Sound():
    def __init__(self, path):
        pygame.init()
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(path)
    
    def LoadSound(self, path):
        self.sound = pygame.mixer.sound(path)    
    def play(self, volume):
        pygame.mixer.sound.play(self.sound)
        pygame.mixer.set_volume(volume)
    def pause(self):
        pygame.mixer.pause()
    def unpause(self):
        pygame.mixer.unpause()

class Music():
    def __init__(self, path):
        pygame.init()
        pygame.mixer.init()
    def play(self):
        pass

class Physics2D():
    def __init__(self):
        pass

        
        

    
        
            
                    
    
             


     


    


