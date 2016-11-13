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

#importing needed libraries
import pygame
from pygame.locals import *
import Tkinter
import sys
from PIL import ImageTk, Image

#Class for the Player
class Player():
    def __init__(self,surf,xpos,ypos):
        #inital image is idle
        self.idle=pygame.image.load("images/Idle__000.png").convert_alpha()
        #run animations are contained in runAnims
        self.runAnims=[pygame.image.load("images/Run__00"+str(i)+".png").convert_alpha() for i in range(10)]
        self.image=self.idle
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.surface=surf
        self.dist=5
        self.frame=0
        #last state is used to see where the player was facing last
        self.lastState='right'
        
    def keys(self):
        key=pygame.key.get_pressed()
        #frame is used for changing the running frame of the character
        self.frame+=1
        #frame resets after reaching the last frame
        if self.frame==10:
            self.frame=0
        #enables running up until the width of the screen to the right
        if key[pygame.K_RIGHT]:
            self.image=self.runAnims[self.frame]
            if self.rect.x<500:
                self.rect.x+=self.dist
            self.lastState="right"    
        #enables running up until the width of the screen to the right
        elif key[pygame.K_LEFT]:
            #flips the image, since it's running in the opposite direction
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

#Class for the bullet
class Bullet():
    def __init__(self,surf,xpos,ypos):
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

    #setting a variable for the pygame clock
    fpsClock=pygame.time.Clock()

    #creating pygame surface display
    DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
    pygame.display.set_caption('Ballimination')
    background=pygame.image.load("images/background.png")
    DISPLAYSURF.fill(WHITE)

    #creating the initial player and the list needed for bullets
    player=Player(DISPLAYSURF,50,360)
    bullets=[]

    #main game loop
    while True:        
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            #shoots a bullet when you press the spacebar
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                bullet=Bullet(DISPLAYSURF,player.rect.x+25,player.rect.y)
                bullets.append(bullet)
                
        #handles movement of player       
        player.keys()

        #updates every single bullet on screen
        for i in bullets:
            i.update()

        #removes out-of-screen bullets from the list of bullets
        for i in bullets:
            if i.dead==True:
                bullets.remove(i)
        
        #drawing surface, player and bullets
        DISPLAYSURF.blit(background,(0,0))
        player.draw(DISPLAYSURF)
        for i in bullets:
            i.draw()
        pygame.display.update()
        
        fpsClock.tick(FPS)        
    
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

