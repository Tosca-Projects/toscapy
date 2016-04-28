'''
Interfaceable
=============

Version 0.9 by Tal Liron

Straightforward interface-oriented programming for Python.

It allows a class to support multiple interfaces, whereby each interface has
its own namespace. A method by the same name on multiple interfaces could have
a different implementation entirely.

Usage example:

    from interfaceable import Interfaceable, interfacemethod
    
    class Greeter:
        __metaclass__ = Interfaceable
        
        def __init__(self, source):
            self.source = source
        
        @interfacemethod('english')
        def hello(self, n):
            print 'Hello %s from %s' % (n, self.source)
    
        @interfacemethod('spanish', 'hello')
        def hola(self, n):
            print 'Hola %s from %s' % (n, self.source)

The class will have an 'interface' method that will return an Interface instance
with methods bound to the class instance.
    
    g = Greeter('god')
    g.interface('english').hello('Tal')
    g.interface('english').hello('Allan')
    g.interface('spanish').hello('Matt')

If you want to monkey patch these methods, make sure to bind them to the instance:

    import new

    def hello2(self, n):
        print 'HOLA %s FROM %s' % (n, self.source)

    g.interface('spanish').hello = new.instancemethod(hello2, g, None)
    g.interface('spanish').hello('Matt')

You can change the name of the 'interface' method by setting _get_interface_method_name
in the class:

    class Greeter:
        __metaclass__ = Interfaceable
        _get_interface_method_name = 'cast_to'

By default, the 'interface' method is not thread-safe. To guarantee thread safety,
set a lock at self._interface_lock:

    import threading

    class Greeter:
        __metaclass__ = Interfaceable
        
        def __init__(self):
            self._interface_lock = threading.Lock()
'''

# TODO: handle inheritance and overriding!

import new

class Interfaceable(type):
    '''
    Metaclass for interfaceable classes.
    
    Use @interfacemethod() to decorate the methods to be bound to interfaces.
    
    '''
    
    def __new__(cls, name, parents, dct):
        cls._interfaces = {}
        
        for v in dct.itervalues():
            if hasattr(v, '_interface_name') and hasattr(v, '_method_name'):
                if v._interface_name in cls._interfaces:
                    interface = cls._interfaces[v._interface_name]
                else:
                    interface = cls._interfaces[v._interface_name] = {}
                if v._method_name in interface:
                    raise 'Method %s already bound to interface %s' % (v._method_name, v._interface_name)
                interface[v._method_name] = v
        
        def get_interface(self, interface_name):
            '''
            Gets an interface for an instance.
            
            The first time an interface is accessed, it is created based on the class-defined
            interface methods and bound to the instance.
            '''
            try:
                if hasattr(self, '_interface_lock'):
                    self._interface_lock.acquire()
                
                if not hasattr(self, '_interfaces'):
                    self._interfaces = {}
                    
                if interface_name in self._interfaces:
                    return self._interfaces[interface_name] 
                
                if interface_name not in self.__class__._interfaces:
                    raise 'Unsupported interface %s' % interface_name
                
                interface = self._interfaces[interface_name] = Interface()
                for k, v in self.__class__._interfaces[interface_name].iteritems():
                    setattr(interface, k, new.instancemethod(v, self, None))
                return interface
            finally:
                if hasattr(self, '_interface_lock'):
                    self._interface_lock.release()

        # Add get_interface method to class (default name: 'interface')
        get_interface_method_name = dct.get('_get_interface_method_name') or 'interface'
        dct[get_interface_method_name] = get_interface
        
        return super(Interfaceable, cls).__new__(cls, name, parents, dct)

def interfacemethod(interface_name, name=None):
    '''
    Decorator for methods that are to be bound to an interface.
    
    In unspecified, the name of the method on the interface will be the same as the declared method name.
    '''
    def decorator(f):
        f._interface_name = interface_name
        if name is None:
            f._method_name = f.__name__
        else:
            f._method_name = name
        return f
    return decorator

class Interface:
    '''
    Used to identify interface instances.
    '''
    pass
