# This file was converted from input/simple.yaml by ToscaPy on 2016-04-28 19:23:10.378868.

from tosca.interfaceable import interfacemethod
import tosca.blueprint

class depends_on(tosca.blueprint.Relationship):
    ''' cloudify.relationships.depends_on '''

    def __init__(self, connection_type='all_to_all'):
        self.connection_type = connection_type

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'preconfigure')
    def preconfigure(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'postconfigure')
    def postconfigure(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'establish')
    def establish(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'unlink')
    def unlink(self, ctx):
        pass

class contained_in(depends_on):
    ''' cloudify.relationships.contained_in '''

class file_system_contained_in_compute(contained_in):
    ''' cloudify.relationships.file_system_contained_in_compute '''

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'unlink')
    def unlink(self, ctx):
        ctx.script.script_runner.tasks.run(self, ctx, script_path='https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/resources/rest-service/cloudify/fs/unmount.sh')

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'establish')
    def establish(self, ctx):
        ctx.script.script_runner.tasks.run(self, ctx, script_path='https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/resources/rest-service/cloudify/fs/mount.sh')

class connected_to(depends_on):
    ''' cloudify.relationships.connected_to '''

class file_system_depends_on_volume(depends_on):
    ''' cloudify.relationships.file_system_depends_on_volume '''

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'preconfigure')
    def preconfigure(self, ctx):
        ctx.script.script_runner.tasks.run(self, ctx, script_path='https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/resources/rest-service/cloudify/fs/fdisk.sh', device_name={'get_attribute': ['TARGET', 'device_name']})
