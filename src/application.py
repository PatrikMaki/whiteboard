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
import utils.gui.guiv2 as gui
import utils.protocol.client.clientv1 as client
from _thread import *
import sys
#allow any user to create a new session and invite others to join the session. The user who has
#created the session would serve as the host and can accept or decline the requests for joining
#the session. The session would end when the host leaves or ends the session.
g = None
class Application:
       
       def __init__(self,c):
              self.client = c
       
       session_id = None
       events = []
       def addSession(self,input):
              
            #new
            #add a new dict as a session
            #add the dict to events
            #
            #new
            #print("ii")
            '''
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
            '''

            # Set the canvas scrolling region
            #self.canvas.config(scrollregion=self.canvas.bbox("all"))

       def createSession(self,session_id):
              e={
               'id': session_id, #can be changed to name later
               'time': time.time(),
               'type': 'create',
              }
              #start gui and link it to this session
              self.events.append(e)
              self.client.send(e)
              print("session created:",e)
              
       def login(self,user_id):
              e={
                'id': user_id,
                'time': time.time(),
                'type': 'login'            
              }
              self.events.append(e)
              self.client.send(e) 
              print("session created:",e)
              
       def response(self,e):
              print("response:",e)
              
       def session_response(self,e):
              if e["status"]=='ok':
                     self.session_id = e["id"]
                     print(self.session_id)
              
       def inviteToSession(self,session_id, user_id):
              """ 
              host client sends an invitation to join a session 
              to another client indicated by user id via the server
              """
              e={
               'user_id':user_id,
               'time': time.time(),
               'type': 'invite',
               'session_id': session_id
              }
               
              self.events.append(e)
              self.client.send(e)
              #print("invite")
              
       def accept_invite(self,session_id):
              e={
               'session_id': session_id,
               'time': time.time(),
               'type': 'accept_invite'
              }
               
              self.events.append(e)
              self.client.send(e)
              self.session_id = session_id
              #print("accept invite")
              
       def requestToJoin(self,session_id):
              """ 
              new client sends an invitation to join a session 
              to host client that is a host of a session indicated by user id via the server
              """
              e={
               'id':session_id,
               'time': time.time(),
               'type': 'request'
              }
               
              self.events.append(e)
              self.client.send(e)
              #print("request")
              
       def accept(self,session_id,user_id):
              """ 
              host client accepts a request to join
              """
              e={
               'session_id': session_id,
               'time': time.time(),
               'type': 'accept',
               'user_id': user_id
              }
               
              self.events.append(e)
              self.client.send(e)
              #print("accept")
       def accept_handler(self, e:dict):
              self.session_id = e["session_id"]
       def decline(self,session_id,user_id):
              e={
               'session_id': session_id,
               'time': time.time(),
               'type': 'decline',
               'user_id': user_id
              }
               
              self.events.append(e)
              self.client.send(e)
              #print("decline")
             
       def list_users(self):
              e={
               'time': time.time(),
               'type': 'list_users',
              }
              self.events.append(e)
              self.client.send(e)
              #print("list users request")
              
       def list_users_response(self,e:dict):
              print(e)
              
       def list_sessions(self):
              e={
               'time': time.time(),
               'type': 'list_sessions',
              }
              self.events.append(e)
              self.client.send(e)
              #print("list users request")
              
       def list_sessions_response(self,e:dict):
              print(e)
                  
              
       def help(self):
              print("START OPTIONS: HOSTNAME PORT")
              print("Commands:")
              print("create <id>")
              print("login <id>")
              print("gui")
              print("invite <session_id> <user_id>") #invite a user to a session
              print("request <id>") #request to join a session by id
              print("accept <session_id> <user_id>") #accept user by id
              print("accept_invite <session_id>") #create a bug ticket :)
              print("decline <user_id>") #decline a user by ip       
              print("list_users")
              print("list_sessions")
       def get_session_id(self):
              return self.session_id
       def run(self):
              
               #TODO: make possible to work over internet.
               #TODO: create session!
               #TODO: invite session
               #TODO: request to join session
               #TODO: join session
               #print session id in whiteboard
               #TODO: instead of ip adrresse have user names????
               
               self.help()
               for a in sys.stdin:
                      #a = input("command: ")
                      #print("'"+a+"'")
                      if a=="q" or a=="c" or a=="quit":
                             os._exit(0)
                      else:
                            b = a.split()
                            if b[0]=="create":
                                   self.createSession(b[1])
                            elif b[0]=="login":
                                   self.login(b[1])
                            elif b[0]=="gui":
                                   g.set_running(True)
                            elif b[0]=="invite":
                                   self.inviteToSession(b[1],b[2])
                            elif b[0]=="request":
                                   self.requestToJoin(b[1])
                            elif b[0]=="accept":
                                   self.accept(b[1],b[2])
                            elif b[0]=="accept_invite":
                                   self.accept_invite(b[1])
                            elif b[0]=="decline":
                                   self.decline(b[1],b[2])
                            elif b[0]=="list_users":
                                   self.list_users()
                            elif b[0]=="list_sessions":
                                   self.list_sessions()
                            else:
                                   self.help()
                      
               #TODO: create gui using frames!
               print("end")

def main():
    hostname = "127.0.0.1"
    port = 65432
    if len(sys.argv) == 2:
       hostname = sys.argv[1]
    elif len(sys.argv) == 3:
       hostname = sys.argv[1]
       port = sys.argv[2]
    global g
    g = gui.Gui()
    c = client.Client(hostname,port)
    c.connect()
    app = Application(c)
    start_new_thread(app.run,())
    g.set_client(c)
    start_new_thread(c.receive,(g,app))
    while not g.is_running():
           time.sleep(0.1)
    c.set_session_id(app.get_session_id())
    g.run(app.get_session_id())

if __name__ == '__main__':
    main()
#A = Application()
#A.run()
