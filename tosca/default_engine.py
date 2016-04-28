import os, stat, datetime, shutil, urllib
import yaml
from argparse import ArgumentParser
from engine import Engine
from cStringIO import StringIO

def data_merge(a, b):
    '''
    Merges b into a and return merged result
    
    Note: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen
    
    From: http://stackoverflow.com/a/15836901/849021
    '''
    key = None
    try:
        if a is None or isinstance(a, str) or isinstance(a, unicode) or isinstance(a, int) or isinstance(a, long) or isinstance(a, float):
            a = b
        elif isinstance(a, list):
            if isinstance(b, list):
                a.extend(b)
            else:
                a.append(b)
        elif isinstance(a, dict):
            if isinstance(b, dict):
                for key in b:
                    if key in a:
                        a[key] = data_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                raise 'Cannot merge non-dict "%s" into dict "%s"' % (b, a)
        else:
            raise 'Cannot merge "%s" into "%s"' % (b, a)
    except TypeError, e:
        raise 'TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a)
    return a

def parse_type_name(name, default_module_name):
    dot = name.rfind('.')
    if dot != -1:
        return name[:dot], name[dot + 1:]
    else:
        return default_module_name, name

def join_type_name(module_name, class_name):
    if module_name:
        return module_name + '.' + class_name
    else:
        return class_name

def one_liner(value):
    return value.strip().replace('\n', ' ')

class PythonModule:
    def __init__(self, yaml_name, module_name, output_dir, executable=False):
        self.yaml_name = yaml_name
        self.module_name = module_name
        self.output_dir = output_dir
        self.executable = executable
        self.ioh = StringIO()
        self.io = StringIO()
        self.class_names = []
        self.class_data = {}
        self.imports = []

        if self.executable:
            self.writeh('#!/usr/bin/env python\n\n')
        self.writeh('# This file was converted from %s by ToscaPy on %s.\n\n' % (self.yaml_name, datetime.datetime.utcnow()))
    
    def writeh(self, s):
        self.ioh.write(s)

    def write(self, s):
        self.io.write(s)

    def save(self, backup=False):
        #print self.io.getvalue()
        
        for i in self.imports:
            self.writeh('import %s\n' % i)

        py_name = os.path.join(self.output_dir, self.module_name.replace('.', os.path.sep) + '.py')
        
        if backup:
            self.backup(py_name)
        
        # Make sure we have directories and __init__.py files
        dirs = []
        dir = py_name
        while dir != self.output_dir:
            dir = os.path.dirname(dir)
            dirs.insert(0, dir)
        for dir in dirs:
            self.ensure_init(dir)

        with open(py_name, 'w') as f:
            self.ioh.seek(0)
            self.io.seek(0)
            shutil.copyfileobj(self.ioh, f)
            shutil.copyfileobj(self.io, f)
            
        if self.executable:
            os.chmod(py_name, os.stat(py_name).st_mode | stat.S_IEXEC)
    
    def ensure_init(self, dir):
        if not os.path.isdir(dir):
            os.mkdir(dir)
        init = os.path.join(dir, '__init__.py')
        if not os.path.isfile(init):
            open(init, 'a').close()

    def backup(self, name):
        '''Adds a .bak.# extension to the file, where # is incremented if it already exists'''
        if os.path.isfile(name):
            i = 0
            while True:
                i += 1
                backup = '%s.bak.%d' % (name, i)
                if not os.path.isfile(backup):
                    os.rename(name, backup)
                    break

class DefaultEngine(Engine):
    def __init__(self):
        self.convert_parser = ArgumentParser(prog='convert', description='converts YAML to Python')
        self.convert_parser.add_argument('name', help='YAML blueprint filename')
        self.convert_parser.add_argument('-o', '--output', help='output directory', default='output')
    
    def handle(self, command):
        if command.name == 'convert':
            self.handle_convert(command)
    
    def handle_convert(self, command):
        arguments = self.convert_parser.parse_args(command.arguments)
        name = arguments.name
        output = arguments.output
        self.convert(name, output)
        command.handled = True
    
    def get_yaml(self, name, root=None):
        if not root:
            root = os.path.dirname(name)
        
        if name.startswith('http:') or name.startswith('https:'):
            source = urllib.urlopen(name).read()
        else:
            if not os.path.isfile(name):
                name = os.path.join(root, name)
            with open(name, 'r') as f:
                source = f.read()
            
        blueprint = yaml.load(source)

        # Handle imports recursively
        if 'imports' in blueprint:
            for i in blueprint['imports']:
                i = self.get_yaml(i, root)
                data_merge(blueprint, i)

        return blueprint
    
    def convert(self, name, output_dir):
        blueprint = self.get_yaml(name)

        main_module_name = os.path.basename(name)
        if main_module_name.endswith('.yaml'):
            main_module_name = main_module_name[:-5]
        
        modules = {}
        
        # Type modules
        
        if ('node_types' in blueprint) or ('relationships' in blueprint) or ('data_types' in blueprint):
            # Gather node types and relationships
            # We'll use 'root' to differentiate between the two class hieararchies
            classes = {}
            if 'node_types' in blueprint:
                for c in blueprint['node_types'].values():
                    c['root'] = 'tosca.blueprint.Node'
                classes.update(blueprint['node_types'])
            if 'relationships' in blueprint:
                for c in blueprint['relationships'].values():
                    c['root'] = 'tosca.blueprint.Relationship'
                    c['interfaces'] = {}
                    if 'source_interfaces' in c:
                        c['interfaces'].update(c['source_interfaces'])
                    if 'target_interfaces' in c:
                        c['interfaces'].update(c['target_interfaces'])
                classes.update(blueprint['relationships'])
            if 'data_types' in blueprint:
                for c in blueprint['data_types'].values():
                    c['root'] = 'tosca.blueprint.Data'
                classes.update(blueprint['data_types'])
                
            # Make sure we have the modules and that the classes are in order
            # TODO: this is buggy :(
            for type_name, t in classes.iteritems():
                module_name, class_name = parse_type_name(type_name, main_module_name)

                # Make sure we have the module
                if module_name in modules:
                    module = modules[module_name]
                else:
                    module = modules[module_name] = PythonModule(name, module_name, output_dir)

                if 'derived_from' in t:
                    derived_from = t['derived_from']
                else:
                    derived_from = 'tosca.blueprint.Node'
                derived_module_name, derived_class_name = parse_type_name(derived_from, main_module_name)
                if derived_module_name == module_name:
                    if derived_class_name not in module.class_names:
                        module.class_names.append(derived_class_name)
                else:
                    if (derived_module_name != module.module_name) and (derived_module_name not in module.imports):
                        module.imports.append(derived_module_name)
                if class_name not in module.class_names:
                    module.class_names.append(class_name)

                module.class_data[class_name] = t
            
            for module in modules.itervalues():
                module.writeh('from tosca.interfaceable import interfacemethod\n')
                    
                for class_name in module.class_names:
                    t = module.class_data[class_name]
                
                    # Class definition
                    module.write('\nclass %s' % class_name)
                    if 'derived_from' in t:
                        root = t['derived_from']
                    else:
                        root = t['root']
                    derived_module_name, derived_class_name = parse_type_name(root, main_module_name)
                    if derived_module_name == module.module_name:
                        module.write('(%s)' % derived_class_name)
                    else:
                        module.write('(%s)' % root)
                    module.write(':\n')
                    module.write("    ''' %s '''\n" % join_type_name(module.module_name, class_name))
                    
                    # Properties
                    if 'properties' in t:
                        module.write('\n    def __init__(self')
                        has_description = False
                        for property_name, p in t['properties'].iteritems():
                            module.write(', %s' % property_name)
                            if 'default' in p:
                                module.write('=%s' % repr(p['default']))
                            else:
                                module.write('=None')
                            if 'description' in p:
                                has_description = True
                        module.write('):\n')
                        if has_description:
                            module.write("        '''\n")
                            for property_name, p in t['properties'].iteritems():
                                if 'description' in p:
                                    module.write('        %s -- %s\n' % (property_name, one_liner(p['description'])))
                            module.write("        '''\n")
                        for property_name, p in t['properties'].iteritems():
                            module.write('        self.%s = %s\n' % (property_name, property_name))
                    
                    # Methods
                    if 'interfaces' in t:
                        used_method_names = []
                        for interface_name, i in t['interfaces'].iteritems():
                            for method_name, m in i.iteritems():
                                # Make sure not to reuse method names
                                py_method_name = method_name
                                while py_method_name in used_method_names:
                                    py_method_name += '_'
                                used_method_names.append(py_method_name)
                                
                                module.write('\n    @interfacemethod(%s, %s)\n' % (repr(interface_name), repr(method_name)))
                                module.write('    def %s(self, ctx):\n' % py_method_name)
                                if 'implementation' in m:
                                    ii = m['implementation']
                                    if 'executor' in m:
                                        module.write('        ctx.executors.%s.%s(self, ctx' % (m['executor'], ii))
                                    elif ii.endswith('.sh'): # TODO: this looks wrong, but NodeCellar does this
                                        module.write('        ctx.run(self, %s' % repr(ii))
                                    else:
                                        module.write('        ctx.%s(self, ctx' % ii)
                                    if 'inputs' in m:
                                        for input_name, iii in  m['inputs'].iteritems():
                                            if 'default' in iii:
                                                module.write(', %s=%s' % (input_name, self.parse_input(iii['default'])))
                                            else:
                                                module.write(', %s=%s' % (input_name, self.parse_input(iii)))
                                    module.write(')\n')
                                elif m:
                                    module.write('        ctx.run(self, %s)\n' % repr(m))
                                else:
                                    module.write('        pass\n')

            # Blueprint module

            if main_module_name in modules:
                main_module = modules[main_module_name]
            else:
                main_module = modules[main_module_name] = PythonModule(name, main_module_name, output_dir) 

            if 'node_templates' in blueprint:
                if 'tosca.blueprint' not in main_module.imports:
                    main_module.imports.append('tosca.blueprint')
                for t in blueprint['node_templates'].values():
                    template_module_name = parse_type_name(t['type'], main_module_name)[0]
                    if (template_module_name != main_module_name) and (template_module_name not in main_module.imports):
                        main_module.imports.append(template_module_name)
                    if 'relationships' in t:
                        for r in t['relationships']:
                            relationship_module_name = parse_type_name(r['type'], main_module_name)[0]
                            if (relationship_module_name != main_module_name) and (relationship_module_name not in main_module.imports):
                                main_module.imports.append(relationship_module_name)
            
            main_module.write('\nclass Blueprint(tosca.blueprint.Blueprint):\n')

            if 'description' in blueprint:
                main_module.write("    '''\n")
                for line in blueprint['description'].strip().split('\n'):
                    main_module.write('    %s\n' % line)
                main_module.write("    '''\n")

            if 'inputs' in blueprint:
                main_module.write('\n    def __init__(self, ctx')
                for name in blueprint['inputs'].iterkeys():
                    main_module.write(', %s' % name)
                main_module.write('):\n')
                main_module.write("        '''\n")
                for name, i in blueprint['inputs'].iteritems():
                    main_module.write('        %s -- %s\n' % (name, one_liner(i['description'])))
                main_module.write("        '''\n")
                for name in blueprint['inputs'].iterkeys():
                    main_module.write('        self.%s = %s\n' % (name, name))
            
            main_module.write('\n        ctx.blueprint = self\n')

            if 'plugins' in blueprint:
                main_module.write('\n        # Plugins\n')
                for plugin_name, p in blueprint['plugins'].iteritems():
                    if 'executor' in p:
                        main_module.write('        setattr(ctx, %s, ctx.%s(ctx))\n' % (repr(plugin_name), p['executor']))
                    else:
                        main_module.write('        setattr(ctx, %s, ctx.%s(ctx)\n' % (repr(plugin_name), p))
                    if 'install' in p:
                        if p['install']:
                            main_module.write('        ctx.%s.install(ctx)\n' % plugin_name)
            
            if 'node_templates' in blueprint:
                # Make sure we have the node templates in order
                # TODO: this is buggy :(
                template_names = []
                for template_name, t in blueprint['node_templates'].iteritems():
                    if 'relationships' in t:
                        for r in t['relationships']:
                            if 'target' in r:
                                if r['target'] not in template_names:
                                    template_names.append(r['target'])
                    if template_name not in template_names:
                        template_names.append(template_name)
                    
                main_module.write('\n        # Node templates\n')
                for template_name in template_names:
                    t = blueprint['node_templates'][template_name]
                    main_module.write('\n        self.%s = %s()\n' % (template_name, t['type']))
                    
                    if 'properties' in t:
                        for property_name, p in t['properties'].iteritems():
                            if 'get_input' in p:
                                input = p['get_input']
                                main_module.write('        self.%s.%s = self.%s\n' % (template_name, property_name, input))
                                
                    if 'relationships' in t:
                        for r in t['relationships']:
                            if 'target_interfaces' in r:
                                main_module.write('        r = self.%s.relate(ctx, self.%s, %s)\n' % (template_name, r['target'], r['type']))
                                for interface_name, i in r['target_interfaces'].iteritems():
                                    main_module.write('        i = r.interface[%s]\n' % repr(interface_name))
                                    for call_name, c in i.iteritems():
                                        main_module.write('        i.%s(' % call_name)
                                        if 'inputs' in c:
                                            wrote_first = False
                                            for input_name, ii in c['inputs'].iteritems():
                                                if wrote_first:
                                                    main_module.write(', ')
                                                else:
                                                    wrote_first = True
                                                main_module.write('%s=%s' % (input_name, self.parse_input(ii)))
                                        main_module.write(')\n')
                            else:
                                main_module.write('        self.%s.relate(ctx, self.%s, %s)\n' % (template_name, r['target'], r['type']))
                    
            if 'outputs' in blueprint:
                main_module.write('\n    # Outputs\n')
                for output_name, o in blueprint['outputs'].iteritems():
                    main_module.write('\n    def get_%s(self, ctx):\n' % output_name)
                    if 'description' in o:
                        main_module.write("        '''\n")
                        main_module.write('        %s\n' % one_liner(o['description']))
                        main_module.write("        '''\n")
                    main_module.write('        %s = {}\n' % output_name)
                    for value_name, v in o['value'].iteritems():
                        if 'get_property' in v:
                            arguments = v['get_property']
                            main_module.write('        %s[%s] = self.%s.%s\n' % (output_name, repr(value_name), arguments[0], arguments[1]))
                    main_module.write('        return %s\n' % output_name)
            
            
            if 'workflows' in blueprint:
                main_module.write('\n    # Workflows\n')
                for workflow_name, w in blueprint['workflows'].iteritems():
                    main_module.write('\n    def do_%s(self, ctx' % workflow_name)
                    has_description = False
                    if 'parameters' in w:
                        for parameter_name, p in w['parameters'].iteritems():
                            if 'default' in p:
                                main_module.write(', %s=%s' % (parameter_name, repr(p['default'])))
                            else:
                                main_module.write(', %s=None' % parameter_name)
                            if 'description' in p:
                                has_description = True
                    main_module.write('):\n')
                    if has_description:
                        main_module.write("        '''\n")
                        for parameter_name, p in w['parameters'].iteritems():
                            if 'description' in p:
                                main_module.write('        %s -- %s\n' % (parameter_name, one_liner(p['description'])))
                        main_module.write("        '''\n")
                    if 'mapping' in w:
                        main_module.write('        ctx.%s(ctx' % w['mapping'])
                    else:
                        main_module.write('        ctx.%s(ctx' % w)
                    if 'parameters' in w:
                        for parameter_name, p in w['parameters'].iteritems():
                            main_module.write(', %s' % parameter_name)
                    main_module.write(')\n')
        
        for module in modules.values():
            module.save()

    def parse_input(self, value):
        # TODO
        return repr(value)
