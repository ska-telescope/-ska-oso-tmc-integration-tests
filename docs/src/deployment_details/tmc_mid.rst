TMC Mid Deployment
=======================

TMC Mid deployment comes with following components:

1. **Central Node** 

2. **Subarray Node**

3. **Csp Master Leaf Node**

4. **Csp Subarray Leaf Node**

5. **Sdp Master Leaf Node**

6. **Sdp Subarray Leaf Node**

7. **Dish Leaf Node**

Configurable options
--------------------

* a. **instances** : User can provide the array of device server deployment instances required for node.

    Default for nodes are:

    #. **Central Node** : ["01"] 

    #. **Subarray Node** :["01", "02"]

    #. **Csp Master Leaf Node** : ["01"] 

    #. **Csp Subarray Leaf Node** : ["01", "02"]

    #. **Sdp Master Leaf Node** : ["01"]

    #. **Sdp Subarray Leaf Node** : ["01", "02"]

    #. **Dish Leaf Node** : ["01", "02"]

* b. **file** : User can provide custom device server configuration file to  nodes.Default is  `configuration files <https://gitlab.com/ska-telescope/ska-tmc/ska-tmc-integration/-/blob/main/charts/ska-tmc-mid/data/>`_

* c. **enabled** : User can opt to disable any node by setting this value to False.Default is True for all nodes.

* d. **CspMasterFQDN** : This value is present under csp master leaf node device server, User can use this to change the FQDN of csp master.

* e. **SdpMasterFQDN** : This value is present under sdp master leaf node device server, User can use this to change the FQDN of sdp master.

Additional few Central node specific configurations are:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
a. **subarray_count** : User can set this subarray count according to number of subarray node devices  are deployed. default is 2. 

b. **DishLeafNodePrefix** : User can set this value according to the FQDN prefix required by the deployed dish leaf node devices. Default is  "ska_mid/tm_leaf_node/d0" .

c. **DishIDs** : User can set this value to provide the ID's of dishes present in the deployment. Default is ["SKA001", "SKA002", "SKA003", "SKA004"]