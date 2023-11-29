# SKA TMC Integration

This project is used to integrate and release the TMC (Telescope Monitoring and Control) subsystem of the SKA telescopes. It includes both TMC Low and TMC Mid.

## Documentation

Click below to access the TMC documentation.

[![Documentation Status](https://readthedocs.org/projects/ska-telescope-ska-tmc-integration/badge/?version=latest)](https://developer.skao.int/projects/ska-tmc-integration/en/latest/)

The documentation for this project, including how to get started with it,can be found in the `docs` folder, and can be better browsed in the SKA development portal:

* [CentralNode documentation](https://developer.skao.int/projects/ska-tmc-centralnode/en/latest/ "SKA Developer Portal: CentralNode documentation")
* [SubarrayNode documentation](https://developer.skao.int/projects/ska-tmc-subarraynode/en/latest/ "SKA Developer Portal: SubarrayNode documentation")
* [CSP Leaf Node documentation](https://developer.skao.int/projects/ska-tmc-cspleafnodes/en/latest/ "SKA Developer Portal: CSP Leaf Nodes documentation")
* [SDP Leaf Node documentation](https://developer.skao.int/projects/ska-tmc-sdpleafnodes/en/latest/ "SKA Developer Portal: SDP Leaf Nodes documentation")
* [Dish Leaf Node documentation](https://developer.skao.int/projects/ska-tmc-dishleafnode/en/latest/ "SKA Developer Portal: Dish Leaf Node documentation")

## TMC Components versions

### TMC Mid

|Component| OCI Name | Version |
| :-- | :-- |:--------|
| Central Node| ska-tmc-centralnode | 0.11.6  |
| Subarray Node| ska-tmc-subarraynode | 0.13.13 |
| CSP Master Leaf Node| ska-tmc-cspleafnodes | 0.10.3  |
| CSP Subarray Leaf Node| ska-tmc-cspleafnodes | 0.10.3  |
| SDP Master Leaf Node| ska-tmc-sdpleafnodes | 0.14.2  |
| SDP Subarray Leaf Node| ska-tmc-sdpleafnodes | 0.14.2  |
| Dish Leaf Node| ska-tmc-dishleafnode | 0.7.0   |


### TMC Low

|Component| OCI Name | Version |
| :-- | :-- |:--------|
| Central Node| ska-tmc-centralnode | 0.11.8  |
| Subarray Node| ska-tmc-subarraynode | 0.13.11 |
| CSP Master Leaf Node| ska-tmc-cspleafnodes | 0.9.2   |
| CSP Subarray Leaf Node| ska-tmc-cspleafnodes | 0.10.1   |
| SDP Master Leaf Node| ska-tmc-sdpleafnodes | 0.13.2  |
| SDP Subarray Leaf Node| ska-tmc-sdpleafnodes | 0.13.2  |


### Deployment of Subsystem in Integration 
 #### Deployment of Dish LMC Helm Chart
 * To Deploy dish lmc chart in integration run following command
    ```bash
    make k8s-install-chart-car KUBE_NAMESPACE=<KUBE_NAMESPACE> K8S_CHART_PARAMS='-f charts/dish_lmc_values.yml 
      --set "global.dishes={001}"' 
      HELM_RELEASE=<DISH_LMC_HELM_RELEASE> K8S_CHART=<DISH_LMC_CHART_NAME>
    ```
    All values required for deploying dish lmc can be provided in charts/dish_lmc_values.yml file.

    Refer this link for set flag option https://gitlab.com/ska-telescope/ska-dish-lmc#-set-flag-options
    
    After running above command dish lmc with dish Id 001 deployed in provided Kubernetes Namespace(i.e KUBE_NAMESPACE)

    To deploy multiple dishes provide multiple values to global.dishes. 
    Example: `global.dishes={036,002,...}`

 * Uninstall dish lmc chart
    ```bash
    make k8s-do-uninstall-chart KUBE_NAMESPACE=<KUBE_NAMESPACE> HELM_RELEASE=<DISH_LMC_HELM_RELEASE> K8S_CHART=<DISH_LMC_CHART_NAME>
    ```
 * Test dish lmc with TMC as an entrypoint
    To test Dish LMC within the TMC integration, you can set a specific flag to control whether you want to use a real device or a mock device. Here's how you can do it:
    ```bash
    --set global.Dish.isSimulated.enabled=true or false
    ```
    If you set "enabled" to true, Dish LMC will use a mock device for testing and if you set "enabled" to false, Dish LMC will use a real device for testing.

