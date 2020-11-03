import time
import numpy as np
import pygame
import sys
import seaborn as sns

from pygame.locals import *
pygame.init()


class Network:
    def __init__(self, xmin, xmax, ymin, ymax):
        """
        xmin: 150,
        xmax: 450, 
        ymin: 100, 
        ymax: 600
        """
        
        self.StaticDiscipline = {
            'xmin': xmin, 
            'xmax': xmax, 
            'ymin': ymin, 
            'ymax': ymax
        }

    def network(self, xsource, ysource = 100, Ynew = 600, divisor = 50): #ysource will always be 100
        """
        For Network A
        ysource: will always be 100
        xsource: will always be between xmin and xmax (static discipline)
        
        For Network B
        ysource: will always be 600
        xsource: will always be between xmin and xmax (static discipline)
        """
        
        while True:
            ListOfXsourceYSource = []
            Xnew = np.random.choice([i for i in range(self.StaticDiscipline['xmin'], self.StaticDiscipline['xmax'])], 1)
            #Ynew = np.random.choice([i for i in range(self.StaticDiscipline['ymin'], self.StaticDiscipline['ymax'])], 1)

            source = (xsource, ysource)
            target = (Xnew[0], Ynew)

            #Slope and intercept
            slope = (ysource - Ynew)/(xsource - Xnew[0])
            intercept = ysource - (slope*xsource)
            if (slope != np.inf) and (intercept != np.inf):
                break
            else:
                continue
                
        #print(source, target)
        # randomly select 50 new values along the slope between xsource and xnew (monotonically decreasing/increasing)
        XNewList = [xsource]

        if xsource < Xnew:
            differences = Xnew[0] - xsource
            increment = differences /divisor
            newXval = xsource
            for i in range(divisor):

                newXval += increment
                XNewList.append(int(newXval))
        else:
            differences = xsource - Xnew[0]
            decrement = differences /divisor
            newXval = xsource
            for i in range(divisor):

                newXval -= decrement
                XNewList.append(int(newXval))
                

        #determine the values of y, from the new values of x, using y= mx + c
        yNewList = []
        for i in XNewList:
            findy = (slope * i) + intercept#y = mx + c
            yNewList.append(int(findy))

        ListOfXsourceYSource = [(x, y) for x, y in zip(XNewList, yNewList)]

        return XNewList, yNewList
    
    
    
    def DefaultToPosition(self, x1, x2 = 300, divisor = 50):
        DefaultPositionA = 300
        DefaultPositionB = 300
        XNewList = []
        if x1 < x2:
            differences = x2 - x1
            increment = differences /divisor
            newXval = x1
            for i in range(divisor):
                newXval += increment
                XNewList.append(int(np.floor(newXval)))

        else:
            differences = x1 - x2
            decrement = differences /divisor
            newXval = x1
            for i in range(divisor):
                newXval -= decrement
                XNewList.append(int(np.floor(newXval)))
        return XNewList
    
    

    
class pytennis:
    def __init__(self, fps = 50):
        self.net = Network(150,450,100,600)
        
        # Testing
        self.net = Network(150, 450, 100, 600)
        NetworkA = self.net.network(300, ysource=100, Ynew=600)  # Network A
        NetworkB = self.net.network(200, ysource=600, Ynew=100)  # Network B
        # NetworkA

        # display test plot of network A
        sns.jointplot(NetworkA[0], NetworkA[1])

        # display test plot of network B
        sns.jointplot(NetworkB[0], NetworkB[1])
        
        out = self.net.DefaultToPosition(250)
        
        pygame.init()
        self.FPS = fps
        self.fpsClock = pygame.time.Clock()

        # set up the window
        self.DISPLAYSURF = pygame.display.set_mode((600, 700), 0, 32)
        pygame.display.set_caption('REINFORCEMENT LEARNING (Discrete Mathematics) - TABLE TENNIS')
        # set up the colors
        self.BLACK = ( 0,0,0)
        self.WHITE = (255, 255, 255)
        self.RED= (255,0,0)
        self.GREEN = ( 0, 255,0)
        self.BLUE = ( 0,0, 255)
        
        # draw on the surface object
        #self.display()
        
        

        
    def display(self):
        self.DISPLAYSURF.fill(self.WHITE)
        pygame.draw.rect(self.DISPLAYSURF, self.GREEN, (150, 100, 300, 500))
        pygame.draw.rect(self.DISPLAYSURF, self.RED, (150, 340, 300, 20))
        pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (0, 20, 600, 20))
        pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (0, 660, 600, 20))
        return
    
    
    
    def reset(self):
        return
    
    
    
    def render(self):
        # diplay team players
        self.PLAYERA = pygame.image.load('images/cap.jpg')
        self.PLAYERA = pygame.transform.scale(self.PLAYERA, (50, 50))
        self.PLAYERB = pygame.image.load('images/cap.jpg')
        self.PLAYERB = pygame.transform.scale(self.PLAYERB, (50, 50))
        self.ball = pygame.image.load('images/ball.png')
        self.ball = pygame.transform.scale(self.ball, (15, 15))

        self.playerax = 150
        self.playerbx = 250
        self.directionA = 'right'
        self.directionB = 'right'
        self.ballDirection = 'top'
        self.ballx = 250
        self.bally = 300
        
        
        
        nextplayer = 'A'
        lastxcoordinate = 350
        count = 0
        
        while True:
            self.display()
            if nextplayer == 'A':
                #playerA should play
                if count == 0:
                    #playerax = lastxcoordinate
                    NetworkA = self.net.network(lastxcoordinate, ysource = 100, Ynew = 600) #Network A
                    out = self.net.DefaultToPosition(lastxcoordinate)

                    #update lastxcoordinate

                    self.bally = NetworkA[1][count]
                    self.playerax = self.ballx
                    count += 1
        #             soundObj = pygame.mixer.Sound('sound/sound.wav')
        #             soundObj.play()
        #             time.sleep(0.4)
        #             soundObj.stop()
                else:
                    self.ballx = NetworkA[0][count]
                    self.bally = NetworkA[1][count]
                    self.playerbx = self.ballx
                    self.playerax = out[count]
                    count += 1

                #let playerB play after 50 new coordinate of ball movement
                if count == 49:
                    count = 0
                    nextplayer = 'B'
                else:
                    nextplayer = 'A'





            else:
                #playerB can play
                if count == 0:
                    #playerbx = lastxcoordinate
                    NetworkB = self.net.network(lastxcoordinate, ysource = 600, Ynew = 100) #Network B
                    out = self.net.DefaultToPosition(lastxcoordinate)

                    #update lastxcoordinate
                    self.bally = NetworkB[1][count]
                    self.playerbx = self.ballx
                    count += 1

        #             soundObj = pygame.mixer.Sound('sound/sound.wav')
        #             soundObj.play()
        #             time.sleep(0.4)
        #             soundObj.stop()
                else:
                    self.ballx = NetworkB[0][count]
                    self.bally = NetworkB[1][count]
                    self.playerbx = out[count]
                    self.playerax = self.ballx
                    count += 1
                #update lastxcoordinate

                #let playerA play after 50 new coordinate of ball movement
                if count == 49:
                    count = 0
                    nextplayer = 'A'
                else:
                    nextplayer = 'B'




            #CHECK BALL MOVEMENT
            self.DISPLAYSURF.blit(self.PLAYERA, (self.playerax, 50))
            self.DISPLAYSURF.blit(self.PLAYERB, (self.playerbx, 600))
            self.DISPLAYSURF.blit(self.ball, (self.ballx, self.bally))

            #update last coordinate
            lastxcoordinate = self.ballx 

            pygame.display.update()
            self.fpsClock.tick(self.FPS)

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


           
        
if __name__ == '__main__':
    tennis = pytennis(fps = 70)
    tennis.reset()
    tennis.render()