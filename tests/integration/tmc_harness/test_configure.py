import pytest
# from assertpy import assert_that

from tests.resources.test_harness.helpers import check_subarray_obs_state

class TestSubarrayNodeObsStateTransitions(object):

    @pytest.mark.SKA_mid
    def test_idle_to_ready_valid_data(
        self, subarray_node, command_input_factory
    ):
        # GB put tests in a class, that can be named as
        # "WithSubarrayNodeTransitions" ----> Done

        # GB if you name the test in an evocative way then you
        # can rmove this description string   ----> done
        configure_json = command_input_factory.create_subarray_configuration(
            "configure_mid"
        )
        # GB no parameters given to the factory? something
        # to say for example "generate a valid string"?
        # GB also, why not instantiating an object that
        # acts as a factory as in
        # GB   json_factory is the object, returned by a fixture
        # GB   and then: json_factory.create_ubarray_configuration
        # (< args to specify types of config string to be generated>)

        if (
            subarray_node.state != subarray_node.ON_STATE
        ):  # GB do we have to use literals or can we use constants
            # defined somewhere?
            # like subarray_node.ON_STATE
            subarray_node.move_to_on()

        if subarray_node.obs_state != subarray_node.IDLE_OBS_STATE:
            subarray_node.force_change_obs_state(subarray_node.IDLE_OBS_STATE)

        # GB why do we need to assret this? isn't it guaranteed
        # by the previous method? --> Done

        subarray_node.configure_subarray(configure_json)

        check_subarray_obs_state(obs_state="READY")  #

        # assert_that(subarray_node.obs_state).equals(
        #     subarray_node.READY_OBS_STATE
        # )
        # GB shouldn't we make an assertion here?
        # in case:
        # GB I'm very fond of using assertpy
        # GB 2 reasons: the flueny style comes very handy and
        # it is extensible
        # GB so it could look like this
        # GB assert_that(subarray_node.obs_state).withTimeout
        # (SUBARRAY_NODE_OBSTSTATE_TIMEOUT).equals(subarray_node.IDLE_STATE)
        # GB the above assumes that assert_that() has been
        # extended with 'withTimeout()'.
        # GB no need to do it now - there are mote urgent
        # thinsg to do now - consider
        #  it food for thoughts.

        # GB are there other things that we need to check?
        # GB like some output of the command? or of the state?
