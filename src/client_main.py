import utils.gui.application as app
import utils.gui.guiv2 as gui
import utils.protocol.client.clientv1 as client
from _thread import *
#this program should first initiate the server then the client???...

def main():
    g = gui.Gui()
    c = client.Client()
    c.connect()
    g.set_client(c)
    start_new_thread(c.receive,(g,))
    g.run()

if __name__ == '__main__':
    main()