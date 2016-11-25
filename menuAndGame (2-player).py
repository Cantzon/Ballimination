#    15-112: Principles of Programming and Computer Science
#    Final Project
#    Name      : Hari Krishna
#    AndrewID  : hkrishn1

#    File Created: November 7, 2016
#    Modification History:
#    Start              End
#    7/11/16 9:30pm    7/11/16 10:30pm
#    8/11/16 2:30pm    8/11/16 6:00pm
#    9/11/16 8:00pm    9/11/16 10:00pm
#    10/11/16 3:00am   10/11/16 6:30am
#    11/11/16 1:00pm   11/11/16 5:00pm
#    11/11/16 8:30pm   11/11/16 11:30pm
#    13/11/16 6:00pm   13/11/16 8:30pm
#    16/11/16 3:00am   16/11/16 6:00am
#    18/11/16 8:00pm   18/11/16 10:00pm
#    20/11/16 4:30pm   18/11/16 6:30pm
#    21/11/16 2:00pm    8/11/16 6:00pm
#    23/11/16 1:00am   10/11/16 4:00am

#importing needed libraries
import pygame
from pygame.locals import *
import Tkinter
import sys
from PIL import ImageTk, Image
import random
import shelve

#Class for the Player
class Player(pygame.sprite.Sprite):
    def __init__(self,surf,xpos,ypos,whichPlayer):
        pygame.sprite.Sprite.__init__(self)         
        self.idle=pygame.image.load("images/Idle__000.png").convert_alpha()
        self.heart=pygame.image.load("images/heart.png").convert_alpha()
        self.runAnims=[pygame.image.load("images/Run__00"+str(i)+".png").convert_alpha() for i in range(10)]
        self.image=self.idle
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.surface=surf
        self.playerNum=whichPlayer
        self.dist=5
        self.frame=0
        self.lastState='right'
        self.lives=3
        self.powerUp=False
        
    def keys(self):
        key=pygame.key.get_pressed()
        if self.playerNum==1:
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
        elif self.playerNum==2:
            self.frame+=1
            if self.frame==10:
                self.frame=0
            if key[pygame.K_d]:
                self.image=self.runAnims[self.frame]
                if self.rect.x<500:
                    self.rect.x+=self.dist
                self.lastState="right"    
            elif key[pygame.K_a]:
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
        if self.playerNum==1:
            for i in range(self.lives):
                self.surface.blit(self.heart,((i*25),0))
        else:
            for i in range(self.lives):
                self.surface.blit(self.heart,((i*25)+500,0))

#Class for the bullet 
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
        self.origX=xpos
        self.origY=ypos
        self.speed = [orientation, 0]
        area = pygame.display.get_surface().get_rect()
        self.width, self.height = area.width, area.height-35
        self.dead=False
        self.ammoSpawn=random.randint(1,10)

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

#Class for the powerup 
class Ammo(pygame.sprite.Sprite):
    def __init__(self,surf,xpos,ypos):
        pygame.sprite.Sprite.__init__(self) 
        self.image=pygame.image.load("images/ammo.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.dist = 2
        self.surface = surf
        self.dead = False

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def update(self):
        #makes note of when the bullet goes out of the screen
        if self.rect.y < 420:
            self.rect.y += self.dist

#helper function for class Ball
def clip(val, minval, maxval):
    return min(max(val, minval), maxval)

#Function to quit menu on the click of the Quit Button
def quitMenu(root):
    root.destroy()

#function to display help screen
def helpScreen(oldWindow):
    oldWindow.destroy()
    
    #creating menu window
    root=Tkinter.Tk()
    root.geometry("577x472")
    root.resizable(0,0)
    
    #creating background
    menuBGPhoto=ImageTk.PhotoImage(Image.open("images/backgroundOld.png"))
    BGLabel=Tkinter.Label(root,image=menuBGPhoto)
    BGLabel.place(x=0,y=0,relwidth=1,relheight=1)
    
    #creating help screen
    helpPhoto=ImageTk.PhotoImage(Image.open("images/Controls.png"))
    helpLabel=Tkinter.Label(root,image=helpPhoto)

    #creating button
    backBtnPhoto=ImageTk.PhotoImage(Image.open("images/backbutton.png")) 
    backBtn=Tkinter.Button(root,image=backBtnPhoto,command=lambda x=root:back(x))

    helpLabel.pack(pady=(40,0))
    backBtn.pack(pady=(20,0))
    
    root.mainloop()

#function to go back from help menu
def back(oldWindow):
    oldWindow.destroy()
    mainMenu()
    
#Function to go to the main menu once the player runs out of lives
def gameOver(surface,text,high):
    surface.blit(text,(220,220))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    mainMenu(high)
    
#Game window
def main(root,high=-1):
    #destroying old window
    root.destroy()

    #initalising pygame
    pygame.init()
    
    #declaring constants
    FPS=60
    WHITE = (255, 255, 255)
    pause_text = pygame.font.SysFont('Consolas', 32).render('PAUSE', True, pygame.color.Color('White'))
    gameOver_text = pygame.font.SysFont('Consolas', 32).render('GAME OVER', True, pygame.color.Color('Red'))
    level_text= pygame.font.SysFont('Consolas', 32).render('LEVEL 1', True, pygame.color.Color('White'))
    RUNNING=0
    PAUSE=1
    GAMEOVER=2
    isPause=False
    gravity=0.25
    RIGHT=2.5
    LEFT=-2.5
    level=1
    gotHit=False
    state=RUNNING
    startTime=0
    endTime=0
    Score=shelve.open('score2.txt')
    curScore=0
    
    #checking if highscore exists
    if Score.has_key('highscore')==False:
        Score['highscore']=0
    #if game is restarted in-game, check highscore (otherwise, shelf won't update properly)
    if high!=-1:
        Score['highscore']=high
        
    #text for current and high scores
    curScore_text=pygame.font.SysFont('Consolas', 20).render(('Current Score: '+str(curScore)), True, pygame.color.Color('Black'))
    highScore_text=pygame.font.SysFont('Consolas', 20).render(('High Score: '+str(Score['highscore'])), True, pygame.color.Color('Black'))

    #setting a variable for the pygame clock
    fpsClock=pygame.time.Clock()

    #creating pygame surface display
    DISPLAYSURF=pygame.display.set_mode((577,472),0,32)
    pygame.display.set_caption('Ballimination')
    background=pygame.image.load("images/backgroundOld.png")
    DISPLAYSURF.fill(WHITE)

    #levels
    levels={1:[[Ball(1,0,250,RIGHT)],0],2:[[Ball(1,0,250,RIGHT),Ball(1,577,250,LEFT)],0],3:[[Ball(2,0,250,RIGHT)],0],4:[[Ball(3,0,250,RIGHT)],0],5:[[Ball(4,0,200,RIGHT)],0]}
    levels1={1:[[Ball(1,0,250,RIGHT)],0],2:[[Ball(1,0,250,RIGHT),Ball(1,577,250,LEFT)],0],3:[[Ball(2,0,250,RIGHT)],0],4:[[Ball(3,0,250,RIGHT)],0],5:[[Ball(4,0,200,RIGHT)],0]}
    levels2={1:[[Ball(1,0,250,RIGHT)],0],2:[[Ball(1,0,250,RIGHT),Ball(1,577,250,LEFT)],0],3:[[Ball(2,0,250,RIGHT)],0],4:[[Ball(3,0,250,RIGHT)],0],5:[[Ball(4,0,200,RIGHT)],0]}
    levels3={1:[[Ball(1,0,250,RIGHT)],0],2:[[Ball(1,0,250,RIGHT),Ball(1,577,250,LEFT)],0],3:[[Ball(2,0,250,RIGHT)],0],4:[[Ball(3,0,250,RIGHT)],0],5:[[Ball(4,0,200,RIGHT)],0]}
    levels4={1:[[Ball(1,0,250,RIGHT)],0],2:[[Ball(1,0,250,RIGHT),Ball(1,577,250,LEFT)],0],3:[[Ball(2,0,250,RIGHT)],0],4:[[Ball(3,0,250,RIGHT)],0],5:[[Ball(4,0,200,RIGHT)],0]}
    levels5={1:[[Ball(1,0,250,RIGHT)],0],2:[[Ball(1,0,250,RIGHT),Ball(1,577,250,LEFT)],0],3:[[Ball(2,0,250,RIGHT)],0],4:[[Ball(3,0,250,RIGHT)],0],5:[[Ball(4,0,200,RIGHT)],0]}
  
    #creating the required objects
    player1=Player(DISPLAYSURF,225,360,1)
    player2=Player(DISPLAYSURF,275,360,2)
    players=[player1,player2]
    bullets=[]
    balls=levels[1][0]
    deadBalls=levels1[1][0]
    deadBalls1=levels2[1][0]
    deadBalls2=levels3[1][0]
    deadBalls3=levels4[1][0]
    deadBalls4=levels5[1][0]
    ammo=[]
    
    #starting level 1
    level_text = pygame.font.SysFont('Consolas', 32).render('LEVEL '+str(level), True, pygame.color.Color('White')) 
    DISPLAYSURF.blit(background,(0,0))
    for player in players:
        player.draw(DISPLAYSURF)
    DISPLAYSURF.blit(level_text,(220,220))
    DISPLAYSURF.blit(curScore_text,(205,0))
    DISPLAYSURF.blit(highScore_text,(220,15))
    pygame.display.update()
    pygame.time.delay(2000)


    
    #main game loop
    while True and (player1.lives!=0 or player2.lives!=0):        
        for event in pygame.event.get():
            #quit event
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            #shoots a bullet when you press the spacebar
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                if player1.lives!=0:
                    if isPause!=True:
                        #allows to shoot multiple bullets when powerup is enabled
                        if player1.powerUp==True:
                            bullet=Bullet(DISPLAYSURF,player1.rect.x+25,player1.rect.y)
                            bullets.append(bullet)
                        elif player1.powerUp==False:
                            if bullets==[]:
                                bullet=Bullet(DISPLAYSURF,player1.rect.x+25,player1.rect.y)
                                bullets.append(bullet)
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_w:
                if player2.lives!=0:
                    if isPause!=True:
                        #allows to shoot multiple bullets when powerup is enabled
                        if player2.powerUp==True:
                            bullet=Bullet(DISPLAYSURF,player2.rect.x+25,player2.rect.y)
                            bullets.append(bullet)
                        elif player2.powerUp==False:
                            if bullets==[]:
                                bullet=Bullet(DISPLAYSURF,player2.rect.x+25,player2.rect.y)
                                bullets.append(bullet)
            #pause event
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if state==PAUSE:
                        state=RUNNING
                        isPause=False
                    else:
                        state=PAUSE
                        isPause=True
                        
        if state==RUNNING:                
            #handles movement of player
            for player in players:
                player.keys()

            #updates every bullet on screen and removes dead bullets
            for i in bullets:
                i.update()
                if i.dead==True:
                    bullets.remove(i)

            #updates every ball on screen and removes dead balls
            for i in balls:
                i.speed[1] += gravity
                i.update()
                if i.dead==True:
                    balls.remove(i)

            for i in ammo:
                i.update()
                if i.dead==True:
                    ammo.remove(i)

            #collision b/w ball and player
            for ball in balls:
                for player in players:
                    if pygame.sprite.collide_rect(player,ball):
                        player.lives-=1
                        if player1.lives==0 and player2.lives==0:
                            high=Score['highscore']
                            gameOver(DISPLAYSURF,gameOver_text,high)
                        #if player has lives remaining, restart the level
                        else:
                            player1.rect.x=225
                            player2.rect.x=275
                            level_text = pygame.font.SysFont('Consolas', 32).render('LEVEL '+str(level), True, pygame.color.Color('White'))
                            DISPLAYSURF.blit(level_text,(220,220))
                            pygame.display.update()
                            pygame.time.delay(2000)
                            ammo=[]
                            player1.powerUp==False
                            player2.powerUp==False
                            if levels1[level][1]!=1:
                                balls=deadBalls
                                print 'ya'
                                for j in balls:
                                    j.rect.x=j.origX
                                    j.rect.y=j.origY
                                    j.speed[1]=0
                                levels1[level][1]=1
                            elif levels2[level][1]!=1:
                                balls=deadBalls1
                                print 'ya1'
                                for j in balls:
                                    j.rect.x=j.origX
                                    j.rect.y=j.origY
                                    j.speed[1]=0
                                levels2[level][1]=1
                            elif levels3[level][1]!=1:
                                balls=deadBalls2
                                print 'ya2'
                                for j in balls:
                                    j.rect.x=j.origX
                                    j.rect.y=j.origY
                                    j.speed[1]=0
                                levels3[level][1]=1
                            elif levels4[level][1]!=1:
                                balls=deadBalls3
                                print 'ya3'
                                for j in balls:
                                    j.rect.x=j.origX
                                    j.rect.y=j.origY
                                    j.speed[1]=0
                                levels4[level][1]=1
                            elif levels5[level][1]!=1:
                                balls=deadBalls4
                                print 'ya4'
                                for j in balls:
                                    j.rect.x=j.origX
                                    j.rect.y=j.origY
                                    j.speed[1]=0
                                levels5[level][1]=1



                #collision between ball and bullet 
                for i in bullets:
                    if pygame.sprite.collide_rect(ball,i):
                        ball.dead=True
                        curScore+=5
                        if curScore>Score['highscore']:
                            Score['highscore']=curScore
                        if ball.ammoSpawn==1 and ammo==[]:
                            ammo.append(Ammo(DISPLAYSURF,ball.rect.x,ball.rect.y))
                        deadBalls.append(ball)
                        bullets.remove(i)
                        if ball.num>1:
                            balls.append(Ball(ball.num-1,i.rect.x-10,i.rect.y-50,LEFT))
                            balls.append(Ball(ball.num-1,i.rect.x+10,i.rect.y-50,RIGHT))

            for i in ammo:
                for player in players:
                    if pygame.sprite.collide_rect(player,i):
                        i.dead=True
                        player.powerUp=True
                        startTime=pygame.time.get_ticks()

            for player in players:
                if player.powerUp==True:
                    endTime=pygame.time.get_ticks()
                    if endTime-startTime>=5000:
                        player.powerUp=False
                
            #drawing surface, player, ball and bullets
            DISPLAYSURF.blit(background,(0,0))
            for player in players:
                player.draw(DISPLAYSURF)
            for ball in balls:
                DISPLAYSURF.blit(ball.image, ball.rect)
            for i in bullets:
                i.draw()
            if ammo!=[]:
                for i in ammo:
                    i.draw()

        #pause screen        
        elif state==PAUSE:
            DISPLAYSURF.blit(pause_text,(250,220))

        #When level is finished
        if balls==[]:
            ammo=[]
            player1.rect.x=225
            player2.rect.x=275
            level+=1
            level_text = pygame.font.SysFont('Consolas', 32).render('LEVEL '+str(level), True, pygame.color.Color('White'))
            DISPLAYSURF.blit(level_text,(220,220))
            curScore_text=pygame.font.SysFont('Consolas', 20).render(('Current Score: '+str(curScore)), True, pygame.color.Color('Black'))
            highScore_text=pygame.font.SysFont('Consolas', 20).render(('High Score: '+str(Score['highscore'])), True, pygame.color.Color('Black'))
            DISPLAYSURF.blit(curScore_text,(205,0))
            DISPLAYSURF.blit(highScore_text,(220,15))
            pygame.display.update()
            pygame.time.delay(2000)
            balls=levels[level][0]
            deadBalls=levels1[level][0]
            deadBalls1=levels2[level][0]
            deadBalls2=levels3[level][0]
            deadBalls3=levels4[level][0]
            deadBalls4=levels5[level][0]

        #displaying score texts and displaying scores
        curScore_text=pygame.font.SysFont('Consolas', 20).render(('Current Score: '+str(curScore)), True, pygame.color.Color('Black'))
        highScore_text=pygame.font.SysFont('Consolas', 20).render(('High Score: '+str(Score['highscore'])), True, pygame.color.Color('Black'))
        DISPLAYSURF.blit(curScore_text,(205,0))
        DISPLAYSURF.blit(highScore_text,(220,15))

        
        #updating display window    
        pygame.display.update()
        fpsClock.tick(FPS)

        #Game over
        if player1.lives==0 and player2.lives==0:
            high=Score['highscore']
            gameOver(DISPLAYSURF,gameOver_text,high)
            
        for player in players:
            if player.lives==0:
                players.remove(player)

            
            
def mainMenu(high=-1):

        
    #creating menu window
    root=Tkinter.Tk()
    root.geometry("577x472")
    root.resizable(0,0)
    
    #creating background
    menuBGPhoto=ImageTk.PhotoImage(Image.open("images/background.png"))
    BGLabel=Tkinter.Label(root,image=menuBGPhoto)
    BGLabel.place(x=0,y=0,relwidth=1,relheight=1)

    #creating buttons
    playBtnPhoto=ImageTk.PhotoImage(Image.open("images/playbutton.png"))
    quitBtnPhoto=ImageTk.PhotoImage(Image.open("images/quitbutton.png"))
    helpBtnPhoto=ImageTk.PhotoImage(Image.open("images/helpbutton.png"))    
    playBtn=Tkinter.Button(root,image=playBtnPhoto,command=lambda x=root:main(x,high))
    helpBtn=Tkinter.Button(root,image=helpBtnPhoto,command=lambda x=root:helpScreen(x))
    quitBtn=Tkinter.Button(root,image=quitBtnPhoto,command=lambda x=root:quitMenu(x))

    #packing everything
    playBtn.pack(pady=(175,5))
    helpBtn.pack(pady=5)
    quitBtn.pack()

    #main loop
    root.mainloop()

mainMenu()

