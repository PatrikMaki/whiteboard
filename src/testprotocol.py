import application as app
import utils.protocol.client.clientv1 as client

import json
import time
import socket
import random
from _thread import *
from statistics import mean, median

HOSTNAME = '127.0.0.1'
PORT = 65432



class TestEvent:
  def __init__(self):
    self.test_events = [
      { 'id': 'id', 'time': '', 'type': 'line', 'x1': 0, 'y1': 0, 'x2': 2000, 'y2': 2000, 'origin': ''},
      { 'id': 'id', 'time': '', 'type': 'image', 'x1': 10, 'y1': 10, 'x2': 100, 'y2': 100, 'image': '' },
      { 'id': 'id', 'time': '', 'type': 'note', 'x1': 10, 'y1': 10, 'note': "", 'frame_id': 'frame_id' },
      { 'id': 'id', 'time': '', 'type': 'updateNote', 'x1': 10, 'y1': 10, 'note': 'text' },
      { 'id': 'id', 'frame_id': 'frame_id', 'type': 'moveNote', 'x': 100, 'y': 100 },
      { 'id': 'id', 'frame_id': 'delete_frame_id', 'type': 'deleteNote' },
      { 'id': 'id', 'type': 'delete' },
      { 'id': 'id', 'time': '', 'type': 'commentbox', 'x1': 10, 'y1': 10, 'x2': 100, 'y2': 100, 'comment': "" },
      { 'id': 'id', 'time': '', 'type': 'updateComment', 'x1': 100, 'y1': 100, 'comment': 'text' }
    ]

    self.index_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]

  def getRandomEvent(self, client_name):
    event = self.test_events[random.choice(self.index_distribution)]
    
    if 'origin' in event:
      event['origin'] = client_name
    
    if 'image' in event:
      # create string with size of an image
      image_size = 10000 # 10KB
      image_string = ''
      for i in range(1000):
        image_string += '0123456789'
      
      event['image'] = image_string
    
    if 'time' in event:
      event['time'] = time.time()
    
    return event



class TestClient:
  def __init__(self, hostname, port, name):
    self.c = client.Client(hostname, port)
    self.c.connect()
    self.c.s.settimeout(2)
    self.a = app.Application(self.c)
    self.name = name
    self.times = []

  def login(self):
    self.a.login(self.name)
  
  def request(self, session):
    self.a.requestToJoin(session)
  
  def create(self, session):
    self.a.createSession(session)
  
  def accept(self, session, user):
    self.a.accept(session, user)
  
  def receice_event(self):
    try:
      data = self.c.recvall(self.c.s, 4)
    except socket.timeout:
      return {}

    n = int.from_bytes(data,byteorder='big')

    json_object = self.c.recvall(self.c.s, n)
    jsonstring = json_object.decode('utf8', errors='ignore')

    e: dict = json.loads(jsonstring)

    return e

  def run_client(self, timeout):
    start_new_thread(self.receive_traffic, (timeout,))
    #start_new_thread(self.send_traffic, (timeout,))
    self.send_traffic(timeout)
  
  def run_host(self, timeout):
    #start_new_thread(self.receive_traffic, (timeout,))
    self.receive_traffic(timeout)
  
  def send_traffic(self, timeout):
    while timeout > time.time():
      time_to_sleep = random.randrange(1, 3)
      time.sleep(time_to_sleep)
      
      event = TestEvent()
      e = event.getRandomEvent(self.name)
      self.c.send(e)
  
  def receive_traffic(self, timeout):
    while timeout > time.time():
      try:
        if self.name == 'host':
          print('waiting...')
        
        data = self.c.recvall(self.c.s, 4)
      except socket.timeout:
        continue
      
      n = int.from_bytes(data,byteorder='big')
      if self.name == 'host':
        print(f'got {n} bytes')
      
      json_object = self.c.recvall(self.c.s, n)
      jsonstring = json_object.decode('utf8', errors='ignore')

      e: dict = json.loads(jsonstring)

      if 'time' in e:
        self.times.append(time.time() - e['time'])



class Test:
  def __init__(self, server_ip, server_port, client_count, duration):
    self.test_name = 'testsession'
    self.duration = duration
    self.clients = []
    self.results = []

    self.host = TestClient(server_ip, server_port, 'host')
    self.host.login()
    e = self.host.receice_event()

    self.host.create(self.test_name)
    e = self.host.receice_event()

    if 'type' in e and e['type'] == 'session_response':
      self.host.a.session_response(e)
    else:
      print('could not create session for testing')

    for i in range(1, client_count):
      test_client = TestClient(server_ip, server_port, f'client{i}')
      test_client.login()
      test_client.request(self.test_name)

      self.host.accept(self.test_name, test_client.name)

      test_client.c.set_session_id(self.host.a.get_session_id())

      self.clients.append(test_client)

  def run(self):
    timeout = time.time() + self.duration

    for client in self.clients:
      print('starting client')
      start_new_thread(client.run_client, (timeout,))
    
    print('starting host')
    self.host.run_host(timeout)

    print('saving results')
    self.results.append(self.host.times)
  
  def end(self):
    #TODO: end session
    print('end(): todo')
  
  def print_average_times(self):
    for run in self.results:
      print(f'average time from client to client:\t{mean(run) * 1000} ms')
  
  def print_median_times(self):
    for run in self.results:
      print(f'median time from client to client:\t{median(run) * 1000} ms')
  
  def print_result_size(self):
    for run in self.results:
      print(f'received {len(run)} timestamps from clients')



def main():
  print('init test')
  test = Test(HOSTNAME, PORT, 4, 30.0)

  print('run test')
  test.run()

  print('results')
  test.print_average_times()
  test.print_median_times()
  test.print_result_size()

  print('end test')
  test.end()



if __name__ == '__main__':
  main()