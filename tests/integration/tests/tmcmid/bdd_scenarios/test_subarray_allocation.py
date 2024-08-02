"""
Verify we can run scripts again a TMC simulator.
"""

import dataclasses
import importlib
import sys

from pytest_bdd import given, parsers, scenarios, then, when
from ska_control_model import ObsState

from tests.integration.tests.conftest import EventsSummary, event_recorder
from tests.resources.test_harness.central_node import CentralNodeWrapper
from tests.resources.test_harness.subarray_node import SubarrayNodeWrapper
from tests.resources.test_harness.tmc_mid import TMCMid

scenarios("mid/subarray_allocation.feature")


@dataclasses.dataclass
class TMCContext:
    tmc_mid: TMCMid
    cn_wrapper: CentralNodeWrapper
    san_wrapper: SubarrayNodeWrapper


@dataclasses.dataclass
class TestContext:
    events: EventsSummary
    command_history: list


@given("a telescope control system", target_fixture="tmc_context")
def new_tmccontext(tmc_mid, subarray_node) -> TMCContext:
    return TMCContext(
        tmc_mid=tmc_mid,
        cn_wrapper=tmc_mid.central_node,
        san_wrapper=subarray_node,
    )


@given(parsers.parse("{obsstate} subarray {subarray_id:d}"))
def add_subarray_with_obsstate(tmc_context: TMCContext, obsstate, subarray_id):
    if subarray_id != 1:
        raise NotImplementedError("TMC harness only supports one subarray")

    initial_obsstate = getattr(ObsState, obsstate)
    match initial_obsstate:
        case ObsState.IDLE:
            kwargs = dict(assign_input_json="")
        case ObsState.READY:
            kwargs = dict(assign_input_json="", configure_input_json="")
        case ObsState.EMPTY:
            kwargs = {}
        case _:
            raise NotImplementedError(f"ObsState {obsstate} not supported")

    tmc_context.cn_wrapper.move_to_on()
    tmc_context.san_wrapper.move_to_on()
    tmc_context.san_wrapper.force_change_of_obs_state(obsstate, **kwargs)


@when(
    parsers.parse("I run {script} on subarray {subarray_id:d} with SBD {sbd}"),
    target_fixture="ctx",
)
def run_observing_script(tmc_context: TMCContext, script, subarray_id, sbd, constants):
    spec = importlib.util.spec_from_file_location(
        "my.observing.script", constants["SCRIPTS_DIR"] / script
    )
    foo = importlib.util.module_from_spec(spec)
    sys.modules["my.observing.script"] = foo
    spec.loader.exec_module(foo)

    # oso_constants.DEFAULT_TIMEOUT_FOR_ASSIGN_RESOURCE_CMD = 120

    with event_recorder(tmc_context.san_wrapper) as events:
        foo.init(subarray_id)
        foo.main(constants["DATA_DIR"] / "sbds" / sbd, "test_SBI")

        summary = EventsSummary(events)

    results = TestContext(events=summary, command_history=[])

    return results


@then(parsers.parse("the subarray obsState passes through {obsstate} {count:d} times"))
def assert_obsstate_count(ctx: TestContext, obsstate, count):
    obsstate_enum = ObsState[obsstate]
    assert ctx.events.obsstate_counts[obsstate_enum] == count


@then(parsers.parse("the final obsState is {obsstate}"))
def assert_final_obsstate(ctx: TestContext, obsstate):
    obsstate_enum = ObsState[obsstate]
    assert ctx.events.final_obsstate == obsstate_enum
