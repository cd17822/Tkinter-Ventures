import Tkinter as TK
import random

class Animation(object):
    #This class is taken from lecture notes created by Prof David Kosbie (CMU)
    def mousePressed(self, event): pass
    def keyPressed(self, event): pass
    def mouseHeld(self,event):pass
    def mouseReleased(self,event):pass
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
        self.timerFiredDelay = 10 #in ms
        def timerFiredWrapper(): 
            self.timerFired() 
            redrawAllWrapper() 
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper) 
        self.init() 
        timerFiredWrapper() 
        root.mainloop()

class Palindromica(Animation):
    def init(self):
        self.clicks=0
        self.inMenu=True
        self.timerCounter=0
        self.pausedTimerCounter=0
        self.objArr=[]
        self.lines=[Line(-100,self.height)] #this way there's always a line to be drawn (just off screen)
        self.speedConstant=5
        self.generateConstant=int((1.0/self.speedConstant)*100)
        self.separation=self.speedConstant*self.generateConstant
        self.paused=False
        self.palindromeLength=1
        self.goldenIndex=0
        self.click="digit"
        self.score=Score(1)
        self.time=Time()
        self.pauseLimit=40
        self.backgroundColor="light blue"
        self.inHelp=False
        self.inGameOver=False
        self.hit=False
        self.inCharlie=False

    def timerFired(self):
        if self.paused==False and self.timerCounter<3000 and self.inMenu==False:
            self.timerCounter+=1
            self.generateOrNah()
            self.popCheck()
        else:
            self.pausedTimerCounter+=1

    def redrawAll(self):
        self.drawBackground()
        if self.inHelp:
            self.drawHowToPlay()
        elif self.inMenu:
            self.drawMenu()
        elif self.inCharlie:
            self.drawCharlie()
        else:
            self.time.draw(self.canvas, self.width,self.height,self.timerCounter)
            if self.timerCounter<3000:
                if self.paused==False:
                    self.drawDigit()
                    self.drawLines()
                    self.score.draw(self.canvas,self.width,self.height)
                else:
                    self.drawPauseScreen()
                    self.drawDigitPaused()
                    self.drawLinesPaused()
                    if self.palindromeLength>0:
                        self.score.drawPaused(self.canvas,self.width,self.height,self.palindromeLength)
                    else:
                        self.score.drawPausedWrong(self.canvas,self.width,self.height,self.palindromeLength)
            else:
                self.drawDigit()
                self.score.draw(self.canvas,self.width,self.height)
                self.inGameOver=True
                self.drawGameOverScreen()

    def mousePressed(self,event):
        if self.clicks>0: #because getting to the screen is pretty chill
            if self.inHelp==True:
                self.init()
            elif self.inCharlie==True:
                self.init()
            elif self.inMenu==True:
                if event.y>self.height/6*5 and event.x>self.width/5*4:
                    self.inMenu=False
                    self.inCharlie=True
                elif event.y>self.height/3:
                    self.inMenu=False
                elif event.y>self.height/10:
                    self.inMenu=False
                    self.inHelp=True
            elif self.paused==False and self.clicks>1:
                self.makeLine(event)
                self.lineDrop(event)
                self.hit=True
            if self.inGameOver==True:
                self.init()
        self.clicks+=1

    def mouseHeld(self,event):
        if self.paused==False and self.clicks>1 and not self.inMenu:
            self.makeLine(event)

    def mouseReleased(self,event):
        if self.paused==False and self.clicks>1  and not self.inMenu and self.hit==False:
            self.lineDrop(event)

    def keyPressed(self,event):
        if event.keysym=="r":
            self.init()
            self.clicks=1

    def drawMenu(self):
        activefill="dark green"
        self.canvas.create_text(self.width-110,self.height-14,text="Charlie DiGiovanna",fill="dark grey",
                                activefill=activefill,font=("Helvetica",24))
        self.canvas.create_text(self.width/2,self.height/5,text="what's this?",
                                font=("Helvetica",64),fill="grey",activefill=activefill)
        self.canvas.create_text(self.width/2,self.height/2,text="palindromica",
                                font=("Helvetica",155),fill="dark grey",activefill=activefill)
        self.canvas.create_text(self.width/2,self.height/5*4,text="click to play.",
                                font=("Helvetica",64),fill="grey",activefill=activefill)

    def drawHowToPlay(self):
        self.canvas.create_text(self.width/2,self.height/2,
                        text="Click to create mirrors exposing the\nsymmetry of panlindromic numbers.",
                        fill="dark grey", font=("Helvetica",64))
        self.canvas.create_text(self.width/2,self.height/6,text="631717822",font=("Helvetica",64))
        self.canvas.create_rectangle(self.width/2-1,self.height/6-70,self.width/2+1,self.height/6+70,
            fill="green")
        self.canvas.create_rectangle(self.width/2-55,self.height/6-50,self.width/2+55,self.height/6+50,
            outline="red")

        self.canvas.create_rectangle(self.width/2-1+124,self.height/6-70,self.width/2+1+124,self.height/6+70,
            fill="green")
        self.canvas.create_rectangle(self.width/2-35+124,self.height/6-50,self.width/2+35+124,self.height/6+50,
            outline="red")

    def drawPauseScreen(self):
        self.canvas.create_rectangle(-5,-5,self.width+5,self.height+5,fill="black")
        if self.pausedTimerCounter>self.pauseLimit:
            self.unpause()

    def drawBackground(self):
        self.canvas.create_rectangle(-5,-5,self.width+5,self.height+5,fill=self.backgroundColor)

    def drawCharlie(self):
        self.canvas.create_text(self.width/2,self.height/5,text="Charlie DiGiovanna",font=("Helvetica",96),
            fill="dark grey")
        self.canvas.create_text(self.width/2,self.height/2-20,text="Binghamton University",font=("Helvetica",72),
            fill="dark grey")
        self.canvas.create_text(self.width/2,self.height/5*3,text="Computer Science/Math",font=("Helvetica",48),
            fill="dark grey")
        self.canvas.create_text(self.width/2,self.height/5*4,text="www.github.com/cd17822",font=("Helvetica",72),
            fill="dark grey")

    def unpause(self):
        self.hit=False
        self.pausedTimerCounter=0
        self.lines[0]=Line(-100,self.height)
        self.removePalindromicValues()
        if self.palindromeLength>0:
            self.score.value+=self.palindromeLength
        else:
            self.score.value-=1
        self.paused=False

    def lineDrop(self,event):
        frozenLineX=event.x
        self.palindromeLength=self.palindromeCheck(event)
        self.lines[0]=Line(frozenLineX,self.height)
        self.paused=True

    def palindromeCheck(self,event):
        trueness=1
        self.paused=True
        for i in xrange(len(self.objArr)):
            if abs(event.x-self.objArr[i].position)<self.separation/5: #on digit
                self.goldenIndex=i
                self.click="digit"
                if len(self.objArr)-i<len(self.objArr)/2:
                    determinant=i
                else:
                    determinant=len(self.objArr)-i
                for j in xrange(1,determinant):
                    if self.objArr[i+j].value==self.objArr[i-j].value:
                        trueness+=2
                    else:
                        if trueness>1:
                            return trueness
                        else:
                            return 0
            elif (self.objArr[i].position-event.x<self.separation/2
                                        and self.objArr[i].position-event.x>0): #to the left of digit
                self.goldenIndex=i-1
                self.click="space"
                trueness=0
                if len(self.objArr)-i<len(self.objArr)/2:
                    determinant=i
                else:
                    determinant=len(self.objArr)-i
                for j in xrange(1,determinant):
                    if self.objArr[i-j].value==self.objArr[i+j-1].value:
                        trueness+=2
                    else:
                        return trueness
            elif (event.x-self.objArr[i].position<self.separation/2 
                                        and event.x-self.objArr[i].position>0): #to the right of digit
                self.goldenIndex=i
                self.click="space"
                trueness=0
                if len(self.objArr)-i<len(self.objArr)/2:
                    determinant=i
                else:
                    determinant=len(self.objArr)-i
                for j in xrange(1,determinant):
                    if self.objArr[i-j+1].value==self.objArr[i+j].value:
                        trueness+=2
                    else:
                        return trueness
        return 0

        '''
        #A different approach to palindromeCheck():
            trueness=1
            self.paused=True
            for i in xrange(len(self.objArr)):
                if abs(event.x-self.objArr[i].position)<self.separation/5: #on digit
                    self.click="digit"
                    self.goldenIndex=i
                    i=self.goldenIndex
                    j=self.goldenIndex
                    i-=1
                    j+=1
                    print "Digit:" + str(self.objArr[i].value) + "," +str(self.objArr[j].value)
                    while i>=0 and j<=len(self.objArr):
                        if self.objArr[i].value==self.objArr[j].value:
                            trueness+=2
                            i-=1
                            j+=1
                        elif trueness>1:
                            return trueness
                        else:
                            return 0
                elif (self.objArr[i].position-event.x<self.separation/2
                                                and self.objArr[i].position-event.x>0): #to the left of digit
                    self.click="space"
                    self.goldenIndex=i-1
                    i=self.goldenIndex
                    j=self.goldenIndex
                    j+=1
                    print "Left:" + str(self.objArr[i].value) + "," +str(self.objArr[j].value)
                    trueness=0
                    while i>=0 and j<=len(self.objArr):
                        if self.objArr[i].value==self.objArr[j].value:
                            trueness+=2
                            i-=1
                            j+=1
                        else:
                            return trueness
                elif (event.x-self.objArr[i].position<self.separation/2 
                                                and event.x-self.objArr[i].position>0): #to the right of digit 
                    self.click="space"
                    self.goldenIndex=i
                    i=self.goldenIndex
                    j=self.goldenIndex
                    j+=1
                    print "Right:" + str(self.objArr[i].value) + "," +str(self.objArr[j].value)
                    trueness=0
                    while i>=0 and j<=len(self.objArr):
                        if self.objArr[i].value==self.objArr[j].value:
                            trueness+=2
                            i-=1
                            j+=1
                        else:
                            return trueness
            return 0
        '''

    def makeLine(self,event):
        self.lines[0]=Line(event.x,self.height)
        
    def drawLines(self):
        for line in self.lines:
            line.draw(self.canvas)

    def drawLinesPaused(self):
        for line in self.lines:
            line.drawPaused(self.canvas)

    def popCheck(self):
        if self.objArr[0].position<(-self.separation/4):
            self.objArr.pop(0)

    def generateOrNah(self):
        if self.timerCounter%self.generateConstant==1:
            self.generateDigit()

    def generateDigit(self):
        value=random.randint(0,9)
        self.objArr.append(Digit(value,self.timerCounter,self.width,self.height,self.backgroundColor))

    def drawDigit(self):
        if len(self.objArr)!=0:
            for digit in self.objArr:
                digit.draw(self.canvas,self.timerCounter,self.speedConstant)

    def drawDigitPaused(self):
        if self.pauseLimit-self.pausedTimerCounter>0:
            if self.palindromeLength==0:
                self.canvas.create_text(self.width/2,self.height/7*6,
                    text="das da wrong numba",font=("Helvetica",self.width/10),fill="dark grey")
                self.objArr[self.goldenIndex].drawPaused(self.canvas,self.timerCounter,self.speedConstant)
                if self.click=="space":
                    self.objArr[self.goldenIndex+1].drawPaused(
                                            self.canvas,self.timerCounter,self.speedConstant)
            elif self.palindromeLength%2==1:
                for i in xrange(self.palindromeLength):
                    try:
                        self.objArr[self.goldenIndex-((self.palindromeLength-1)/2)+i].drawPaused(
                                            self.canvas,self.timerCounter,self.speedConstant)
                    except:pass
            else:
                try:
                    for j in xrange(self.palindromeLength):
                        self.objArr[self.goldenIndex-((self.palindromeLength-2)/2)+j].drawPaused(
                                            self.canvas,self.timerCounter,self.speedConstant)
                except:pass

    def removePalindromicValues(self):
        if self.palindromeLength==0:
            pass
        elif self.palindromeLength%2==1:
            for i in xrange(self.palindromeLength):
                self.objArr.pop(self.goldenIndex-((self.palindromeLength-1)/2))
        else:
            for j in xrange(self.palindromeLength):
                self.objArr.pop(self.goldenIndex-((self.palindromeLength-2)/2))

    def drawGameOverScreen(self):
        self.canvas.create_text(self.width/2,self.height/7,
            text="game over.",font=("Helvetica",self.width/10),fill="dark grey")
        self.canvas.create_text(self.width/2,self.height/7*6,
            text="score: "+str(self.score.value),font=("Helvetica",self.width/10),fill="dark grey")


class Digit(Palindromica):
    def __init__(self,value,initTime,width,height,backgroundColor):
        self.value=value
        self.initTime=initTime
        self.width=width
        self.height=height
        self.position=0
        self.font=128
        self.backgroundColor=backgroundColor

    def draw(self,canvas,currentTime,speedConstant):
        self.position=self.width+60-speedConstant*(currentTime-self.initTime)
        canvas.create_text(self.position,self.height/2,text=str(self.value),font=("Helvetica",self.font))

    def drawPaused(self,canvas,currentTime,speedConstant):
        self.position=self.width+60-speedConstant*(currentTime-self.initTime)
        canvas.create_text(self.position,self.height/2,text=str(self.value),font=("Helvetica",self.font),
            fill=self.backgroundColor)

class Line(Palindromica):
    def __init__(self,x,height):
        self.x=x
        self.height=height
        self.regFill="green"
        self.pauseFill="green"

    def draw(self,canvas):
        canvas.create_rectangle(self.x-1,-5,self.x+1,self.height+5,fill=self.regFill)

    def drawPaused(self,canvas):
        canvas.create_rectangle(self.x-1,-5,self.x+1,self.height+5,fill=self.pauseFill)

class Score(Palindromica):
    def __init__(self,value):
        self.value=value
        self.fill="dark grey"

    def draw(self,canvas,width,height):

        canvas.create_text(30+width/15,height/15,
            text=("Score: "+str(self.value)),fill=self.fill,font=("Helvetica",32))

    def drawPaused(self,canvas,width,height,palindromeLength):
        canvas.create_text(30+width/15,height/15,
            text=("Score: "+str(self.value)),fill=self.fill,font=("Helvetica",32))
        if self.value<10:
            canvas.create_text(30+width/7,height/15,
                text=(" + "+str(palindromeLength)),fill=self.fill,font=("Helvetica",32))
        else:
            canvas.create_text(30+width/6.7,height/15,
                text=(" + "+str(palindromeLength)),fill=self.fill,font=("Helvetica",32))

    def drawPausedWrong(self,canvas,width,height,palindromeLength):
        canvas.create_text(30+width/15,height/15,
            text=("Score: "+str(self.value)),fill=self.fill,font=("Helvetica",32))
        if self.value<10:
            canvas.create_text(30+width/7,height/15,
                text=(" - 1"),fill=self.fill,font=("Helvetica",32))

class Time(Palindromica):
    def __init__(self):
        self.gameTotalTime=3000
        self.fill="dark grey"

    def draw(self,canvas,width,height,timerCounter):
        if (self.gameTotalTime-timerCounter)/100>=10:
            canvas.create_text(width/7*6,height/15,
                text="Time: "+str((self.gameTotalTime-timerCounter)/100),fill=self.fill,font=("Helvetica",32))
            canvas.create_text(width/6.46*6,height/15,
                text="."+str((self.gameTotalTime-timerCounter)%100),fill=self.fill,font=("Helvetica",32))
        elif (self.gameTotalTime-timerCounter)/100.0>0:
            canvas.create_text(width/7*6,height/15,
                text="Time: "+str((self.gameTotalTime-timerCounter)/100),fill=self.fill,font=("Helvetica",32))
            canvas.create_text(width/6.46*5.95,height/15,
                text="."+str((self.gameTotalTime-timerCounter)%100),fill=self.fill,font=("Helvetica",32))
        else:
            canvas.create_text(width/7*6,height/15,
                text="Time: "+str((self.gameTotalTime-timerCounter)/100),fill=self.fill,font=("Helvetica",32))
            canvas.create_text(width/6.46*5.9,height/15,
                text="."+str((self.gameTotalTime-timerCounter)%100),fill=self.fill,font=("Helvetica",32))

Palindromica().run()
