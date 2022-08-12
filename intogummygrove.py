#################################################
# Term Project: Into Gummy Grove!
#
# Your name: Kevin Mao  
# Your andrew id: kevinmao
#################################################

import math, copy, random
from cmu_112_graphics import *

#################################################
# The Coding Begins! 
#################################################
#Classes 
#################################################

class Player:
    def __init__(self, name):
        self.name = name
        self.gold = 500 
        self.base = 1000
        self.pieces = []
    
    def buyPiece(self, Piece):
        if Piece.gold <= self.gold:
            self.pieces.append(Piece)
            self.gold -= Piece.gold

class Piece:
    def __init__(self, name, health, attack, range, gold, row, col, mobility, team):
        self.name = name
        self.health = health
        self.attack = attack
        self.range = range
        self.gold = gold
        self.row = row
        self.col = col
        self.mobility = mobility
        self.acted = False
        self.team = team
        self.moved = 0

    def atc(self, other):
        if self.team != other.team:
            other.health -= self.attack
    
    def move(self, newrow, newcol):
        self.row = newrow
        self.col = newcol        

#################################################
#Graphics 
#################################################
def playIntoGummyGrove():
    runApp(width = 1280, height = 720)

def appStarted(app):
    #Grid Layout
    app.rows = 9 
    app.cols = 9
    app.sideMargin = app.width/4
    app.tandbMargin = app.height / 12
    app.grid = []
    app.cellSize = (app.height - (2*app.tandbMargin)) / app.rows
    for row in range(app.rows):
        temp = []
        for col in range(app.cols):
            temp.append(0)
        app.grid.append(temp)

    #Gamplay 
    app.turns = 0
    app.currentPlayer = (app.turns % 2) + 1
    app.pieceSelection = None
    app.gameOver = False

    #Players
    app.player1 = Player("Kevin")
    app.player2 = Player("Ben")

    #Images
    app.tank = app.loadImage('tank.png')
    app.collect = app.loadImage('collect.png')

    app.etank = app.loadImage('etank.png')
    app.ecollect = app.loadImage('ecollect.png')

    app.panda = app.loadImage('panda.png')
    app.panda = app.scaleImage(app.panda, 1/8)

    app.cat = app.loadImage('cat.png')
    app.cat = app.scaleImage(app.cat, 1/4)

    app.capy = app.loadImage('capy.png')
    app.capy = app.scaleImage(app.capy, 1/4)

    app.base1 = app.loadImage('base1.png')
    app.base1row = 8
    app.base1col = 4
    app.base2 = app.loadImage('base2.png')
    app.base2row = 0
    app.base2col = 4

    app.gummygrove = app.loadImage('gummygrove.jpg')
    app.gumgrov = app.scaleImage(app.gummygrove, 1/8)

    app.avatar = app.cat

    #UI Locations 
    app.nextturnx = app.width / 8
    app.nextturny = app.height * 5 / 6
    app.buybtnr = app.height / 12

    app.attacking = False
    app.moving = False

    #Resource Board: 
    app.resboard = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 1, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 1, 0, 0, 0, 0, 1, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 1, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                    ]
    app.reslocations = []
    for row in range(len(app.resboard)):
        for col in range(len(app.resboard[row])):
            if app.resboard[row][col] == 1:
                app.reslocations.append((row, col))            


    #heightBoard
    app.heiboard = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 1, 0, 1, 0, 0, 0, 0, 0, 2 ],
                    [ 1, 0, 0, 0, 0, 1, 2, 0, 1 ],
                    [ 0, 0, 1, 0, 2, 1, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
                    [ 1, 0, 0, 1, 0, 0, 0, 0, 1 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 1, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                    ]

    app.hght = app.cellSize * 1/2

    #views
    app.view = 0

    app.movement = 0
    app.aimSelectionRow = -1
    app.aimSelectionCol = -1

    app.mode = 'splScrnMode'

# Splash Screen Mode

def splScrnMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "white")
    canvas.create_text(app.width/2, 150, text='INTO GUMMY GROVE!', font = "Unispace 22 bold", fill = "grey15")
    canvas.create_text(app.width/2, 250, text='Press any key for the game!', fill = "grey15")
    canvas.create_image(app.width / 2, (app.height * 5/8), image=ImageTk.PhotoImage(app.gumgrov))
    canvas.create_image(app.width * 1 / 2, (app.height * 7/8), image=ImageTk.PhotoImage(app.cat))
    canvas.create_image(app.width * 13 / 16, (app.height * 6/8), image=ImageTk.PhotoImage(app.panda))
    canvas.create_image(app.width * 3 / 16, (app.height * 5/8), image=ImageTk.PhotoImage(app.capy))

def splScrnMode_keyPressed(app, event):
    app.mode = 'gameMode'

#ISOMETRIC  
def getIsometric(x, y, app):
    newx = x - y
    newy = x * 0.5 + y * 0.5
    return newx, newy

def getCellMidPoint(app, row, col):
    topx = col * app.cellSize
    topy = row * app.cellSize
    tx,ty = getIsometric(topx, topy, app)
    leftx = (col) * app.cellSize
    lefty = (row + 1) * app.cellSize
    lx,ly = getIsometric(leftx, lefty, app)
    tx, ly = tx + app.width/2, ly + app.tandbMargin
    return tx, ly

def getRowCol(app, x, y):
    x -= app.width/2 
    y -= app.tandbMargin
    col = (y + 0.5 * x) // app.cellSize
    row = (y - 0.5 * x) // app.cellSize
    return row, col

#BUYBUYBUY maybe make damage from father ranges lower
def buyResourceCollector(app, row, col, player):
    if len(player.pieces) < 8:
        if app.currentPlayer == 1:
            resourceCollector = Piece("collect", 100, 0, 0, 200, row, col, 1, 1)
            player.buyPiece(resourceCollector)
        else:
            resourceCollector = Piece("ecollect", 100, 0, 0, 200, row, col, 1, 2)
            player.buyPiece(resourceCollector)

def buyTank(app, row, col, player):
    if len(player.pieces) < 8:
        if app.currentPlayer == 1:
            tank = Piece("tank", 300, 200, 5, 200, row, col, 2, 1)
            player.buyPiece(tank)
        else:
            tank = Piece("etank", 300, 200, 5, 200, row, col, 2, 2)
            player.buyPiece(tank)

#USER INPUT FUNCTIONS
import math
def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

def gameMode_keyPressed(app, event):
    if event.key == 'p':
        app.mode = 'splScrnMode'
        if app.gameOver:
            appStarted(app)
    if app.gameOver:
        return
    if event.key == 'q':
        if app.currentPlayer == 1:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                if row > 6:
                    buyResourceCollector(app, row, col, app.player1)
        if app.currentPlayer == 2:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                if row < 3:
                    buyResourceCollector(app, row, col, app.player2)
    if event.key == 'w':
        if app.currentPlayer == 1:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                if row > 6:
                    buyTank(app, row, col, app.player1)
        if app.currentPlayer == 2:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                if row < 3:
                    buyTank(app, row, col, app.player2)
    if event.key == 'e':
        app.moving, app.attacking = False, False
        app.pieceSelection = None
        addMoney(app)
        app.turns += 1
        app.currentPlayer = (app.turns % 2) + 1
        for piece in app.player1.pieces:
            piece.acted = False
        for piece in app.player2.pieces:
            piece.acted = False
    if event.key == 's':
        if not app.moving:
            app.moving = True
        else:
            app.moving = False
    if event.key == 'a':
        if app.pieceSelection != None and not app.pieceSelection.acted:
            if not app.attacking:
                app.attacking = True
            else:
                app.attacking = False
    if event.key == 'Up':
        if app.pieceSelection != None and app.pieceSelection.team == app.currentPlayer and app.moving:
            if not app.pieceSelection.acted:
                if isLegal(app, app.pieceSelection.row - 1, app.pieceSelection.col):
                    if abs(app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)] - app.heiboard[int(app.pieceSelection.row) - 1][int(app.pieceSelection.col)]) <= 1:
                        app.pieceSelection.row -= 1
                        if app.pieceSelection.moved < (app.pieceSelection.mobility - 1):
                            app.pieceSelection.moved += 1
                        else:
                            app.pieceSelection.acted = True
                            app.pieceSelection.moved = 0
                        app.pieceSelection.range += app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)]

            else:
                app.moving, app.attacking = False, False
    if event.key == 'Right':
        if app.pieceSelection != None and app.pieceSelection.team == app.currentPlayer and app.moving:
            if not app.pieceSelection.acted:
                if isLegal(app, app.pieceSelection.row, app.pieceSelection.col + 1):
                    if abs(app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)] - app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col) + 1]) <= 1:
                        app.pieceSelection.col += 1
                        if app.pieceSelection.moved < (app.pieceSelection.mobility - 1):
                            app.pieceSelection.moved += 1
                        else:
                            app.pieceSelection.acted = True
                            app.pieceSelection.moved = 0
                        app.pieceSelection.range += app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)]
            else:
                app.moving, app.attacking = False, False
    if event.key == 'Down':
        if app.pieceSelection != None and app.pieceSelection.team == app.currentPlayer and app.moving:
            if not app.pieceSelection.acted:
                if isLegal(app, app.pieceSelection.row + 1, app.pieceSelection.col):
                    if abs(app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)] - app.heiboard[int(app.pieceSelection.row) + 1][int(app.pieceSelection.col)]) <= 1:
                        app.pieceSelection.row += 1
                        if app.pieceSelection.moved < (app.pieceSelection.mobility - 1):
                            app.pieceSelection.moved += 1
                        else:
                            app.pieceSelection.acted = True
                            app.pieceSelection.moved = 0
                        app.pieceSelection.range += app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)]
            else:
                app.moving, app.attacking = False, False
    if event.key == 'Left':
        if app.pieceSelection != None and app.pieceSelection.team == app.currentPlayer and app.moving:
            if not app.pieceSelection.acted:
                if isLegal(app, app.pieceSelection.row, app.pieceSelection.col - 1):
                    if abs(app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)] - app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col) - 1]) <= 1:
                        app.pieceSelection.col -= 1
                        if app.pieceSelection.moved < (app.pieceSelection.mobility - 1):
                            app.pieceSelection.moved += 1
                        else:
                            app.pieceSelection.acted = True
                            app.pieceSelection.moved = 0
                        app.pieceSelection.range += app.heiboard[int(app.pieceSelection.row)][int(app.pieceSelection.col)]
            else:
                app.moving, app.attacking = False, False
    if event.key == '1':
        app.view = 1
    if event.key == '2':
        app.view = 2
    if event.key == '0':
        app.view = 0
    if event.key == '3':
        app.view = 3
    
    if event.key == 'm': 
        appStarted(app)
        from random import randint
        app.heiboard[0][0] = randint(0, 2)
        app.heiboard[8][0] = randint(0, 2)
        app.heiboard[0][8] = randint(0, 2)
        app.heiboard[8][8] = randint(0, 2)
        chunkSize = app.rows - 1
        while(chunkSize > 1):
            half = chunkSize / 2
            half = int(half)
            #square step
            for row in range(0, 8, chunkSize):
                for col in range(0, 8, chunkSize):
                    avg = (app.heiboard[row][col] + app.heiboard[row][col+ chunkSize] + app.heiboard[row + chunkSize][col] + app.heiboard[row + chunkSize][col + chunkSize]) / 4
                    app.heiboard[int(row + half)][int(col + half)] = int(avg) + randint(0,1)
            chunkSize /= 2
            chunkSize = int(chunkSize)
        #makes resource locations and bases at height 0
        for rows in range(len(app.heiboard)):
            for cols in range(len(app.heiboard[rows])):
                if app.resboard[rows][cols] == 1:
                    app.heiboard[rows][cols] = 0
        app.heiboard[0][4] == 0
        app.heiboard[8][4] == 0
    if event.key == 'n':
        appStarted(app)
        app.heiboard = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 1, 0, 1, 0, 0, 0, 0, 0, 2 ],
                    [ 1, 0, 0, 0, 0, 1, 2, 0, 1 ],
                    [ 0, 0, 1, 0, 2, 1, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
                    [ 1, 0, 0, 1, 0, 0, 0, 0, 1 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 1, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                    ]
    if event.key == 'v':
        app.avatar = app.capy
        pass
    
    if event.key == 'x':
        app.avatar = app.panda
        pass
    
    if event.key == 'k':
        app.avatar = app.cat
        pass

def getTile(app, event):
    row, col = getRowCol(app, event.x, event.y)
    return row, col

def selectPiece(app, event):
    row, col = getRowCol(app, event.x, event.y)
    for piece in app.player1.pieces:
        if row == piece.row and col == piece.col:
            app.pieceSelection = piece
    for piece in app.player2.pieces:
        if row == piece.row and col == piece.col:
            app.pieceSelection = piece

def aimPiece(app, event):
    row, col = getRowCol(app, event.x, event.y)
    if gridDis(app.pieceSelection.row, app.pieceSelection.col, row, col) <= app.pieceSelection.range:
        app.aimSelectionRow = row
        app.aimSelectionCol = col

def addMoney(app):
    for piece in app.player1.pieces:
        if piece.name == "collect":
            if (piece.row, piece.col) in app.reslocations:
                app.player1.gold += 50
    for piece in app.player2.pieces:
        if piece.name == "ecollect":
            if (piece.row, piece.col) in app.reslocations:
                app.player2.gold += 50

def gameMode_mousePressed(app, event):
    if app.gameOver:
        return
    row, col = getRowCol(app, event.x, event.y)
    if event.x > (app.width * 70/80) and event.x < (app.width * 79/80) and event.y > (app.height * 3/4) and event.y < (app.height * 75/80):
        if app.attacking:
            if app.pieceSelection.team == app.currentPlayer:
                if not app.pieceSelection.acted:
                    if not app.pieceSelection.range < gridDis(app.pieceSelection.row, app.pieceSelection.col, app.aimSelectionRow, app.aimSelectionCol):
                        attackPiece(app, app.aimSelectionRow, app.aimSelectionCol, app.pieceSelection)
                        if app.player1.base <= 0:
                            app.gameOver = True
                        if app.player2.base <= 0:
                            app.gameOver = True
                        app.pieceSelection.acted = True
                        app.pieceSelection = None
                        app.moving, app.attacking = False, False
                else:
                    app.moving, app.attacking = False, False
    #Selecting a Piece
    else:
        if app.pieceSelection != None and app.attacking:
            aimPiece(app, event)
        else:
            app.moving, app.attacking = False, False
            selectPiece(app, event)

#Action! 
def isLegal(app, row, col):
    if row >= app.rows or col >= app.cols:
        return False
    if row < 0 or col < 0:
        return False
    for pieces in app.player1.pieces:
        if pieces.row == row and pieces.col == col:
            return False
    for pieces in app.player2.pieces:
        if pieces.row == row and pieces.col == col:
            return False
    if (row, col) == (app.base1row, app.base1col) or (row, col) == (app.base2row, app.base2col):
        return False
    return True

def movePiece(app, row, col, piece):
    if row < app.rows and col < app.cols:
        if row >= 0 and col >= 0:
            piece.move(row, col)

def gridDis(row1, col1, row2, col2):
    return abs(row1-row2) + abs(col1-col2)

def attackPiece(app, row, col, p):
    if p.team == 1:
        if row == app.base2row and col == app.base2col:
            app.player2.base -= p.attack
        else:
            for enpiece in app.player2.pieces:
                if enpiece.row == row and enpiece.col == col:
                    p.atc(enpiece)
                    if enpiece.health <= 0:
                        app.player2.pieces.remove(enpiece)  
    else:
        if row == app.base1row and col == app.base1col:
            app.player1.base -= p.attack
        else:
            for enpiece in app.player1.pieces:
                if enpiece.row == row and enpiece.col == col:
                    p.atc(enpiece)
                    if enpiece.health <= 0:
                        app.player1.pieces.remove(enpiece)            
#DRAW BOARD FUNCTIONS
def drawBoard(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "grey15")
    for row in range(app.rows):
        for col in range(app.cols):
            if app.view == 0:
                drawCell(app, canvas, row, col)
                if app.heiboard[row][col] == 0:
                    drawPieces(app, row, col, canvas, 0)
                drawHeight(app, canvas, row, col, app.heiboard[row][col])
            elif app.view == 1:
                if app.heiboard[row][col] == 0:
                    drawCell(app, canvas, row, col)
                    drawPieces(app, row, col, canvas, 0)
                    drawHeight(app, canvas, row, col, app.heiboard[row][col])
            elif app.view == 2:
                if app.heiboard[row][col] == 1:
                    drawHeight(app, canvas, row, col, app.heiboard[row][col])
            elif app.view == 3:
                if app.heiboard[row][col] == 2:
                    drawHeight(app, canvas, row, col, app.heiboard[row][col])


def drawCell(app, canvas, row, col):   
    #top  
    topx = col * app.cellSize
    topy = row * app.cellSize
    tx,ty = getIsometric(topx, topy, app)
    #bottom
    botx = (col + 1) * app.cellSize
    boty = (row + 1) * app.cellSize
    bx,by = getIsometric(botx, boty, app)
    #left
    leftx = (col) * app.cellSize
    lefty = (row + 1) * app.cellSize
    lx,ly = getIsometric(leftx, lefty, app)
    #right
    rightx = (col + 1) * app.cellSize
    righty = (row) * app.cellSize
    rx,ry = getIsometric(rightx, righty, app)
    ty, by, ly, ry = ty + app.tandbMargin, by + app.tandbMargin, ly + app.tandbMargin, ry + app.tandbMargin
    tx, bx, lx, rx = tx + app.width/2, bx + app.width/2, lx + app.width/2, rx + app.width/2
    if app.resboard[row][col] == 1:
        canvas.create_polygon(rx, ry, tx, ty, lx, ly, bx, by, fill = "tan", width = 3, outline = "black")
    else:
        canvas.create_polygon(rx, ry, tx, ty, lx, ly, bx, by, fill = "dimgrey", width = 3, outline = "black")
    if app.pieceSelection != None and row == app.pieceSelection.row and col == app.pieceSelection.col:
        canvas.create_polygon(rx, ry, tx, ty, lx, ly, bx, by, fill = "light goldenrod yellow", width = 3, outline = "black")
    if app.attacking == True:
        if (row, col) == (app.aimSelectionRow, app.aimSelectionCol):
            canvas.create_polygon(rx, ry, tx, ty, lx, ly, bx, by, fill = "tomato2", width = 3, outline = "black")
    
    
def drawHeight(app, canvas, row, col, howhigh):
    if howhigh <= 0:
        return
    topx = col * app.cellSize
    topy = row * app.cellSize
    tx,ty = getIsometric(topx, topy, app)
    #bottom
    botx = (col + 1) * app.cellSize
    boty = (row + 1) * app.cellSize
    bx,by = getIsometric(botx, boty, app)
    #left
    leftx = (col) * app.cellSize
    lefty = (row + 1) * app.cellSize
    lx,ly = getIsometric(leftx, lefty, app)
    #right
    rightx = (col + 1) * app.cellSize
    righty = (row) * app.cellSize
    rx,ry = getIsometric(rightx, righty, app)
    ty, by, ly, ry = ty + app.tandbMargin, by + app.tandbMargin, ly + app.tandbMargin, ry + app.tandbMargin
    tx, bx, lx, rx = tx + app.width/2, bx + app.width/2, lx + app.width/2, rx + app.width/2
    high = howhigh * app.hght
    hty, hby, hly, hry = ty - high, by - high, ly - high, ry - high
    canvas.create_polygon(lx, hly, bx, hby, bx, by, lx, ly, fill = "dimgrey", width = 3, outline = "black")
    canvas.create_polygon(bx, hby, bx, by, rx, ry, rx, hry, fill = "dimgrey", width = 3, outline = "black")
    canvas.create_polygon(tx, hty, rx, hry, bx, hby, lx, hly, fill = "dimgrey", width = 3, outline = "black")
    if app.pieceSelection != None and row == app.pieceSelection.row and col == app.pieceSelection.col:
        canvas.create_polygon(tx, hty, rx, hry, bx, hby, lx, hly, fill = "light goldenrod yellow", width = 3, outline = "black")
    if app.attacking == True:
        if (row, col) == (app.aimSelectionRow, app.aimSelectionCol):
            canvas.create_polygon(tx, hty, rx, hry, bx, hby, lx, hly, fill = "tomato2", width = 3, outline = "black")
    drawPieces(app, row, col, canvas, high)

def drawGameInfo(app, canvas):
    canvas.create_rectangle(app.width/80,app.height/40, app.width/4, app.height/4, fill = "grey7", outline = "navy", width = 1)
    canvas.create_text(app.width/30, app.height * 10/100, text = f"Current Player: {app.currentPlayer}", fill = "White", font = "Unispace 15 bold", anchor = "w")
    canvas.create_text(app.width/30, app.height * 13/100, text =  f"Total Num Turns: {app.turns}", fill = "White", font = "Unispace 11", anchor = "w")
    if app.currentPlayer == 1:
        canvas.create_text(app.width/30, app.height * 16/100, text = f"Player 1 Gold: {app.player1.gold}", fill = "White", font = "Unispace 11", anchor = "w")
        canvas.create_text(app.width/30, app.height * 19/100, text = f"Player 1 Base Health: {app.player1.base}", fill = "White", font = "Unispace 11", anchor = "w")
    if app.currentPlayer == 2:
        canvas.create_text(app.width/30, app.height * 16/100, text = f"Player 2 Gold: {app.player2.gold}", fill = "White", font = "Unispace 11", anchor = "w")
        canvas.create_text(app.width/30, app.height * 19/100, text = f"Player 2 Base Health: {app.player2.base}", fill = "White", font = "Unispace 11", anchor = "w")

def drawControls(app, canvas):
    canvas.create_rectangle(app.width/80, app.height * 77.5/100, app.width/4, app.height * 98/100, fill = "grey7", outline = "navy", width = 1)
    canvas.create_text(app.width * 0.13125, app.height * 81/100, text = f"Controls", fill = "White", font = "Unispace 15 bold")
    canvas.create_text(app.width/30, app.height * 85/100, text = f"Map Levels: 0, 1, 2, 3", fill = "White", font = "System 10", anchor = "w")
    canvas.create_text(app.width/30, app.height * 87/100, text = f"Buy Collector: Q | Buy Tank: W", fill = "White", font = "System 10", anchor = "w")
    canvas.create_text(app.width/30, app.height * 89/100, text = f"Move: S | Attack: A", fill = "White", font = "System 10", anchor = "w")
    canvas.create_text(app.width/30, app.height * 91/100, text = f"Change Avatar: X | V | K", fill = "White", font = "System 10", anchor = "w")
    canvas.create_text(app.width/30, app.height * 93/100, text = f"Square Algorithm Map: M | Default Map: N", fill = "White", font = "System 10", anchor = "w")
    canvas.create_text(app.width/30, app.height * 95/100, text = f"Title Screen: P", fill = "White", font = "System 10", anchor = "w")



def drawPiece(app, canvas, row, col, name, player, height):
    x, y = getCellMidPoint(app, row, col)
    if player == 1:
        if name == "tank":
            canvas.create_image(x, (y - 10 - height), image=ImageTk.PhotoImage(app.tank))
        elif name == "collect":
            canvas.create_image(x, (y - 15 - height), image=ImageTk.PhotoImage(app.collect))
    else:
        if name == "etank":
            canvas.create_image(x, (y - 10 - height), image=ImageTk.PhotoImage(app.etank))
        elif name == "ecollect":
            canvas.create_image(x, (y - 15 - height), image=ImageTk.PhotoImage(app.ecollect))

def drawAvatar(app, canvas):
    canvas.create_image(app.width / 3, (app.height * 87/100), image=ImageTk.PhotoImage(app.avatar))

def drawBases(app, canvas):
    x1, y1 = getCellMidPoint(app, app.base1row, app.base1col)
    x2, y2 = getCellMidPoint(app, app.base2row, app.base2col)
    canvas.create_image(x1, y1 - 15, image=ImageTk.PhotoImage(app.base1))
    canvas.create_image(x2, y2 - 15, image=ImageTk.PhotoImage(app.base2))

def drawPieces(app, row, col, canvas, height):
    for piece in app.player1.pieces:
        if piece.row == row and piece.col == col:
            drawPiece(app, canvas, piece.row, piece.col, piece.name, 1, height)
    for piece in app.player2.pieces:
        if piece.row == row and piece.col == col:
            drawPiece(app, canvas, piece.row, piece.col, piece.name, 2, height)

def drawSelection(app, canvas):
     if app.pieceSelection != None:
        canvas.create_rectangle(app. width*60/80, app.height/40, app.width * 79/80, app.height / 4, fill = "grey7", outline = "navy", width = 1)
        canvas.create_text(app.width * 77/100, app.height * 7.5/100, text = f"Health: {app.pieceSelection.health}", fill = "White", anchor = 'w', font = "Unispace 10")
        canvas.create_text(app.width * 77/100, app.height * 10/100, text = f"Range: {app.pieceSelection.range}", fill = "White", anchor = 'w', font = "Unispace 10")
        canvas.create_text(app.width * 77/100, app.height * 12.5/100, text = f"Damage: {app.pieceSelection.attack}", fill = "White", anchor = 'w', font = "Unispace 10")
        canvas.create_text(app.width * 77/100, app.height * 15/100, text = f"Acted: {app.pieceSelection.acted}", fill = "White", anchor = 'w', font = "Unispace 10")
        canvas.create_text(app.width * 77/100, app.height * 17.5/100, text = f"Mobility: {app.pieceSelection.mobility}", fill = "White", anchor = 'w', font = "Unispace 10")
        if app.moving:
            canvas.create_text(app.width * 77/100, app.height * 20/100, text = f"Status: Moving", fill = "White", anchor = 'w', font = "Unispace 10")
        if app.attacking:
            canvas.create_text(app.width * 77/100, app.height * 20/100, text = f"Status: Attacking", fill = "White", anchor = 'w', font = "Unispace 10")

def drawAttackBtn(app, canvas):
    if app.attacking:
        if app.aimSelectionRow != -1:
            if app.pieceSelection.team == app.currentPlayer:
                canvas.create_rectangle(app. width * 89/100, app.height * 81/100, app.width * 99/100, app.height * 98.5/100, fill = "tomato2")
                canvas.create_text(app.width * 92.5/100, app.height * 90/100, text = "ATTACK", fill = "White", anchor = 'w', font = "Unispace 10 bold")

def drawGameOver(app, canvas):
    if app.gameOver:
        canvas.create_rectangle(0, app.height/2 - 20, app.width,
                                app.height/2 + 20, fill = "black")
        if app.player1.base <= 0:
            canvas.create_text(app.width/2, app.height/2, text = "GAME OVER PLAYER 2 WINS",
                                font = "Times 15 bold", 
                                fill = "light goldenrod yellow")
        else:
            canvas.create_text(app.width/2, app.height/2, text = "GAME OVER PLAYER 1 WINS",
                                font = "Times 15 bold", 
                                fill = "light goldenrod yellow")
        canvas.create_text(app.width/2, app.height * 55/100, text = "PRESS P TO RESET",
                            font = "Times 15 bold", fill = "White")

#REDRAWALL
def gameMode_redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawGameInfo(app, canvas)
    drawSelection(app, canvas)
    drawAttackBtn(app, canvas)
    drawBases(app, canvas)
    drawGameOver(app, canvas)
    drawControls(app, canvas)
    drawAvatar(app, canvas)

#################################################
# main
#################################################

def main():
    playIntoGummyGrove()
if __name__ == '__main__':
    main()
