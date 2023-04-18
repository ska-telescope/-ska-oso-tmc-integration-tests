import pytest
import tango
from pytest_bdd import given, parsers, scenarios, then, when


@given(parsers.parse(
    "the TMC device/s state=On and obsState {initial_obsstate}")
)
def given_tmc():
    pass


@when(
    parsers.parse("the command {unexpected_command} is invoked"))

def send_command():
    pass


@then("the command {unexpected_command} shows an error")
def command_responce():
    pass

@then(parsers.parse("the TMC device remains in state=On, and obsState {initial_obsstate}"))
def tmc_status():
   pass

@then(parsers.parse("TMC accepts correct/expected command {expected_command} and performs the operation"))
def tmc_accepts_next_commands():
    pass

scenarios("../features/check_command_not_allowed.feature")
