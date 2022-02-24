from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import time
import base64
import os
import math
import io
import uuid
from pathlib import Path
from pyscreenshot import grab


# a="global"
class Gui:
    # b="class variable in self"
    # class Gui
    # lastx, lasty = 0,0
    # img: Image
    # id=1
    imagename = "photo.gif"
    events = []
    images = []
    texts = {}
    # objects = []
    lastx = 1
    lasty = 1
    kumi = False
    comm = False
    comment_frame_height = 115
    comment_frame_width = 93

    def set_client(self, client):
        self.client = client

    def savePosn(self, event):
        # global lastx, lasty
        self.lastx, self.lasty = event.x, event.y

    color = "black"

    def setColor(self, newcolor):
        # global color
        self.color = newcolor

    def addLine(self, event):
        # global lastx, lasty
        id = self.canvas.create_line((self.lastx, self.lasty, event.x, event.y), fill=self.color)
        # print("first print",id,lastx, lasty, event.x, event.y)
        e = {
            'id': id,
            'time': time.time(),
            'type': 'line',
            'x1': self.lastx,
            'y1': self.lasty,
            'x2': event.x,
            'y2': event.y,
            'origin': 'you'
        }
        # global events
        self.events.append(e)
        self.lastx, self.lasty = event.x, event.y
        self.client.send(e)  # TODO: call from client_main DONE
        # print("print line",id,lastx, lasty, event.x, event.y)

    def addLineFromClient(self, rec_e: dict):
        # print("guiv2 addlinefromclient")
        # e: dict = self.client.receive()
        id = self.canvas.create_line((rec_e["x1"], rec_e["y1"], rec_e["x2"], rec_e["y2"]), fill="blue")
        e = {
            'id': id,
            'time': time.time(),
            'type': 'line',
            'x1': rec_e["x1"],
            'y1': rec_e["y1"],
            'x2': rec_e["x2"],
            'y2': rec_e["y2"],
            'origin': 'other'
        }
        self.events.append(e)

    # addphoto
    def image_to_byte_array(self, image: Image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image.format)
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr

    def chooseImage(self):
        # filetypes = [("jpeg files","*.jpg"),("all files","*.*"),("png files","*.png"),("all files","*.*")]
        self.imagename = filedialog.askopenfilename(initialdir="/", title="Select file")

    def addPhoto(self):

        # global img
        # global images
        '''
        generate the path to the file relative to your python script:
        script_location = Path(__file__).absolute().parent
        file_location = script_location / 'file.yaml'
        file = file_location.open()
        '''
        # print(self.lastx)
        # with open(photo, "rb") as imag:

        # image_data_base64_encoded_string = base64.b64encode(imag.read())
        # imagestring = image_data_base64_encoded_string.decode('utf-8')
        # print()

        #
        #

        image = Image.open(self.imagename)
        imagestring = base64.b64encode(self.image_to_byte_array(image)).decode('utf-8')
        img = ImageTk.PhotoImage(image)
        # img=PhotoImage(data=image_data_base64_encoded_string)
        # x2 = int() + self.lastx
        # y2 = int(img.height) + self.lasty
        print(img.height)
        x2 = img.height() + self.lastx
        y2 = img.width() + self.lasty
        # print("x2",x2)
        # print("Y2",y2)
        id = self.canvas.create_image(self.lastx, self.lasty, anchor=NW, image=img)
        # self.canvas.image= self.img
        self.images.append(img)
        # imagestring = base64.b64encode(image.read())
        # imagestring = imagestring.decode('utf-8')
        e = {
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

    def addPhotoFromClient(self, rec_e: dict):
        #
        # global img
        # global images
        # print("clientphotoinput")
        img = PhotoImage(data=rec_e["image"].encode("utf8"))
        id = self.canvas.create_image(rec_e["x1"], rec_e["y1"], anchor=NW, image=img)
        self.images.append(img)
        e = {
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
        # self.texts.append(txt)
        # note = self.canvas.itemcget(id).get("1.0",'end-1c')
        print(event)
        txt = event.widget
        e = {
            'id': str(txt).split(".")[3],
            'time': time.time(),
            'type': 'updateNote',
            'x1': self.lastx,
            'y1': self.lasty,
            'note': txt.get("1.0", 'end-1c')
        }
        self.events.append(e)
        self.client.send(e)
        print("sent stufff", e)

    def addNote(self):
        # TODO add id and make text changing viewable from other clients
        note = ""
        id = str(uuid.uuid4())
        frame_id = str(uuid.uuid4())
        frame = Frame(self.canvas, relief=RIDGE, width=110, height=150, bg="gray", name=frame_id)
        frame.place(x=self.lastx, y=self.lasty)
        txt = Text(frame, width=10, height=5, bd='10', bg="gray", name=id)
        closebutton = Button(frame, width=1, height=1, bd="0", text="X", command=lambda: self.deleteNote(id, frame_id))
        closebutton.grid(row=0, column=0, sticky="ne")
        movebutton = Button(frame, text="Move", width=2, height=1, bd="0", command=lambda: self.moveNote(id, frame_id))
        movebutton.grid(row=0, column=0, sticky="nw")

        # id = self.canvas.create_text(self.lastx, self.lasty,text=note)
        # self.canvas.itemcget(id).bind('<Enter>',updateNote)
        txt.grid(row=1, column=0)
        # txt.tag_set("id",id)
        # self.canvas.itemcget(id).insert('1.0',note)
        txt.insert('1.0', note)
        self.texts[id] = txt
        # note = self.canvas.itemcget(id).get("1.0",'end-1c')
        e = {
            'id': id,
            'time': time.time(),
            'type': 'note',
            'x1': self.lastx,
            'y1': self.lasty,
            'note': "",
            'frame_id': frame_id
        }
        #print(e)
        self.events.append(e)
        self.client.send(e)
        txt.bind('<Return>', self.updateNote)

    # TODO remove old commented-out code
    def addNoteFromClient(self, rec_e: dict):
        id = rec_e["id"]
        frame_id = rec_e["frame_id"]
        frame = Frame(self.canvas, relief=RIDGE, width=110, height=150, bg="gray", name=frame_id)
        frame.place(x=rec_e["x1"], y=rec_e["y1"])
        txt = Text(frame, width=10, height=5, bd='10', bg="gray", name=id)
        txt.insert('1.0', rec_e["note"])
        closebutton = Button(frame, width=1, height=1, bd="0", text="X", command=lambda: self.deleteNote(id, frame_id))
        closebutton.grid(row=0, column=0, sticky="ne")
        movebutton = Button(frame, text="Move", width=2, height=1, bd="0", command=lambda: self.moveNote(id, frame_id))
        movebutton.grid(row=0, column=0, sticky="nw")

        # id = self.canvas.create_text(self.lastx, self.lasty,text=note)
        # self.canvas.itemcget(id).bind('<Enter>',updateNote)
        txt.grid(row=1, column=0)

        # self.texts.append(txt)
        # id = self.canvas.create_text(x=rec_e["x1"],y=rec_e["y1"],width=15, height=5, bd='10')
        # self.canvas.itemcget(id).insert('1.0',rec_e["note"])
        self.texts[id] = txt
        e = {
            'id': id,
            'time': time.time(),
            'type': 'note',
            'x1': rec_e["x1"],
            'y1': rec_e["y1"],
            'note': rec_e["note"],
            'frame_id': frame_id
        }
        self.events.append(e)
        txt.bind('<Return>', self.updateNote)

    # does not change the coordinates of the note in events
    # id is actually needed in involving moving
    # may want to use it if undo needs to move notes
    def moveNote(self, id, frame_id):
        print("moving")
        toggle_kumi = False
        toggle_comment = False
        if self.kumi:
            self.kumi = True
            self.erase()
            toggle_kumi = True
        elif self.comm:
            self.comm = True
            self.addCommentToggle()
            toggle_comment = True

        self.canvas.bind("<B1-Motion>", self.nothing)
        self.canvas.bind("<Button-1>",
                         lambda event, tx_id=id, fr_id=frame_id, tg_kumi=toggle_kumi, tg_comment=toggle_comment:
                         self.getCoordsAndMove(event, tx_id, fr_id, tg_kumi, tg_comment))

    def getCoordsAndMove(self, e, id, frame_id, toggle_kumi, toggle_comment):
        print("moving note to:", e.x, e.y)
        frame = self.canvas.nametowidget(frame_id)
        frame.place(x=e.x, y=e.y)
        if toggle_kumi:
            self.erase()
        elif toggle_comment:
            self.addCommentToggle()
        else:
            self.canvas.bind("<B1-Motion>", self.addLine)
            self.canvas.bind("<Button-1>", self.savePosn)
        self.moveNoteFromServer(id, frame_id, e.x, e.y)

    # send event to server
    def moveNoteFromServer(self, id, frame_id, x, y):
        e = {
            'id': id,
            'frame_id': frame_id,
            'type': 'moveNote',
            'x': x,
            'y': y
        }
        self.events.append(e)
        self.client.send(e)

    # get event from server
    def moveNoteComingFromServer(self, e):
        self.events.append(e)
        frame_id = e["frame_id"]
        x = e["x"]
        y = e["y"]
        frame = self.canvas.nametowidget(frame_id)
        frame.place(x=x, y=y)

    def updateNoteFromClient(self, e):
        self.events.append(e)
        print(e["id"])
        txt = self.texts[e["id"]]
        if txt:
            print("it works")
            txt.delete('1.0', 'end-1c')
            txt.insert('1.0', e["note"])
        else:
            print("not work")

    # coming from this client
    def deleteNote(self, delete_id, delete_frame_id):
        self.deleteNoteFromServer(delete_id, delete_frame_id)
        print("deleting", delete_id)
        delete_frame = self.canvas.nametowidget(delete_frame_id)
        delete_frame.grid_forget()
        delete_frame.destroy()

    # coming from this client
    def deleteNoteFromServer(self, delete_id, delete_frame_id):
        e = {
            'id': delete_id,
            'frame_id': delete_frame_id,
            'type': 'deleteNote'
        }
        self.events.append(e)
        self.client.send(e)

    # coming from another client -> server
    def deleteNoteComingFromServer(self, e):
        self.events.append(e)
        delete_id = e["id"]
        delete_frame_id = e["frame_id"]
        print("deleting", delete_id)
        # below code removes all events with id=delete_id
        # = all events involving the note
        # does not make a difference really
        # if used, include in deleteNote as well
        """delete_index = []
        for i, note in enumerate(self.events):
            if note["id"] == delete_id:
                self.canvas.delete(note["id"])
                delete_index.append(i)
        for j in reversed(delete_index):
            del self.events[j]"""
        # --------------------
        delete_frame = self.canvas.nametowidget(delete_frame_id)
        delete_frame.grid_forget()
        delete_frame.destroy()


    def printLine(self):
        print("\nEvents:")
        for event in self.events:
            #if event["type"] != "line":
             print(event)
        print("\n")

    def erase(self):
        print("test")
        if self.kumi:
            self.kumi = False
            self.canvas.bind("<B1-Motion>", self.addLine)
            self.erase_btn.config(relief=RAISED)
        else:
            self.kumi = True
            self.comm = True
            self.addCommentToggle()
            # self.canvas.bind("<Button-1>", self.savePosn)
            self.canvas.bind("<B1-Motion>", self.delete)
            self.erase_btn.config(relief=SUNKEN)
        print(self.kumi)

    # def distance(x0,x1,x2,y0,y1,y2):
    # return abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/math.sqrt((x2-x1)**2 + (y2 -y1)**2)
    def dist(self, x1, y1, x2, y2, x3, y3):  # x3,y3 is the point
        px = x2 - x1
        py = y2 - y1

        norm = px * px + py * py
        if norm == 0:
            norm = 1

        u = ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

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

        dist = (dx * dx + dy * dy) ** .5

        return dist

    def FindPoint(self, x1, y1, x2, y2, x, y):
        # print(x1,y1,x2,y2,x,y)
        if (x > x1 and x < x2 and
                y > y1 and y < y2):
            return True
        else:
            return False

    def deleteFromServer(self, id):
        e = {
            'id': id,
            'type': 'delete'
        }
        self.client.send(e)

    def deleteFromClient(self, e):
        self.canvas.delete(e["id"])
        i = 0
        while i < len(self.events):
            if self.events[i]["id"] == e["id"]:
                # del self.events[e["id"]]
                del self.events[i]
                # break
            i += 1

    def delete(self, event):  # TODO: rename to erase
        for a in self.events:
            if a["type"] == "line":
                # print(event.x, a["x1"],a["x2"],event.y,a["y1"],a["y2"])
                x0 = event.x
                y0 = event.y
                x1 = a["x1"]
                x2 = a["x2"]
                y1 = a["y1"]
                y2 = a["y2"]
                # dist = self.distance(event.x, a["x1"],a["x2"],event.y,a["y1"],a["y2"])
                # doesn't work for a finite line segment:
                # dist = (abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1)))/(math.sqrt((x2-x1)**2 + (y2 -y1)**2))

                # let's create an imaginary box i...

                # actually lets use code from the internet:
                dist = self.dist(x1, y1, x2, y2, x0, y0)

                # print(dist)
                if dist < 10:
                    self.deleteFromServer(a["id"])
                    self.canvas.delete(a["id"])
                    # del self.events[a["id"]]
                    i = 0
                    while i < len(self.events):
                        if self.events[i]["id"] == a["id"]:
                            # del self.events[e["id"]]
                            del self.events[i]
                            # break
                        i += 1
            '''
            elif a["type"]=="image": #TODO: erase should not delete images
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
            '''
            # TODO add delete note

    # affects lines only
    def undo(self):
        # how many "line" events should be removed
        # 30-ish seems to be optimal
        remove_amount = 30
        j = 0

        for e in reversed(self.events):
            if j > remove_amount:
                break
            if e["type"] == "line":
                if e["origin"] == "you":
                    self.deleteFromServer(e["id"])
                    self.canvas.delete(e["id"])
                    i = 0
                    while i < len(self.events):
                        if self.events[i]["id"] == e["id"]:
                            del self.events[i]
                        i += 1
                    j += 1

    def savePng(self):
        # takes a screenshot of the tkinter window
        # TODO: better place to save screenshot?
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        # print(x, y, w, h)
        ss = grab(bbox=(x, y, w + x, h + y))
        ss.show()
        ss.save("./../whiteboard.png")

    def saveJpeg(self):
        # takes a screenshot of the tkinter window
        # TODO: better place to save screenshot?
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        # print(x, y, w, h)
        ss = grab(bbox=(x, y, w + x, h + y))
        ss.show()
        ss.save("./../whiteboard.jpeg")

    def addCommentToggle(self):
        if self.comm:
            self.comm = False
            self.canvas.bind("<B1-Motion>", self.addLine)
            self.canvas.bind("<Button-1>", self.savePosn)
            self.comment_btn.config(relief=RAISED)
            print("binded addline")

        else:
            self.comm = True
            self.kumi = True
            self.erase()
            self.canvas.bind("<Button-1>", self.addCommentbox)
            self.canvas.bind("<B1-Motion>", self.nothing)
            self.comment_btn.config(relief=SUNKEN)
            print("binded to addcomment, unbound motion")

    # used for binding a button to nothing
    def nothing(self, event):
        pass

    def addCommentbox(self, event):
        # TODO add globals for widths and heights etc..
        x0 = event.x
        y0 = event.y
        stop = False

        for a in self.events:
            if a["type"] == "image":
                x1 = a["x1"]
                x2 = a["x2"]
                y1 = a["y1"]
                y2 = a["y2"]

                dist = self.dist(x1, y1, x2, y2, x0, y0)
                if dist < 30:
                    print("image found")

                    c_x0 = x2
                    c_y0 = y2
                    for c in self.events:
                        if c["type"] == "commentbox":
                            c_x1 = c["x1"]
                            c_x2 = c["x2"]
                            c_y1 = c["y1"]
                            c_y2 = c["y2"]

                            dist = self.dist(c_x1, c_y1, c_x2, c_y2, c_x0, c_y0)
                            # dist should be 0 if there is a commentbox already
                            if dist < 10:
                                print("another commentbox found")
                                print(c_x1, c_y1, c_x2, c_y2)
                                self.addChildComment(c_x1)
                                stop = True
                                break
                    if stop:
                        break
                    comment = ""
                    id = str(uuid.uuid4())
                    # width and height are different units in frames and other boxes...
                    frame = Frame(self.canvas, relief=RIDGE, width=self.comment_frame_width,
                                  height=self.comment_frame_height, bg="gray")
                    frame.place(x=x2, y=y2)
                    txt = Text(frame, width=10, height=5, bd='4', bg="white", name=id)
                    label = Label(frame, text="By you")
                    label.place(x=0, y=0)
                    txt.place(x=0, y=20)

                    txt.insert('1.0', comment)
                    self.texts[id] = txt

                    e = {
                        'id': id,
                        'time': time.time(),
                        'type': 'commentbox',
                        'x1': x2,
                        'y1': y2,
                        'x2': x2 + self.comment_frame_width,
                        'y2': y2 + self.comment_frame_height,
                        'comment': ""
                    }
                    print(e)
                    self.events.append(e)
                    self.client.send(e)
                    txt.bind('<Return>', self.updateComment)
                    break

    def addChildComment(self, x0):
        comments = []
        for c in self.events:
            if c["type"] == "commentbox":
                if c["x1"] == x0:
                    comments.append(c)
        y0 = 0
        for c in comments:
            if c["y2"] > y0:
                y0 = c["y2"]

        comment = ""
        id = str(uuid.uuid4())
        # width and height are different units in frames and other boxes...
        frame = Frame(self.canvas, relief=RIDGE, width=self.comment_frame_width, height=self.comment_frame_height,
                      bg="gray")
        frame.place(x=x0, y=y0)
        txt = Text(frame, width=10, height=5, bd='4', bg="white", name=id)
        label = Label(frame, text="By you")
        label.place(x=0, y=0)
        txt.place(x=0, y=20)

        txt.insert('1.0', comment)
        self.texts[id] = txt

        e = {
            'id': id,
            'time': time.time(),
            'type': 'commentbox',
            'x1': x0,
            'y1': y0,
            'x2': x0 + self.comment_frame_width,
            'y2': y0 + self.comment_frame_height,
            'comment': ""
        }
        # print(e)
        self.events.append(e)
        self.client.send(e)
        txt.bind('<Return>', self.updateComment)

    def updateComment(self, event):
        txt = event.widget
        e = {
            'id': str(txt).split(".")[3],
            'time': time.time(),
            'type': 'updateComment',
            'x1': event.x,
            'y1': event.y,
            'comment': txt.get("1.0", 'end-1c')
        }
        self.events.append(e)
        self.client.send(e)
        # print("sent stufff", e)

    def addCommentboxFromClient(self, rec_e: dict):
        id = rec_e["id"]

        frame = Frame(self.canvas, relief=RIDGE, width=self.comment_frame_width, height=self.comment_frame_height,
                      bg="gray")
        frame.place(x=rec_e["x1"], y=rec_e["y1"])
        txt = Text(frame, width=10, height=5, bd='4', bg="white", name=id)
        address = str(rec_e["address"][1])
        label = Label(frame, text="By " + address)
        # TODO: use grid for placement
        label.place(x=0, y=0)
        txt.place(x=0, y=20)

        txt.insert('1.0', rec_e["comment"])

        self.texts[id] = txt
        e = {
            'id': id,
            'time': time.time(),
            'type': 'commentbox',
            'x1': rec_e["x1"],
            'y1': rec_e["y1"],
            'x2': rec_e["x2"],
            'y2': rec_e["y2"],
            'comment': rec_e["comment"]
        }
        self.events.append(e)
        txt.bind('<Return>', self.updateComment)

    def updateCommentFromClient(self, e):
        # print(e)
        # print("update", self.texts[e["id"]])

        txt = self.texts[e["id"]]
        if txt:
            # print("it works")
            txt.delete('1.0', 'end-1c')
            txt.insert('1.0', e["comment"])
        else:
            # print("not work")
            pass

    def run(self):
        # TODO: make possible to work over internet.
        # TODO: create session!
        # TODO: invite session
        # TODO: request to join session
        # TODO: join session
        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # clientv1.connect()#TODO: move to main client_main

        self.canvas = Canvas(root, background="white")
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))

        self.canvas.bind("<Button-1>", self.savePosn)
        self.canvas.bind("<B1-Motion>", self.addLine)

        # print(self.kumi)

        '''
        id = canvas.create_rectangle((10, 10, 30, 30), fill="red")
        canvas.tag_bind(id, "<Button-1>", lambda x: setColor("red"))
        id = canvas.create_rectangle((10, 35, 30, 55), fill="green")
        canvas.tag_bind(id, "<Button-1>", lambda x: setColor("green"))
        id = canvas.create_rectangle((10, 60, 30, 80), fill="blue")
        canvas.tag_bind(id, "<Button-1>", lambda x: setColor("blue"))
        '''
        # id = self.canvas.create_rectangle((10, 80, 50, 120), fill="black")
        # self.canvas.tag_bind(id, "<Button-1>", lambda y: self.printLine())
        # TODO: make button placement look nice
        btn = Button(root, text='QUIT!', width=5,
                     height=2, bd='10', command=root.destroy)
        btn.place(x=0, y=0)
        btn = Button(root, text='print', width=5,
                     height=2, bd='10', command=lambda: self.printLine())
        btn.place(x=0, y=55)
        btn = Button(root, text='show image', width=10,
                     height=5, bd='10', command=lambda: self.addPhoto())
        btn.place(x=0, y=110)
        btn = Button(root, text='choose image', width=10,
                     height=5, bd='10', command=lambda: self.chooseImage())
        btn.place(x=0, y=210)
        # txt2 = Text(root, width=10, height=5, bd='10')
        # txt.place(x=105, y=300)
        btn = Button(root, text='sticky note:', width=10,
                     height=5, bd='10', command=lambda: self.addNote())
        btn.place(x=0, y=300)
        self.erase_btn = Button(root, text="Erase", width=5,
                                height=2, bd='10', command=lambda: self.erase())
        self.erase_btn.place(x=65, y=0)
        # self.addLineFromClient()
        btn = Button(root, text='undo', width=5,
                     height=2, bd='10', command=lambda: self.undo())
        btn.place(x=65, y=55)
        # save PNG
        self.btn = Button(root, text="save PNG", width=10,
                          height=2, bd='10', command=lambda: self.savePng())
        self.btn.place(x=0, y=400)
        # save JPEG
        self.btn = Button(root, text="save JPEG", width=10,
                          height=2, bd='10', command=lambda: self.saveJpeg())
        self.btn.place(x=0, y=465)
        self.comment_btn = Button(root, text="add comment", width=10,
                                  height=2, bd='10', command=lambda: self.addCommentToggle())
        self.comment_btn.place(x=0, y=525)

        root.mainloop()
