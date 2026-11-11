import pytest

from aiflags.hashing import bucket, in_rollout


def test_same_user_always_gets_same_bucket():
    assert bucket("subject_gen_v2", "sara") == bucket("subject_gen_v2", "sara")


def test_bucket_is_in_range():
    for i in range(1000):
        assert 0 <= bucket("subject_gen_v2", f"user_{i}") <= 9999


def test_rollout_percentage_is_respected():
    users = [f"user_{i}" for i in range(100_000)]
    inside = sum(in_rollout("subject_gen_v2", u, 10) for u in users)
    assert 9_500 <= inside <= 10_500  # about 10%, with a little randomness


def test_zero_and_hundred_percent():
    assert not any(in_rollout("f", f"u{i}", 0) for i in range(1000))
    assert all(in_rollout("f", f"u{i}", 100) for i in range(1000))


def test_increasing_rollout_never_removes_users():
    # A user who has the new version at 5% must still have it at 25%
    for i in range(5000):
        u = f"user_{i}"
        if in_rollout("subject_gen_v2", u, 5):
            assert in_rollout("subject_gen_v2", u, 25)


def test_different_flags_pick_different_users():
    # With 2 flags at 10%, about 10% x 10% = 1% of users should get both.
    # If we hashed only user_id, the SAME 10% would get both.
    users = [f"user_{i}" for i in range(20_000)]
    both = sum(in_rollout("flag_a", u, 10) and in_rollout("flag_b", u, 10) for u in users)
    assert both / len(users) < 0.02


def test_separator_prevents_collisions():
    assert bucket("ab", "c") != bucket("a", "bc")


def test_invalid_percentage_is_rejected():
    with pytest.raises(ValueError):
        in_rollout("f", "u", 150)