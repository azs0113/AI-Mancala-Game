

import pygame, sys, random, time, hashlib, copy
from pygame.locals import *

# Create the constants (go ahead and experiment with different values)
numSquares = 4  # number of squares for each player
BOARDHEIGHT = 2 # fixed number of rows for 2 plyers
#TILESIZE = 70
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

FPS = 30

numPebbles = 4
searchDepth = 4

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
LIGHT_GREEN =   (  0, 255,   0)
LIGHT_RED   =   (255,   0,   0)
ORANGE      =   (255, 130,   4)
LIGHT_ORANGE=   (255, 167,  79)


BGCOLOR = DARKTURQUOISE
TILECOLOR = ORANGE
SELECTEDCOLOR =LIGHT_ORANGE
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE
img = pygame.image.load('au1.jpg')
imgx = 0
imgy = 0
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.init()
FPSCLOCK = pygame.time.Clock()


H1 = 'H1'
H2 = 'H2'
ANDOR = 'And-Or'
MINMAX = 'MinMax'
LUCKY = 'Lucky'
AICHALLENGE = 'AIvsAI'
AICHALLENGES = 'S:AIvsAI'
AI1 = ANDOR
AI2 = MINMAX
AI1H = H1
AI2H = H2
H = H1
gameMode = 'PlayerVsAI '

DELAY= 50

tiredMove = False

action = [0,0] # X,Y where X is the square place, and Y is the player row

def main():

    global FPSCLOCK, DISPLAYSURF, BASICFONT, PAUSE_SURF, PAUSE_RECT, NEW_SURF, NEW_RECT, MENU_SURF, MENU_RECT 
    global numSquares, numPebbles, searchDepth, rounds, tiredMove, gameMode
    #global XMARGIN,YMARGIN, TILESIZE
    #TILESIZE = getTileSize(numSquares)
    pygame.init()
    pygame.font.init()

    #XMARGIN = int((WINDOWWIDTH - (TILESIZE * numSquares + (numSquares - 1))) / 2)
    #YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('AI gaming project')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    PAUSE_SURF, PAUSE_RECT  = makeText('Pause',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    MENU_SURF, MENU_RECT = makeText('Exit to Menu',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
#---------------- Start Playing ------------------------

    gameIntro()
    #aiPlay(400)
    #gamePlay()
    #optionsMenu()

def startGame(): #Game play modes
    if gameMode ==AICHALLENGE:
        aiPlay(DELAY, False)
    elif gameMode == AICHALLENGES:
        aiPlay(DELAY, True)
    else:
        gamePlay()
    
def gamePlay(): # Human vs AI 
    global XMARGIN,YMARGIN, TILESIZE
    TILESIZE = getTileSize(numSquares)
    XMARGIN = int((WINDOWWIDTH - (TILESIZE * numSquares + (numSquares - 1))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
    
    playerTurn = random.choice([True,False]) # who play first
    if tiredMove:
        tiredRound = random.choice([5,6,7,8,9,10,11,12,13,14])
    else:
        tiredRound = 10000000
    action = [0,0]
    mainBoard = generateNewBoard()
    state = 0
    rounds = 1
    counter = 1
    play = 0
    msg = 'Click tile.' # contains the message
    drawBoard(mainBoard, msg,rounds)
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.time.wait(500)
    gamePause = False
    
    while True: # main game loop
        drawBoard(mainBoard, msg,rounds)
        checkForQuit()

        while gamePause:
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                    tilex, tiley = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                    if (tilex, tiley) == (None, None):
                        # check if the user clicked on an option button
                        if PAUSE_RECT.collidepoint(event.pos):
                                gamePause = False
                                msg = 'Game Resumed !!'
                                drawBoard(mainBoard, msg, rounds)
                                pygame.display.update()
                                FPSCLOCK.tick(FPS)
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard = generateNewBoard()
                            msg = 'New start, your turn !'
                            drawBoard(mainBoard, msg, rounds)
                            pygame.display.update()
                            FPSCLOCK.tick(FPS)
                        elif MENU_RECT.collidepoint(event.pos):
                            gameIntro() #go to main menu
                elif event.type == KEYUP: # get all the KEYUP events
                    if event.key == K_SPACE:
                        gamePause = False
                        msg = 'Game Resumed !!'
                        drawBoard(mainBoard, msg, rounds)
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                else:
                    msg = 'Game Pause !!'
                    drawBoard(mainBoard, msg, rounds)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    
        if playerTurn:
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                    tilex, tiley = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                    if (tilex, tiley) == (None, None):
                        # check if the user clicked on an option button
                        if PAUSE_RECT.collidepoint(event.pos):
                            if gamePause:
                                gamePause = False
                            else:
                                gamePause = True
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard = generateNewBoard()
                            msg = 'New start, your turn !'
                            drawBoard(mainBoard, msg, rounds)
                            pygame.display.update()
                            FPSCLOCK.tick(FPS)
                        elif MENU_RECT.collidepoint(event.pos):
                            gameIntro() #go to main menu
                            
                    else:
                        # check if the clicked tile was next to the blank spot
                        action[0]= tilex
                        action[1] = tiley
                        if isValidMove(mainBoard,action,1):
                            print('Player Chose:' + str(action[:]) +':' + str(mainBoard[action[0]][action[1]]))
                            playAnimation(mainBoard,action, 'you are playing...', 500, rounds)
                            if isGoalState(mainBoard,1):
                                gameState =1
                                msg = 'You Won ! Congratulation !'
                            playerTurn = False
                            play +=1
                            
                        else:
                            msg = 'Please select a valid square'
        else:
            # computer play
            if isGoalState(mainBoard,0):
                msg='Game Over, ' + str(AI1) + 'won! give up trying!' 
                gamestate = -1
                gameOver(mainBoard,msg, rounds)
            elif isGoalState(mainBoard,1):
                msg = 'Game over, you won! I can not make a move !' 
                gamestate = 1
                gameOver(mainBoard,msg, rounds)
            if counter == tiredRound:
                if tiredPlayer == 0:
                    action = getRandomMove(mainBoard,0)
                    print('The AI Got Tired, You are impressive !!!')
                    counter = 1
                    tiredRound = random.choice([5,6,7,8,9,10,11,12,13,14])
            else:   
                action = getBestMove(mainBoard,0)
            print(str(AI1) +' Computer Chose:' + str(action[:]) +':' + str(mainBoard[action[0]][action[1]]))    
            playAnimation(mainBoard,action, 'Computer is playing...', 500, rounds)
            playerTurn = True
            play +=1
            if isGoalState(mainBoard,0):
                msg='Game Over, you lost'
                gamestate = -1
            elif isGoalState(mainBoard,1):
                msg = 'You won!'
                gamestate = 1
            else:    
                msg = 'it is your turn now !'
        if play ==2:        
            rounds +=1
            counter +=1
            play = 0
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def aiPlay(gameDelay, stepPlay): # AI vs AI
    global XMARGIN,YMARGIN, TILESIZE
    TILESIZE = getTileSize(numSquares)
    XMARGIN = int((WINDOWWIDTH - (TILESIZE * numSquares + (numSquares - 1))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
    
    playerTurn = random.choice([True,False]) # who play first
    if tiredMove:
        tiredRound = random.choice([10,12,14,16,18,20,22,24])
    else:
            tiredRound = 10000000
    action = [0,0]
    rounds = 1
    play = 0
    counter = 1
    mainBoard = generateNewBoard()
    state = 0
    msg = 'Let the game start...' 
    drawBoard(mainBoard, msg,rounds)
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.time.wait(500)
    gamePause = False
    while True:# main game loop
        drawBoard(mainBoard, msg, rounds)
        checkForQuit()
        
        if counter == tiredRound:
            tiredPlayer = random.choice([0,1])
        while gamePause:
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                    tilex, tiley = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                    if (tilex, tiley) == (None, None):
                        # check if the user clicked on an option button
                        if PAUSE_RECT.collidepoint(event.pos):
                                gamePause = False
                                msg = 'Game Resumed !!'
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard = generateNewBoard()
                            msg = 'New start, your turn !'
                            drawBoard(mainBoard, msg, rounds)
                            pygame.display.update()
                            FPSCLOCK.tick(FPS)
                        elif MENU_RECT.collidepoint(event.pos):
                            gameIntro() #go to main menu
                elif event.type == KEYUP: # get all the KEYUP events
                    if event.key == K_SPACE:
                        gamePause = False
                        msg = 'Game Resumed !!'
                else:
                    msg = 'Game Pause !!'
                    drawBoard(mainBoard, msg, rounds)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                tilex, tiley = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (tilex, tiley) == (None, None):
                    # check if the user clicked on an option button
                    if PAUSE_RECT.collidepoint(event.pos):
                        if gamePause:
                            gamePause = False
                        else:
                            gamePause = True
                    
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard = generateNewBoard()
                        msg = 'New start, your turn !'
                        drawBoard(mainBoard, msg, rounds)
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                    elif MENU_RECT.collidepoint(event.pos):
                        gameIntro() #go to main menu
            elif event.type == KEYUP: # get all the KEYUP events
                if event.key == K_SPACE:
                    gamePause = True

        if playerTurn:
            # computer B play
            if counter == tiredRound:
                if tiredPlayer == 1:
                    action = getRandomMove(mainBoard,1)
                    print(str(AI2)+' Got Tired !!!')
                    counter = 1
                    tiredRound = random.choice([10,12,14,16,18,20,22,24])
            else:   
                action = getBestMove(mainBoard,1)
            print(str(AI2) +' Chose:' + str(action[:]) +':' + str(mainBoard[action[0]][action[1]]))
            playAnimation(mainBoard,action, str(AI2) +' is playing...', gameDelay, rounds)
            playerTurn = False
            play +=1
            if isGoalState(mainBoard,1):
                msg='Game Over, ' + str(AI2) +' won'
                gamestate = 1
                gameOver(mainBoard,msg,rounds)
            elif isGoalState(mainBoard,0):
                msg = 'Game over, ' + str(AI1) +' won' 
                gamestate = -1
                gameOver(mainBoard,msg,rounds)
            else:    
                msg = str(AI1) +' turn !'
                        
        else:
            # computer A play
            if counter == tiredRound:
                if tiredPlayer == 0:
                    action = getRandomMove(mainBoard,0)
                    print(str(AI1)+' Got Tired !!!')
                    counter = 1
                    tiredRound = random.choice([10,12,14,16,18,20,22,24])
            else:   
                action = getBestMove(mainBoard,0)
            print(str(AI1) +' Chose:' + str(action[:]) +':' + str(mainBoard[action[0]][action[1]]))
            playAnimation(mainBoard,action, str(AI1) +' is playing...', gameDelay, rounds)
            playerTurn = True
            play +=1
            if isGoalState(mainBoard,0):
                msg='Game Over, ' + str(AI1) + 'won' 
                gamestate = -1
                gameOver(mainBoard,msg, rounds)
            elif isGoalState(mainBoard,1):
                msg = 'Game over, '+ str(AI2) + 'won!' 
                gamestate = 1
                gameOver(mainBoard,msg, rounds)
            else:    
                msg = str(AI2) +' turn !'
        if play ==2:        
            rounds +=1
            counter += 1
            play = 0
        if stepPlay:
            gamePause = True
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    

def optionsMenu(): # UI to select different options
    global numSquares, numPebbles, searchDepth, TILESIZE, rounds, tiredMove, gameMode
    global squaresDown_SURF, squaresDown_RECT, squaresUp_SURF, squaresUp_RECT
    global AI1, AI2, AI1H, AI2H
    textSurf2, textRect2 = makeText('Game Settings:', MESSAGECOLOR, BGCOLOR, 50, WINDOWHEIGHT - 550)

    textSurf3, textRect3 = makeText('Squares:', MESSAGECOLOR, BGCOLOR, 20, WINDOWHEIGHT - 500)
    squaresDown_SURF,   squaresDown_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  150, WINDOWHEIGHT - 500)    
    squaresUp_SURF, squaresUp_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  300, WINDOWHEIGHT - 500)

    textSurf4, textRect4 = makeText('Pebbles:', MESSAGECOLOR, BGCOLOR, 20, WINDOWHEIGHT - 450)
    pebblesDown_SURF, pebblesDown_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  150, WINDOWHEIGHT - 450)    
    pebblesUp_SURF, pebblesUp_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  300, WINDOWHEIGHT - 450)

    textSurf5, textRect5 = makeText('Game Mode:', MESSAGECOLOR, BGCOLOR, 20, WINDOWHEIGHT - 400)
    modeDown_SURF, modeDown_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  150, WINDOWHEIGHT - 400)    
    modeUp_SURF, modeUp_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  300, WINDOWHEIGHT - 400)

    textSurf6, textRect6 = makeText('Tired Play:', MESSAGECOLOR, BGCOLOR, 20, WINDOWHEIGHT - 350)
    tiredDown_SURF, tiredDown_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  150, WINDOWHEIGHT - 350)    
    tiredUp_SURF, tiredUp_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  300, WINDOWHEIGHT - 350)

#AI settinngs

    textSurf7, textRect7 = makeText('AI Settings:', MESSAGECOLOR, BGCOLOR, 500, WINDOWHEIGHT - 550)

    textSurf8, textRect8 = makeText('Search Depth:', MESSAGECOLOR, BGCOLOR, 450, WINDOWHEIGHT - 500)
    plysDown_SURF,   plysDown_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  600, WINDOWHEIGHT - 500)    
    plysUp_SURF, plysUp_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  750, WINDOWHEIGHT - 500)

    textSurf9, textRect9 = makeText('AI 1:', MESSAGECOLOR, BGCOLOR, 450, WINDOWHEIGHT - 475)
    textSurf10, textRect10 = makeText('Algorithim:', MESSAGECOLOR, BGCOLOR, 450, WINDOWHEIGHT - 450)
    ai1Down_SURF,   ai1Down_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  600, WINDOWHEIGHT - 450)    
    ai1Up_SURF, ai1Up_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  750, WINDOWHEIGHT - 450)    

    textSurf11, textRect11 = makeText('Algorithim:', MESSAGECOLOR, BGCOLOR, 450, WINDOWHEIGHT - 400)
    h1Down_SURF, h1Down_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  600, WINDOWHEIGHT - 400)    
    h1Up_SURF, h1Up_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  750, WINDOWHEIGHT - 400)    

    textSurf12, textRect12 = makeText('AI 2:', MESSAGECOLOR, BGCOLOR, 450, WINDOWHEIGHT - 375)
    textSurf13, textRect13 = makeText('Algorithim:', MESSAGECOLOR, BGCOLOR, 450, WINDOWHEIGHT - 350)
    ai2Down_SURF,   ai2Down_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  600, WINDOWHEIGHT - 350)    
    ai2Up_SURF, ai2Up_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  750, WINDOWHEIGHT - 350)    

    textSurf14, textRect14 = makeText('Algorithim:', MESSAGECOLOR, BGCOLOR, 450, WINDOWHEIGHT - 300)
    h2Down_SURF,   h2Down_RECT = makeText('<', TEXTCOLOR, TILECOLOR,  600, WINDOWHEIGHT - 300)    
    h2Up_SURF, h2Up_RECT  = makeText('>',TEXTCOLOR, TILECOLOR,  750, WINDOWHEIGHT - 300)
    
    img = pygame.image.load('auMenu.jpg')
    imgx = 0
    imgy = 0
    #pygame.draw.rect(DISPLAYSURF, BGCOLOR, (50, 50, 750, 450), 0)

    #gameMode = 'PlayerVsAI'
    modeList = ['PlayerVsAI','AIvsAI','S:AIvsAI']
    algoList = [ANDOR,MINMAX,LUCKY]
    #tiredMove = False
    index1 =0
    index2 = 1
    index3 = 0
    while True:
        squaresVal_SURF, squaresVal_RECT = makeText(str(numSquares), TEXTCOLOR, BGCOLOR, 220, WINDOWHEIGHT - 500)
        pebblesVal_SURF, pebblesVal_RECT = makeText(str(numPebbles), TEXTCOLOR, BGCOLOR, 220, WINDOWHEIGHT - 450)
        modeVal_SURF, modeVal_RECT = makeText(str(gameMode), TEXTCOLOR, BGCOLOR, 175, WINDOWHEIGHT - 400)
        tiredVal_SURF, tiredVal_RECT = makeText(str(tiredMove), TEXTCOLOR, BGCOLOR, 200, WINDOWHEIGHT - 350)
        #AI Vals
        plysVal_SURF, plysVal_RECT = makeText(str(searchDepth), TEXTCOLOR, BGCOLOR, 675, WINDOWHEIGHT - 500)
        ai1Val_SURF, ai1Val_RECT = makeText(str(AI1), TEXTCOLOR, BGCOLOR, 650, WINDOWHEIGHT - 450)
        h1Val_SURF, h1Val_RECT = makeText(str(AI1H), TEXTCOLOR, BGCOLOR, 675, WINDOWHEIGHT - 400)
        ai2Val_SURF, ai2Val_RECT = makeText(str(AI2), TEXTCOLOR, BGCOLOR, 650, WINDOWHEIGHT - 350)
        h2Val_SURF, h2Val_RECT = makeText(str(AI2H), TEXTCOLOR, BGCOLOR, 675, WINDOWHEIGHT - 300)
        
        DISPLAYSURF.blit(img,(imgx,imgy))
        
        DISPLAYSURF.blit(textSurf2, textRect2)
        DISPLAYSURF.blit(textSurf3, textRect3)
        DISPLAYSURF.blit(textSurf4, textRect4)
        DISPLAYSURF.blit(textSurf5, textRect5)
        DISPLAYSURF.blit(textSurf6, textRect6)
        DISPLAYSURF.blit(textSurf7, textRect7)
        DISPLAYSURF.blit(textSurf8, textRect8)
        DISPLAYSURF.blit(textSurf9, textRect9)
        DISPLAYSURF.blit(textSurf10, textRect10)
        DISPLAYSURF.blit(textSurf11, textRect11)
        DISPLAYSURF.blit(textSurf12, textRect12)
        DISPLAYSURF.blit(textSurf13, textRect13)
        DISPLAYSURF.blit(textSurf14, textRect14)
        DISPLAYSURF.blit(squaresDown_SURF, squaresDown_RECT)
        DISPLAYSURF.blit(squaresVal_SURF, squaresVal_RECT)
        DISPLAYSURF.blit(squaresUp_SURF, squaresUp_RECT)
        DISPLAYSURF.blit(pebblesDown_SURF, pebblesDown_RECT)
        DISPLAYSURF.blit(pebblesVal_SURF, pebblesVal_RECT)
        DISPLAYSURF.blit(pebblesUp_SURF, pebblesUp_RECT)
        DISPLAYSURF.blit(modeDown_SURF, modeDown_RECT)
        DISPLAYSURF.blit(modeVal_SURF, modeVal_RECT)
        DISPLAYSURF.blit(modeUp_SURF, modeUp_RECT)
        DISPLAYSURF.blit(tiredDown_SURF, tiredDown_RECT)
        DISPLAYSURF.blit(tiredVal_SURF, tiredVal_RECT)
        DISPLAYSURF.blit(tiredUp_SURF, tiredUp_RECT)
        
        DISPLAYSURF.blit(plysUp_SURF, plysUp_RECT)
        DISPLAYSURF.blit(plysDown_SURF, plysDown_RECT)
        DISPLAYSURF.blit(plysVal_SURF, plysVal_RECT)
        DISPLAYSURF.blit(ai1Up_SURF, ai1Up_RECT)
        DISPLAYSURF.blit(ai1Down_SURF, ai1Down_RECT)
        DISPLAYSURF.blit(ai1Val_SURF, ai1Val_RECT)

        DISPLAYSURF.blit(h1Up_SURF, h1Up_RECT)
        DISPLAYSURF.blit(h1Down_SURF, h1Down_RECT)
        DISPLAYSURF.blit(h1Val_SURF, h1Val_RECT)
        
        DISPLAYSURF.blit(ai2Up_SURF, ai2Up_RECT)
        DISPLAYSURF.blit(ai2Down_SURF, ai2Down_RECT)
        DISPLAYSURF.blit(ai2Val_SURF, ai2Val_RECT)

        DISPLAYSURF.blit(h2Up_SURF, h2Up_RECT)
        DISPLAYSURF.blit(h2Down_SURF, h2Down_RECT)
        DISPLAYSURF.blit(h2Val_SURF, h2Val_RECT)

        checkForQuit()
        
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                # check if the user clicked on an option button
                if squaresDown_RECT.collidepoint(event.pos):
                    if numSquares > 2:
                        numSquares -=1
                elif squaresUp_RECT.collidepoint(event.pos):
                    numSquares +=1
                elif pebblesUp_RECT.collidepoint(event.pos):
                    numPebbles +=1
                elif pebblesDown_RECT.collidepoint(event.pos):
                    if numPebbles > 1:
                        numPebbles -=1                    
                elif modeUp_RECT.collidepoint(event.pos):
                    if index1 <2:
                        index1 += 1
                        gameMode = modeList[index1]
                elif modeDown_RECT.collidepoint(event.pos):
                    if index1 >0:
                        index1 -= 1
                        gameMode = modeList[index1]
                elif tiredUp_RECT.collidepoint(event.pos):
                    tiredMove = True
                elif tiredDown_RECT.collidepoint(event.pos):
                    tiredMove = False
                    #AI Settings
                elif plysUp_RECT.collidepoint(event.pos):
                    searchDepth += 1
                elif plysDown_RECT.collidepoint(event.pos):
                    if searchDepth >2:
                        searchDepth -=1
                elif ai1Up_RECT.collidepoint(event.pos):
                    if index2 <2:
                        index2 += 1
                        AI1 = algoList[index2]
                elif ai1Down_RECT.collidepoint(event.pos):
                    if index2 >0:
                        index2 -=1
                        AI1 = algoList[index2]
                elif h1Up_RECT.collidepoint(event.pos):
                    AI1H= H2
                elif h1Down_RECT.collidepoint(event.pos):
                    AI1H = H1
                elif ai2Up_RECT.collidepoint(event.pos):
                    if index3 <2:
                        index3 += 1
                        AI2 = algoList[index3]
                elif ai2Down_RECT.collidepoint(event.pos):
                    if index3 >0:
                        index3 -=1
                        AI2 = algoList[index3]
                elif h2Up_RECT.collidepoint(event.pos):
                    AI2H= H2
                elif h2Down_RECT.collidepoint(event.pos):
                    AI2H = H1
                                     
        #button("Play",150,450,100,50,GREEN,LIGHT_GREEN,"play")
        button("Back",350,450,100,50,WHITE,LIGHT_RED,"goBack")
        #button("Exit",550,450,100,50,WHITE,LIGHT_RED,"quit")
        pygame.display.update()
        FPSCLOCK.tick(FPS)    
    
def terminate(): # quit game
    pygame.quit()
    sys.exit()

def getAllValidMoves(board,player): # returns all the valid list of actions
    actions = []
    for x in range(numSquares):
        action = [x,player]
        if isValidMove(board, action, player):
            actions.append(x)
    return actions

def andOrAlg(board, searchDepth,player): # AND-OR algorithm 
    V = -1
    action = [0,0]
    bestAction = [0,0]
    searchLevel = 1
    pathStates = []
    actions = getAllValidMoves(board,player)
    for x in range(len(actions)):
        newBoard = getBoardCopy(board)
        action[0] = actions[x]
        action[1] = player
        newBoard = makeMove(board, action)
        newV = andAlg(newBoard,player, searchLevel, pathStates)
        if newV >V:
            V  = newV
            bestAction[0] = action[0]
            bestAction[1] = player
    
    return bestAction

def orAlg(board, player, searchLevel, pathStates):
    stateStr = getStateStr(board)

    if isGoalState(board, player):
        if len(pathStates) > 0:
            pathStates.pop()
        return utility(board, player)
    elif searchLevel == searchDepth:
        if len(pathStates) > 0:
            pathStates.pop()
        return utility(board, player)
    V = -1
    searchLevel +=1
    actions = getAllValidMoves(board,player)
    for x in range(len(actions)):
        
        newBoard = getBoardCopy(board)
        action[0] = actions[x]
        action[1] = player
        newBoard = makeMove(board, action)
        stateStr = getStateStr(board)
        if len(pathStates) > 0 :
            for i in range(len(pathStates)):
                if stateStr == pathStates[i]:
                    return utility(newBoard, player)
        pathStates.append(stateStr)
        
        newV = andAlg(newBoard,player, searchLevel,pathStates)
        if len(pathStates) > 0:
            pathStates.pop()
        if newV >V:
            V  = newV + V

    return V

def andAlg(board,player, searchLevel, pathStates):
    stateStr = getStateStr(board)
    
    if isGoalState(board, player):
        if len(pathStates) > 0 :
            pathStates.pop()
        return utility(board,player)
    elif searchLevel == searchDepth:
        if len(pathStates) > 0:
            pathStates.pop()
        return utility(board,player)
    V = numSquares * numPebbles + 1
    searchLevel +=1
    actions = getAllValidMoves(board,player)
    for x in range(len(actions)):        
        newBoard = getBoardCopy(board)
        action[0] = actions[x]
        action[1] = player
        newBoard = makeMove(board, action)
        stateStr = getStateStr(board)
        for i in range(len(pathStates)):
            if stateStr == pathStates[i]:
                return utility(newBoard, player)
        pathStates.append(stateStr)
        
        newV = orAlg(newBoard,player,searchLevel,pathStates)
        if len(pathStates) > 0:
            pathStates.pop()
        
        if newV < V:
            V  = newV + V

    return V


def MinMax(board, searchDepth,player): # MinMax algorithm
    V = -1
    action = [0,0]
    bestAction = [5,5]
    a = -1   # alpha
    b = numSquares * numPebbles + 1
    searchLevel = 0
    leavesCount = 0
    pathStates = []
    hashTable = []
    actions = getAllValidMoves(board,player)
    #print('Valid Actions:' + str(actions[:]))
    actions = orderMoves(board, actions, player)
    #print('Sorted Actions:' + str(actions[:]))
    for x in range(len(actions)): 
        newBoard = getBoardCopy(board)
        action[0] = actions[x]
        action[1] = player
        newBoard = makeMove(board, action)
        newV = minA(newBoard, a, b, player, searchLevel, leavesCount,pathStates,hashTable)
        if newV >=V:
            V  = newV
            bestAction[0] = action[0]
            bestAction[1] = player
        if V>=b:
            return bestAction
        elif V>a:
            a = V #update alpha
    return bestAction

def maxA(board, a, b, player, searchLevel,leavesCount, pathStates, hashTable):
    newHash = 0
    stateStr = getStateStr(board)
    newHash = getHash(stateStr)
    if len(hashTable) > 0:
        for x in range(len(hashTable)):
            if newHash == hashTable[x][0]:
                if len(pathStates) > 0:
                    pathStates.pop()
                return utility(board, player)
    hashTable.append([newHash,utility(board, player)])
    if isGoalState(board, player):
        if len(pathStates) > 0:
            pathStates.pop()
        return utility(board, player)
    elif searchLevel == searchDepth:
        if len(pathStates) > 0:
            pathStates.pop()
        return utility(board, player)
    V = -1
    searchLevel +=1
    actions = getAllValidMoves(board,player)
    actions = orderMoves(board, actions, player)
    for x in range(len(actions)):
        if searchLevel == searchDepth:
            leavesCount +=1
        
        newBoard = getBoardCopy(board)
        action[0] = actions[x]
        action[1] = player
        newBoard = makeMove(newBoard, action)
        stateStr = getStateStr(board)
        if len(pathStates) > 0 :
            for i in range(len(pathStates)):
                if stateStr == pathStates[i]:
                    return utility(newBoard, player)
        pathStates.append(stateStr)
        
        newV = minA(newBoard, a, b, player, searchLevel, leavesCount,pathStates,hashTable)
        if len(pathStates) > 0:
            pathStates.pop()
        if newV >V:
            V  = newV
        if V>=b:
            #print('MaxPruned Value:' +str(V) + ' at node:' +str(searchLevel))
            return V   # prune based on beta
        elif V>a:
            a = V      # update alpha
    #print('MaxTaken Value:' +str(V) + ' at node:' +str(searchLevel))    
    return V

def minA(board, a, b, player, searchLevel,leavesCount, pathStates, hashTable):
    newHash = 0
    stateStr = getStateStr(board)
    newHash = getHash(stateStr)
    if len(hashTable) > 0 :
        for x in range(len(hashTable)):
            if newHash == hashTable[x][0]:
                if len(pathStates) > 0:
                    pathStates.pop()
                return utility(board, player)
    hashTable.append([newHash,utility(board, player)])
    if isGoalState(board, player):
        if len(pathStates) > 0 :
            pathStates.pop()
        return utility(board,player)
    elif searchLevel == searchDepth:
        if len(pathStates) > 0:
            pathStates.pop()
        return utility(board,player)
    V = numSquares * numPebbles + 1
    searchLevel +=1
    valActions = getAllValidMoves(board,player)
    actions = orderMoves(board, valActions, player)
    for x in range(len(actions)-1,0,-1):
        if searchLevel == searchDepth:
            leavesCount +=1
        
        newBoard = getBoardCopy(board)
        action[0] = actions[x]
        action[1] = player
        newBoard = makeMove(newBoard, action)
        stateStr = getStateStr(board)
        for i in range(len(pathStates)):
            if stateStr == pathStates[i]:
                return utility(newBoard, player)
        pathStates.append(stateStr)
        
        newV = maxA(newBoard, a, b, player, searchLevel, leavesCount,pathStates,hashTable)
        if len(pathStates) > 0:
            pathStates.pop()
        
        if newV < V:
            V  = newV
        if V<=a:
            #print('MinPruned Value:' +str(V) + ' at node:' +str(searchLevel))
            return V   # prune based on alpha
        elif V < b:
            b = V      # update beta
    #print('MinTaken Value:' +str(V) + ' at node:' +str(searchLevel))    
    return V


def orderMoves(board, actions, player): # Move ordering function
    values = []
    for x in range(len(actions)):
        newBoard = makeMove(board, [actions[x],player])
        value =[actions[x],utility(newBoard,player)]
        values.append(value)
    #sorting    
    for x in range(len(values)):
        temp = []
        for i in range(len(values)):
            if values[i][1] >values[x][1]:
                temp = copy.deepcopy(values[x])
                values[x] = copy.deepcopy(values[i])
                values[i] = copy.deepcopy(temp)
    orderedActions = []
    for x in range(len(values)):
        orderedActions.append(values[x][0])
    return orderedActions            
        
def getStateStr(board): # returns the State as String
    stateStr = ''
    for x in range(numSquares):
        stateStr = stateStr + str(board[x][0]) + ','
    for x in range(numSquares):
        stateStr = stateStr + str(board[x][1]) + ','            
    return stateStr

def getHash(stateStr): # returns the Hash value
    hashStr = hashlib.md5(stateStr.encode())
    return hashStr.hexdigest()

def gameOver(board, msg, rounds): # game is finished, It doesn't allow the computer to play more
    while True: # main game loop
        drawBoard(board, msg,rounds)
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                tilex, tiley = getSpotClicked(board, event.pos[0], event.pos[1])

                if (tilex, tiley) == (None, None):
                    # check if the user clicked on an option button
                    if NEW_RECT.collidepoint(event.pos):
                         aiGame(500)
                    elif MENU_RECT.collidepoint(event.pos):
                        gameIntro() #go to main menu
        pygame.display.update()
        FPSCLOCK.tick(FPS)                        

def checkForQuit(): 
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def h1(board,player): # Heuristic function 1
    # heuristic 1 using the number of pebbles in the player
    #return the total number of pebbles
    count = 0
    for x in range(numSquares):
        count += board[x][player]
    return count


def h2(board, player): # Heuristic function 2
    # heuristic 2 using the number of empty boxes in player(will send the oppnent as player)
    #return the total number of empty squares
    count = 0
    for x in range(numSquares):
        if board[x][player -1]== 0:
            count += 1
    return count

def utility(board,player): # selects the Utility function h1 or h2
    if player==0:
        if AI1H == H1:
            return h1(board, player)
        else:
            return h2(board, player)
    elif player == 1:
        if AI2H == H1:
            return h1(board, player)
        else:
            return h2(board, player)
        

def getTileSize(numSquares):
    if numSquares > 4:
        squareSize = int(( WINDOWWIDTH - 40) / numSquares)
    else:
        squareSize = 150
    return squareSize

def isGoalState(board,player):
    total = 0;
    for x in range(numSquares):
        total = total + board[x][player]
    if total == numPebbles * numSquares * 2:
        return True
    else:
        return False
    
def playAnimation(board,action, message, animationDelay,rounds):
    # Note: This function does not check if the move is valid.
    value = board[action[0]][action[1]]
    # prepare the base surface
    drawBoard(board, message,rounds)
    baseSurf = DISPLAYSURF.copy()
    # draw the selected tile in different color.
    drawTile(action[0], action[1], board[action[0]][action[1]],SELECTEDCOLOR)
    targetx, targety = action[0], action[1] # initialze the target tile as the current tile

    while value > 0:
        if targety == 0:
            if targetx < (numSquares -1) :
                targetx = targetx + 1
                board[targetx][targety] = board[targetx][targety] + 1
                board[action[0]][action[1]] = board[action[0]][action[1]] - 1
                value = value - 1
            else:
                targetx = targetx
                targety = 1
                board[targetx][targety] = board[targetx][targety] + 1
                board[action[0]][action[1]] = board[action[0]][action[1]] - 1
                value = value -1
            
        elif targety ==1:
            if targetx > 0:
                targetx = targetx - 1
                board[targetx][targety] = board[targetx][targety] + 1
                board[action[0]][action[1]] = board[action[0]][action[1]] -1
                value = value - 1
            else:
                targetx = targetx
                targety = 0
                board[targetx][targety] = board[targetx][targety] + 1
                board[action[0]][action[1]] = board[action[0]][action[1]] -1
                value = value - 1
                
        drawBoard(board, message,rounds)
        drawTile(action[0], action[1], board[action[0]][action[1]],SELECTEDCOLOR)
        baseSurf = DISPLAYSURF.copy()
        pygame.display.update()
        pygame.time.wait(animationDelay)
        FPSCLOCK.tick(FPS)


    
def getStartingBoard():
    # Return a board starting board.
    # For example, if numSquares is 3 and numPebbles is 2, this function
    # returns [[2, 2, 2], [2, 2, 2]]
    board = []
    for x in range(numSquares):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(numPebbles)
        board.append(column)
    return board

def getBoardCopy(board):
    newBoard = copy.deepcopy(board)
##    newBoard = []
##    for x in range(numSquares):
##        column = []
##        for y in range(BOARDHEIGHT):
##            column.append(board[x][y])
##        newBoard.append(column)
    return newBoard

def makeMove(board, move): 
    # This function does not check if the move is valid.
    targetx, targety = action[0], action[1] # initialze the target tile as the current tile
    value = board[action[0]][action[1]]
    newBoard = getBoardCopy(board)
    while value > 0:
        if targety == 0 :
            if targetx < (numSquares -1) :
                targetx = targetx + 1
                newBoard[targetx][targety] = newBoard[targetx][targety] + 1
                newBoard[action[0]][action[1]] = newBoard[action[0]][action[1]] - 1
                value = value - 1
            else:
                targetx = targetx
                targety = 1
                newBoard[targetx][targety] = newBoard[targetx][targety] + 1
                newBoard[action[0]][action[1]] = newBoard[action[0]][action[1]] - 1
                value = value -1
            
        elif targety ==1:
            if targetx > 0:
                targetx = targetx - 1
                newBoard[targetx][targety] = newBoard[targetx][targety] + 1
                newBoard[action[0]][action[1]] = newBoard[action[0]][action[1]] -1
                value = value - 1
            else:
                targetx = targetx
                targety = 0
                newBoard[targetx][targety] = newBoard[targetx][targety] + 1
                newBoard[action[0]][action[1]] = newBoard[action[0]][action[1]] -1
                value = value - 1

    return newBoard
    

def isValidMove(board, action, player):
    if board[action[0]][action[1]] == 0:
        return False
    elif action[1] != player:
        return False
    else:
        return True


def getRandomMove(board, player):
    # funtion to return a random move for Lucky No AI !!
    validMoves = []
    action[1] = player
    for i in range(numSquares):
        action[0] = i
        if isValidMove(board,action,player):
            validMoves.append(action[0])
    action[0]= random.choice(validMoves)
    return action    
    
# function to get the best action avilable to take     
def getBestMove(board, player):
    if player == 0:
        if AI1 == LUCKY:
            return getRandomMove(board, player)
        elif AI1 == ANDOR:
            return andOrAlg(board, searchDepth, player)
        else:
            return MinMax(board, searchDepth, player)
    elif player == 1:
        if AI2 == LUCKY:
            return getRandomMove(board, player)
        elif AI2 == ANDOR:
            return andOrAlg(board, searchDepth, player)
        else:
            return MinMax(board, searchDepth, player)        

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, tileColor, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, tileColor, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def text_objects(text, font):
    textSurf = font.render(text, True, BLACK)
    return textSurf, textSurf.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT/2))
    DISPLAYSURF.blit(textSurf, textRect)
 
    pygame.display.update()
    time.sleep(5)
    main()   
 

def button(msg,x,y,w,h,icolor,acolor,action= None):
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w >mouse[0]> x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF,acolor,(x,y,w,h))
        if click[0] == 1 and action!= None:
            
            if action == "play":
                startGame()
            elif action =="quit":
                terminate()
            elif action =="options":
                optionsMenu()
            elif action =='goBack':
                gameIntro()
                        
    pygame.draw.rect(DISPLAYSURF,icolor,(x,y,w,h))
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg,smallText)
    textRect.center = ((x+(w/2)), (y + (h/2)))
    DISPLAYSURF.blit(textSurf,textRect)

def gameIntro():
    intro = True
    img = pygame.image.load('au1.jpg')
    imgx = 0
    imgy = 0 

        
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
##        DISPLAYSURF.fill(WHITE)
        
                       
        DISPLAYSURF.blit(img,(imgx,imgy))
        largeText = pygame.font.Font('freesansbold.ttf',115)
        textSurf, textRect = text_objects(" ", largeText)
        textRect.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT/2))
        DISPLAYSURF.blit(textSurf, textRect)

        button("Play",150,450,100,50,GREEN,LIGHT_GREEN,"play")
        button("Options",350,450,100,50,WHITE,LIGHT_RED,"options")
        button("Exit",550,450,100,50,WHITE,LIGHT_RED,"quit")

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoard(board, message,plys):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    if plys:
        roundText = 'Round:' + str(int(plys))
        textSurf2, textRect2 = makeText(roundText, MESSAGECOLOR, BGCOLOR, 5, 570)
        DISPLAYSURF.blit(textSurf2, textRect2)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            #if board[tilex][tiley]:
            drawTile(tilex, tiley, board[tilex][tiley],TILECOLOR)

    left, top = getLeftTopOfTile(0, 0)
    width = numSquares * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(PAUSE_SURF, PAUSE_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(MENU_SURF, MENU_RECT)

def generateNewBoard():
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    board = getStartingBoard()
    return (board)

main()
