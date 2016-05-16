# This file was converted from input/simple.yaml by ToscaPy on 2016-04-28 19:23:10.378883.

from tosca.interfaceable import interfacemethod
import tosca.blueprint

class Root(tosca.blueprint.Node):
    ''' cloudify.nodes.Root '''

    @interfacemethod('cloudify.interfaces.lifecycle', 'start')
    def start(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.lifecycle', 'create')
    def create(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.lifecycle', 'stop')
    def stop(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.lifecycle', 'configure')
    def configure(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.lifecycle', 'delete')
    def delete(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.validation', 'creation')
    def creation(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.validation', 'deletion')
    def deletion(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.monitoring', 'start')
    def start_(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.monitoring', 'stop')
    def stop_(self, ctx):
        pass

class Router(Root):
    ''' cloudify.nodes.Router '''

class FileSystem(Root):
    ''' cloudify.nodes.FileSystem '''

    def __init__(self, fs_type=None, use_external_resource=False, fs_mount_path=None, partition_type=83):
        '''
        fs_type -- The type of the File System. Supported types are [ext2, ext3, ext4, fat, ntfs, swap]
        use_external_resource -- Enables the use of already formatted volumes.
        fs_mount_path -- The path of the mount point.
        partition_type -- The partition type. 83 is a Linux Native Partition.
        '''
        self.fs_type = fs_type
        self.use_external_resource = use_external_resource
        self.fs_mount_path = fs_mount_path
        self.partition_type = partition_type

    @interfacemethod('cloudify.interfaces.lifecycle', 'configure')
    def configure(self, ctx):
        ctx.script.script_runner.tasks.run(self, ctx, script_path='https://raw.githubusercontent.com/cloudify-cosmo/cloudify-manager/master/resources/rest-service/cloudify/fs/mkfs.sh')

class Compute(Root):
    ''' cloudify.nodes.Compute '''

    def __init__(self, agent_config={'install_method': 'remote', 'port': 22}, ip='', install_agent='', cloudify_agent={}, os_family='linux'):
        '''
        os_family -- Property specifying what type of operating system family this compute node will run.
        '''
        self.agent_config = agent_config
        self.ip = ip
        self.install_agent = install_agent
        self.cloudify_agent = cloudify_agent
        self.os_family = os_family

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'restart_amqp')
    def restart_amqp(self, ctx):
        ctx.executors.host_agent.agent.cloudify_agent.operations.restart(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'configure')
    def configure(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.installer.operations.configure(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'create_amqp')
    def create_amqp(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.operations.create_agent_amqp(self, ctx, install_agent_timeout=300)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'create')
    def create(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.installer.operations.create(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'install_plugins')
    def install_plugins(self, ctx):
        ctx.executors.host_agent.agent.cloudify_agent.operations.install_plugins(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'stop')
    def stop(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.installer.operations.stop(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'start')
    def start(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.installer.operations.start(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'validate_amqp')
    def validate_amqp(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.operations.validate_agent_amqp(self, ctx, validate_agent_timeout=20)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'delete')
    def delete(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.installer.operations.delete(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'restart')
    def restart(self, ctx):
        ctx.executors.central_deployment_agent.agent.cloudify_agent.installer.operations.restart(self, ctx)

    @interfacemethod('cloudify.interfaces.cloudify_agent', 'stop_amqp')
    def stop_amqp(self, ctx):
        ctx.executors.host_agent.agent.cloudify_agent.operations.stop(self, ctx)

    @interfacemethod('cloudify.interfaces.host', 'get_state')
    def get_state(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'start')
    def start_(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'stop')
    def stop_(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'install')
    def install(self, ctx):
        pass

    @interfacemethod('cloudify.interfaces.monitoring_agent', 'uninstall')
    def uninstall(self, ctx):
        pass

class Container(Compute):
    ''' cloudify.nodes.Container '''

class VirtualIP(Root):
    ''' cloudify.nodes.VirtualIP '''

class SoftwareComponent(Root):
    ''' cloudify.nodes.SoftwareComponent '''

class WebServer(SoftwareComponent):
    ''' cloudify.nodes.WebServer '''

    def __init__(self, port=80):
        self.port = port

class Volume(Root):
    ''' cloudify.nodes.Volume '''

class Network(Root):
    ''' cloudify.nodes.Network '''

class SecurityGroup(Root):
    ''' cloudify.nodes.SecurityGroup '''

class ObjectStorage(Root):
    ''' cloudify.nodes.ObjectStorage '''

class DBMS(SoftwareComponent):
    ''' cloudify.nodes.DBMS '''

class ApplicationModule(Root):
    ''' cloudify.nodes.ApplicationModule '''

class CloudifyManager(SoftwareComponent):
    ''' cloudify.nodes.CloudifyManager '''

    def __init__(self, cloudify_packages=None, cloudify={'transient_deployment_workers_mode': {'global_parallel_executions_limit': 50, 'enabled': True}, 'cloudify_agent': {'remote_execution_port': 22, 'max_workers': 5, 'min_workers': 2, 'user': 'ubuntu'}, 'resources_prefix': '', 'policy_engine': {'start_timeout': 30}, 'workflows': {'task_retries': -1, 'task_retry_interval': 30}}):
        '''
        cloudify_packages -- Links to Cloudify packages to be installed on the manager
        cloudify -- Configuration for Cloudify Manager
        '''
        self.cloudify_packages = cloudify_packages
        self.cloudify = cloudify

class Tier(Root):
    ''' cloudify.nodes.Tier '''

class MessageBusServer(SoftwareComponent):
    ''' cloudify.nodes.MessageBusServer '''

class Database(Root):
    ''' cloudify.nodes.Database '''

class LoadBalancer(Root):
    ''' cloudify.nodes.LoadBalancer '''

class Subnet(Root):
    ''' cloudify.nodes.Subnet '''

class ApplicationServer(SoftwareComponent):
    ''' cloudify.nodes.ApplicationServer '''

class Port(Root):
    ''' cloudify.nodes.Port '''
