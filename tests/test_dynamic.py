import random
import unittest

from tests import DHTNode

MAX_NODES = 10

class DynamicDHTTest(unittest.TestCase):
  def setUp(self):
    self.nodes = [DHTNode('name%d' % i) for i in xrange(MAX_NODES)]
    map(lambda n: n.start(), self.nodes)

  def test_add_and_leave(self):
    for n in xrange(1, MAX_NODES):
      self.nodes[n].join(self.nodes[n-1])

    for i in range(500):
      node = random.choice(self.nodes)
      node.put('key_%d' % i, 'value_%d' % i)

    remove_node = random.choice(self.nodes)
    remove_keys = remove_node.keys()
    self.assertTrue(len(remove_keys) > 0)

    try:
      remove_node.leave()
    except:
      self.fail('Failed to remove node from DHT')

    # Ensure that all nodes see 1 less peer and the removed node sees only
    # itself.
    for node in self.nodes:
      if node == remove_node:
        self.assertEqual(len(node.peers()), 1)
      else:
        self.assertEqual(len(node.peers()), MAX_NODES - 1)

    # Check that remove node only has keys that were on it, and all the other
    # nodes can see all keys.
    for node in self.nodes:
      for i in range(500):
        key = 'key_%d' % i
        value = 'value_%d' % i
        if node == remove_node and key not in remove_keys:
          value = ''
        self.assertEqual(node.get(key), value)

    # Add the removed node back and see that all nodes see all keys.
    while True:
      node = random.choice(self.nodes)
      if node != remove_node:
        remove_node.join(node)
        break

    for node in self.nodes:
      for i in xrange(500):
        self.assertEqual(node.get('key_%d' % i), 'value_%d' % i)

  def tearDown(self):
    map(lambda n: n.stop(), self.nodes)
