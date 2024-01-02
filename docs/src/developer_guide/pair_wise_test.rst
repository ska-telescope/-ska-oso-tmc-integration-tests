############################################
TMC MID integration Testing guidelines
#############################################

****************************
Pair wise testing / Real-CSP
****************************

Pair wise testing is way of testing the TMC code with real CSP subsystem in place. 
using latest `test harness` implemented. 

Commands implemented
^^^^^^^^^^^^^^^^^^^^
To test with tmc_csp execute the command `make k8s-test MARK=tmc-csp CSP_SIMULATION_ENABLED=false`.

* ``ON`` -               Testing On command on TMC with Real-CSP in place.
    
* ``Off`` - Testing Off command on TMC  with Real-CSP in place.

* ``AssignResources`` -  Testing AssignResources command on TMC with Real-CSP in place.

* ``Configure`` -  Testing Configure command on TMC with Real-CSP in place.

* ``End`` -  Testing End command on TMC with Real-CSP in place.
    
* ``ReleaseResources`` - Testing ReleaseResources command on TMC with Real-CSP in place.

* ``Standby`` -  Testing StandBy command on TMC with Real-CSP in place.
    


