import socket
import json
import sys
from testview import viewtestv1

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
#data: bytes
s: socket
def connect():
    print("connect")
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

def receive():
    print("receive")
    #global data
    #data = s.recv(1024)
    global s
    while True:
        try:
            # data received from client
            data = s.recv(4)
            print("a",data)
        except socket.timeout:
            print("Didn't receive data! [Timeout 0.5s]")
            continue
        n = int.from_bytes(data,byteorder='big')
        print("b",n)
        json_object = s.recv(n)
        print("c",json_object)
        jsonstring = json_object.decode('utf8', errors='ignore')
        print("d",jsonstring)
        e = json.loads(jsonstring)
        print("should print addLine")
        viewtestv1.addLine(e)

