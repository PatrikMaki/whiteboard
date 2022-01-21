from tkinter import *
from tkinter import ttk
import time
#old

events = []
def savePosn(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

color = "black"
def setColor(newcolor):
    global color
    color = newcolor

def addLine(event):
    global lastx, lasty
    id = canvas.create_line((lastx, lasty, event.x, event.y), fill=color)
    print("first print",id,lastx, lasty, event.x, event.y)
    e={
        'id': id,
        'time': time.time(),
        'type': 'line',
        'x1': lastx,
        'y1': lasty,
        'x2': event.x,
        'y2': event.y
    }
    events.append(e)
    lastx, lasty = event.x, event.y
    #print("print line",id,lastx, lasty, event.x, event.y)
    

def printLine():
    for event in events:
        print(event)

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", savePosn)
canvas.bind("<B1-Motion>", addLine)



'''
id = canvas.create_rectangle((10, 10, 30, 30), fill="red")
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("red"))
id = canvas.create_rectangle((10, 35, 30, 55), fill="green")
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("green"))
id = canvas.create_rectangle((10, 60, 30, 80), fill="blue")
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("blue"))
'''
id = canvas.create_rectangle((10, 80, 50, 120), fill="white")
canvas.tag_bind(id, "<Button-1>", lambda y: printLine())

root.mainloop()