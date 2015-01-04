import Tkinter as TK
import random
import math
import copy

class Animation(object):
    #This class is taken from lecture notes created by Prof David Kosbie (CMU)
    def mousePressed(self, event): pass
    def keyPressed(self, event): pass
    def timerFired(self): pass
    def init(self): pass
    def redrawAll(self): pass
    def run(self, height=640, width=1136): 
        root = TK.Tk() 
        self.width = width 
        self.height = height
        self.canvas = TK.Canvas(root, width=width, height=height) 
        self.canvas.pack() 
        def redrawAllWrapper(): 
            self.canvas.delete(TK.ALL) 
            self.redrawAll()
        def mousePressedWrapper(event): 
            self.mousePressed(event) 
            redrawAllWrapper() 
        def keyPressedWrapper(event): 
            self.keyPressed(event) 
            redrawAllWrapper() 
        def mouseHeldWrapper(event): #created
            self.mouseHeld(event)
            redrawAllWrapper()
        def mouseReleasedWrapper(event): #created
            self.mouseReleased(event)
            redrawAllWrapper()
        root.bind("<Button-1>", mousePressedWrapper) 
        root.bind("<Key>", keyPressedWrapper) 
        root.bind("<B1-Motion>", mouseHeldWrapper) #created
        root.bind("<ButtonRelease-1>", mouseReleasedWrapper) #created
        self.timerFiredDelay = 10
        def timerFiredWrapper(): 
            self.timerFired() 
            redrawAllWrapper() 
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper) 
        self.init() 
        timerFiredWrapper() 
        root.mainloop()

class Bonkers(Animation):
    def init(self):
        self.timerCounter=0
        self.theBall=Ball(50,self.height/2,15,"cyan")
        self.theGoal=Goal(self.width-100,self.height/2-40,80)
        self.thePlayTourButton=PlayButton(self.width/2-150,self.height*3/5,70,True)
        self.thePlayRandomButton=PlayButton(self.width/2+150,self.height*3/5,70,False)
        self.theInstructionsButton=InstructionsButton(65,self.height-65,55)
        self.theAcknowledgementsButton=AcknowledgementsButton(self.width-65,
                                                              self.height-65,55)
        self.theHelpButton=HelpButton(50,50,30)
        self.theBarrierAdditionButton=BarrierAdditionButton(self.width-60,
                self.height-60)
        self.theHelpScreen=HelpScreen(self.width/2-200,self.height/2-100)
        self.theGoalBox=PopBox(self.width/2-200, self.height/2-100,"GOAL")
        self.theRetryBox=PopBox(self.width/2-200, self.height/2-100,"OUT OF BOUNDS")
        self.theSureSaveBox=SureSaveBox(self.width/2-200,self.height/2-100)
        self.originalBally=copy.deepcopy(self.theBall.y)
        self.originalBallx=copy.deepcopy(self.theBall.x)
        self.inMenuScreen=True
        self.inPlayingScreen=False
        self.inTestMode=False
        self.inInstructionsScreen=False
        self.inAcknowledgementsScreen=False
        self.inBarrierBuilderMode=False
        self.inHelpScreen=False
        self.inLevelCreatorMode=False
        self.firstBallClick=False
        self.circleClicked=False
        self.sureSaveMode=False
        self.barrierHits=0
        self.retries=0
        self.releasedx=0
        self.releasedy=0
        self.held=False
        self.heldx=(-10) #just want it off the screen
        self.heldy=(-10) #same^
        self.barrierList=[]
        self.circleList=[]
        self.circleListMaker(5)
        self.currentLevel=0
        self.barrierTotal=0
        self.comparedToPar=0
        self.tourBarriersUsed=[]
        self.parArray=[1,2,2,1,2,2,1,4,3,5]
        self.levelList=[
        #1
        [[525, 309, 40]],
        #2
        [[525, 309, 40], [522, 83, 40], [528, 540, 40], [713, 310, 40], [328, 309, 40]],
        #3
        [[537, 320, 230], [537, 320, 130], [537, 320, 70], [537, 320, 40]],
        #4
        [[531, 342, 140], [627, 214, 40], [427, 220, 40]],
        #5
        [[697, 510, 40], [683, 76, 40], [432, 301, 40], [551, 407, 40], [560, 198, 40]],
        #6
        [[562, 490, 40], [423, 301, 40], [518, 84, 40], [456, 186, 40], [470, 408, 40], 
        [687, 437, 40], [544, 309, 40], [677, 324, 40], [617, 43, 40]],
        #7
        [[512, 320, 40], [339, 466, 40], [277, 362, 40], [568, 557, 40], [656, 472, 40], 
        [442, 555, 40], [727, 357, 40], [352, 131, 80], [655, 131, 80]],
        #8
        [[274, 331, 40], [399, 115, 40], [408, 544, 40], [275, 473, 40], [406, 267, 40], 
        [525, 327, 40], [525, 459, 40], [408, 393, 40], [631, 398, 40], [633, 263, 40], 
        [266, 179, 40], [527, 213, 40], [636, 547, 40], [747, 330, 40], [629, 111, 40], 
        [745, 487, 40], [753, 165, 40]],
        #9
        [[180, 333, 40], [64, 526, 40], [178, 207, 40], [181, 460, 40], [57, 156, 40], 
        [529, 338, 90], [970, 161, 40], [845, 316, 40], [969, 468, 40]],
        #10
        [[298, 304, 110], [511, 312, 90], [686, 319, 70], [822, 325, 50]]
        ]
    
    def mousePressed(self, event):
        if self.inMenuScreen:
            #clicks play tour button
            if self.circularHitBox(event,self.thePlayTourButton):
                self.exitOtherScreens()
                self.inPlayingScreen=True
                self.currentLevel+=1
            #clicks play random button
            if self.circularHitBox(event,self.thePlayRandomButton):
                self.exitOtherScreens()
                self.inPlayingScreen=True
            #clicks instructions button
            if self.circularHitBox(event,self.theInstructionsButton):
                self.exitOtherScreens()
                self.inInstructionsScreen=True
            #clicks acknowledgements button
            if self.circularHitBox(event,self.theAcknowledgementsButton):
                self.exitOtherScreens()
                self.inAcknowledgementsScreen=True
        elif self.inPlayingScreen:
            if not self.inHelpScreen:
                #clicks GOAL Box to start new game
                if self.inGoal()==True:
                    if self.rectangularHitBox(event,self.theGoalBox):
                        if self.currentLevel==0:
                            self.newGame()
                        else:
                            self.nextLevel()
                #clicks OUT OF BOUNDS box
                if self.offScreen()==True:
                    if self.rectangularHitBox(event,self.theRetryBox):
                        self.retry()
                #below is if you click on the ball
                if self.circularHitBox(event,self.theBall):
                    if self.ballMovement()!=True:
                        if self.inBarrierBuilderMode==False:                                
                            if self.inGoal()!=True:
                                self.firstBallClick=True
                #below is if you click the barrier addition button
                if not self.inBarrierBuilderMode and self.ballMovement()!=True:
                    if self.rectangularHitBox(event,self.theBarrierAdditionButton):
                        self.inBarrierBuilderMode=True
                elif self.inBarrierBuilderMode:
                    #below is should you wish to create barriers
                    if not self.rectangularHitBox(event,self.theBarrierAdditionButton):
                        self.barrierList.append(Barrier(event.x,event.y))
                    #below is if youre done building barriers
                    else:
                        self.inBarrierBuilderMode=False
                #clicks help
                if self.circularHitBox(event,self.theHelpButton):
                    self.inHelpScreen=True
            #clicks help box to exit help
            if self.inHelpScreen:
                if self.rectangularHitBox(event,self.theHelpScreen):
                    self.inHelpScreen=False
        elif self.inLevelCreatorMode:
            #makes self.circleClicked return the object (the circle) you clicked
            for circle in self.circleList:
                if self.circularHitBox(event,circle):
                    self.circleClicked=circle
            if self.sureSaveMode:
                if self.rectangularHitBox(event,self.theSureSaveBox):
                    alreadyInLevels=self.readLevels()
                    self.writeLevels(str(alreadyInLevels)+"\n"+str(self.circleList))
                    self.sureSaveMode=False
                    print self.readLevels()
                else:
                    self.sureSaveMode=False
        else:
            if self.circularHitBox(event,self.theHelpButton):
                    self.inHelpScreen=True
            #clicks help box to exit help
            if self.inHelpScreen:
                if self.rectangularHitBox(event,self.theHelpScreen):
                    self.inHelpScreen=False

    def mouseHeld(self, event):
        if self.inPlayingScreen:
            if self.firstBallClick==True:
                self.heldx=event.x
                self.heldy=event.y
                self.held=True
        if self.inLevelCreatorMode:
            if self.circleClicked!=False:
                self.circleClicked.x=event.x
                self.circleClicked.y=event.y

    def mouseReleased(self, event):
        if self.firstBallClick==True:
            self.releasedx=event.x
            self.releasedy=event.y
            self.held=False
        if self.circleClicked!=False:
            self.circleClicked=False

    def keyPressed(self, event):
        if event.keysym=="c": #CREATE mode
            self.exitOtherScreens()
            self.inLevelCreatorMode=True
        if event.keysym=="q" and self.currentLevel>0 and self.currentLevel<11: 
            #QHEAT (cheat) and go to next level
            self.nextLevel()
        if event.keysym=="p": #PLUS a circle in charlie mode
            if self.inLevelCreatorMode:
                self.circleListMaker(1)
        if event.keysym=="b" and self.inLevelCreatorMode: #BIGGER; last circle.rad + 10
            if len(self.circleList)>0:
                self.circleList[len(self.circleList)-1].rad+=10
        if event.keysym=="t": #TEST; test the level you just created
            self.test()
        if event.keysym=="m": #MENU
            self.init()
        if event.keysym=="n": #NEW GAME
            if self.inGoal() and self.currentLevel>0:
                self.nextLevel()
            if self.currentLevel==0:
                self.newGame()
        if event.keysym=="u": #UNDO
            if self.inBarrierBuilderMode==True and not self.inHelpScreen:
                if len(self.barrierList)>0:
                    self.barrierList.pop(len(self.barrierList)-1)
            elif self.inLevelCreatorMode:
                if len(self.circleList)>0:
                    self.circleList.pop(len(self.circleList)-1)
        if event.keysym=="b": #BUILD (same as clicking barrier builder addition button)
            if (self.ballMovement()!=True and not self.inHelpScreen 
                and self.firstBallClick==False):
                if self.inBarrierBuilderMode==False:
                    self.inBarrierBuilderMode=True
                else: 
                    self.inBarrierBuilderMode=False
        if event.keysym=="r" and not self.inGoal():#RETRY, ball to goes to starting position
            if not self.inHelpScreen:
                self.retry()
        if event.keysym=="s": #SAVE a level
            if self.inLevelCreatorMode:
                self.sureSaveMode=True

    def redrawAll(self):
        if self.inMenuScreen:
            self.drawMenuScreen()
        elif self.inInstructionsScreen:
            self.drawInstructionsScreen()
        elif self.inAcknowledgementsScreen:
            self.drawAcknowledgementsScreen()
        elif self.inPlayingScreen:
            self.drawLevel(self.currentLevel)
        if self.inLevelCreatorMode:
            self.drawLevelCreatorMode()
            if self.sureSaveMode:
                self.theSureSaveBox.draw(self.canvas)
        if self.inHelpScreen:
            self.theHelpScreen.draw(self.canvas)

    def writeLevels(self,substance):
        with open("Bonkers Levels.txt","w") as writeLevels:
            writeLevels.write(str(substance))

    def readLevels(self):
        try:
            with open("Bonkers Levels.txt","r") as readLevels:
                return readLevels.read()
        except:
            with open("Bonkers Levels.txt","w") as readLevels:
                return readLevels.write("")

    def writeHighs(self,substance):
        with open("Bonkers Highs.txt","w") as writeHighs:
            writeHighs.write(str(substance))

    def readHighs(self):
        try:
            with open("Bonkers Highs.txt","r") as readHighs:
                return readHighs.read()
        except:
            with open("Bonkers Highs.txt","w") as readHighs:
                return readHighs.write("99") #Default High is 99 until beaten

    def test(self):
        self.exitOtherScreens()
        self.inPlayingScreen=True

    def newGame(self):
        localtourBarrierUsed=self.tourBarriersUsed
        self.init()
        self.tourBarriersUsed=localtourBarrierUsed
        self.inMenuScreen=False
        self.inPlayingScreen=True

    def nextLevel(self):
        self.tourBarriersUsed.append(len(self.barrierList)+self.retries)
        localCurrentLevel=self.currentLevel
        self.newGame()
        self.currentLevel=localCurrentLevel+1
        if self.currentLevel>10:
            for i in xrange(len(self.parArray)):
                self.comparedToPar+=(self.tourBarriersUsed[i]-self.parArray[i])
                self.barrierTotal+=self.tourBarriersUsed[i]
            legit=True
            for i in self.tourBarriersUsed:
                if i==0:
                    legit=False #see if q was used at all
            if legit==True:
                if int(self.readHighs())>self.barrierTotal:
                    self.writeHighs(str(self.barrierTotal))
        self.drawLevel(self.currentLevel)

    def retry(self):
        #cant just overwrite a self.init() because need to count retries
        self.theBall=Ball(50,self.height/2,15,"cyan")
        self.inBarrierBuilderMode=False
        self.firstBallClick=False
        self.barrierHits=0
        self.releasedx=0
        self.releasedy=0
        self.held=False
        self.heldx=(-10)
        self.heldy=(-10)
        self.retries+=1

    def drawLevel(self,levelNumber):
        if levelNumber==0:
            self.drawPlayingScreen()
        elif levelNumber>10:
            self.drawResultsScreen()
        else:
            self.drawPlayingScreen()
            self.currentLevel=levelNumber
            self.circleList=[]
            for i in xrange(len(self.levelList[levelNumber-1])):
                self.circleList.append(Circle(self.levelList[levelNumber-1][i][0],
                                              self.levelList[levelNumber-1][i][1],
                                              self.levelList[levelNumber-1][i][2],
                                              "black","dark grey"))

    def exitOtherScreens(self):
        self.inMenuScreen=False
        self.inPlayingScreen=False
        self.inInstructionsScreen=False
        self.inAcknowledgementsScreen=False
        self.inBarrierBuilderMode=False
        self.inHelpScreen=False
        self.inLevelCreatorMode=False

    def circularHitBox(self,event,anObject):
        if (((event.x-anObject.x)**2+(event.y-anObject.y)**2)**0.5<=anObject.rad):
            return True

    def rectangularHitBox(self,event,anObject):
        if (event.x>anObject.x0 and event.x<anObject.x1 and 
            event.y>anObject.y0 and event.y<anObject.y1):
            return True

    def drawMenuScreen(self):
        self.canvas.create_rectangle(-1,-1,self.width+50,
            self.height+50,fill="lavender") #lavender background
        self.canvas.create_text(self.width-80,20,text="Charlie DiGiovanna",
            font=("Verdana",13,"bold"))
        for i in xrange(29):
            self.canvas.create_oval(i*21,i*21,i*22,i*22,fill="white")
        self.canvas.create_text(self.width/2,self.height/4,
            text="Welcome to\n   Bonkers",font=("Verdana",64))
        self.thePlayTourButton.draw(self.canvas)
        self.thePlayRandomButton.draw(self.canvas)
        self.theInstructionsButton.draw(self.canvas)
        self.theAcknowledgementsButton.draw(self.canvas)

    def drawAcknowledgementsScreen(self):
        self.canvas.create_rectangle(-1,-1,self.width+50,
            self.height+50,fill="lavender") #lavender background
        self.theHelpButton.draw(self.canvas)
        self.canvas.create_text(self.width/2,self.height/2-8,
            text="A big thanks to Brock Schmid for advice with coding",
            font="Verdana")
        self.canvas.create_text(self.width/2,self.height/2+12,
            text="and David Kosbie for his beautiful Animation Class.",
            font="Verdana")

    def drawInstructionsScreen(self):
        self.canvas.create_rectangle(-1,-1,self.width+50,
            self.height+50,fill="lavender") #lavender background
        self.theHelpButton.draw(self.canvas)
        instructionArray=["Direct the ball into the Goal by clicking and holding",
        "Avoid the Black Holes!","You can create Barriers for your ball to bounce off of",
        "Don't fly off the screen, you won't bounce!","",
        "Building Barriers:","To build barriers, you must first enter Barrier Builder Mode",
        "To do this, either press the plus sign on the bottom right or B on your keyboard",
        "While in Barrier Builder Mode, click anywhere on the screen to place a barrier",
        "Press U on your keyboard to remove the most recently created barrier",
        "To exit the mode, click on the check on the bottom right or B on your keyboard","",
        "Tour Mode:",
        "Go through levels using as few barriers and retries as possible",
        "Each retry adds to your barrier total","Try your best to beat your previous low!",
        "",
        "Random Mode:","Practice your skills using randomly generated maps",
        "Neither barrier count nor retries are recorded"]
        for i in xrange(len(instructionArray)):
            if i<4:
                self.canvas.create_text(self.width/2,self.height/5.25+i*25,
                    text=instructionArray[i],font=("Verdana",18,"bold"))
            else:
                self.canvas.create_text(self.width/2,self.height/4.25+i*20,
                    text=instructionArray[i],font="Verdana")

    def drawPlayingScreen(self):
        if self.inBarrierBuilderMode:
            self.canvas.create_rectangle(-1,-1,self.width+50,
                self.height+50,fill="beige") #lavender background
        else:
            self.canvas.create_rectangle(-1,-1,self.width+50,
                self.height+50,fill="lavender") #lavender background
        for circle in self.circleList: #draw circles
            circle.draw(self.canvas)
        if self.inBarrierBuilderMode==False: #draw barrier builder button
            self.theBarrierAdditionButton.drawNotBarrierBuilderMode(self.canvas)
        elif self.inBarrierBuilderMode==True:
            self.theBarrierAdditionButton.drawBarrierBuilderMode(self.canvas)
        if self.firstBallClick==True: #move if clicked
            if self.hittingCircles()!=True:
                if self.inGoal()!=True:
                    self.ballMovement()
        if self.held==True: #draw green dot where youre holding in mouse
            GreenDot(self.heldx,self.heldy).draw(self.canvas)
        for barrier in self.barrierList: #draw barriers
            barrier.draw(self.canvas)
        self.hittingCircles() #check for hits on circles
        self.hittingBarrier() #check for hits on barriers
        self.inGoal() #check for goal
        self.offScreen() #check if out of bounds
        if self.currentLevel==0:
            self.drawRandomScore()
        else:
            self.drawTourScore()
        self.theHelpButton.draw(self.canvas) #draw help button
        self.theBall.draw(self.canvas) #draw ball
        self.theGoal.draw(self.canvas) #draw goal

    def timerFired(self):
        #increases timer counter by 1 for every x milliseconds; x is set by "delay"
        self.timerCounter+=1

    def circleListMaker(self,number):
        for i in xrange(number):
            self.circleList.append(Circle(random.randint(100,self.width-200),
                random.randint(50,self.height-50),40,
                "green","pink"))

    def hittingCircles(self):
        for circle in self.circleList:
            #sees if hits circles
            if (((self.theBall.x-circle.x)**2+(self.theBall.y-
                circle.y)**2)**0.5<=self.theBall.rad+circle.rad):
                    return True

    def hittingBarrier(self):
        #counts barrier hits
        for barrier in self.barrierList:
            #sees if hits a barrier while going upward
            if (self.theBall.y-self.theBall.rad>=barrier.y0 and
                self.theBall.y-self.theBall.rad<=barrier.y1 and
                self.theBall.x>=barrier.x0 and
                self.theBall.x<=barrier.x1):
                self.barrierHits+=1
            #sees if hits a barrier while going downward
            if (self.theBall.y+self.theBall.rad>=barrier.y0 and
                self.theBall.y+self.theBall.rad<=barrier.y1 and
                self.theBall.x>=barrier.x0 and
                self.theBall.x<=barrier.x1):
                self.barrierHits+=1

    def ballMovement(self): 
        #dictates ball movement and returns true if moving
        speedConstant=15.001
        #^^there must be a .001 because it tends to crash if the ball reaches
        #exact release coordinates, which it often will
        if (self.releasedx != 0 and 
            self.releasedy != 0 and 
            self.releasedx-self.originalBallx!=0 and 
            self.releasedy-self.originalBally!=0):
            slope=((self.releasedy-self.originalBally)*1.0/
                  (self.releasedx-self.originalBallx))
            if self.barrierHits%2==0:
                self.theBall.x+=speedConstant
                self.theBall.y+=speedConstant*slope
            elif self.barrierHits%2==1:
                self.theBall.x+=speedConstant
                self.theBall.y-=speedConstant*slope
            return True

    def inGoal(self):
        #if ball is in goal, draws Goal Box and returns True
        if self.theBall.x+self.theBall.rad>self.theGoal.x0:
            if self.theBall.x+self.theBall.rad<self.theGoal.x1:
                if self.theBall.y>self.theGoal.y0:
                    if self.theBall.y<self.theGoal.y1:
                        self.theGoalBox.draw(self.canvas)
                        self.firstBallClick=False
                        return True

    def offScreen(self):
        if (self.theBall.x<-20 or self.theBall.x>self.width+20 or 
            self.theBall.y<-20 or self.theBall.y>self.height):
            self.theRetryBox.draw(self.canvas)
            return True

    def drawRandomScore(self):
        self.canvas.create_text(self.width-70,25,text="Barriers",
            font=("Verdana",25))
        self.canvas.create_text(self.width-70,55,
            text=str(len(self.barrierList)+self.retries),
            font=("Verdana",40))
        self.canvas.create_text(self.width-70,90,text="Retry's",
            font=("Verdana",25))
        self.canvas.create_text(self.width-70,125,text=str(self.retries),
            font=("Verdana",40))        

    def drawTourScore(self):
        self.canvas.create_text(self.width-70,25,text="Barriers",
            font=("Verdana",25))
        self.canvas.create_text(self.width-70,60,
            text=str(len(self.barrierList)+self.retries),
            font=("Verdana",40))
        self.canvas.create_text(self.width-70,100,text="Retry's",
            font=("Verdana",25))
        self.canvas.create_text(self.width-70,135,text=str(self.retries),
            font=("Verdana",40))
        self.canvas.create_text(self.width-70,175,text="Par",
            font=("Verdana",25))
        self.canvas.create_text(self.width-70,210,
            text=str(self.parArray[self.currentLevel-1]),font=("Verdana",40))
        self.canvas.create_rectangle(15,self.height-60,
            65,self.height-10,fill="white")
        self.canvas.create_rectangle(15+3,self.height-60+3,
            65-3,self.height-10-3,fill="gold")
        self.canvas.create_text(40,self.height-50,
            text="Hole",font=("Verdana",12),fill="black")
        self.canvas.create_text(40,self.height-30,
            text=str(self.currentLevel),font=("Verdana",32),fill="black")

    def drawLevelCreatorMode(self):
        self.canvas.create_rectangle(-1,-1,self.width+50,
            self.height+50,fill="beige") #lavender background
        self.theBall.draw(self.canvas) #draw ball
        self.theGoal.draw(self.canvas) #draw goal
        self.theHelpButton.draw(self.canvas) #draw help button
        for circle in self.circleList: #draw circles
            circle.draw(self.canvas)

    def drawResultsScreen(self):
        #Lavender background:
        self.canvas.create_rectangle(-1,-1,self.width+50,
            self.height+50,fill="lavender")
        #Bonkers Balls:
        for i in xrange(29):
            self.canvas.create_oval(i*21,i*21,i*22,i*22,fill="white")
        #Header:
        self.canvas.create_text(self.width/2,self.height/12,
            text="Bonkers Tour",font=("Verdana",28))
        self.canvas.create_text(self.width/2,self.height/12+40,
            text="Results",font=("Verdana",45))
        #Hole Number:
        for i in xrange(1,11):
            self.canvas.create_text(self.width/5,self.height/4+i*40,text=str(i),
                font=("Verdana",20))
        #Barriers Used:
        for i in xrange(len(self.tourBarriersUsed)):
            self.canvas.create_text(self.width/5+160,self.height/4+i*40+40,
                text=str(self.tourBarriersUsed[i]),font=("Verdana",20))
        #Pars:
        for i in xrange(len(self.parArray)):
            self.canvas.create_text(self.width/5+320,self.height/4+i*40+40,
                text=str(self.parArray[i]),font=("Verdana",20))
        #Compared to Pars:
        for i in xrange(len(self.parArray)):
            if self.tourBarriersUsed[i]-self.parArray[i]>1:
                self.canvas.create_text(self.width/5+480,self.height/4+i*40+40,
                text="+"+str(self.tourBarriersUsed[i]-self.parArray[i]),font=("Verdana",20))
            else:
                self.canvas.create_text(self.width/5+480,self.height/4+i*40+40,
                text=str(self.tourBarriersUsed[i]-self.parArray[i]),font=("Verdana",20))
        #Column Headers:
        self.canvas.create_text(self.width/5,self.height/4,text="Hole",
            font=("Verdana",20,"bold"))
        self.canvas.create_text(self.width/5+160,self.height/4,text="Barriers",
            font=("Verdana",20,"bold"))
        self.canvas.create_text(self.width/5+320,self.height/4,text="Par",
            font=("Verdana",20,"bold"))
        self.canvas.create_text(self.width/5+480,self.height/4,text="+/-",
            font=("Verdana",20,"bold"))
        #Total Barriers Box:
        self.canvas.create_rectangle(self.width/5+640,self.height/4-100,
            self.width/5+800,self.height/4+160-100,fill="white")
        self.canvas.create_rectangle(self.width/5+640,self.height/4-100,
            self.width/5+800,self.height/4+160-100,fill="white")
        self.canvas.create_rectangle(self.width/5+640+10,self.height/4+10-100,
            self.width/5+800-10,self.height/4+160-10-100,fill="purple")
        self.canvas.create_rectangle(self.width/5+640+10,self.height/4+10-100,
            self.width/5+800-10,self.height/4+160-10-100,fill="purple")
        self.canvas.create_text(self.width/5+720,self.height/4+60-100,
            text=str(self.barrierTotal),font=("Verdana",80),fill="white")
        self.canvas.create_text(self.width/5+720,self.height/4+110-100,
            text="Barriers",font=("Verdana",16),fill="white")
        self.canvas.create_text(self.width/5+720,self.height/4+130-100,
            text="Used",font=("Verdana",16),fill="white")
        #Compared to Par Box:
        self.canvas.create_rectangle(self.width/5+640,self.height/4+250-150,
            self.width/5+800,self.height/4+160+250-150,fill="white")
        if self.comparedToPar<0:
            self.canvas.create_rectangle(self.width/5+640+10,self.height/4+10+250-150,
                self.width/5+800-10,self.height/4+160-10+250-150,fill="dark green")
            self.canvas.create_text(self.width/5+720,self.height/4+110+250-150,
                text="Below",font=("Verdana",16),fill="white")
            self.canvas.create_text(self.width/5+720,self.height/4+60+250-150,
                text=str(abs(self.comparedToPar)),font=("Verdana",80),fill="white")
            self.canvas.create_text(self.width/5+720,self.height/4+130+250-150,
                text="Par",font=("Verdana",16),fill="white")
        elif self.comparedToPar>0:
            self.canvas.create_rectangle(self.width/5+640+10,self.height/4+10+250-150,
                self.width/5+800-10,self.height/4+160-10+250-150,fill="red")
            self.canvas.create_text(self.width/5+720,self.height/4+110+250-150,
                text="Above",font=("Verdana",16),fill="white")
            self.canvas.create_text(self.width/5+720,self.height/4+60+250-150,
                text=str(self.comparedToPar),font=("Verdana",80),fill="white")
            self.canvas.create_text(self.width/5+720,self.height/4+130+250-150,
                text="Par",font=("Verdana",16),fill="white")
        else:
            self.canvas.create_rectangle(self.width/5+640+10,self.height/4+10+250-150,
                self.width/5+800-10,self.height/4+160-10+250-150,fill="dark green")
            self.canvas.create_text(self.width/5+720,self.height/4+30+250+12-150,
                text="You",font=("Verdana",35),fill="white")
            self.canvas.create_text(self.width/5+720,self.height/4+70+250+12-150,
                text="Shot",font=("Verdana",35),fill="white")
            self.canvas.create_text(self.width/5+720,self.height/4+110+250+12-150,
                text="Par!",font=("Verdana",35),fill="white")
        #Best Score Box:
        self.canvas.create_rectangle(self.width/5+640,self.height/4+300,
            self.width/5+800,self.height/4+160+300,fill="white")
        self.canvas.create_rectangle(self.width/5+640+10,self.height/4+10+300,
            self.width/5+800-10,self.height/4+160-10+300,fill="gold")
        self.canvas.create_text(self.width/5+720,self.height/4+30+290+12,
            text="Best Score",font=("Verdana",16),fill="black")
        self.canvas.create_text(self.width/5+720,self.height/4+85+290+12,
            text=self.readHighs(),font=("Verdana",80),fill="black")
        self.canvas.create_text(self.width/5+720,self.height/4+85+338+12,
            text="Barriers",font=("Verdana",14),fill="black")
        #Add the Help Button:
        self.theHelpButton.draw(self.canvas)


class Circle(object):
    def __init__(self, x, y, rad, outsideColor, insideColor):
        self.x=x
        self.y=y
        self.rad=rad
        self.outsideColor=outsideColor #black
        self.insideColor=insideColor #dark grey

    def draw(self, canvas):
        canvas.create_oval(self.x-self.rad,
            self.y-self.rad,
            self.x+self.rad,
            self.y+self.rad,
            fill=self.outsideColor)
        canvas.create_oval(self.x-self.rad*0.75,
            self.y-self.rad*0.75,
            self.x+self.rad*0.75,
            self.y+self.rad*0.75,
            fill=self.insideColor)
        canvas.create_oval(self.x-self.rad*0.35,
            self.y-self.rad*0.35,
            self.x+self.rad*0.35,
            self.y+self.rad*0.35,
            fill=self.outsideColor)

    def __repr__(self):
        return "(%d, %d, %d)"%(self.x,self.y,self.rad)

class Ball(object):
    def __init__(self,x,y,rad,color):
        self.ball=True
        self.x=x
        self.y=y
        self.rad=rad
        self.color=color

    def draw(self,canvas):
        canvas.create_oval(self.x-self.rad,
            self.y-self.rad,
            self.x+self.rad,
            self.y+self.rad,
            fill=self.color)

class Barrier(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.x0=self.x-40
        self.x1=self.x+40
        self.y0=self.y-6
        self.y1=self.y+6
        self.barrierColor="orange"

    def draw(self,canvas):
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1,fill=self.barrierColor)

class BarrierAdditionButton(object):
    def __init__(self,x0,y0): 
        #takes in the top right coordinates, adds 50 to each to get bottom 2
        self.fillColor="blue"
        self.barrierBuilderModeCircleColor="green"
        self.notBarrierBuilderModeCircleColor="orange"
        self.x0=x0
        self.y0=y0
        self.x1=self.x0+50
        self.y1=self.y0+50

    def drawBarrierBuilderMode(self,canvas):
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1,
            fill="white")
        canvas.create_rectangle(self.x0+3,self.y0+3,self.x1-3,self.y1-3,
            fill=self.fillColor,activefill="red")
        canvas.create_polygon(self.x0+10,self.y0+30,self.x0+13,self.y0+27,
            self.x0+22,self.y0+35,self.x0+37,self.y0+10,self.x0+40,self.y0+13,
            self.x0+23,self.y0+40,fill=self.barrierBuilderModeCircleColor)
    
    def drawNotBarrierBuilderMode(self,canvas):
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1,
            fill="white")
        canvas.create_rectangle(self.x0+3,self.y0+3,self.x1-3,self.y1-3,
            fill=self.fillColor,activefill="green")
        canvas.create_polygon(self.x0+10,self.y0+23,self.x0+10,self.y0+27,
            self.x0+23,self.y0+27,self.x0+23,self.y0+40,self.x0+27,self.y0+40,
            self.x0+27,self.y0+27,self.x0+40,self.y0+27,self.x0+40,self.y0+23,
            self.x0+27,self.y0+23,self.x0+27,self.y0+10,self.x0+23,self.y0+10,
            self.x0+23,self.y0+23,
            fill=self.notBarrierBuilderModeCircleColor)

class Goal(object):
    def __init__(self,x0,y0,height): #should take in height of goal (how tall goal is)
        self.x0=x0
        self.y0=y0
        self.height=height
        self.x1=self.x0+13
        self.y1=self.y0+self.height
        self.color="gold"

    def draw(self,canvas):
        canvas.create_polygon(self.x0,self.y0,
            self.x1,self.y0,
            self.x1,self.y1,
            self.x0,self.y1,
            self.x0,self.y1-3,
            self.x1-3,self.y1-3,
            self.x1-3,self.y0+3,
            self.x0,self.y0+3,
            fill=self.color)
        canvas.create_rectangle(self.x0,self.y0+3,self.x0+1,self.y1-3)

class GreenDot(object):
    def __init__(self,x0,y0):
        self.x0=x0
        self.y0=y0

    def draw(self,canvas):
        canvas.create_oval(self.x0-5,self.y0-5,self.x0+5,self.y0+5,
            fill="chartreuse")

class HelpButton(object):
    def __init__(self,x,y,rad):
        self.x=x
        self.y=y
        self.rad=rad
        self.x0=self.x-self.rad
        self.y0=self.y-self.rad
        self.x1=self.x+self.rad
        self.y1=self.y+self.rad
        self.fontColor="white"

    def draw(self,canvas):
        canvas.create_oval(self.x0,self.y0,self.x1,self.y1,fill="purple",
            activefill="red")
        canvas.create_text(self.x,self.y,text="Help",
            fill=self.fontColor,font="Verdana")

class PlayButton(object):
    def __init__(self,x,y,rad,tour):
        self.x=x
        self.y=y
        self.rad=rad
        self.tour=tour #True is tour, anything else is random
        self.buttonColor="blue"
        self.fontColor="white"
        self.activeFill="red"

    def draw(self,canvas):
        canvas.create_oval(self.x-self.rad,self.y-self.rad,
            self.x+self.rad,self.y+self.rad,fill=self.buttonColor,
            activefill="red")
        canvas.create_text(self.x,self.y,text="Play",
            font=("Verdana",self.rad-20),fill=self.fontColor)
        if self.tour==True:
            canvas.create_text(self.x,self.y+35,text="Tour",
                font=("Verdana",self.rad-70),fill=self.fontColor)
        else:
            canvas.create_text(self.x,self.y+35,text="Random",
                font=("Verdana",self.rad-70),fill=self.fontColor)

class InstructionsButton(object):
    def __init__(self,x,y,rad):
        self.x=x
        self.y=y
        self.rad=rad
        self.buttonColor="purple"
        self.fontColor="white"
        self.activeFillColor="red"

    def draw(self,canvas):
        canvas.create_oval(self.x-self.rad,self.y-self.rad,
            self.x+self.rad,self.y+self.rad,fill=self.buttonColor,
            activefill=self.activeFillColor)
        canvas.create_text(self.x,self.y,text="Instructions",
            font=("Verdana",10),fill=self.fontColor)

class AcknowledgementsButton(object):
    def __init__(self,x,y,rad):
        self.x=x
        self.y=y
        self.rad=rad
        self.buttonColor="purple"
        self.fontColor="white"
        self.activeFillColor="red"

    def draw(self,canvas):
        canvas.create_oval(self.x-self.rad,self.y-self.rad,
            self.x+self.rad,self.y+self.rad,fill=self.buttonColor,
            activefill=self.activeFillColor)
        canvas.create_text(self.x,self.y,text="Acknowledgements",
            font=("Verdana",10),fill=self.fontColor)

class HelpScreen(object):
    def __init__(self,x0,y0):
        self.x0=x0
        self.y0=y0
        self.x1=self.x0+400
        self.y1=self.y0+225

    def draw(self,canvas):
        canvas.create_rectangle(self.x0,
                        self.y0,self.x1,self.y1,
                        fill="white")
        canvas.create_rectangle(self.x0+10,
                        self.y0+10,self.x1-10,self.y1-10,
                        fill="purple")
        canvas.create_text(self.x0+200,self.y0+45,
                        text="Help",font=("Verdana",55),fill="gold")
        canvas.create_text(self.x0+180,self.y0+135,
                        text=
                        "    Press M for Menu\n\
    Press B to enter or exit Barrier Builder Mode\n\
    Press U for Undo in Barrier Builder Mode\n\
    Press N in Random Mode for New Level\n\
    Click to Exit",
        font="Verdana",fill="gold")

class PopBox(object):
    def __init__(self,x0,y0,text):
        self.x0=x0
        self.y0=y0
        self.text=text
        self.x1=self.x0+400
        self.y1=self.y0+225

    def draw(self,canvas):
        canvas.create_rectangle(self.x0,
                            self.y0,self.x1,self.y1,
                            fill="white")
        canvas.create_rectangle(self.x0+10,
                            self.y0+10,self.x1-10,self.y1-10,
                            fill="blue",activefill="red")
        canvas.create_text((self.x1-self.x0)/2+self.x0,(self.y1-self.y0)/2+self.y0-20,
                            text=self.text,font=("Verdana",480/len(self.text)),fill="gold")
        if self.text=="GOAL":
            canvas.create_text((self.x1-self.x0)/2+self.x0,(self.y1-self.y0)/2+self.y0+55,
                                text="Click or Press N to continue",
                                font="Verdana",fill="gold")
        elif self.text=="OUT OF BOUNDS":
            canvas.create_text((self.x1-self.x0)/2+self.x0,(self.y1-self.y0)/2+self.y0+55,
                                text="Click or Press R to retry",
                                font="Verdana",fill="gold")

class SureSaveBox(object):
    def __init__(self,x0,y0):
        self.x0=x0
        self.y0=y0
        self.x1=self.x0+400
        self.y1=self.y0+220

    def draw(self,canvas):
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1,fill="white")
        canvas.create_rectangle(self.x0+10,self.y0+10,
            self.x1-10,self.y1-10,fill="red",activefill="green")
        canvas.create_text(self.x0+200,self.y0+110,text="ARE YOU SURE YOU WANT TO SAVE?",
            font=("Verdana",16),fill="white")

Bonkers().run()
