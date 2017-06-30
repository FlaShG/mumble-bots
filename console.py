#!/usr/bin/python
import sys

import bots
import mumble

def main(argv):
  certfile=None
  keyfile=None
  if len(argv)>2:
      certfile=argv[1]
      keyfile=argv[2]
  c = bots.InteractiveBot(botcertfile=certfile,botkeyfile=keyfile)
  c.interact()

if __name__ == '__main__':
  main(sys.argv)
else:
  raise Exception("Importing console.py is rather useless, isn't it?")
