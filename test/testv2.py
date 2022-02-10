#this is a performance test
#step1 start server
#step2 start client 1
#step3 start client 2
#step4 client 1 sends messages
#step5 client 2 receives messages
#step6 ... send more different messages
#
import os, sys
# patch the python import find path to include parent directory and local directory if the test is run from parent directory
sys.path.insert(1, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))
sys.path.insert(1, os.path.abspath('src'))
sys.path.insert(1, os.path.abspath('../src'))

from asyncio import Protocol
import testclient.testclientv2 as client
from src import server_main
from _thread import *
import threading
import time

class testwrapper:
    counterLine=0
    counterPhoto=0
    counterNote=0
    def addLineFromClient(self,e:dict):
        print("a")
        self.counterLine += 1
    def addPhotoFromClient(self,e:dict):
        print("b")
        self.counterLine += 1
    def addNoteFromClient(self,e:dict):
        print("c")
        self.counterLine += 1

def connect_receive():
    print("should print connect")
    client.connect()
    print("should print receive")
    client.receive()


#start_new_thread(main,()) does not work

#start_new_thread(connect,())
#start_new_thread(receive,())
print("SHOULD START SERVER")
start_new_thread(server_main.main,())
start_new_thread(connect_receive,())
