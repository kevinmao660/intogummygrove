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
        self.gold = 100000 
        self.base = 100
        self.pieces = []
    
    def buyPiece(self, Piece):
        if Piece.gold <= self.gold:
            self.pieces.append(Piece)
            self.gold -= Piece.gold

class Piece:
    def __init__(self, name, health, attack, range, gold, row, col, mobility):
        self.name = name
        self.health = health
        self.attack = attack
        self.range = range
        self.gold = gold
        self.row = row
        self.col = col
        self.mobility = mobility
        self.acted = False

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
    testTank = Piece("tank", 500, 500, 500, 500, 7, 2, 100)
    app.player1.buyPiece(testTank)

    app.player2 = Player("Ben")
    testTank = Piece("tank", 500, 500, 500, 500, 0, 2, 100)
    app.player2.buyPiece(testTank)

    #testTank
    app.tank = app.loadImage('tank.png')
    app.collect = app.loadImage('collect.png')

    app.etank = app.loadImage('etank.png')
    app.ecollect = app.loadImage('ecollect.png')

    #UI Locations 
    app.nextturnx = app.width / 8
    app.nextturny = app.height * 5 / 6
    app.buybtnr = app.height / 12

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

#Buttons 
def drawEndButton(app, canvas):
    canvas.create_oval(app.nextturnx - app.buybtnr, app.nextturny - app.buybtnr, 
                        app.nextturnx + app.buybtnr, app.nextturny + app.buybtnr, 
                        fill = "goldenrod")
    canvas.create_text(app.nextturnx, app.nextturny, text = "End Turn")
    pass

#BUYBUYBUY
def buyResourceCollector(row, col, player):
    resourceCollector = Piece("collect", 100, 0, 0, 200, row, col, 0)
    player.buyPiece(resourceCollector)

#USER INPUT FUNCTIONS
import math
def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

def keyPressed(app, event):
    if event.key == 'b':
        if app.currentPlayer == 1:
            row, col = getTile(app, event)
            buyResourceCollector(row, col, app.player1)
        if app.currentPlayer == 2:
            row, col = getTile(app, event)
            buyResourceCollector(row, col, app.player2)

def getTile(app, event):
    row, col = getRowCol(app, event.x, event.y)
    return row, col

def mousePressed(app, event):
    row, col = getRowCol(app, event.x, event.y)
    if distance(event.x, event.y, app.nextturnx, app.nextturny) < app.buybtnr:
        app.turns += 1
        app.currentPlayer = (app.turns % 2) + 1
        for piece in app.player1.pieces:
            piece.acted = False
        for piece in app.player2.pieces:
            piece.acted = False
    elif app.pieceSelection == None:
        if app.currentPlayer == 1:
            for piece in app.player1.pieces:
                if row == piece.row and col == piece.col:
                    app.pieceSelection = piece
        if app.currentPlayer == 2:
            for piece in app.player2.pieces:
                if row == piece.row and col == piece.col:
                    app.pieceSelection = piece
    else:
        if not app.pieceSelection.acted:
            movePiece(app, row, col, app.pieceSelection)
            app.pieceSelection.acted = True
            app.pieceSelection = None

#Action! 
def movePiece(app, row, col, piece):
    if row < app.rows and col < app.cols:
        if row >= 0 and col >= 0:
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

def drawGameOver(app, canvas):
    if app.isGameOver:
        canvas.create_rectangle(0, app.height/2 - 20, app.width,
                                app.height/2 + 20, fill = "black")
        canvas.create_text(app.width/2, app.height/2, text = "GAME OVER",
                            font = "Times 15 bold", 
                            fill = "light goldenrod yellow")

def drawGameInfo(app, canvas):
    canvas.create_rectangle(app.width/80,app.height/40, app.width/4, app.height/4, fill = "Yellow")
    canvas.create_text(app.width/10, app.height/10, text = f"Player = {app.currentPlayer}")
    canvas.create_text(app.width/10, app.height/8, text = f"Turns: {app.turns}")

def drawPiece(app, canvas, row, col, name, player):
    x, y = getCellMidPoint(app, row, col)
    if player == 1:
        if name == "tank":
            canvas.create_image(x, (y - 10), image=ImageTk.PhotoImage(app.tank))
        elif name == "collect":
            canvas.create_image(x, (y-10), image=ImageTk.PhotoImage(app.collect))
    else:
        if name == "tank":
            canvas.create_image(x, (y - 10), image=ImageTk.PhotoImage(app.etank))
        elif name == "collect":
            canvas.create_image(x, (y-10), image=ImageTk.PhotoImage(app.ecollect))

def drawPieces(app, canvas):
    for piece in app.player1.pieces:
        drawPiece(app, canvas, piece.row, piece.col, piece.name, 1)
    for piece in app.player2.pieces:
        drawPiece(app, canvas, piece.row, piece.col, piece.name, 2)

def drawSelection(app, canvas):
    while app.pieceSelection != None:
        canvas.create_rectangle(app. width*60/80, app.height/40, app.width * 79/80, app.height / 4, fill = "light goldenrod")
        pass

#REDRAWALL
def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    drawGameInfo(app, canvas)
    drawEndButton(app, canvas)
    drawSelection(app, canvas)
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

