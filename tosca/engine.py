
class Engine:
    def handle(self, command):
        pass

class Command:
    def __init__(self):
        self.name = None
        self.arguments = []
        self.ctx = None
        self.handled = False
    
    def __str__(self):
        return 'name: %s, handled: %s' % (self.name, self.handled)
