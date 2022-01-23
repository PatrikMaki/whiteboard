#move gui here
from tkinter import *
from tkinter import ttk
import time

#a="global"
class Gui:
    #b="class variable in self"
    #class Gui
    events = []
    def set_client(self,client):
        self.client = client

    def savePosn(self,event):
        #global lastx, lasty
        self.lastx, self.lasty = event.x, event.y

    color = "black"
    def setColor(self,newcolor):
        #global color
        self.color = newcolor

    def addLine(self,event):
        #global lastx, lasty
        id = self.canvas.create_line((self.lastx, self.lasty, event.x, event.y), fill=self.color)
        #print("first print",id,lastx, lasty, event.x, event.y)
        e={
            'id': id,
            'time': time.time(),
            'type': 'line',
            'x1': self.lastx,
            'y1': self.lasty,
            'x2': event.x,
            'y2': event.y
        }
        #global events
        self.events.append(e)
        self.lastx, self.lasty = event.x, event.y
        self.client.send(e) #TODO: call from client_main DONE
        #print("print line",id,lastx, lasty, event.x, event.y)
    

    def printLine(self):
        for event in self.events:
            print(event)

    def run(self):

        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #clientv1.connect()#TODO: move to main client_main

        self.canvas = Canvas(root, background="white")
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas.bind("<Button-1>", self.savePosn)
        self.canvas.bind("<B1-Motion>", self.addLine)



        '''
        id = canvas.create_rectangle((10, 10, 30, 30), fill="red")
        canvas.tag_bind(id, "<Button-1>", lambda x: setColor("red"))
        id = canvas.create_rectangle((10, 35, 30, 55), fill="green")
        canvas.tag_bind(id, "<Button-1>", lambda x: setColor("green"))
        id = canvas.create_rectangle((10, 60, 30, 80), fill="blue")
        canvas.tag_bind(id, "<Button-1>", lambda x: setColor("blue"))
        '''
        id = self.canvas.create_rectangle((10, 80, 50, 120), fill="white")
        self.canvas.tag_bind(id, "<Button-1>", lambda y: self.printLine())

        root.mainloop()