import pygame,sys
from pygame.locals import *

class Player():
    def __init__(self,surf,xpos,ypos):
        self.image=pygame.image.load("cat1.png").convert_alpha()
        self.x=xpos
        self.y=ypos
        self.surface=surf
    def keys(self):
        dist=10
        key=pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            if self.x<500:
                self.x+=dist
        elif key[pygame.K_LEFT]:
            if self.x!=0:
                self.x-=dist
    def draw(self,surface):
        self.surface.blit(self.image,(self.x,self.y))

class Weapon(Player):
    def __init__(self,surf,xpos,ypos,bg,wxpos,wypos):
        Player.__init__(self,surf,xpos,ypos)
        self.wimage=pygame.image.load("cat1.png").convert_alpha()
        self.wx=wxpos
        self.wy=wypos
        self.background=bg

    def Shoot(self):
        dist=10
        while self.wy>0:
            self.surface.blit(self.background,(0,0))
            self.surface.blit(self.image,(self.x,self.y))
            self.surface.blit(self.wimage,(self.wx,self.wy))
            self.wy-=dist
            pygame.display.update()
pygame.init()

FPS=30
fpsClock=pygame.time.Clock()

DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
background=pygame.image.load("background.png")
DISPLAYSURF.fill(WHITE)


player=Player(DISPLAYSURF,50,360)


while True:
      
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONDOWN:
            weapon=Weapon(DISPLAYSURF,player.x,player.y,background,player.x+25,player.y)
            player.draw(DISPLAYSURF)
            pygame.display.update()
            weapon.Shoot()
            pygame.display.update()

            

    player.keys()
    DISPLAYSURF.blit(background,(0,0))
    player.draw(DISPLAYSURF)

    pygame.display.update()
    fpsClock.tick(FPS)
