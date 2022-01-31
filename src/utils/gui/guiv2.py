#move gui here
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import time
import base64
import os
import math
import io
import uuid
from pathlib import Path

#a="global"
class Gui:
    #b="class variable in self"
    #class Gui
    #lastx, lasty = 0,0
    #img: Image
    #id=1
    events = []
    images = []
    texts = {}
    #objects = []
    lastx=1
    lasty=1
    kumi=False
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
        #print("guiv2 addlinefromclient")
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
    def image_to_byte_array(self, image:Image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image.format)
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr

    def addPhoto(self,photo):

        #global img
        #global images
        '''
        generate the path to the file relative to your python script:
        script_location = Path(__file__).absolute().parent
        file_location = script_location / 'file.yaml'
        file = file_location.open()
        '''
        #print(self.lastx)
        #with open(photo, "rb") as imag:
        
            #image_data_base64_encoded_string = base64.b64encode(imag.read()) 
        #imagestring = image_data_base64_encoded_string.decode('utf-8')
        #print()

       
        #
        #

        image = Image.open(photo)
        imagestring = base64.b64encode(self.image_to_byte_array(image)).decode('utf-8')
        img = ImageTk.PhotoImage(image)
        #img=PhotoImage(data=image_data_base64_encoded_string)
        #x2 = int() + self.lastx
        #y2 = int(img.height) + self.lasty
        print(img.height)
        x2=img.height() + self.lastx
        y2=img.width() + self.lasty
        #print("x2",x2)
        #print("Y2",y2)
        id = self.canvas.create_image(self.lastx, self.lasty,anchor=NW, image=img)
        #self.canvas.image= self.img
        self.images.append(img)
        #imagestring = base64.b64encode(image.read())
        #imagestring = imagestring.decode('utf-8')
        e={
            'id': id,
            'time': time.time(),
            'type': 'image',
            'x1': self.lastx,
            'y1': self.lasty,
            'x2': x2,
            'y2': y2,
            'image': imagestring
        }
        self.events.append(e)
        self.client.send(e)
        

    def addPhotoFromClient(self,rec_e:dict):
        #
        #global img
        #global images
        #print("clientphotoinput")
        img=PhotoImage(data=rec_e["image"].encode("utf8"))
        id = self.canvas.create_image(rec_e["x1"], rec_e["y1"],anchor=NW, image=img)
        self.images.append(img)
        e={
            'id': id,
            'time': time.time(),
            'type': 'image',
            'x1': rec_e["x1"],
            'y1': rec_e["y1"],
            'x2': rec_e["x2"],
            'y2': rec_e["y2"],
            'image': rec_e["image"]
        }
        self.events.append(e)
    def updateNote(self, event):
            #self.texts.append(txt)
            #note = self.canvas.itemcget(id).get("1.0",'end-1c')
            print(event)
            txt = event.widget
            e={
                'id': str(txt)[1:],
                'time': time.time(),
                'type': 'updateNote',
                'x1': self.lastx,
                'y1': self.lasty,
                'note': txt.get("1.0",'end-1c')
            }
            self.events.append(e)
            self.client.send(e)
            print("sent stufff",e)
    
    def addNote(self):
        #TODO add id and make text changing viewable from other clients
        
        
        
        
        note = ""
        id = str(uuid.uuid4())
        txt=Text(width=10, height=5, bd='10',bg="gray",name=id)
        
        #id = self.canvas.create_text(self.lastx, self.lasty,text=note)
        #self.canvas.itemcget(id).bind('<Enter>',updateNote)
        txt.place(x=self.lastx, y=self.lasty)
        #txt.tag_set("id",id)
        #self.canvas.itemcget(id).insert('1.0',note)
        txt.insert('1.0', note)
        self.texts[id]=txt
        #note = self.canvas.itemcget(id).get("1.0",'end-1c')
        e={
            'id': id,
            'time': time.time(),
            'type': 'note',
            'x1': self.lastx,
            'y1': self.lasty,
            'note': ""
        }
        self.events.append(e)
        self.client.send(e)
        txt.bind('<Return>',self.updateNote)

    def addNoteFromClient(self,rec_e:dict):
        id = rec_e["id"]
        txt=Text(width=10, height=5, bd='10',background="gray",name=id)
        txt.place(x=rec_e["x1"], y=rec_e["y1"])
        txt.insert('1.0', rec_e["note"])
        
        #self.texts.append(txt)
        #id = self.canvas.create_text(x=rec_e["x1"],y=rec_e["y1"],width=15, height=5, bd='10')
        #self.canvas.itemcget(id).insert('1.0',rec_e["note"])
        self.texts[id]=txt
        e={
            'id': id,
            'time': time.time(),
            'type': 'note',
            'x1': rec_e["x1"],
            'y1': rec_e["y1"],
            'note': rec_e["note"]
        }
        self.events.append(e)
        txt.bind('<Return>',self.updateNote)
        
    def updateNoteFromClient(self,e):
        #print("updfate",self.texts[e["id"]])
        print(e["id"])
        txt = self.texts[e["id"]]
        if txt:
            print("it works")
            txt.insert('1.0', e["note"])
        else:
            print("not work")
        

    def printLine(self):
        for event in self.events:
            print(event)
    def erase(self):
        print("test")
        if self.kumi:
            self.kumi=False
            self.canvas.bind("<B1-Motion>", self.addLine)
            self.btn.config(relief=RAISED)
        else:
            self.kumi=True
            #self.canvas.bind("<Button-1>", self.savePosn)
            self.canvas.bind("<B1-Motion>", self.delete)
            self.btn.config(relief=SUNKEN)
        print(self.kumi)
    
    #def distance(x0,x1,x2,y0,y1,y2):
        #return abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/math.sqrt((x2-x1)**2 + (y2 -y1)**2)
    def dist(self, x1, y1, x2, y2, x3, y3): # x3,y3 is the point
        px = x2-x1
        py = y2-y1

        norm = px*px + py*py
        if norm==0:
            norm = 1

        u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        x = x1 + u * px
        y = y1 + u * py

        dx = x - x3
        dy = y - y3

        # Note: If the actual distance does not matter,
        # if you only want to compare what this function
        # returns to other results of this function, you
        # can just return the squared distance instead
        # (i.e. remove the sqrt) to gain a little performance

        dist = (dx*dx + dy*dy)**.5

        return dist

    def FindPoint(self,x1, y1, x2, y2, x, y):
        #print(x1,y1,x2,y2,x,y)
        if (x > x1 and x < x2 and
            y > y1 and y < y2) :
            return True
        else :
            return False
    def deleteFromServer(self,id):
        e={
            'id': id,
            'type': 'delete'
        }
        self.client.send(e)

    def deleteFromClient(self,e):
        self.canvas.delete(e["id"])
        i=0
        while i<len(self.events):
            if self.events[i]["id"]==e["id"]:
                #del self.events[e["id"]]
                del self.events[i]
                #break
            i+=1
    def delete(self,event):
        for a in self.events:
            if a["type"]=="line":
                #print(event.x, a["x1"],a["x2"],event.y,a["y1"],a["y2"])
                x0 = event.x
                y0 = event.y
                x1 = a["x1"]
                x2 = a["x2"]
                y1 = a["y1"]
                y2 = a["y2"]
                #dist = self.distance(event.x, a["x1"],a["x2"],event.y,a["y1"],a["y2"])
                #doesn't work for a finite line segment:
                #dist = (abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1)))/(math.sqrt((x2-x1)**2 + (y2 -y1)**2))
                
                #let's create an imaginary box i...

                #actually lets use code from the internet:
                dist = self.dist(x1,y1,x2,y2,x0,y0)
              
                
                #print(dist)
                if dist < 10:
                    self.deleteFromServer(a["id"])
                    self.canvas.delete(a["id"])
                    #del self.events[a["id"]]
                    i=0
                    while i<len(self.events):
                        if self.events[i]["id"]==a["id"]:
                            #del self.events[e["id"]]
                            del self.events[i]
                            #break
                        i+=1

            elif a["type"]=="image":
                #print("delete image?")
                x0=event.x
                y0=event.y
                x1 = a["x1"]
                x2 = a["x2"]
                y1 = a["y1"]
                y2 = a["y2"]
                if self.FindPoint(x1,y1,x2,y2,x0,y0):
                    self.deleteFromServer(a["id"])
                    self.canvas.delete(a["id"])
                    #del self.events[a["id"]]
                    i=0
                    while i<len(self.events):
                        if self.events[i]["id"]==a["id"]:
                            #del self.events[e["id"]]
                            del self.events[i]
                            #break
                        i+=1
                    #print("image deleted")
            #TODO add delete note

    def undo(self):
        print("undo")
        #reverse the previous action
                

    def run(self):
        
        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #clientv1.connect()#TODO: move to main client_main

        self.canvas = Canvas(root, background="white")
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        
        self.canvas.bind("<Button-1>", self.savePosn)
        self.canvas.bind("<B1-Motion>", self.addLine)

        #print(self.kumi)

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
             height=5, bd='10', command= lambda: self.addPhoto("photo.gif"))
        btn.place(x=0, y=110)
        txt = Text(root, width=10, height=5, bd='10')
        txt.place(x=105, y=210)
        btn = Button(root, text='show gif:', width=10,
             height=5, bd='10', command= lambda: self.addPhoto(txt.get("1.0",'end-1c')))
        btn.place(x=0, y=210)
        #txt2 = Text(root, width=10, height=5, bd='10')
        #txt.place(x=105, y=300)
        btn = Button(root, text='sticky note:', width=10,
             height=5, bd='10', command= lambda: self.addNote())
        btn.place(x=0, y=300)
        self.btn = Button(root, text="Erase", width=5,
            height=2, bd='10', command= lambda: self.erase())
        self.btn.place(x=65, y=0)
        #self.addLineFromClient()
        btn = Button(root, text='undo', width=10,
             height=5, bd='10', command= lambda: self.undo())
        #self.btn.place(x=65, y=0)

        
        root.mainloop()