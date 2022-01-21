import socket
import json


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
#data: bytes
s: socket
'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
'''
def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

def send(dictionary: dict):
    json_object = json.dumps(dictionary)
    n = len(json_object).to_bytes(4, byteorder='big')
    global s
    s.sendall(n)
    s.sendall(json_object.encode("utf8"))
        




#print('Received', repr(data))