import pygame,sys
from pygame.locals import *

'''class Ball(pygame.sprite.Sprite):
    def __init__(self,color,initial_position):
        pygame.sprite.Sprite.__init__(self)
        size=20
        self.gravity=900
        self.vx=0
        self.vy=0
        self.bounce=0.9

        self.image=pygame.Surface((size,size),pygame.SRCALPHA,32)
        pygame.draw.circle(self.image,color,(size/2,size/2),size/2)
        self.rect=self.image.get_rect()
        self.rect.center=initial_position

    def update(self,time_passed,size):
        self.vx+=self.gravity*time_passed
        ydistance=int(self.vy*time_passed)
        self.rect.bottom+=ydistance
        if ydistance==0 and self.rect.bottom==size[1]:
            self.vx=0
            self.rect.left+=int(self.vx*time_passed)
        if self.rect.right>=size[0]:
            self.rect.right=size[0]
            self.vx=-self.vx
        if self.rect.left<=0:
            self.rect.left=0
            self.vx=-self.vx
        if self.rect.bottom>=size[1]:
            self.rect.bottom=size[1]
            self.vy=-self.vy*self.bounce
'''
class Ball(pygame.sprite.Sprite):
    def __init__(self,color,initial_position):
        pygame.sprite.Sprite.__init__(self)
        size=20
        self.gravity=900
        self.velocity=0
        self.bounce=0.9

        self.image=pygame.Surface((size,size),pygame.SRCALPHA,32)
        pygame.draw.circle(self.image,color,(size/2,size/2),size/2)
        self.rect=self.image.get_rect()
        self.rect.center=initial_position

    def update(self,time_passed,size):
        self.velocity+=self.gravity*time_passed
        print int(self.velocity*time_passed)
        self.rect.bottom+=int(self.velocity*time_passed)
        
        if self.rect.bottom>=size[1]:
            self.rect.bottom=size[1]
            self.velocity=-self.velocity*self.bounce

pygame.init()

FPS=30
fpsClock=pygame.time.Clock()

DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
pygame.display.set_caption('Animation')


WHITE = (255, 255, 255)
background=pygame.image.load("background.png")
DISPLAYSURF.fill(WHITE)

ball=Ball((0,0,0),(50,50))

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    
    
    DISPLAYSURF.blit(background,(0,0))
    ball.update(pygame.time.get_ticks(),[577,472])

    pygame.display.update()
    fpsClock.tick(FPS)
