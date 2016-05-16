# This file was converted from input/simple.yaml by ToscaPy on 2016-04-28 19:23:10.378829.

from tosca.interfaceable import interfacemethod
import tosca.blueprint

class AgentConfig(tosca.blueprint.Data):
    ''' cloudify.datatypes.AgentConfig '''

    def __init__(self, install_method=None, password=None, disable_requiretty=None, key=None, extra=None, process_management=None, max_workers=None, user=None, env=None, min_workers=None, port=None):
        '''
        install_method -- Specifies how (and if) the cloudify agent should be installed. Valid values are: * none - No agent will be installed on the host. * remote - An agent will be installed using SSH on linux hosts and WinRM on windows hosts. * init_script - An agent will be installed via a script that will run on the host when it gets created.                 This method is only supported for specific IaaS plugins. * provided - An agent is assumed to already be installed on the host image.              That agent will be configured and started via a script that will run on the host when it gets created.              This method is only supported for specific IaaS plugins.
        password -- For host agents that are installed via SSH (on linux) and WinRM (on windows) this property can be used to connect to the host. For linux hosts, this property is optional in case the key property is properly configured (either explicitly or implicitly during bootstrap). For windows hosts that are installed via WinRM, this property is also optional and depends on whether the password runtime property has been set by the relevant IaaS plugin, prior to the agent installation.
        disable_requiretty -- For linux based agents, disables the requiretty setting in the sudoers file. By default, this value will be true.
        key -- For host agents that are installed via SSH, this is the path to the private key that will be used to connect to the host. In most cases, this value will be derived automatically during bootstrap.
        extra -- Optional additional low level configuration details. (type: dictionary)
        process_management -- Process management specific configuration. (type: dictionary)
        max_workers -- Maximum number of agent workers. By default, the value will be 5.
        user -- For host agents, the agent will be installed for this user.
        env -- Optional environment variables that the agent will be started with. (type: dictionary)
        min_workers -- Minimum number of agent workers. By default, the value will be 0. Note: For windows based agents, this property is ignored and min_workers is set to the value of max_workers.
        port -- For host agents that are installed via SSH (on linux) and WinRM (on windows), this is the port used to connect to the host. The default values are 22 for linux hosts and 5985 for windows hosts.
        '''
        self.install_method = install_method
        self.password = password
        self.disable_requiretty = disable_requiretty
        self.key = key
        self.extra = extra
        self.process_management = process_management
        self.max_workers = max_workers
        self.user = user
        self.env = env
        self.min_workers = min_workers
        self.port = port
