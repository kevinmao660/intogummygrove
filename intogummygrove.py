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
        self.gold = 1000 
        self.base = 10000
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
    pass

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

    #Players
    app.player1 = Player("Kevin")
    app.player2 = Player("Ben")

    #Images
    app.tank = app.loadImage('tank.png')
    app.collect = app.loadImage('collect.png')

    app.etank = app.loadImage('etank.png')
    app.ecollect = app.loadImage('ecollect.png')

    app.base1 = app.loadImage('base1.png')
    app.base2 = app.loadImage('base2.png')

    #UI Locations 
    app.nextturnx = app.width / 8
    app.nextturny = app.height * 5 / 6
    app.buybtnr = app.height / 12

    app.attacking = False
    app.moving = False

    #Resource Board: 
    app.resboard = [[ 1, 0, 0, 0, 0, 0, 0, 0, 1 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                    [ 1, 0, 0, 0, 0, 0, 0, 0, 1 ]
                    ]
    app.reslocations = [(0,0), (8,0), (0,8), (8,8)]


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
def buyResourceCollector(app, row, col, player):
    if app.currentPlayer == 1:
        resourceCollector = Piece("collect", 100, 0, 0, 200, row, col, 0, 1)
        player.buyPiece(resourceCollector)
    else:
        resourceCollector = Piece("ecollect", 100, 0, 0, 200, row, col, 0, 2)
        player.buyPiece(resourceCollector)

def buyTank(app, row, col, player):
    if app.currentPlayer == 1:
        tank = Piece("tank", 300, 100, 5, 200, row, col, 2, 1)
        player.buyPiece(tank)
    else:
        tank = Piece("etank", 300, 100, 5, 200, row, col, 2, 2)
        player.buyPiece(tank)

#USER INPUT FUNCTIONS
import math
def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

def keyPressed(app, event):
    if event.key == 'b':
        if app.currentPlayer == 1:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                buyResourceCollector(app, row, col, app.player1)
        if app.currentPlayer == 2:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                buyResourceCollector(app, row, col, app.player2)
    if event.key == 't':
        if app.currentPlayer == 1:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                buyTank(app, row, col, app.player1)
        if app.currentPlayer == 2:
            row, col = getTile(app, event)
            if isLegal(app, row, col):
                buyTank(app, row, col, app.player2)
    

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

def addMoney(app):
    for piece in app.player1.pieces:
        if piece.name == "collect":
            if (piece.row, piece.col) in app.reslocations:
                app.player1.gold += 100
    for piece in app.player2.pieces:
        if piece.name == "ecollect":
            if (piece.row, piece.col) in app.reslocations:
                app.player2.gold += 100
    pass

def mousePressed(app, event):
    row, col = getRowCol(app, event.x, event.y)
    #Ending the Turn
    if distance(event.x, event.y, app.nextturnx, app.nextturny) < app.buybtnr:
        app.moving, app.attacking = False, False
        app.pieceSelection = None
        addMoney(app)
        app.turns += 1
        app.currentPlayer = (app.turns % 2) + 1
        for piece in app.player1.pieces:
            piece.acted = False
        for piece in app.player2.pieces:
            piece.acted = False
    #move the piece
    elif app.moving:
        if app.pieceSelection.team == app.currentPlayer:
            if not app.pieceSelection.acted:
                if isLegal(app, row, col):
                    if not app.pieceSelection.mobility < gridDis(app.pieceSelection.row, app.pieceSelection.col, row, col):
                        movePiece(app, row, col, app.pieceSelection)
                        app.pieceSelection.acted = True
                        app.pieceSelection = None
                        app.moving, app.attacking = False, False
            else:
                app.moving, app.attacking = False, False
    #go to moving
    elif event.x > (app.width * 59/80) and event.x < (app.width * 68/80):
        if event.y > (app.height * 3/4) and event.y < (app.height * 75/80):
            app.moving = True
    #attack the piece
    elif app.attacking:
        if app.pieceSelection.team == app.currentPlayer:
            if not app.pieceSelection.acted:
                if not app.pieceSelection.range < gridDis(app.pieceSelection.row, app.pieceSelection.col, row, col):
                    attackPiece(app, row, col, app.pieceSelection)
                    app.pieceSelection.acted = True
                    app.pieceSelection = None
                    app.moving, app.attacking = False, False
            else:
                app.moving, app.attacking = False, False
    #go to attacking
    elif event.x > (app.width * 70/80) and event.x < (app.width * 79/80):
        if event.y > (app.height * 3/4) and event.y < (app.height * 75/80):
            app.attacking = True

    #Selecting a Piece
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
    return True

def movePiece(app, row, col, piece):
    if row < app.rows and col < app.cols:
        if row >= 0 and col >= 0:
            piece.move(row, col)

def gridDis(row1, col1, row2, col2):
    return abs(row1-row2) + abs(col1-col2)

def attackPiece(app, row, col, p):
    if p.team == 1:
        for enpiece in app.player2.pieces:
            if enpiece.row == row and enpiece.col == col:
                p.atc(enpiece)
                if enpiece.health <= 0:
                    app.player2.pieces.remove(enpiece)  
    else:
        for enpiece in app.player1.pieces:
            if enpiece.row == row and p.col == col:
                p.atc(enpiece)
                if enpiece.health <= 0:
                    app.player1.pieces.remove(enpiece)            
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
    if app.resboard[row][col] == 1:
        canvas.create_polygon(rx, ry, tx, ty, lx, ly, bx, by, fill = "turquoise", width = 3, outline = "black")
    else:
        canvas.create_polygon(rx, ry, tx, ty, lx, ly, bx, by, fill = "light goldenrod", width = 3, outline = "black")
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
    canvas.create_text(app.width/10, app.height/10, text = f"Current Player is : {app.currentPlayer}")
    canvas.create_text(app.width/10, app.height/8, text = f"Total Number of Turns: {app.turns}")
    if app.currentPlayer == 1:
        canvas.create_text(app.width/10, app.height/7, text = f"Player Gold: {app.player1.gold}")
        canvas.create_text(app.width/10, app.height/6, text = f"Player Base Health: {app.player1.base}")
    if app.currentPlayer == 2:
        canvas.create_text(app.width/10, app.height/7, text = f"Player Gold: {app.player2.gold}")
        canvas.create_text(app.width/10, app.height/6, text = f"Player Base Health: {app.player2.base}")
    

def drawPiece(app, canvas, row, col, name, player):
    x, y = getCellMidPoint(app, row, col)
    if player == 1:
        if name == "tank":
            canvas.create_image(x, (y - 10), image=ImageTk.PhotoImage(app.tank))
        elif name == "collect":
            canvas.create_image(x, (y-10), image=ImageTk.PhotoImage(app.collect))
    else:
        if name == "etank":
            canvas.create_image(x, (y - 10), image=ImageTk.PhotoImage(app.etank))
        elif name == "ecollect":
            canvas.create_image(x, (y-10), image=ImageTk.PhotoImage(app.ecollect))

def drawPieces(app, canvas):
    for piece in app.player1.pieces:
        drawPiece(app, canvas, piece.row, piece.col, piece.name, 1)
    for piece in app.player2.pieces:
        drawPiece(app, canvas, piece.row, piece.col, piece.name, 2)

def drawSelection(app, canvas):
     if app.pieceSelection != None:
        canvas.create_rectangle(app. width*60/80, app.height/40, app.width * 79/80, app.height / 4, fill = "light goldenrod")
        canvas.create_text(app.width * 5/6, app.height/10, text = f"Current Selection = {app.pieceSelection.name}")
        canvas.create_text(app.width * 5/6, app.height/8, text = f"Health: {app.pieceSelection.health}")
        canvas.create_text(app.width * 5/6, app.height/7, text = f"Range: {app.pieceSelection.range}")
        canvas.create_text(app.width * 5/6, app.height/6, text = f"Damage: {app.pieceSelection.attack}")
        canvas.create_text(app.width * 5/6, app.height/5, text = f"Acted: {app.pieceSelection.acted}")
        canvas.create_text(app.width * 5/6, app.height * 9/40, text = f"Mobility: {app.pieceSelection.mobility}")

def drawAttackBtn(app, canvas):
    if app.pieceSelection != None:
        if app.pieceSelection.team == app.currentPlayer:
            canvas.create_rectangle(app. width*70/80, app.height * 3/4, app.width * 79/80, app.height * 75/80, fill = "light goldenrod")
            canvas.create_rectangle(app. width*59/80, app.height * 3/4, app.width * 68/80, app.height * 75/80, fill = "light goldenrod")
            canvas.create_text(app.width * 75/80, app.height * 67/80, text = "attack")
            canvas.create_text(app.width * 64/80, app.height * 67/80, text = "move")

#REDRAWALL
def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    drawGameInfo(app, canvas)
    drawEndButton(app, canvas)
    drawSelection(app, canvas)
    drawAttackBtn(app, canvas)
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

