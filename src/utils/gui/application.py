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
#allow any user to create a new session and invite others to join the session. The user who has
#created the session would serve as the host and can accept or decline the requests for joining
#the session. The session would end when the host leaves or ends the session.
class Application:
     events = []
     def run(self):
          #TODO: make possible to work over internet.
          #TODO: create session!
          #TODO: invite session
          #TODO: request to join session
          #TODO: join session
          #TODO: create gui using frames!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          root = Tk()
          root.columnconfigure(0, weight=1)
          root.rowconfigure(0, weight=1)

          #clientv1.connect()#TODO: move to main client_main

          self.canvas = Canvas(root, background="white")
          self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
          
          #self.canvas.bind("<Button-1>", self.savePosn)
          #self.canvas.bind("<B1-Motion>", self.addLine)

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
          btn = Button(root, text='QUIT!', width=5,
             height=2, bd='10', command=root.destroy)
          btn.place(x=0, y=55)

          root.mainloop()
A = Application()
A.run()