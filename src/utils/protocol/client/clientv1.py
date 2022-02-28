import socket
import ssl
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
    def __init__(self,host,port):
        self.HOST = host
        self.PORT = port
        
    session_id = None
    def set_session_id(self, id):
        self.session_id = id
    def connect(self):
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
        self.s = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.s.connect((self.HOST, self.PORT))

    def send(self, dictionary: dict):
        if not "session_id" in dictionary and self.session_id:
            dictionary["session_id"]=self.session_id
        json_object = json.dumps(dictionary)
        n = len(json_object).to_bytes(4, byteorder='big')
        #global s
        self.s.sendall(n)
        self.s.sendall(json_object.encode("utf8"))
        
    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
    
    def receive(self,gui,app):
        print("receive")
        #global data
        #data = s.recv(1024)
        #global s
        while True:
            try:
                # data received from server
                #data = self.s.recv(4)
                data = self.recvall(self.s, 4)
                #print("a",data)
            except socket.timeout:
                print("Didn't receive data! [Timeout 0.5s]")
                continue
            n = int.from_bytes(data,byteorder='big')
            #print("b",n)
            #json_object = self.s.recv(n)
            json_object = self.recvall(self.s, n)
            #print("c",json_object)
            jsonstring = json_object.decode('utf8', errors='ignore')
            #print("d",jsonstring)
            e: dict = json.loads(jsonstring)
            #print("should print addLine")
            if e["type"]=="line":
                #viewtestv1.addLine(e)
                gui.addLineFromClient(e)
            elif e["type"]=="image": #fixed!
                gui.addPhotoFromClient(e)
            elif e["type"]=="note":
                gui.addNoteFromClient(e)
            elif e["type"]=="delete":
                #print("client delete")
                gui.deleteFromClient(e)
            elif e["type"]=="updateNote":
                gui.updateNoteFromClient(e)
            elif e["type"]=="deleteNote":
                gui.deleteNoteComingFromServer(e)
            elif e["type"]=="moveNote":
                gui.moveNoteComingFromServer(e)
            elif e["type"]=="commentbox":
                gui.addCommentboxFromClient(e)
            elif e["type"]=="updateComment":
                gui.updateCommentFromClient(e)
            elif e["type"]=="list_users_response":
                app.list_users_response(e)
            elif e["type"]=="login_response":
                app.response(e)
            elif e["type"]=="session_response":
                app.response(e)
                app.session_response(e)
            elif e["type"]=="invite_response":
                app.response(e)
            elif e["type"]=="request_response":
                app.response(e)
            elif e["type"]=="list_sessions_response":
                app.response(e)
            elif e["type"]=="request":
                app.response(e)
            elif e["type"]=="accept":
                app.response(e)
                app.accept_handler(e)
            elif e["type"]=="accept_invite":
                app.response(e)
            elif e["type"]=="invite":
                print("invited")
                app.response(e)
                
                
        




#print('Received', repr(data))
