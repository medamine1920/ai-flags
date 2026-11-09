import pytest
from sdk.aiflags.hashing import bucket, in_rollout

def test_separator_prevents_collisions():
    assert bucket("ab", "c") != bucket("a", "bc")


def test_invalid_percentage_is_rejected():
    with pytest.raises(ValueError):
        in_rollout("f", "u", 150)