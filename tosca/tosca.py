#!/usr/bin/env python

'''
TOSCA.py

  tosca touch myblueprint

Looks for myblueprint.yaml or myblueprint.py. Chooses the newer one, converts to the other version. Renames existing files with .bak.#.

The myblueprint.py will put all structures in a ctx.
The parser must be extensible in some way.

The myblueprint.py will define a list of engines. (Or is there a default configured list of engines?)
Arguments will be parsed and placed in the Command instance.
Command will be sent to the engines in order. (The first engine is always tosca.py itself, the "default" engine.)
If an engine handles the comment, it can set the command.complete = True to stop handling.

e.g.:

  tosca validate myblueprint
  tosca upload myblueprint
  tosca deploy myblueprint

Engines can modify the ctx and also put their own stuff in it.
'''

import sys
from context import Context
from engine import Command
from default_engine import DefaultEngine

default_engine = DefaultEngine()
engines = [default_engine]

def main():
    global engines
    
    command = Command()
    command.name = sys.argv[1]
    command.arguments = sys.argv[2:]
    command.ctx = Context()
    for engine in engines:
        engine.handle(command)
        if not command.handled:
            break
    
    if not command.handled:
        print 'Unsupported command: %s' % command.name

if __name__ == '__main__':
    main()
