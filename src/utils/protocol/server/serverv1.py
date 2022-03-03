# import socket programming library
import socket
import os
import ssl
import json
import time
# import thread module
from _thread import *
import threading

import pathlib

from matplotlib import use
from utils.protocol.server.certificate import create_certificate

class Server:


    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    print_lock = threading.Lock()
    sessions = {} #key is session id(string ot int) values is events list
    users = {} #key is user id and value is connection
    connections = {} #key is address string ip:port, value is user
    hosts = {} #key is host session_id and value is connection
    members = {} #key is session_id and value is a list of connections
    invitations = {} #key user_id value is session_id
    #events = [] #del
    def login(self, e:dict, address, c):
        if e["id"] in self.users:
            return {'type':'login_response',
                    'description':'user already exists',
                    'status':'error'}
        self.users[e["id"]]=c
        return {'type':'login_response',
                    'description':'user created',
                    'status':'ok'}
        
    def disconnect(self, c, addr): 
        # user is removed from users dict
        e = {
            'type':'disconnect'
        }
        for session in self.hosts:
            if self.hosts[session].fileno() == c.fileno():
                del self.hosts[session]
                for cc in self.members[session]:
                    if cc!=c:
                        self.send_message(cc, e)
                del self.members[session]
                break
        for user in self.users:
            if self.users[user].fileno()==c.fileno():
                del self.users[user]
                break
    
    def create_session(self,e:dict, address, c):
        id = e["id"] #session_id
        if id in self.sessions:
            return {'type':'session_response',
                'description':'session already exists',
                'status':'error',
                'id':id}
        #self.sessions[id] = self.events
        self.sessions[id] = []
        self.hosts[id]=c
        self.members[id]=[c]
        return {'type':'session_response',
                'description':'session created',
                'status':'ok',
                'id':id
                }
        
    def invite_to_session(self, e:dict):
        u = self.users.get(e["user_id"],None)
        if u:
            #print("invite to session:")
            #print(u)
            #print(e)
            self.invitations[e["user_id"]] = e["session_id"]
            self.send_message(u,e)
        else:
            return {'type':'invite_response',
                    'description':'user does not exists',
                    'status':'error'}
            
    def request_to_join_session(self,e:dict,c):
        userfound = False
        user = None
        for a in self.users:
            if self.users[a].fileno() == c.fileno():
                userfound=True
                print("user found",a)
                user = a
                break
        if not userfound:
            return {'type':'request_response',
                    'description':'user not logged exists',
                    'status':'error'}
        
        s = self.hosts.get(e["id"],None)
        if s:
            #print(s)
            e["user_id"]=user
            host = self.hosts[e["id"]]
            self.send_message(host,e)
            print("message send")
        else:
            return {'type':'request_response',
                    'description':'host does not exists',
                    'status':'error'}
            
    def accept(self,e:dict):
        user_id = e["user_id"]
        session_id = e["session_id"]
        client_c = self.users[user_id]
        self.members[session_id].append(client_c)
        self.send_message(client_c,e)
        
    def accept_invite(self,e:dict, c):
        userfound = False
        user = None
        for a in self.users:
            if self.users[a].fileno() == c.fileno():
                userfound=True
                print("user found",a)
                user = a
                break
        if not userfound:
            return {'type':'request_response',
                    'description':'user not logged exists',
                    'status':'error'}
        if not (user in self.invitations and self.invitations[user] == e["session_id"]):
            return {'type':'request_response',
                    'description':'trying hack?',
                    'status':'error'}
        s = self.hosts.get(e["session_id"],None)
        if s:
            #print(s)
            e["user_id"]=user
            host = self.hosts[e["session_id"]]
            self.send_message(host,e)
            print("message send")
            self.members[e["session_id"]].append(c)
        else:
            return {'type':'request_response',
                    'description':'host does not exists',
                    'status':'error'}
            
        '''
        print("accept_invite\n",e)
        user_id = e["user_id"]
        session_id = e["session_id"]
        client_c = self.users[user_id]
        host_c = self.hosts[session_id]
        self.members[session_id].append(client_c)
        self.send_message(host_c,e)
        print(host_c,client_c)
        '''
    def decline(self,e:dict):
        user_id = e["user_id"]
        session_id = e["session_id"]
        client_c = self.users[user_id]
        #self.members[session_id].append(client_c)
        self.send_message(client_c,e)
        
    def list_users(self):
        users =[]
        for u in self.users.keys():
            users.append(str(u))
        e={
            'time': time.time(),
            'type': 'list_users_response',
            'users': users
            }
        return e
    
    def list_sessions(self):
        sessions =[]
        for u in self.sessions.keys():
            sessions.append(str(u))
        e={
            'time': time.time(),
            'type': 'list_sessions_response',
            'sessions': sessions
            }
        return e
    
    def send_message(self,c,e):
        try:
            json_object = json.dumps(e)
            n = len(json_object).to_bytes(4, byteorder='big')
            c.sendall(n)
            c.sendall(json_object.encode("utf8"))
        except Exception as e:
            print("error",e)
        
    def update_events(self,c,i, addr, session_id):
        if not session_id in self.sessions:
            return 0
        events = self.sessions[session_id]
        #global events
        #print(i)
        #print(len(events))
        #print("update events",len(events),i)
        if i<len(events):
                #print("server should start sending")
                #print(i,len(self.events))
                #print(self.events)
                while i<len(events):
                    #print(self.events[i]["address"]!=addr)
                    #print(events[i], addr)
                    if events[i]["address"]!=addr:
                        #print("sending message")
                        self.send_message(c,events[i])
                        #print(self.events[i])
                        #json_object = json.dumps(self.events[i])
                        #n = len(json_object).to_bytes(4, byteorder='big')
                        #c.sendall(n)
                        #c.sendall(json_object.encode("utf8"))
                    i+=1
        return i
    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data 
    
    # thread function
    def threaded(self, c, addr):
        session_id = 0
        c.settimeout(0.5)
        i=0
        #print("new client",c)
        while True:
            data=None
            try:
                # data received from client
                #data = c.recv(4)
                #print("a",data)
                data = self.recvall(c,4)
            except socket.timeout:
                #print("Didn't receive data! [Timeout 0.5s]")
                
                i = self.update_events(c,i,addr,session_id)
                continue
        
            if not data:
                print('Bye')
                self.disconnect(c,addr)
                # lock released on exit
                self.print_lock.release()
                break
            
            i = self.update_events(c,i,addr,session_id)

            n = int.from_bytes(data,byteorder='big')
            #print("b",n)
            #json_object = c.recv(n)
            json_object = self.recvall(c,n)
            #print("c",json_object)
            jsonstring = json_object.decode('utf8', errors='ignore')
            print("received",jsonstring)
            e = json.loads(jsonstring)
            e["address"] = addr
            if e["type"]=='delete':
                #del self.events[e["id"]]
                #for a in self.events:
                j=0
                '''
                while j<len(self.events):
                    if self.events[j]["id"]==e["id"]:
                        #print(self.events)
                        del self.events[j]
                        i-=1
                        print("delete event",j,i)
                        #print(self.events)
                        break
                    j+=1
                '''
            elif e["type"]=='login':
                a = self.login(e, addr, c)       
            elif e["type"]=='create':
                a = self.create_session(e, addr, c)
                if a["status"]=="ok":
                    session_id = a["id"]
            elif e["type"]=='invite':
                a = self.invite_to_session(e)
            elif e["type"]=='request':
                a = self.request_to_join_session(e,c)
            elif e["type"]=='accept':
                a = self.accept(e)
                session_id = e["session_id"]
            elif e["type"]=='decline':
                a = self.decline(e)
            elif e["type"]=='list_users':
                a = self.list_users()
            elif e["type"]=='list_sessions':
                a = self.list_sessions()
            elif e["type"]=='accept_invite': 
                a = self.accept_invite(e,c)
                session_id = e["session_id"]
            
                    
            if a:
                self.send_message(c,a)
                print(a)
            #all events should be appended to a correct event list
            #in the sessons dict
            #self.events.append(e)
            session_id = e.get("session_id",None)
            if session_id and session_id in self.sessions:
                self.sessions[session_id].append(e)
                print("this wont print")
            #i = self.update_events(c,i,addr)
            #i = self.update_events(c,i,addr)
            #print(e)
            # reverse the given string from client
            #data = data[::-1]
  
            # send back reversed string to client
            #c.send(data)
  
        # connection closed
        c.close()
  
  
    def run(self): #rename to something else than main
        host = ""
    
        # reverse a port on your computer
        # in our case it is 12345 but it
        # can be anything
        #port = 12345
        port = self.PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        certpath = pathlib.Path(os.environ.get("SERVER_CERT_PATH", "./cert/cert.pem"))
        keypath = pathlib.Path(os.environ.get("SERVER_KEY_PATH", "./cert/key.pem"))

        if not certpath.exists() or not keypath.exists():
            create_certificate()

        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
        context.load_cert_chain(keyfile=keypath, certfile=certpath)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        print("socket binded to port", port)
  
        # put the socket into listening mode
        s.listen(5)
        print("socket is listening")
  
        # a forever loop until client wants to exit
        while True:
  
            # establish connection with client
            c, addr = s.accept()
            c = context.wrap_socket(c, server_side=True)
  
            # lock acquired by client
            self.print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1])
  
            # Start a new thread and return its identifier
            start_new_thread(self.threaded, (c,addr))
            self.print_lock.release()
        s.close()
  
'''  
if __name__ == '__main__':
    Main()
'''

#note to self: new comments can resurrect old code :D













'''

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
'''