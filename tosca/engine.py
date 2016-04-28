
class Engine:
    def handle(self, command):
        pass

class Command:
    def __init__(self):
        self.name = None
        self.arguments = []

    def __str__(self):
        return 'name: %s, handled: %s' % (self.name, self.handled)
