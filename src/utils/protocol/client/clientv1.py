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
    #TODO make new code work!:
    def receive(self,gui):
        print("receive")
        #global data
        #data = s.recv(1024)
        #global s
        while True:
            try:
                # data received from server
                data = self.s.recv(4)
                print("a",data)
            except socket.timeout:
                print("Didn't receive data! [Timeout 0.5s]")
                continue
            n = int.from_bytes(data,byteorder='big')
            print("b",n)
            json_object = self.s.recv(n)
            print("c",json_object)
            jsonstring = json_object.decode('utf8', errors='ignore')
            print("d",jsonstring)
            e: dict = json.loads(jsonstring)
            print("should print addLine")
            if e["type"]=="line":
                #viewtestv1.addLine(e)
                gui.addLineFromClient(e)
            else: #TODO: fix!
                gui.addPhotoFromClient(e)
        




#print('Received', repr(data))