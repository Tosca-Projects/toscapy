
class Context:
    def __init__(self):
        self.imports = []
        self.input = {}
        self.output = {}
        self.node_template = {}

class Import:
    def __init__(self, url):
        self.url = url

class Input:
    def __init__(self, description=None):
        self.description = description

class Output:
    def __init__(self, description=None):
        self.description = description
        self.value = {}

class Value:
    def __init__(self, value):
        self.value = value
    
    def get(self):
        return self.value

class MethodValue:
    def __init__(self, scope, method, arguments):
        self.scope = scope
        self.method = method
        self.arguments = arguments

    def get(self):
        if self.scope:
            m = getattr(self.scope, self.method)
        else:
            m = globals()[self.method]
        return m(**self.arguments)

class NodeTemplate:
    def __init__(self, type):
        self.type = type
        self.relationships = []
        self.property = {}

class Relationship:
    def __init__(self, type):
        self.type = type
        self.target = None
        self.target_interface = {}
        self.property = {}

class TargetInterface:
    def __init__(self):
        pass
