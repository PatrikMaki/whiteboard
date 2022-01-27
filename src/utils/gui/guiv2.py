#move gui here
from tkinter import *
from tkinter import ttk
#from PIL import ImageTk,Image does not work?
import time
import base64
import os
from pathlib import Path

#a="global"
class Gui:
    #b="class variable in self"
    #class Gui
    #lastx, lasty = 0,0
    #img: Image
    events = []
    images = []
    lastx=1
    lasty=1
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
    
    def addLineFromClient(self,rec_e:dict):
        print("guiv2 addlinefromclient")
        #e: dict = self.client.receive()
        id = self.canvas.create_line((rec_e["x1"], rec_e["y1"], rec_e["x2"], rec_e["y2"]), fill="blue")
        e={
            'id': id,
            'time': time.time(),
            'type': 'line',
            'x1': rec_e["x1"],
            'y1': rec_e["y1"],
            'x2': rec_e["x2"],
            'y2': rec_e["y2"]
        }
        self.events.append(e)
    
    #addphoto
    def addPhoto(self,photo):
        #global img
        #global images
        '''
        generate the path to the file relative to your python script:
        script_location = Path(__file__).absolute().parent
        file_location = script_location / 'file.yaml'
        file = file_location.open()
        '''
        print(self.lastx)
        with open(photo, "rb") as image:
            image_data_base64_encoded_string = base64.b64encode(image.read()) 
        imagestring = image_data_base64_encoded_string.decode('utf-8')
        print()
        img=PhotoImage(data=image_data_base64_encoded_string)
        id = self.canvas.create_image(self.lastx, self.lasty,anchor=NW, image=img)
        #self.canvas.image= self.img
        self.images.append(img)
        e={
            'id': id,
            'time': time.time(),
            'type': 'image',
            'x1': self.lastx,
            'y1': self.lasty,
            'image': imagestring
        }
        self.events.append(e)
        self.client.send(e)
        

    def addPhotoFromClient(self,rec_e:dict):
        #
        #global img
        #global images
        print("clientphotoinput")
        img=PhotoImage(data=rec_e["image"].encode("utf8"))
        id = self.canvas.create_image(rec_e["x1"], rec_e["y1"],anchor=NW, image=img)
        self.images.append(img)
        e={
            'id': id,
            'time': time.time(),
            'type': 'image',
            'x1': rec_e["x1"],
            'y1': rec_e["y1"],
            'image': rec_e["image"]
        }
        self.events.append(e)

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
        #id = self.canvas.create_rectangle((10, 80, 50, 120), fill="black")
        #self.canvas.tag_bind(id, "<Button-1>", lambda y: self.printLine())

        btn = Button(root, text='QUIT!', width=5,
             height=2, bd='10', command=root.destroy)
        btn.place(x=0, y=0)
        btn = Button(root, text='print', width=5,
             height=2, bd='10', command= lambda: self.printLine())
        btn.place(x=0, y=55)
        btn = Button(root, text='show gif', width=10,
             height=5, bd='10', command= lambda: self.addPhoto("red.gif"))
        btn.place(x=0, y=110)
        txt = Text(root, width=10, height=5, bd='10')
        txt.place(x=105, y=210)
        btn = Button(root, text='show gif:', width=10,
             height=5, bd='10', command= lambda: self.addPhoto(txt.get("1.0",'end-1c')))
        btn.place(x=0, y=210)
        #self.addLineFromClient()

        root.mainloop()