# import socket programming library
import socket
import json
import time
# import thread module
from _thread import *
import threading

PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

print_lock = threading.Lock()

events = []

def update_events(c,i):
    global events
    print("update events",len(events),i)
    if i<len(events):
            print("server should start sending")
            while i<len(events):
                json_object = json.dumps(events[i])
                n = len(json_object).to_bytes(4, byteorder='big')
                c.sendall(n)
                c.sendall(json_object.encode("utf8"))
                i+=1
    return i

# thread function
def threaded(c):
    c.settimeout(0.5)
    i=0
    print("new client",c)
    while True:
        data=None
        try:
            # data received from client
            data = c.recv(4)
            print("a",data)
        except socket.timeout:
            #print("Didn't receive data! [Timeout 0.5s]")
            i = update_events(c,i)
            continue
        
        if not data:
            print('Bye')
            # lock released on exit
            print_lock.release()
            break
        
        i = update_events(c,i)

        n = int.from_bytes(data,byteorder='big')
        print("b",n)
        json_object = c.recv(n)
        print("c",json_object)
        jsonstring = json_object.decode('utf8', errors='ignore')
        print("d",jsonstring)
        e = json.loads(jsonstring)
        events.append(e)
        # reverse the given string from client
        #data = data[::-1]
  
        # send back reversed string to client
        #c.send(data)
  
    # connection closed
    c.close()
  
  
def Main():
    host = ""
    
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    #port = 12345
    port = PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
  
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
  
    # a forever loop until client wants to exit
    while True:
  
        # establish connection with client
        c, addr = s.accept()
  
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
  
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
        print_lock.release()
    s.close()
  
  
if __name__ == '__main__':
    Main()














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