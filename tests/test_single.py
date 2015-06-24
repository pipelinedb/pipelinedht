import unittest

from tests import DHTNode

class SingleNodeTest(unittest.TestCase):
  def setUp(self):
    self.node = DHTNode('node')
    self.node.start()

  def test_simple(self):
    node = self.node

    # Getting empty key works.
    self.assertEqual(node.get('hello'), '')

    # Deleting non-existent key works.
    try:
      node.delete('hello')
    except:
      self.fail('node failed to delete non-existent key')

    # There must be no keys in a new node.
    self.assertEqual(len(node.keys()), 0)

    # Try putting and getting keys.
    for i in xrange(100):
      node.put('key_%d' % i, 'value_%d' % i)
    for i in xrange(100):
      self.assertEqual(node.get('key_%d' % i), 'value_%d' % i)
    self.assertEqual(len(node.keys()), 100)

    # Delete some keys and ensure that works.
    for i in xrange(1, 100, 2):
      node.delete('key_%d' % i)

    # Enure that 50 keys were deleted.
    self.assertEqual(len(node.keys()), 50)

    # See that undeleted keys are still there.
    for i in xrange(100):
      value = '' if i % 2 else 'value_%d' % i
      self.assertEqual(node.get('key_%d' % i), value)

    # Peers must only return ourself.
    self.assertEqual(node.peers(), [node.name])

  def tearDown(self):
    self.node.stop()
