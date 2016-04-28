
from interfaceable import Interfaceable

class Blueprint:
    pass

class Node:
    __metaclass__ = Interfaceable
    
    def __init__(self):
        self.relationships = []
    
    def relate(self, ctx, target, relationship_class):
        r = relationship_class(ctx, target)
        self.relationships.append(r)
        return r

class Data:
    __metaclass__ = Interfaceable

class Relationship:
    __metaclass__ = Interfaceable

    def __init__(self, ctx, target):
        self.ctx = ctx
        self.target = target
