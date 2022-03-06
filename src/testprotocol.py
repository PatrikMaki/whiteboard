import application as app
import utils.protocol.client.clientv1 as client

import json
import time
import socket
from random import randrange
from _thread import *
from statistics import mean

HOSTNAME = '127.0.0.1'
PORT = 65432



class TestClient:
  def __init__(self, hostname, port, name):
    self.c = client.Client(hostname, port)
    self.c.connect()
    self.c.s.settimeout(0.5)
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

  def run_client(self, timeout):
    # TODO: simulate random client
    start_new_thread(self.receive_traffic, (timeout,))
    start_new_thread(self.send_traffic, (timeout,))
  
  def run_host(self, timeout):
    # TODO: get measurements
    #start_new_thread(self.receive_traffic, (timeout,))
    self.receive_traffic(timeout)
  
  def send_traffic(self, timeout):
    # TODO: simulate gui traffic
    while timeout > time.time():
      time.sleep(randrange(1,3))
      e = {
        'id': 'id',
        'time': time.time(),
        'type': 'line',
        'x1': 1,
        'y1': 2,
        'x2': 3,
        'y2': 4,
        'origin': self.name
      }
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
    self.host.create(self.test_name)

    for i in range(1, client_count):
      test_client = TestClient(server_ip, server_port, f'client{i}')
      test_client.login()
      test_client.request(self.test_name)

      self.host.accept(self.test_name, test_client.name)

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
  
  def print_average_times(self):
    for run in self.results:
      print(f'average time from client to client:\t{mean(run) * 1000} ms')



def main():
  print('init test')
  test = Test(HOSTNAME, PORT, 4, 30.0)

  print('run test')
  test.run()

  print('results')
  test.print_average_times()
  # todo



if __name__ == '__main__':
  main()