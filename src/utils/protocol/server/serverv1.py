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
from utils.protocol.server.certificate import create_certificate

class Server:


    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    print_lock = threading.Lock()
    sessions = {} #key is session id(string ot int) values is events list
    users = {} #key is user id and value is a dict of user info(ip,joined,id)
    connections = {} #key is address string ip:port, value is user
    events = []

    def update_events(self,c,i, addr):
        #global events
        #print("update events",len(events),i)
        if i<len(self.events):
                #print("server should start sending")
                #print(i,len(self.events))
                #print(self.events)
                while i<len(self.events):
                    #print(self.events[i]["address"]!=addr)
                    if self.events[i]["address"]!=addr:
                        #print(self.events[i])
                        json_object = json.dumps(self.events[i])
                        n = len(json_object).to_bytes(4, byteorder='big')
                        c.sendall(n)
                        c.sendall(json_object.encode("utf8"))
                    i+=1
        return i

    # thread function
    def threaded(self, c, addr):
        c.settimeout(0.5)
        i=0
        #print("new client",c)
        while True:
            data=None
            try:
                # data received from client
                data = c.recv(4)
                #print("a",data)
            except socket.timeout:
                #print("Didn't receive data! [Timeout 0.5s]")
                i = self.update_events(c,i,addr)
                continue
        
            if not data:
                print('Bye')
                # lock released on exit
                self.print_lock.release()
                break
            
            i = self.update_events(c,i,addr)

            n = int.from_bytes(data,byteorder='big')
            #print("b",n)
            json_object = c.recv(n)
            #print("c",json_object)
            jsonstring = json_object.decode('utf8', errors='ignore')
            #print("d",jsonstring)
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
            
            self.events.append(e)
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