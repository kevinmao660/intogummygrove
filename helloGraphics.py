# helloGraphics.py VERSION 2.0

from cmu_112_graphics import *

def redrawAll(app, canvas):
    canvas.create_rectangle(60, 60, app.width-60, app.height-60)
    canvas.create_text(app.width/2, app.height/2,
        text='Hello, World!\n>>(o   w   o)<<')
        
runApp(width=400, height=200)

