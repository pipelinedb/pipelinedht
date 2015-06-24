import random
import unittest

from tests import DHTNode

MAX_NODES = 10

class GrowingDHTTest(unittest.TestCase):
  def setUp(self):
    self.nodes = [DHTNode('name%d' % i) for i in xrange(MAX_NODES)]
    map(lambda n: n.start(), self.nodes)

  def test_add(self):
    node0 = self.nodes[0]
    node1 = self.nodes[1]

    node0.put('hello', 'world')
    node1.put('lol', 'cat')

    self.assertEqual(node0.get('hello'), 'world')
    self.assertEqual(node0.get('lol'), '')
    self.assertEqual(node1.get('hello'), '')
    self.assertEqual(node1.get('lol'), 'cat')

    try:
      node0.join(node1)
    except:
      self.fail('node0 failed to join node1.')

    self.assertEqual(len(node0.peers()), 2)
    self.assertEqual(len(node1.peers()), 2)

    # Ensure we can fetch keys from the other node.
    self.assertEqual(node0.get('hello'), 'world')
    self.assertEqual(node0.get('lol'), 'cat')
    self.assertEqual(node1.get('hello'), 'world')
    self.assertEqual(node1.get('lol'), 'cat')

    # Check that keys can be inserted and fetched from both nodes.
    for i in xrange(100):
      if i % 2:
        node0.put('key_%d' % i, 'value_%d' % i)
      else:
        node1.put('key_%d' % i, 'value_%d' % i)

    for i in xrange(100):
      self.assertEqual(node0.get('key_%d' % i), 'value_%d' % i)
      self.assertEqual(node1.get('key_%d' % i), 'value_%d' % i)

  def test_add_multiple(self):
    # Insert 100 keys into each of the 10 nodes.
    for n in xrange(MAX_NODES):
      for i in xrange(100):
        self.nodes[n].put('k%d_%d' % (n, i), str(i))

    for n in xrange(MAX_NODES):
      self.assertEqual(len(self.nodes[n].keys()), 100)

    # Join each node one by one and check that the we can retrieve all keys
    # that are part of the DHT so far from each node in the DHT.
    for n in xrange(1, MAX_NODES):
      try:
        self.nodes[n].join(self.nodes[n-1])
      except:
        self.fail('node%d failed to join node%d' % (n, n-1))

      for i in xrange(100):
        keys = ['k%d_%d' % (n, i) for n in xrange(n + 1)]
        for n in xrange(n + 1):
          for key in keys:
            self.assertEqual(self.nodes[n].get(key), str(i))

    # See that all nodes see all peers.
    for node in self.nodes:
      self.assertEqual(len(node.peers()), MAX_NODES)

    # Put keys into random nodes and see that all nodes can see them.
    for i in xrange(500):
      node = random.choice(self.nodes)
      node.put('hello_%d' % i, 'world_%d' % i)

    for i in xrange(500):
      for node in self.nodes:
        self.assertEqual(node.get('hello_%d' % i), 'world_%d' % i)

  def test_sharding(self):
    for n in xrange(1, MAX_NODES):
      self.nodes[n].join(self.nodes[n-1])

    for i in xrange(1000):
      node = random.choice(self.nodes)
      node.put('key_%d' % i, 'value_%d' % i)

    # Ensure that total number of keys in shards is 1000.
    nodes_keys = map(lambda n: n.keys(), self.nodes)
    nodes_len = map(lambda k: len(k), nodes_keys)
    self.assertEqual(sum(nodes_len), 1000)

    # Ensure that no node has duplicate keys.
    key_set = set()
    key_list = []

    for keys in nodes_keys:
      key_set.update(keys)
      key_list.extend(keys)

    self.assertEqual(set(key_list), key_set)
    self.assertEqual(len(key_list), len(key_set))

    # Ensure that distribution is not too ways off. Each node should have ~100
    # keys.
    for l in nodes_len:
      self.assertTrue(l < 250)
      self.assertTrue(l > 25)

  def tearDown(self):
    map(lambda n: n.stop(), self.nodes)
