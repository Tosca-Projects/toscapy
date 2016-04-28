ToscaPy
=======

An _experimental_ toolkit for using [OASIS TOSCA](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=tosca) bluebrints in Python, specifically for consuming the [YAML Simple Profile specification](http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html). In particular, it is oriented around [Cloudify](http://getcloudify.org/)'s extended DSL.

It works by converting the YAML into clean, idiomatic, "pythonic" Python. Once you're in Python, life is good: you can forget about YAML and its limitations and work in a fully programmable environment.

Why Python? Ruby, for example, might be better suited for crafting DSLs. But the potential cleanliness and readability of Python are unmatched. It is a favorite language for cloud scripting.

The starting point is a `tosca.py` command, which is extensible by attaching your own "engines" to handle commands. Thus you can build a pipeline starting with the YAML, transparently translating it into Python in the first step, and then going on to do great things, such as deploying your blueprint in a cloud, creating a monitoring profile for it, etc.

TOSCA's object-oriented declarative format lends itself pretty well to being implemented in Python ... for the most part:

* `node_types`, `data_types`, and `relationships` become Python classes. Obviously.
* `node_templates` become instances of these `node_types` classes.
* `inputs` become method arguments.
* `properties` become class properties, and in some cases are initialized by class constructors. 
* Python supports a dot notation for namespaces, though it does require multiple files and directories to achieve it, and these will. This actually lends itself to nicely organized code.
* This means that YAML `imports` do not exactly become Python imports. Python imports depend on the namespace structure.
* Python does not support interface-oriented programming, though this is used extensively in TOSCA. For this reason, we've implemented our own little [interface mechanism for Python](toscapy/blob/master/tosca/interfaceable.py). It could be useful in other projects, too!

Quickstart
----------

Requirements (Ubuntu):

    sudo apt install python-setuptools python-dev libyaml-dev
    sudo easy_install pip
    sudo pip install virtualenv

ToscaPy:

    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt

Run the example:

    tosca/tosca.py convert input/simple.yaml

See the Python output in the `output` directory. Yay! You can give it a test run like so (it does nothing, but you'll see that it's real Python):

    PYTHONPATH=$PYTHONPATH:tosca python output/simple.py

The example is taken from the [Cloudify NodeCellar Example](https://github.com/cloudify-cosmo/cloudify-nodecellar-example).

TODO
----

Support `policy_types` and `policy_triggers`
