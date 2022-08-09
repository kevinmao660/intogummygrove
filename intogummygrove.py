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
        self.base = 100
        self.pieces = []
    
    def buyPiece(self, Piece):
        if Piece.gold < self.gold:
            self.pieces.append(Piece)
            self.gold -= Piece.gold

class Piece:
    def __init__(self, health, attack, range, gold, row, col, mobility, team):
        self.health = health
        self.attack = attack
        self.range = range
        self.gold = gold
        self.row = row
        self.col = col
        self.mobility = mobility
        self.team = team

    def attack(self, other):
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
    pass

def appStarted(app):
    #Grid Layout
    app.rows = 8 
    app.cols = 8
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

    #Players
    app.player1 = Player("Kevin")
    testTank = Piece(500, 500, 500, 500, 0, 0, 100, 1)
    app.player1.buyPiece(testTank)
    app.player2 = Player("Ben")

    #testTank
    app.tank = app.loadImage('testTank.png')

    pass

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
    pass

def getRowCol(app, x, y):
    x -= app.width/2 
    y -= app.tandbMargin

    col = (y + 0.5 * x) // app.cellSize
    row = (y - 0.5 * x) // app.cellSize

    return row, col

#USER INPUT FUNCTIONS
def keyPressed(app, event):
    pass

def mousePressed(app, event):
    row, col = getRowCol(app, event.x, event.y)
    if app.pieceSelection == None:
        if app.currentPlayer == 1:
            for piece in app.player1.pieces:
                if row == piece.row and col == piece.col:
                    app.pieceSelection = piece
    else:
        movePiece(app, row, col, app.pieceSelection)
        app.pieceSelection = None

#Action! 
def movePiece(app, row, col, piece):
    if row < app.rows and col < app.cols:
        if row > 0 and col > 0:
            piece.move(row, col)

#DRAW BOARD FUNCTIONS
def drawBoard(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "grey22")
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col)
    pass

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
    #canvas.create_rectangle(topx, topy, botx, boty, width = 3)
    canvas.create_polygon(rx, ry, tx, ty, lx, ly, bx, by, fill = "light goldenrod", width =3, outline = "black")
    pass

#Buttons 

def drawGameOver(app, canvas):
    if app.isGameOver:
        canvas.create_rectangle(0, app.height/2 - 20, app.width,
                                app.height/2 + 20, fill = "black")
        canvas.create_text(app.width/2, app.height/2, text = "GAME OVER",
                            font = "Times 15 bold", 
                            fill = "light goldenrod yellow")

def drawScore(app, canvas):
    pass

def drawPiece(app, canvas, row, col):
    x, y = getCellMidPoint(app, row, col)
    canvas.create_image(x, (y - 10), image=ImageTk.PhotoImage(app.tank))

def drawPieces(app, canvas):
    for pieces in app.player1.pieces:
        drawPiece(app, canvas, pieces.row, pieces.col)

#REDRAWALL
def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    pass

#TIMERFIRED
def timerFired(app):
    pass

# def gameDimensions():
#     return (rows, cols, margin, cellSize)
#################################################
# main
#################################################

def main():
    playIntoGummyGrove()
if __name__ == '__main__':
    main()

