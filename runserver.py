#!/usr/bin/env python

from argparse import ArgumentParser

from dht.server import app

if __name__ == '__main__':
  parser = ArgumentParser(
    description='PiplineDHT -- A simple distributed hash table')
  parser.add_argument('-n', '--name', action='store', required=True,
                      help='name of node')
  parser.add_argument('-k', '--host', action='store', default='localhost',
                      help='hostname to bind to')
  parser.add_argument('-p', '--port', action='store', type=int,
                      required=True, help='port to bind to')

  args = parser.parse_args()

  app.run(host=args.host, port=args.port)
