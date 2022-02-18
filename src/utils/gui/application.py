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
       def addSession(self):
            
            #new
            #add a new dict as a session
            #add the dict to events
            #
            #new
            #print("ii")
            rows = 9
            columns = 5
            buttons = [[Button() for j in range(columns)] for i in range(rows)]
            for i in range(0, rows):
               for j in range(0, columns):
                  buttons[i][j] = Button(self.frame_buttons, text=("%d,%d" % (i+1, j+1)))
                  buttons[i][j].grid(row=i, column=j, sticky='news')

            # Update buttons frames idle tasks to let tkinter calculate buttons sizes
            self.frame_buttons.update_idletasks()

            # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
            first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
            first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
            self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                              height=first5rows_height)

            # Set the canvas scrolling region
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
       def inviteToSession(self):
              print("invite")
              
       def requestToJoin(self):
              print("a")
              
       def accept(self):
              print("accept")
              
       def decline(self):
              print("decline")
             
         
         
         
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
               self.frame_main = Frame(root, bg="gray")
               self.frame_main.grid(sticky='news')
               self.btn = Button(self.frame_main, text='QUIT!', width=5,
                  height=2, bd='10', command=root.destroy)
               self.btn.grid(row=0, column=0, pady=(5, 0), sticky='nw')
               self.btn = Button(self.frame_main, text='Create session', width=5,
                  height=2, bd='10', command=lambda: self.addSession())
               self.btn.grid(row=1, column=0, pady=(5, 0), sticky='nw')
               
               # Create a frame for the canvas with non-zero row&column weights
               self.frame_canvas = Frame(self.frame_main)
               self.frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
               self.frame_canvas.grid_rowconfigure(0, weight=1)
               self.frame_canvas.grid_columnconfigure(0, weight=1)
               # Set grid_propagate to False to allow 5-by-5 buttons resizing later
               self.frame_canvas.grid_propagate(False)

               # Add a canvas in that frame
               self.canvas = Canvas(self.frame_canvas, bg="yellow")
               self.canvas.grid(row=0, column=0, sticky="news")

               # Link a scrollbar to the canvas
               self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
               self.vsb.grid(row=0, column=1, sticky='ns')
               self.canvas.configure(yscrollcommand=self.vsb.set)
               # Create a frame to contain the buttons
               self.frame_buttons = Frame(self.canvas, bg="blue")
               self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')
               # Add 9-by-5 buttons to the frame
               
               #######
               root.mainloop()
A = Application()
A.run()
