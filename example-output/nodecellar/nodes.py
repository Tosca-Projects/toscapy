# This file was converted from input/simple.yaml by ToscaPy on 2016-04-28 19:23:10.378897.

from tosca.interfaceable import interfacemethod
import cloudify.nodes

class NodecellarApplicationModule(cloudify.nodes.ApplicationModule):
    ''' nodecellar.nodes.NodecellarApplicationModule '''

    def __init__(self, application_url='https://github.com/cloudify-cosmo/nodecellar/archive/master.tar.gz', port=8080, startup_script='server.js'):
        '''
        application_url -- URL to an archive containing the application source. The archive must contain one top level directory.
        port -- Web application port
        startup_script -- This script will be used to start the nodejs application. The path is relative to the top level single directory inside the archive
        '''
        self.application_url = application_url
        self.port = port
        self.startup_script = startup_script

    @interfacemethod('cloudify.interfaces.lifecycle', 'start')
    def start(self, ctx):
        ctx.run(self, 'scripts/nodecellar/start-nodecellar-app.sh')

    @interfacemethod('cloudify.interfaces.lifecycle', 'stop')
    def stop(self, ctx):
        ctx.run(self, 'scripts/nodecellar/stop-nodecellar-app.sh')

    @interfacemethod('cloudify.interfaces.lifecycle', 'configure')
    def configure(self, ctx):
        ctx.run(self, 'scripts/nodecellar/install-nodecellar-app.sh')

class MongoDatabase(cloudify.nodes.DBMS):
    ''' nodecellar.nodes.MongoDatabase '''

    def __init__(self, port=27017):
        '''
        port -- MongoDB port
        '''
        self.port = port

    @interfacemethod('cloudify.interfaces.lifecycle', 'start')
    def start(self, ctx):
        ctx.run(self, 'scripts/mongo/start-mongo.sh')

    @interfacemethod('cloudify.interfaces.lifecycle', 'create')
    def create(self, ctx):
        ctx.run(self, 'scripts/mongo/install-mongo.sh')

    @interfacemethod('cloudify.interfaces.lifecycle', 'stop')
    def stop(self, ctx):
        ctx.run(self, 'scripts/mongo/stop-mongo.sh')

class MonitoredMongoDatabase(MongoDatabase):
    ''' nodecellar.nodes.MonitoredMongoDatabase '''

    @interfacemethod('cloudify.interfaces.lifecycle', 'start')
    def start(self, ctx):
        ctx.run(self, 'scripts/mongo/start-mongo.sh')

    @interfacemethod('cloudify.interfaces.lifecycle', 'create')
    def create(self, ctx):
        ctx.run(self, 'scripts/mongo/install-mongo.sh')

    @interfacemethod('cloudify.interfaces.lifecycle', 'stop')
    def stop(self, ctx):
        ctx.run(self, 'scripts/mongo/stop-mongo.sh')

    @interfacemethod('cloudify.interfaces.lifecycle', 'configure')
    def configure(self, ctx):
        ctx.run(self, 'scripts/mongo/install-pymongo.sh')

    @interfacemethod('cloudify.interfaces.monitoring', 'start')
    def start_(self, ctx):
        ctx.diamond.diamond_agent.tasks.add_collectors(self, ctx, collectors_config={'MongoDBCollector': {'config': {'hosts': {'concat': ['localhost:', {'get_property': ['SELF', 'port']}]}}}})

class NodeJSServer(cloudify.nodes.ApplicationServer):
    ''' nodecellar.nodes.NodeJSServer '''

    @interfacemethod('cloudify.interfaces.lifecycle', 'create')
    def create(self, ctx):
        ctx.run(self, 'scripts/nodejs/install-nodejs.sh')

class MonitoredServer(cloudify.nodes.Compute):
    ''' nodecellar.nodes.MonitoredServer '''

    @interfacemethod('cloudify.interfaces.monitoring', 'start')
    def start(self, ctx):
        ctx.diamond.diamond_agent.tasks.add_collectors(self, ctx, collectors_config={'CPUCollector': {}, 'DiskUsageCollector': {'config': {'devices': 'x?vd[a-z]+[0-9]*$'}}, 'MemoryCollector': {}, 'LoadAverageCollector': {}, 'NetworkCollector': {}})

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'start')
    def start_(self, ctx):
        ctx.run(self, 'diamond.diamond_agent.tasks.start')

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'stop')
    def stop(self, ctx):
        ctx.run(self, 'diamond.diamond_agent.tasks.stop')

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'install')
    def install(self, ctx):
        ctx.diamond.diamond_agent.tasks.install(self, ctx, diamond_config={'interval': 1})

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'uninstall')
    def uninstall(self, ctx):
        ctx.run(self, 'diamond.diamond_agent.tasks.uninstall')
