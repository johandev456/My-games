import pygame
from random import randint as rand
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption('First Game')
#atributes
clock= pygame.time.Clock()

x = 50
y = 400
width = 64
height = 64
vel = 10
#sprites and background
walkRight =[pygame.image.load('R'+str(i)+'.png')  for i in range(1,10) ]
walkLeft =[pygame.image.load('L'+str(i)+'.png')  for i in range(1,10) ]
bg = pygame.image.load('bg.gif')
char = [pygame.image.load('standing.png'),pygame.image.load('standing2.png')]
isJump=False
jumpCount=10
left = False
right = False
walkCount =0
counter=0

#class

class player():

    def __init__(self,x,y,height,width,clock,n):
        self.x=x
        self.n=n
        self.clock=clock
        self.y = y
        self.width = width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount =10
        self.left = False
        self.right = False
        self.up=False
        self.down=False
        self.walkCount =0
        self.standing=True
        self.health=10
        self.hitbox=(self.x+17, self.y,self.width, self.height)
        self.visible=True
        self.score=0
    def move(self,win):
        global counter
        if self.visible:
            if self.walkCount + 1 >=27:
                self.walkCount = 0
            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                    self.walkCount+=1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                    self.walkCount+=1
                elif self.up:
                    win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                    self.walkCount+=1
                elif self.down:
                    win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                    self.walkCount+=1
            else:
                if self.left:
                                        
                    win.blit(walkLeft[0],(self.x,self.y))
                else:
                    win.blit(walkRight[0],(self.x,self.y))
            self.hitbox=(self.x+17, self.y,self.width, self.height)
            
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,(0,255,0),(self.hitbox[0],self.hitbox[1]-20,50-((50/10)*(10-self.health)),10))
            
    def hit(self):
     
     if self.health>0:
         self.health-=1
     else:
         
         self.visible=False
     

         
class Projectile():
     def __init__(self,x,y,height,width,color,facing):

         self.x=x
         self.y=y
         self.height=height
         self.width=width
         self.color=color
         self.facing=facing
         self.vel=8*facing

     def draw(self,win):

         pygame.draw.rect(win,self.color,(self.x,self.y,10,10))


# Draw the visual elements
purpleGuy= player(300,410,64,32,clock,1)
purpleGuy2= player(350,410,64,30,clock,2)
shootLoop=0
bullets=[]
font= pygame.font.SysFont('arial',15)
bullets2=[]
def redrawGameWindow(player):
    global walkCount
    global counter
    global win
    win.blit(bg,(0,0))
    for bullet in bullets:
        bullet.draw(win)
    for bullet in bullets2:
        bullet.draw(win)
    text=font.render(' score '+str(player[0].score),1,(255,255,255))
    text2=font.render(' score '+str(player[1].score),1,(255,255,255))
    if player[0].visible:
        win.blit(text,(player[0].hitbox[0],player[0].hitbox[1]-40))
    if player[1].visible:    
        win.blit(text2,(player[1].hitbox[0],player[1].hitbox[1]-40))
    player[0].move(win)
    player[1].move(win) 
   
 
        
    pygame.display.update()
#mainloop

class runner():
    
    def __init__(self,player):
        
        self.player=player
        self.shootLoop=0
    def controller(self):
    
        run= True
        while run:
            clock.tick(27)
            win.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run= False
            keys = pygame.key.get_pressed()
            for bullet in bullets:
                if self.player[1].visible:
                    if bullet.y>self.player[1].hitbox[1]-5 and bullet.y <=self.player[1].hitbox[1]+self.player[1].hitbox[3] :
                        if bullet.x>=self.player[1].hitbox[0] and bullet.x <=self.player[1].hitbox[1]+self.player[1].hitbox[2]:
                            self.player[1].hit()
                            self.player[0].score+=1
                            bullets.pop(bullets.index(bullet))
                if bullet.x >0 and bullet.x<500:
                    bullet.x +=bullet.vel
                else:

                    bullets.pop(bullets.index(bullet))
            for bullet in bullets2:
                if self.player[0].visible:
                    if bullet.y>self.player[0].hitbox[1]-5 and bullet.y <=self.player[0].hitbox[1]+self.player[0].hitbox[3] :
                        if bullet.x>=self.player[0].hitbox[0] and bullet.x <=self.player[0].hitbox[0]+self.player[0].hitbox[2]:
                            self.player[0].hit()
                            self.player[1].score+=1
                            bullets2.pop(bullets2.index(bullet))
                if bullet.x >0 and bullet.x<500:
                    bullet.x +=bullet.vel
                else:

                    bullets2.pop(bullets2.index(bullet))
            facing=0
            facing2=0
            if self.shootLoop >0:
                self.shootLoop +=1
            if self.shootLoop>3:
                self.shootLoop=0
            if keys[pygame.K_SPACE] and self.player[0].visible:
                
                if self.player[0].left:
                    facing=-1
                else:
                    facing=1

                if len(bullets)<5:
                    
                    bullets.append(Projectile(round(self.player[0].x+self.player[0].width//2),round(self.player[0].y+self.player[0].width//2),100,10,(255,255,255),facing))
                    
                self.shootLoop=1

            if keys[pygame.K_l] and self.player[1].visible:
                
                if self.player[1].left:
                    facing2=-1
                else:
                    facing2=1

                if len(bullets2)<5:
                    
                    bullets2.append(Projectile(round(self.player[1].x+self.player[1].width//2),round(self.player[1].y+self.player[1].width//2),100,10,(255,255,255),facing2))
                    
                self.shootLoop=1 
                
            
            if self.player[0].n==1 and self.player[0].visible:
                
                if keys[pygame.K_a] and self.player[0].x>self.player[0].vel:

                        self.player[0].x -= self.player[0].vel
                        self.player[0].left = True
                        self.player[0].right = False
                        self.player[0].standing= False
                elif keys[pygame.K_d] and self.player[0].x<500-self.player[0].width-self.player[0].vel :
                    self.player[0].x +=self.player[0].vel
                    self.player[0].right=True
                    self.player[0].left=False
                    self.player[0].standing= False
              
                elif keys[pygame.K_w] and self.player[0].y>20 :
                    self.player[0].y -=self.player[0].vel
                  
                    self.player[0].up=True
                    self.player[0].standing= False
                elif keys[pygame.K_s] and self.player[0].y<500-self.player[0].height :
                    self.player[0].y +=self.player[0].vel
              
                    self.player[0].up=False
                    self.player[0].down=True
                    self.player[0].standing= False
                    
                else:
                    self.player[0].standing= True
                    
                    self.player[0].walkCount=0
##                if not(self.player[0].isJump):
##                     
##                     if keys[pygame.K_e]: 
##                            self.player[0].isJump=True
##                            self.player[0].right = False
##                            self.player[0].left = False
##                            self.player[0].walkCount=0
##                else:
##                     
##                     if self.player[0].jumpCount >= -10:
##                        neg=1
##                        if self.player[0].jumpCount <0:
##                            neg=-1
##                        self.player[0].y -= (self.player[0].jumpCount **2)*0.5 *neg
##                        self.player[0].jumpCount -=1
##                     else:
##                        self.player[0].isJump = False
##                        self.player[0].jumpCount = 10
            if self.player[1].n==2 and self.player[1].visible:
                        if keys[pygame.K_LEFT] and self.player[1].x>self.player[0].vel:

                            self.player[1].x -= self.player[1].vel
                            self.player[1].left = True
                            self.player[1].right = False
                            self.player[1].standing= False
                                
                        elif keys[pygame.K_RIGHT] and self.player[1].x<500-self.player[1].width-self.player[1].vel :
                            self.player[1].x +=self.player[1].vel
                            self.player[1].right=True
                            self.player[1].left=False
                            self.player[1].standing= False
                        elif keys[pygame.K_UP] and self.player[1].y>20 :
                            self.player[1].y -=self.player[1].vel
                            self.player[1].up=True
                            self.player[1].standing= False
                        elif keys[pygame.K_DOWN] and self.player[1].y<500-self.player[1].height :
                            self.player[1].y +=self.player[1].vel
                            self.player[1].up=False
                            self.player[1].down=True
                            self.player[1].standing= False
                            
                        else:
                            self.player[1].standing= True
                            
                            self.player[1].walkCount=0
##                        if not(self.player[1].isJump):
##                             
##                             if keys[pygame.K_SPACE]: 
##                                    self.player[1].isJump=False
##                                    self.player[1].right = False
##                                    self.player[1].left = False
##                                    self.player[1].walkCount=0
##                        else:
##                             
##                             if self.player[1].jumpCount >= -10:
##                                neg=1
##                                if self.player[1].jumpCount <0:
##                                    neg=-1
##                                self.player[1].y -= (self.player[1].jumpCount **2)*0.5 *neg
##                                self.player[1].jumpCount -=1
##                             else:
##                                self.player[1].isJump = False
##                                self.player[1].jumpCount = 10
                
            redrawGameWindow(self.player)
    
PS=[purpleGuy,purpleGuy2]    
P1=runner(PS)
P1.controller()


    
pygame.quit()

