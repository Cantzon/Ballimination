import pygame,sys
from pygame.locals import *

gravity=0.25
delta = {
    pygame.K_LEFT: (-5, 0),
    pygame.K_RIGHT: (+5, 0),
    pygame.K_UP: (0, -5),
    pygame.K_DOWN: (0, +5),  
    }

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("ball1.png")
        self.rect = self.image.get_rect()
        self.rect.x=0
        self.rect.y=250
        self.speed = [2, 0]
        area = pygame.display.get_surface().get_rect()
        self.width, self.height = area.width, area.height

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.height:
            self.speed[1] = -self.speed[1]
        self.rect.left = clip(self.rect.left, 0, self.width)
        self.rect.right = clip(self.rect.right, 0, self.width)        
        self.rect.top = clip(self.rect.top, 0, self.height)
        self.rect.bottom = clip(self.rect.bottom, 0, self.height)       

def clip(val, minval, maxval):
    return min(max(val, minval), maxval)

pygame.init()

FPS=60
fpsClock=pygame.time.Clock()

DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
pygame.display.set_caption('Animation')


WHITE = (255, 255, 255)
background=pygame.image.load("background.png")
DISPLAYSURF.fill(WHITE)

ball = Ball()

while True:
    fball = ball
    friction = 1
    while True:
        for event in pygame.event.get():
            if ((event.type == pygame.QUIT) or 
                (event.type == pygame.KEYDOWN and 
                 event.key == pygame.K_ESCAPE)):
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                deltax, deltay = delta.get(event.key, (0, 0))
                ball.speed[0] += deltax
                ball.speed[1] += deltay
                friction = 1
            elif event.type == pygame.KEYUP:
                friction = 0.99

#       ball.speed = [friction*ball.speed[0],friction*ball.speed[1]]
        ball.speed[1] += gravity
        ball.update()
        DISPLAYSURF.blit(background, (0, 0))
        DISPLAYSURF.blit(ball.image, ball.rect)
        pygame.display.flip()
        fpsClock.tick(FPS)
