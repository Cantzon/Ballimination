import pygame,sys
from pygame.locals import *


#Class for the Player
class Player(pygame.sprite.Sprite):
    def __init__(self,surf,xpos,ypos):
        pygame.sprite.Sprite.__init__(self)         
        self.idle=pygame.image.load("images/Idle__000.png").convert_alpha()
        self.runAnims=[pygame.image.load("images/Run__00"+str(i)+".png").convert_alpha() for i in range(10)]
        self.image=self.idle
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.surface=surf
        self.dist=5
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
class Bullet(pygame.sprite.Sprite):
    def __init__(self,surf,xpos,ypos):
        pygame.sprite.Sprite.__init__(self) 
        self.image=pygame.image.load("images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.dist = 5
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
            
#class for the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self,pic):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(pic)
        self.rect = self.image.get_rect()
        self.rect.x=0
        self.rect.y=250
        self.speed = [2, 0]
        area = pygame.display.get_surface().get_rect()
        self.width, self.height = area.width, area.height-35

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
            
        
#helper function for class ball
def clip(val, minval, maxval):
    return min(max(val, minval), maxval)

#initialising pygame
pygame.init()

#initialising constants
FPS=45
WHITE = (255, 255, 255)
pause_text = pygame.font.SysFont('Consolas', 32).render('PAUSE', True, pygame.color.Color('White'))
gameOver_text = pygame.font.SysFont('Consolas', 32).render('GAME OVER', True, pygame.color.Color('Red'))
RUNNING=0
PAUSE=1
GAMEOVER=2
gravity=0.25

#default state
state=RUNNING

fpsClock=pygame.time.Clock()

#setting display window
DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
pygame.display.set_caption('Ballimination')
background=pygame.image.load("images/background.png")
DISPLAYSURF.fill(WHITE)

#Setting up objects
player=Player(DISPLAYSURF,250,360)
bullets=[]
balls=[]
ball = Ball("ball1.png")
balls.append(ball)


while True:
      
    for event in pygame.event.get():
        #quit event
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        #shoot bullet event
        elif event.type==pygame.KEYDOWN and event.key==K_SPACE:
            bullet=Bullet(DISPLAYSURF,player.rect.x+25,player.rect.y)
            bullets.append(bullet)
        #pause event
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_p:
                if state==PAUSE:
                    state=RUNNING
                else: 
                    state=PAUSE
            

    if state==RUNNING: 
        player.keys()

        for i in bullets:
            i.update()

        for i in bullets:
            if i.dead==True:
                bullets.remove(i)
        
        ball.speed[1] += gravity
        ball.update()
        
        DISPLAYSURF.blit(background,(0,0))
        player.draw(DISPLAYSURF)
        DISPLAYSURF.blit(ball.image, ball.rect)
        for i in bullets:
            i.draw()
        for i in balls:
            i.speed[1] += gravity
            i.update()
            
        #collision b/w player and ball
        for ball in balls:  
            if pygame.sprite.collide_rect(player,ball):
                state=GAMEOVER
        
    elif state==PAUSE:
        DISPLAYSURF.blit(pause_text,(250,220))
    elif state==GAMEOVER:
        DISPLAYSURF.blit(gameOver_text,(220,220))

    pygame.display.update()
    fpsClock.tick(FPS)
