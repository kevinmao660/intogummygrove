from cmu_112_graphics import *

def redrawAll(app, canvas):
    # The first four parameters are the upper-left (x,y)
    # and the lower-right (x,y) of the rectangle
    canvas.create_rectangle(0, 0, 150, 150, fill='black')

runApp(width=400, height=200)