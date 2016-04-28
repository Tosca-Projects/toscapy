#!/usr/bin/env python

import sys
from engine import Command
from default_engine import DefaultEngine

default_engine = DefaultEngine()
engines = [default_engine]

def main():
    global engines
    
    command = Command()
    command.name = sys.argv[1]
    command.arguments = sys.argv[2:]
    for engine in engines:
        engine.handle(command)
        if not command.handled:
            break
    
    if not command.handled:
        print 'Unsupported command: %s' % command.name

if __name__ == '__main__':
    main()
