import testclient.testclientv1 as client
import testview.viewtestv1 as view
from _thread import *
import threading
import time
def main():
    print("should print main")
    view.main()

def connect_receive():
    print("should print connect")
    client.connect()
    print("should print receive")
    client.receive()

''''
def receive():
    print("should print receive")
    client.receive()

'''
#start_new_thread(main,()) does not work
print("test")
#start_new_thread(connect,())
#start_new_thread(receive,())
#time.sleep(10000) not needed
start_new_thread(connect_receive,())
main()


