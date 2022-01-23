import utils.gui.guiv1 as gui
import utils.protocol.client.clientv1 as client

def main():
    g = gui.Gui()
    c = client.Client()
    c.connect()
    g.set_client(c)
    g.run()

if __name__ == '__main__':
    main()