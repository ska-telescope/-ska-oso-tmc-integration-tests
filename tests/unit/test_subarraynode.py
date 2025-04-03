import pytest

from ska_oso_tmcsim import get_subarraynode_trl


@pytest.mark.parametrize(
    "domain,subarray_id,expected",
    [
        pytest.param(
            "ska_mid",
            1,
            "ska_mid/tm_subarray_node/1",
            id="pre-ADR-9 TMC-Mid single digit ID",
        ),
        pytest.param(
            "ska_mid",
            16,
            "ska_mid/tm_subarray_node/16",
            id="pre-ADR-9 TMC-Mid SAN double digit ID",
        ),
        pytest.param(
            "ska_low",
            1,
            "ska_low/tm_subarray_node/1",
            id="pre-ADR-9 TMC-Low single digit ID",
        ),
        pytest.param(
            "ska_low",
            16,
            "ska_low/tm_subarray_node/16",
            id="pre-ADR-9 TMC-Low SAN double digit ID",
        ),
        pytest.param(
            "mid-tmc",
            1,
            "mid-tmc/subarray/01",
            id="ADR-9 TMC-Mid single digit ID",
        ),
        pytest.param(
            "mid-tmc",
            16,
            "mid-tmc/subarray/16",
            id="ADR-9 TMC-Mid SAN double digit ID",
        ),
        pytest.param(
            "low-tmc",
            1,
            "low-tmc/subarray/01",
            id="ADR-9 TMC-Low single digit ID",
        ),
        pytest.param(
            "low-tmc",
            16,
            "low-tmc/subarray/16",
            id="ADR-9 TMC-Low SAN double digit ID",
        ),
    ],
)
def test_get_subarraynode_trl(domain: str, subarray_id: int, expected: str):
    """
    Verify that CentralNode TRLs are correct for pre- and post-ADR-9.
    """
    san_trl = get_subarraynode_trl(domain, subarray_id)
    assert san_trl == expected
