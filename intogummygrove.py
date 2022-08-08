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
    def _init_(self, name):
        self.name = name
        self.gold = 0 
        self.base = 100
        self.pieces = []
    
    def buyPiece(self, Piece):
        self.pieces.append(Piece)
        self.gold -= Piece.gold

class Piece:
    def _init_(self, health, attack, range, gold, xcord, ycord, mobility, team):
        self.health = health
        self.attack = attack
        self.range = range
        self.gold = gold
        self.x = xcord
        self.y = ycord
        self.mobility = mobility
        self.team = team

    def attack(self, other):
        if self.team != other.team:
            other.health -= self.attack
    
    def move(self, newx, newy):
        self.xcord = newx
        self.ycord = newy        
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
    pass

#ISOMETRIC  
def getIsometric(x, y, app):
    newx = x - y
    newy = x * 0.5 + y * 0.5
    return newx, newy

#USER INPUT FUNCTIONS
def keyPressed(app, event):
    pass

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

def drawScore(app, canvas):
    pass

#REDRAWALL
def redrawAll(app, canvas):
    drawBoard(app, canvas)
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
