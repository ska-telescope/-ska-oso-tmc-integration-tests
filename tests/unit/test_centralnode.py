import pytest

from ska_oso_tmcsim import get_centralnode_trl


@pytest.mark.parametrize(
    "domain,expected",
    [
        pytest.param(
            "ska_mid", "ska_mid/tm_central/central_node", id="pre-ADR-9 TMC-Mid"
        ),
        pytest.param(
            "ska_low", "ska_low/tm_central/central_node", id="pre-ADR-9 TMC-Low"
        ),
        pytest.param("mid-tmc", "mid-tmc/central-node/0", id="ADR-9 TMC-Mid"),
        pytest.param("low-tmc", "low-tmc/central-node/0", id="ADR-9 TMC-Low"),
    ],
)
def test_get_centralnode_trl(domain, expected: str):
    """
    Verify that CentralNode TRLs are correct for pre- and post-ADR-9.
    """
    cn_trl = get_centralnode_trl(domain)
    assert cn_trl == expected
