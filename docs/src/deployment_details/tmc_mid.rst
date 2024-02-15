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

    #. **Csp Master Leaf Node** : ["01"] 

    #. **Sdp Master Leaf Node** : ["01"]

* b. **subarray_count** : User can set this subarray count according to number of device server deployment instances required for node. 

    Default value for nodes is 2.

    #. **Subarray Node**

    #. **Csp Subarray Leaf Node**

    #. **Sdp Subarray Leaf Node** 

* c. **dish_name** : User can set this by providing the list of TRLS using global.namespace_dish.dish_name

    Default Value for dish leaf node is

    #. **Dish Leaf Node** : ["001", "036", "063", "100"]

* d. **file** : User can provide custom device server configuration file to  nodes.Default is  `configuration files <https://gitlab.com/ska-telescope/ska-tmc/ska-tmc-integration/-/blob/main/charts/ska-tmc-mid/data/>`_

* e. **enabled** : User can opt to disable any node by setting this value to False.Default is True for all nodes.

* f. **tmc_subarray_prefix** : This value is present under global, User can use this to change the FQDN prefix of SubarrayNode.

* g. **csp_subarray_ln_prefix** : This value is present under global, User can use this to change the FQDN prefix of CspSubarrayLeafNode.

* h. **sdp_subarray_ln_prefix** : This value is present under global, User can use this to change the FQDN prefix of SdpSubarrayLeafNode.

* i. **csp_master_ln_prefix** : This value is present under global, User can use this to change the FQDN prefix of CspMasterLeafNode.

* j. **sdp_master_ln_prefix** : This value is present under global, User can use this to change the FQDN prefix of SdpMasterLeafNode.

* k. **csp_subarray_prefix** : This value is present under global, User can use this to change the FQDN prefix of CSP Subarray.

* l. **sdp_subarray_prefix** : This value is present under global, User can use this to change the FQDN prefix of SDP Subarray.

* m. **csp_master** : This value is present under global, User can use this to change the FQDN of CSP Master.

* n. **sdp_master** : This value is present under global, User can use this to change the FQDN of SDP Master.

* o. **dish_suffix** : This value is present under global, User can use this to change the FQDN suffix of Dish Master.


Additional few Central node specific configurations are:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
a. **DishLeafNodePrefix** : User can set this value according to the FQDN prefix required by the deployed dish leaf node devices. Default is  "ska_mid/tm_leaf_node/d0" .

b. **DishIDs** : User can set this value to provide the ID's of dishes present in the deployment. Default is ["SKA001", "SKA036", "SKA063", "SKA100"]
