
from interfaceable import Interfaceable

class Blueprint:
    pass

class Node:
    __metaclass__ = Interfaceable
    
    def __init__(self):
        self.relationships = []
    
    def relate(self, target, relationship_class):
        r = relationship_class(target)
        self.relationships.append(r)
        return r

class Relationship:
    __metaclass__ = Interfaceable

    def __init__(self, target):
        self.target = target
