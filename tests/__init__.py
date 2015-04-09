import os
import requests
import socket
import subprocess
import time

RUN_SERVER_CMD = 'python runserver.py --name=%s --port=%d'
SERVER_URL = 'http://localhost:%d'

def assert_success(r):
  if not (r.status_code == 200 and r.text == 'OK'):
    raise Exception('Request failed.')

class DHTNode(object):
  def __init__(self, name, port):
    self.name = name
    # If no port is provided, pick an unused one.
    if port is None:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(('localhost', 0))
      _, port = sock.getsockname()
      sock.close()
    self.port = port
    self.proc = None
    self._url = SERVER_URL % self.port

  def start(self):
    if self.is_running():
      raise Exception('DHTNode[%s] is already running.' % self.name)

    cmd = RUN_SERVER_CMD % (self.name, self.port)
    fnull = open(os.devnull, 'w')
    self.proc = subprocess.Popen(cmd.split(), stdout=fnull, stderr=fnull)
    # Keep on polling for 5 seconds to see if server is up and running.
    for _ in xrange(50):
      time.sleep(0.1)
      if not self.is_running():
        continue
      if self.ping():
        break
    else:
      raise Exception('DHTNode[%s] failed to start up.' % self.name)

  def is_running(self):
    return self.proc and self.proc.poll() is None

  def stop(self):
    if not self.is_running():
      raise Exception('DHTNode[%s] is not running.' % self.name)
    self.proc.kill()
    self.proc.wait()

  def ping(self):
    try:
      r = requests.get(self._url)
    except:
      return False
    return r.status_code == 200 and r.text == 'OK'

  def keys(self):
    r = requests.get(self._url + '/db')
    if r.status_code != 200:
      raise Exception('Request failed')
    return filter(lambda s: s, r.text.split('\r\n'))

  def put(self, key, value):
    r = requests.put(self._url + '/db/%s' % key, data=str(value))
    assert_success(r)

  def get(self, key):
    r = requests.get(self._url + '/db/%s' % key)
    if r.status_code != 200:
      raise Exception('Request failed')
    return r.text

  def delete(self, key):
    r = requests.delete(self._url + '/db/%s' % key)
    assert_success(r)

  def peers(self):
    r = requests.get(self._url + '/dht/peers')
    if r.status_code != 200:
      raise Exception('Request failed')
    return filter(lambda s: s, r.text.split('\r\n'))

  def join(self, *seeds):
    seeds = map(lambda n: '%s:%s:%s' % (n.name, n.host, n.port), seeds)
    r = requests.post(self._url + '/dht/join', '\r\n'.join(seeds))
    assert_success(r)

  def leave(self):
    r = requests.get(self._url + '/dht/leave')
    assert_success(r)
