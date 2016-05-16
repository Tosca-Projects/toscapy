# This file was converted from input/simple.yaml by ToscaPy on 2016-04-28 19:23:10.378954.

from tosca.interfaceable import interfacemethod
import cloudify.relationships
import tosca.blueprint
import nodecellar.nodes

class node_contained_in_nodejs(cloudify.relationships.contained_in):
    ''' simple.node_contained_in_nodejs '''

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'preconfigure')
    def preconfigure(self, ctx):
        ctx.run(self, 'scripts/nodejs/set-nodejs-root.sh')

class node_connected_to_mongo(cloudify.relationships.connected_to):
    ''' simple.node_connected_to_mongo '''

    @interfacemethod('cloudify.interfaces.relationship_lifecycle', 'postconfigure')
    def postconfigure(self, ctx):
        ctx.run(self, 'scripts/mongo/set-mongo-url.sh', mongo_ip_address='')

class Blueprint(tosca.blueprint.Blueprint):
    '''
    This Blueprint installs the nodecellar application on an existing host.
    '''

    def __init__(self, ctx, agent_private_key_path, agent_user, host_ip):
        '''
        agent_private_key_path -- Path to a private key that resided on the management machine. SSH-ing into agent machines will be done with this key.
        agent_user -- User name used when SSH-ing into the started machine
        host_ip -- The ip of the host the application will be deployed on
        '''
        self.agent_private_key_path = agent_private_key_path
        self.agent_user = agent_user
        self.host_ip = host_ip

        ctx.blueprint = self

        # Plugins
        setattr(ctx, 'diamond', ctx.host_agent(ctx))
        setattr(ctx, 'default_workflows', ctx.central_deployment_agent(ctx))
        setattr(ctx, 'agent', ctx.central_deployment_agent(ctx))
        setattr(ctx, 'script', ctx.host_agent(ctx))

        # Node templates

        self.host = nodecellar.nodes.MonitoredServer()
        self.host.ip = self.host_ip

        self.mongod = nodecellar.nodes.MonitoredMongoDatabase()
        self.mongod.relate(ctx, self.host, cloudify.relationships.contained_in)

        self.nodejs = nodecellar.nodes.NodeJSServer()
        self.nodejs.relate(ctx, self.host, cloudify.relationships.contained_in)

        self.nodecellar = nodecellar.nodes.NodecellarApplicationModule()
        r = self.nodecellar.relate(ctx, self.mongod, node_connected_to_mongo)
        i = r.interface['cloudify.interfaces.relationship_lifecycle']
        i.postconfigure(mongo_ip_address='localhost')
        self.nodecellar.relate(ctx, self.nodejs, node_contained_in_nodejs)

    # Outputs

    def get_endpoint(self, ctx):
        '''
        Web application endpoint
        '''
        endpoint = {}
        endpoint['ip_address'] = self.host.ip
        endpoint['port'] = self.nodecellar.port
        return endpoint

    # Workflows

    def do_execute_operation(self, ctx, operation_kwargs={}, node_instance_ids=[], node_ids=[], run_by_dependency_order=False, operation=None, allow_kwargs_override=None, type_names=[]):
        ctx.default_workflows.cloudify.plugins.workflows.execute_operation(ctx, operation_kwargs, node_instance_ids, node_ids, run_by_dependency_order, operation, allow_kwargs_override, type_names)

    def do_scale(self, ctx, node_id=None, scale_compute=True, delta=1):
        '''
        node_id -- Which node (not node instance) to scale
        scale_compute -- If node is contained (transitively) within a compute node and this property is 'true', operate on compute node instead of 'node_id'
        delta -- How many nodes should be added/removed. A positive number denotes increase of instances. A negative number denotes decrease of instances.
        '''
        ctx.default_workflows.cloudify.plugins.workflows.scale(ctx, node_id, scale_compute, delta)

    def do_install(self, ctx):
        ctx.default_workflows.cloudify.plugins.workflows.install(ctx)

    def do_heal(self, ctx, diagnose_value='Not provided', node_instance_id=None):
        '''
        diagnose_value -- Diagnosed reason of failure
        node_instance_id -- Which node instance has failed
        '''
        ctx.default_workflows.cloudify.plugins.workflows.auto_heal_reinstall_node_subgraph(ctx, diagnose_value, node_instance_id)

    def do_uninstall(self, ctx):
        ctx.default_workflows.cloudify.plugins.workflows.uninstall(ctx)

    def do_update(self, ctx, remove_target_instance_ids=[], added_instance_ids=[], reduce_target_instance_ids=[], reduced_instance_ids=[], modified_entity_ids=[], added_target_instances_ids=[], update_id='', removed_instance_ids=[], extend_target_instance_ids=[], extended_instance_ids=[]):
        ctx.default_workflows.cloudify.plugins.workflows.update(ctx, remove_target_instance_ids, added_instance_ids, reduce_target_instance_ids, reduced_instance_ids, modified_entity_ids, added_target_instances_ids, update_id, removed_instance_ids, extend_target_instance_ids, extended_instance_ids)

    def do_install_new_agents(self, ctx, validate=True, node_instance_ids=[], install_agent_timeout=300, install=True, node_ids=[]):
        ctx.default_workflows.cloudify.plugins.workflows.install_new_agents(ctx, validate, node_instance_ids, install_agent_timeout, install, node_ids)
