import pygame,sys
from pygame.locals import *


#Class for the Player
class Player():
    def __init__(self,surf,xpos,ypos):
        self.idle=pygame.image.load("images/Idle__000.png").convert_alpha()
        self.runAnims=[pygame.image.load("images/Run__00"+str(i)+".png").convert_alpha() for i in range(10)]
        self.image=self.idle
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.surface=surf
        self.dist=10
        self.frame=0
        self.lastState='right'
        
    def keys(self):
        key=pygame.key.get_pressed()
        self.frame+=1
        if self.frame==10:
            self.frame=0
        if key[pygame.K_RIGHT]:
            self.image=self.runAnims[self.frame]
            if self.rect.x<500:
                self.rect.x+=self.dist
            self.lastState="right"    
        elif key[pygame.K_LEFT]:
            self.image=pygame.transform.flip(self.runAnims[self.frame],1,0)
            if self.rect.x!=0:
                self.rect.x-=self.dist
            self.lastState="left"   
        elif pygame.event.get()==[]:
            #player's idle state will reflect whichever side he was facing last while running or idle
            if self.lastState=="left":
                self.image=pygame.transform.flip(self.idle,1,0)
            else:
                self.image=self.idle
                
    def draw(self,surface):
        self.surface.blit(self.image, self.rect)

#Class for the bullet which inherits the Player Class
class Bullet():
    def __init__(self,surf,xpos,ypos):
        self.image=pygame.image.load("images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.dist = 10
        self.surface = surf
        self.dead = False

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def update(self):
        #makes note of when the bullet goes out of the screen
        if self.rect.y > 0:
            self.rect.y -= self.dist
        else:
            self.dead = True

pygame.init()

FPS=30
WHITE = (255, 255, 255)

fpsClock=pygame.time.Clock()

DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
pygame.display.set_caption('Ballimination')

background=pygame.image.load("images/background.png")
DISPLAYSURF.fill(WHITE)


player=Player(DISPLAYSURF,50,360)
bullets=[]


while True:
      
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONDOWN:
            bullet=Bullet(DISPLAYSURF,player.rect.x+25,player.rect.y)
            bullets.append(bullet)           
    player.keys()

    for i in bullets:
        i.update()

    for i in bullets:
        if i.dead==True:
            bullets.remove(i)
    

    DISPLAYSURF.blit(background,(0,0))
    player.draw(DISPLAYSURF)
    for i in bullets:
        i.draw()
    pygame.display.update()
    
    fpsClock.tick(FPS)
