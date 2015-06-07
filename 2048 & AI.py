#2048 & AI

from Tkinter import *
import random
import copy

def run():
    #This function is taken from lecture notes created by Prof David Kosbie (CMU)
    # create the root and the canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=405, height=500) #Make height 600 to see the moves that are going on in the AI
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    __init__()
    # set up events
    root.bind("<Key>", lambda event: keyPressed(canvas,event))
    # and launch the app
    root.mainloop()

def __init__():
    canvas.data.base=2
    canvas.data.timerCounter=0
    canvas.data.board=[[0,0,0,0],
                       [0,0,0,0],
                       [0,0,0,0],
                       [0,0,0,0]]
    canvas.data.hypoBoard=copy.deepcopy(canvas.data.board)
    canvas.data.score=0
    canvas.data.gameOverCheck=False
    canvas.data.lastMove="none"
    canvas.data.delay=1 #Higher value -> slower ai moves
    canvas.data.ai = False
    newTile()
    newTile()
    redrawAll()

def redrawAll():
    if (checkUpMove()== False and checkMergeUp()== False and 
    checkLeftMove()== False and checkMergeLeft()== False and 
    checkDownMove()== False and checkMergeDown()== False and 
    checkRightMove()== False and checkMergeRight()== False):
        drawBoard()
        gameOver()
        canvas.data.gameOverCheck=True
    else:
        canvas.delete(ALL)
        drawBoard()
    #printBoardToConsole()

def timerFired():
    canvas.data.timerCounter+=1
    canvas.delete(ALL)
    redrawAll()
    if canvas.data.timerCounter>1:
        ai()
    if canvas.data.gameOverCheck==False:
        canvas.after(canvas.data.delay, timerFired)

def keyPressed(canvas,event):
    if (event.keysym == "Up"):
        goUp()
    if (event.keysym == "Left"):
        goLeft()
    if (event.keysym == "Down"):
        goDown()
    if (event.keysym == "Right"):
        goRight()
    if (event.keysym == "n"):
        __init__()
    if (event.keysym == "a" and canvas.data.ai == False):
        timerFired()
        canvas.data.ai = True
    redrawAll()

def newTile():
    found = False
    for i in xrange(10000):
        if found == False:
            canvas.data.possRow = random.randint(0,3)
            canvas.data.possCol = random.randint(0,3)
            if canvas.data.board[canvas.data.possRow][canvas.data.possCol] == 0:
                twoOrFour=random.randint(1,6)
                if twoOrFour==6:
                    canvas.data.board[canvas.data.possRow][canvas.data.possCol] = canvas.data.base*2
                    #newTileAnimation()
                    found=True
                elif twoOrFour>0 and twoOrFour<6:
                    canvas.data.board[canvas.data.possRow][canvas.data.possCol] = canvas.data.base
                    #newTileAnimation()
                    found=True
                else:
                    canvas.data.gameOverCheck=True

def drawTile(canvas, tileNumber, row, col):
    if tileNumber<=canvas.data.base:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="white")
    elif tileNumber<=canvas.data.base*2:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="dark grey")
    elif tileNumber<=canvas.data.base*2**2:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="magenta")
    elif tileNumber<=canvas.data.base*2**3:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="orange")
    elif tileNumber<=canvas.data.base*2**4:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="pink")
    elif tileNumber<=canvas.data.base*2**5:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="red")
    elif tileNumber<=canvas.data.base*2**6:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="black")
    elif tileNumber<=canvas.data.base*2**7:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="blue")
    elif tileNumber<=canvas.data.base*2**8:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="purple")
    elif tileNumber<=canvas.data.base*2**9:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="maroon")
    elif tileNumber<=canvas.data.base*2**10:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="gold")
    elif tileNumber<=canvas.data.base*2**11:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="cyan")
    elif tileNumber<=canvas.data.base*2**12:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="chartreuse")
    elif tileNumber>canvas.data.base*2**12:
        canvas.create_rectangle(8+col*100,103+row*100,2+col*100+100,197+row*100,fill="white")
    if tileNumber<canvas.data.base*2:
        canvas.create_text(55+col*100,150+row*100,text=canvas.data.tileNumber,font=("Helvetica",60),fill="black")
    elif tileNumber<canvas.data.base*2**6:
        canvas.create_text(55+col*100,150+row*100,text=canvas.data.tileNumber,font=("Helvetica",60),fill="white")
    elif tileNumber<canvas.data.base*2**9:
        canvas.create_text(55+col*100,150+row*100,text=canvas.data.tileNumber,font=("Helvetica",50),fill="white")
    elif tileNumber<canvas.data.base*2**10:
        canvas.create_text(55+col*100,150+row*100,text=canvas.data.tileNumber,font=("Helvetica",40),fill="white")
    elif tileNumber==canvas.data.base*2**10:
        canvas.create_text(55+col*100,150+row*100,text=canvas.data.tileNumber,font=("Helvetica",40),fill="black")
    elif tileNumber<canvas.data.base*2**13:
        canvas.create_text(55+col*100,150+row*100,text=canvas.data.tileNumber,font=("Helvetica",40),fill="white")
    else:
        canvas.create_text(55+col*100,150+row*100,text=canvas.data.tileNumber,font=("Helvetica",33),fill="white")

def drawBoard():
    largestTile=canvas.data.base
    for c in xrange(4):
        for d in xrange(4):
            if canvas.data.board[c][d]>largestTile:
                largestTile=canvas.data.board[c][d]
    if largestTile<canvas.data.base*2**10:
        canvas.create_rectangle(5,5,203,95,fill="orange")
        canvas.create_text(102,53,text=str(canvas.data.base*2**10),font=("Helvetica",64),fill="white")
        canvas.create_text(100,88,text='''(Press "A" to activate AI)''',font=("Helvetiva",10),fill="white")
    else:
        canvas.create_rectangle(5,5,203,95,fill="gold")
        canvas.create_text(102,53,text=canvas.data.base*2**10,font=("Helvetica",64))
        canvas.create_text(100,88,text='''(Press "A" to activate AI)''',font=("Helvetiva",10),fill="black")
    canvas.create_rectangle(206,5,405,95,fill="beige")
    canvas.create_text(305,30,text="Score:",font=("Helvetica",28))
    canvas.create_text(305,68,text=canvas.data.score,font=("Helvetica",50))
    for a in xrange(4):
        for b in xrange(4):
            canvas.create_rectangle(5+a*100,100+b*100,5+a*100+100,b*100+200)
            if canvas.data.board[a][b]!=0:
                canvas.data.tileNumber=canvas.data.board[a][b]
                drawTile(canvas, canvas.data.tileNumber, a, b)

def checkUpMove():
    board=canvas.data.board
    upCheck=False
    for a in xrange(3,-1,-1):
        for b in xrange(3,-1,-1):
            for c in xrange(a-1,-1,-1):
                if board[a][b]!=0 and board[c][b]==0: #check for sliding
                    upCheck=True
                if board[a][b]!=0 and board[a-1][b]==board[a][b]: #check for merges
                    upCheck=True
    return upCheck

def checkDownMove():
    board=canvas.data.board
    downCheck=False
    for a in xrange(4):
        for b in xrange(4):
            for c in xrange(a+1,4):
                if board[a][b]!=0 and board[c][b]==0:
                    downCheck=True
    return downCheck

def checkRightMove():
    board=canvas.data.board
    rightCheck=False
    for a in xrange(3,-1,-1):
        for b in xrange(4):
            for c in xrange(b+1,4):
                if board[a][b]!=0 and board[a][c]==0:
                    rightCheck=True
    return rightCheck

def checkLeftMove():
    board=canvas.data.board
    leftCheck=False
    for a in xrange(4):
        for b in xrange(3,-1,-1):
            for c in xrange(b-1,-1,-1):
                if board[a][b]!=0 and board[a][c]==0:
                    leftCheck=True
    return leftCheck

def moveUp():
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(3,0,-1):
            for b in xrange(3,-1,-1):
                if board[a][b]!=0 and board[a-1][b]==0:
                    board[a-1][b]=board[a][b]
                    board[a][b]=0

def moveDown():
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(3):
            for b in xrange(4):
                if board[a][b]!=0 and board[a+1][b]==0:
                    board[a+1][b]=board[a][b]
                    board[a][b]=0

def moveRight():
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(4):
            for b in xrange(2,-1,-1):
                if board[a][b]!=0 and board[a][b+1]==0:
                    board[a][b+1]=board[a][b]
                    board[a][b]=0

def moveLeft():
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(4):
            for b in xrange(1,4):
                if board[a][b]!=0 and board[a][b-1]==0:
                    board[a][b-1]=board[a][b]
                    board[a][b]=0

def checkMergeUp():
    mergeCheckUp=False
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(1,4):
            for b in xrange(4):
                if board[a][b]!=0 and board[a-1][b]==board[a][b]:
                    mergeCheckUp=True
    return mergeCheckUp

def checkMergeDown():
    mergeCheckDown=False
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(3,0,-1):
            for b in xrange(4):
                if board[a][b]!=0 and board[a-1][b]==board[a][b]:
                    mergeCheckDown=True
    return mergeCheckDown

def checkMergeRight():
    mergeCheckRight=False
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(3,-1,-1):
            for b in xrange(3):
                if board[a][b]!=0 and board[a][b+1]==board[a][b]:
                    mergeCheckRight=True
    return mergeCheckRight

def checkMergeLeft():
    mergeCheckLeft=False
    board=canvas.data.board
    for loop in xrange(3):
        for a in xrange(4):
            for b in xrange(1,4):
                if board[a][b]!=0 and board[a][b-1]==board[a][b]:
                    mergeCheckLeft=True
    return mergeCheckLeft

def mergeUp():
    board=canvas.data.board
    for a in xrange(1,4):
        for b in xrange(4):
            if board[a][b]!=0 and board[a-1][b]==board[a][b]:
                board[a-1][b]=board[a][b]*2
                board[a][b]=0
                canvas.data.score+=board[a-1][b]

def mergeDown():
    board=canvas.data.board
    for a in xrange(2,-1,-1):
        for b in xrange(4):
            if board[a][b]!=0 and board[a+1][b]==board[a][b]:
                board[a+1][b]=board[a][b]*2
                board[a][b]=0
                canvas.data.score+=board[a+1][b]

def mergeRight():
    board=canvas.data.board
    for a in xrange(4):
        for b in xrange(2,-1,-1):
            if board[a][b]!=0 and board[a][b+1]==board[a][b]:
                board[a][b+1]=board[a][b]*2
                board[a][b]=0
                canvas.data.score+=board[a][b+1]

def mergeLeft():
    board=canvas.data.board
    for a in xrange(4):
        for b in xrange(1,4):
            if board[a][b]!=0 and board[a][b-1]==board[a][b]:
                board[a][b-1]=board[a][b]*2
                board[a][b]=0
                canvas.data.score+=board[a][b-1]

def goUp():
    if checkUpMove()== True or checkMergeUp()== True:
        canvas.data.lastMove="up"
        moveUp()
        mergeUp()
        moveUp() #you still need it to move up just in case its possible after a merge
        newTile()
        #print "UP"

def goLeft():
    if checkLeftMove()== True or checkMergeLeft()== True:
        canvas.data.lastMove="left"
        moveLeft()
        mergeLeft()
        moveLeft()
        newTile()
        #print "LEFT"
        
def goDown():
    if checkDownMove()== True or checkMergeDown()== True:
        canvas.data.lastMove="down"
        moveDown()
        mergeDown()
        moveDown()
        newTile()
        #print "DOWN"

def goRight():
    if checkRightMove()== True or checkMergeRight()== True:
        canvas.data.lastMove="right"
        moveRight()
        mergeRight()
        moveRight()
        newTile()
        #print "RIGHT"

def printBoardToConsole():
    print canvas.data.board[0]
    print canvas.data.board[1]
    print canvas.data.board[2]
    print canvas.data.board[3]
    print

def gameOver():
    canvas.create_rectangle(1,260,420,317,fill="red")
    canvas.create_text(205,290,text="GAME OVER", font=("Helvetica",65),fill="yellow")

#functions for AI from here down
def rightColumnFullCheck():
    if (canvas.data.board[0][3]!=0 and 
        canvas.data.board[1][3]!=0 and 
        canvas.data.board[2][3]!=0 and 
        canvas.data.board[3][3]!=0 and 
        canvas.data.board[3][3]!=canvas.data.board[2][3] and 
        canvas.data.board[1][3]!=canvas.data.board[2][3] and 
        canvas.data.board[1][3]!=canvas.data.board[0][3]):
        return True

def greatestTile():
    bigBoy=0 #greatestTile
    for a in xrange(3):
        for b in xrange(3):
            if canvas.data.board[a][b]>bigBoy:
                bigBoy=canvas.data.board[a][b]
    return bigBoy

def topRightCorrection(): #if [1][2] equals topRight and [1][3] is 0 go right then up
    board=canvas.data.board
    if (board[1][2]!=0 and 
        board[1][2]==board[0][3] and 
        board[1][3]==0 and 
        board[1][1]!=board[1][2]):
        return True

def topRowMergeCheck(): #are there tiles in the top row that can merge
    board=canvas.data.board
    if ((board[0][0]==board[0][1] and board[0][0]!=0) or 
        (board[0][1]==board[0][2] and board[0][2]!=0) or 
        (board[0][2]==board[0][3] and board[0][2]!=0) or
        (board[0][0]==board[0][3] and board[0][0]!=0 and board[0][1]==0 and board[0][2]==0) or
        (board[0][0]==board[0][2] and board[0][0]!=0 and board[0][1]==0) or
        (board[0][1]==board[0][3] and board[0][1]!=0 and board[0][2]==0)):
        return True

def freezeCheck(rowNum): #rowNum checks for full unmergeable rows at the index and above
    counter=0
    board=canvas.data.board
    for a in xrange(rowNum+1):
        if (board[a][0]!=0 and 
            board[a][1]!=0 and 
            board[a][2]!=0 and 
            board[a][3]!=0 and #no zeros
            board[a][0]!=board[a][1] and 
            board[a][1]!=board[a][2] and 
            board[a][2]!=board[a][3]): #no merge possibilities
            counter+=1
    if counter-1==rowNum:
        return True

def hypoMoveLeft():
    board=canvas.data.hypoBoard
    for loop in xrange(3):
        for a in xrange(4):
            for b in xrange(1,4):
                if board[a][b]!=0 and board[a][b-1]==0:
                    board[a][b-1]=board[a][b]
                    board[a][b]=0

def hypoMoveRight():
    board=canvas.data.hypoBoard
    for loop in xrange(3):
        for a in xrange(4):
            for b in xrange(2,-1,-1):
                if board[a][b]!=0 and board[a][b+1]==0:
                    board[a][b+1]=board[a][b]
                    board[a][b]=0

def hypoMoveDown():
    board=canvas.data.hypoBoard
    for loop in xrange(3):
        for a in xrange(3):
            for b in xrange(4):
                if board[a][b]!=0 and board[a+1][b]==0:
                    board[a+1][b]=board[a][b]
                    board[a][b]=0

def hypoMergeLeft():
    board=canvas.data.hypoBoard
    for a in xrange(4):
        for b in xrange(1,4):
            if board[a][b]!=0 and board[a][b-1]==board[a][b]:
                board[a][b-1]=board[a][b]*2
                board[a][b]=0

def hypoMergeRight():
    board=canvas.data.hypoBoard
    for a in xrange(4):
        for b in xrange(2,-1,-1):
            if board[a][b]!=0 and board[a][b+1]==board[a][b]:
                board[a][b+1]=board[a][b]*2
                board[a][b]=0

def hypoMergeDown():
    board=canvas.data.hypoBoard
    for a in xrange(2,-1,-1):
        for b in xrange(4):
            if board[a][b]!=0 and board[a+1][b]==board[a][b]:
                board[a+1][b]=board[a][b]*2
                board[a][b]=0
                
def hypoLeft():
    hypoMoveLeft()
    hypoMergeLeft()
    hypoMoveLeft()

def hypoRight():
    hypoMoveRight()
    hypoMergeRight()
    hypoMoveRight()

def hypoDown():
    hypoMoveDown()
    hypoMergeDown()
    hypoMoveDown()

def leftAndUp():
    freezedRow=(-1)
    for a in xrange(3):
        if freezeCheck(a)==True:
            freezedRow+=1
    if freezedRow>=0:
        canvas.data.hypoBoard=copy.deepcopy(canvas.data.board)
        hypoLeft()
        for b in xrange(4):
            if canvas.data.hypoBoard[freezedRow][b]==canvas.data.hypoBoard[freezedRow+1][b]:
                if canvas.data.board[freezedRow][b]!=canvas.data.board[freezedRow+1][b]:
                    return True

def rightAndUp():
    freezedRow=(-1)
    for a in xrange(3):
        if freezeCheck(a)==True:
            freezedRow+=1
    if freezedRow>=0:
        canvas.data.hypoBoard=copy.deepcopy(canvas.data.board)
        hypoRight()
        for b in xrange(4):
            if canvas.data.hypoBoard[freezedRow][b]==canvas.data.hypoBoard[freezedRow+1][b]:
                if canvas.data.board[freezedRow][b]!=canvas.data.board[freezedRow+1][b]:
                    return True

def upMergeToFrozen():
    freezedRow=(-1)
    for a in xrange(4):
        if freezeCheck(a)==True:
            freezedRow+=1
        else:
            break
    if freezedRow==2:
        for b in xrange(4):
            if (canvas.data.board[freezedRow][b]==canvas.data.board[freezedRow+1][b]):
                return True
    elif freezedRow==1:
        for b in xrange(4):
            if (canvas.data.board[freezedRow][b]==canvas.data.board[freezedRow+1][b] or
                canvas.data.board[freezedRow][b]==canvas.data.board[freezedRow+2][b] and 
                canvas.data.board[freezedRow+1][b]==0):
                return True
    elif freezedRow==0:
        for b in xrange(4):
            if (canvas.data.board[freezedRow][b]==canvas.data.board[freezedRow+1][b] or
                canvas.data.board[freezedRow][b]==canvas.data.board[freezedRow+2][b] and 
                canvas.data.board[freezedRow+1][b]==0 or
                canvas.data.board[freezedRow][b]==canvas.data.board[freezedRow+3][b] and 
                canvas.data.board[freezedRow+1][b]==0  and canvas.data.board[freezedRow+2][b]==0):
                return True

def upMergeToTopFrozen():
    for a in xrange(4):
        if canvas.data.board[0][a]==canvas.data.board[1][a] and canvas.data.board[0][a]!=0:
            return True #just incase upmergetofrozen doesnt work

def mergeRightBeforeUp(): #jamisons first scenario where 00 10 and 11 are the same or same thing over 1
    board=canvas.data.board
    if (board[0][0]!=0 and 
        board[0][0]==board[1][0] and 
        board[0][0]==board[1][1] and 
        board[0][1]==board[0][0]*2):
        return True
    elif (board[0][1]!=0 and 
        board[0][1]==board[1][1] and 
        board[0][1]==board[1][2] and 
        board[0][2]==board[1][1]*2):
        return True

def slideRightBeforeUpMerge(): #jamisons second scenario where you should make sure theres a clear column before a 00 and 10 merge
    board=canvas.data.board
    if (board[0][0]==board[1][0] and 
        board[0][0]>=0 and 
        freezeCheck(0)==True and
        board[2][0]!=0 and
        board[3][0]!=0):
        return True

def topRightMerge(): #you always want to make the 03 higher
    board=canvas.data.board
    if ((board[0][3]==board[1][3] or
        (board[0][3]==board[2][3]  and board[1][3]==0) or
        (board[0][3]==board[3][3] and board[1][3]==0 and board[2][3]==0)) and
        board[0][3]!=0):
        return True

def goUpNotTopMerge():
    board=canvas.data.board
    if board[0][0]==board[0][1] and board[1][1]==board[0][0] and board[0][0]!=0:
        return True
    elif board[0][1]==board[0][2] and board[0][2]==board[1][1] and board[0][1]!=0:
        return True
    elif board[0][2]==board[0][3] and board[0][3]==board[1][2] and board[0][2]!=0:
        return True

def needaShimmy():
    board=canvas.data.board
    if board[0][3]<board[0][2]/32 and board[0][3]!=0:
        return True

def shimmyDown():
    board=canvas.data.board
    if needaShimmy()==True:
        canvas.data.hypoBoard=copy.deepcopy(canvas.data.board)
        hypoDown()
        hypoRight()
        if canvas.data.hypoBoard[0][3]==canvas.data.board[0][2]:
            return True

def topRowGradient(): #gradient and frozen
    board=canvas.data.board
    if board[0][3]>board[0][2] and board[0][2]>board[0][1] and board[0][1]>board[0][0]:
        if board[0][0]!=0 and board[0][1]!=0 and board[0][2]!=0 and board[0][3]!=0:
            return True

def secondRowGradient():
    board=canvas.data.board
    if board[1][3]<board[1][2] and board[1][2]<board[1][1] and board[1][1]<board[1][0]:
        if board[1][0]!=0 and board[1][1]!=0 and board[1][2]!=0 and board[1][3]!=0:
            return True

def oneZeroWrong():
    if topRowGradient()==True:
        if canvas.data.board[1][0]<canvas.data.board[1][1] and canvas.data.board[1][0]!=0:
            return True

def ai():
    #last move cases
    if canvas.data.lastMove=="shimmyDown" and canvas.data.board[0][3]==0:
        goRight()
        #print "completed the shimmy"
    elif canvas.data.lastMove=="shimmyDown" and canvas.data.board[0][3]!=0 and canvas.data.board[0][3]==canvas.data.board[1][3]:
        goDown()
        #completed the shimmy
    elif canvas.data.lastMove=="shimmyDown" and canvas.data.board[0][3]!=0 and canvas.data.board[0][3]!=canvas.data.board[1][3]:
        goUp()
        #completed the shimmy
    elif canvas.data.lastMove=="downNeedUp" and canvas.data.board[0][3]!=0:
        goLeft()
        canvas.data.lastMove="leftAfterDown"
        #print "left after down"
    elif canvas.data.lastMove=="leftAfterDown" and canvas.data.board[0][3]!=0:
        goLeft()
        canvas.data.lastMove="leftAfterDown"
        #print "still left after down"
    elif canvas.data.lastMove=="leftAfterDown" and canvas.data.board[0][3]==0:
        goUp()
        #print "up after left after down"
    elif canvas.data.lastMove=="downNeedUp" and (checkMergeUp()==True or checkUpMove()==True):
        goUp()
        #print "down needed up"
    elif canvas.data.lastMove=="leftNeedUp" and (checkMergeUp()==True or checkUpMove()==True):
        goUp()
        #print "left needed up"
    elif canvas.data.lastMove=="rightNeedUp" and (checkUpMove()==True or checkMergeUp()==True):
        goUp()
        #print "right needed up"
    #shimmy cases
    elif shimmyDown()==True:
        goDown()
        canvas.data.lastMove="shimmyDown"
        #print "shimmied down"
    elif needaShimmy()==True and (checkLeftMove()==True or checkMergeLeft()==True):
        goLeft()
        #canvas.data.lastMove="shimmy"
        ##print "shimmied left"
    elif needaShimmy()==True and (checkRightMove()==True or checkMergeRight()==True):
        goRight()
        #canvas.data.lastMove="shimmy"
        ##print "shimmied right"
    #last lastmove case (shimmy should override this)
    elif canvas.data.lastMove=="leftNeedRight" and (checkRightMove()==True or checkMergeRight()==True):
        goRight()
        #print "left needed right"
    elif topRightMerge()==True:
        goUp()
        #print "top right merge"
    elif mergeRightBeforeUp()==True and (checkRightMove()==True or checkMergeRight()==True):
        goRight()
        #print "go right for a merge instead of up"
    elif goUpNotTopMerge()==True:
        goUp()
        #print "go up before merging the top"
    elif slideRightBeforeUpMerge()==True and (checkRightMove()==True or checkMergeRight()==True):
        goRight()
        #print "go right instead of up because you dont want a bad filler"
    elif topRightCorrection()==True:
        goRight()
        canvas.data.lastMove="rightNeedUp"
        #print "top right correction"
    elif upMergeToFrozen()==True or upMergeToTopFrozen()==True:
        goUp()
        #print "up merge to a frozen row"
    elif topRowMergeCheck()==True:
        goRight()
        #print "merge the top row"
    #second row frozen cases
    elif checkMergeRight()==True and secondRowGradient()==True:
        goRight()
        #print "right because top 2 rows are frozen and secrow gradient"
    elif secondRowGradient()==True and checkRightMove()==True:
        goRight()
    elif leftAndUp()==True and freezeCheck(1)==True:
        goLeft()
        canvas.data.lastMove="leftNeedUp"
        #print "beginning of left and up"
    #elif checkMergeUp()==True or checkUpMove()==True: #new
     #   goUp()
        #print we like ups
    elif rightAndUp()==True and freezeCheck(1)==True:
        goRight()
        #print "hypo'd right to go up"
    elif checkMergeLeft()==True and freezeCheck(1)==True:
        goLeft()
        #print "left cuz second row is frozen"
    #general cases
    elif rightAndUp()==True and freezeCheck(0)==True and oneZeroWrong()==None:
        goRight()
        #print "hypo'd right to go up"
    elif leftAndUp()==True and freezeCheck(0)==True:
        goLeft()
        canvas.data.lastMove="leftNeedUp"
        #print "beginning of left and up"
    elif rightAndUp()==True and freezeCheck(0)==True:
        goRight()
        #print "hypo'd right to go up"
    elif oneZeroWrong()==True and canvas.data.board[1][0]==canvas.data.board[2][0]:
        goUp()
        #print "one zero correction"
    elif checkMergeLeft()==True and topRowGradient()==True:
        goLeft()
        #print "left merge"
    elif checkLeftMove()==True and topRowGradient()==True:
        goLeft()
    elif checkMergeUp()==True:
        goUp()
        #print "up merge"
    elif checkMergeRight()==True:
        goRight()
        #print "right merge"
    elif checkUpMove()==True:
        goUp()
        #print "up move"
    elif checkRightMove()==True:
        goRight()
        ##print "right move"
    elif freezeCheck(0)==True and (checkLeftMove()==True or checkMergeLeft()==True):
        goLeft()
        ##print "left move because needed and frozen top row"
    elif checkLeftMove()==True:
        goLeft()
        canvas.data.lastMove="leftNeedRight"
        ##print "left because abandoned"
    elif rightColumnFullCheck()==True and checkDownMove()==True:
        goDown()
        canvas.data.lastMove="downNeedUp"
        ##print "down move because right is filled"
    else:
        goDown()
        canvas.data.lastMove="downNeedUp"
        ##print "shit gotta go down"
    if canvas.data.lastMove[0]=="r":
        canvas.create_text(200,550,text="RIGHT",fill="red",font=("Helvetica",64))
    if canvas.data.lastMove[0]=="l":
        canvas.create_text(200,550,text="LEFT",fill="red",font=("Helvetica",64))
    if canvas.data.lastMove[0]=="d":
        canvas.create_text(200,550,text="DOWN",fill="red",font=("Helvetica",64))
    if canvas.data.lastMove[0]=="u":
        canvas.create_text(200,550,text="UP",fill="red",font=("Helvetica",64))

def aiLoop():
    while canvas.data.gameOverCheck==False:
        ai()

run()