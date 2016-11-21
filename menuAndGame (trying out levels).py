#    15-112: Principles of Programming and Computer Science
#    Final Project
#    Name      : Hari Krishna
#    AndrewID  : hkrishn1

#    File Created: November 7, 2016
#    Modification History:
#    Start              End
#    7/11/16 9:30pm    7/11/16 10:30pm
#    8/11/16 2:00pm    8/11/16 6:00pm
#    9/11/16 8:00pm    9/11/16 10:00pm
#    10/11/16 3:00am   10/11/16 6:00am
#    11/11/16 1:00pm   11/11/16 5:00pm
#    11/11/16 8:00pm   11/11/16 11:00pm
#    13/11/16 6:00pm   13/11/16 8:00pm
#    16/11/16 3:00am   16/11/16 6:00am
#    18/11/16 8:00pm   18/11/16 10:00pm

#importing needed libraries
import pygame
from pygame.locals import *
import Tkinter
import sys
from PIL import ImageTk, Image

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
        self.dist = 15
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
    def __init__(self,number,xpos,ypos,orientation):
        pygame.sprite.Sprite.__init__(self)
        self.num=number
        self.image = pygame.image.load("images/ball"+str(self.num)+".png")
        self.rect = self.image.get_rect()
        self.rect.x=xpos
        self.rect.y=ypos
        self.speed = [orientation, 0]
        area = pygame.display.get_surface().get_rect()
        self.width, self.height = area.width, area.height-35
        self.dead=False

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

#helper function for class Ball
def clip(val, minval, maxval):
    return min(max(val, minval), maxval)

#Function to quit menu on the click of the Quit Button
def quitMenu(root):
    root.destroy()
    
#Game window
def main(root):
    #destroying old window
    root.destroy()

    #initalising pygame
    pygame.init()
    
    #declaring constants
    FPS=60
    WHITE = (255, 255, 255)
    pause_text = pygame.font.SysFont('Consolas', 32).render('PAUSE', True, pygame.color.Color('White'))
    gameOver_text = pygame.font.SysFont('Consolas', 32).render('GAME OVER', True, pygame.color.Color('Red'))
    RUNNING=0
    PAUSE=1
    GAMEOVER=2
    isPause=False
    gravity=0.25
    RIGHT=2.5
    LEFT=-2.5
    level=1

    #default state
    state=RUNNING

    #setting a variable for the pygame clock
    fpsClock=pygame.time.Clock()

    #creating pygame surface display
    DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
    pygame.display.set_caption('Ballimination')
    background=pygame.image.load("images/background.png")
    DISPLAYSURF.fill(WHITE)

    #creating the required objects
    player=Player(DISPLAYSURF,250,360)
    bullets=[]
    balls=[]
    ball = Ball(1,0,200,RIGHT)
    balls.append(ball)
    
    #main game loop
    while True:        
        for event in pygame.event.get():
            #quit event
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            #shoots a bullet when you press the spacebar
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                if isPause!=True:
                    bullet=Bullet(DISPLAYSURF,player.rect.x+25,player.rect.y)
                    bullets.append(bullet)
            #pause event
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if state==PAUSE:
                        state=RUNNING
                        isPause=False
                    else:
                        if state!=GAMEOVER:
                            state=PAUSE
                            isPause=True
                        
        if state==RUNNING:                
            #handles movement of player       
            player.keys()

            #updates every single bullet on screen
            for i in bullets:
                i.update()

            #removes out-of-screen bullets from the list of bullets
            for i in bullets:
                if i.dead==True:
                    bullets.remove(i)

            for i in balls:
                i.speed[1] += gravity
                i.update()
                if i.dead==True:
                    balls.remove(i)
            
            #drawing surface, player, ball and bullets
            DISPLAYSURF.blit(background,(0,0))
            player.draw(DISPLAYSURF)
            for ball in balls:
                DISPLAYSURF.blit(ball.image, ball.rect)
            for i in bullets:
                i.draw()

            #collision b/w player and ball
            for ball in balls:  
                if pygame.sprite.collide_rect(player,ball):
                    state=GAMEOVER
                for i in bullets:
                    if pygame.sprite.collide_rect(ball,i):
                        ball.dead=True
                        bullets.remove(i)
                        if ball.num>1:
                            balls.append(Ball(ball.num-1,i.rect.x-10,i.rect.y-50,LEFT))
                            balls.append(Ball(ball.num-1,i.rect.x+10,i.rect.y-50,RIGHT))

                
        elif state==PAUSE:
            DISPLAYSURF.blit(pause_text,(250,220))
            
        elif state==GAMEOVER:
            DISPLAYSURF.blit(gameOver_text,(220,220))
            
        pygame.display.update()
        fpsClock.tick(FPS)

        if balls==[] and ball.num<4:
            player.rect.x=250
            balls.append(Ball(level+1,0,200,RIGHT))
            level+=1
            
    
#creating menu window
root=Tkinter.Tk()
root.geometry("577x472")
root.resizable(0,0)

#creating background
menuBGPhoto=ImageTk.PhotoImage(Image.open("images/background.png"))
BGLabel=Tkinter.Label(root,image=menuBGPhoto)
BGLabel.place(x=0,y=0,relwidth=1,relheight=1)

#creating title label
titlePhoto=ImageTk.PhotoImage(Image.open("images/title.png"))
title=Tkinter.Label(root,image=titlePhoto)

#creating buttons
playBtnPhoto=ImageTk.PhotoImage(Image.open("images/playbutton.png"))
quitBtnPhoto=ImageTk.PhotoImage(Image.open("images/quitbutton.png"))
playBtn=Tkinter.Button(root,image=playBtnPhoto,command=lambda x=root:main(x))
quitBtn=Tkinter.Button(root,image=quitBtnPhoto,command=lambda x=root:quitMenu(x))

#packing everything
title.pack(pady=50)
playBtn.pack(pady=10)
quitBtn.pack()

#main loop
root.mainloop()

