import socket
import json

class Client:

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
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

    def send(self, dictionary: dict):
        json_object = json.dumps(dictionary)
        n = len(json_object).to_bytes(4, byteorder='big')
        #global s
        self.s.sendall(n)
        self.s.sendall(json_object.encode("utf8"))
        




#print('Received', repr(data))