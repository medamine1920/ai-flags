"""Deterministic user bucketing for percentage rollouts."""

import hashlib

BUCKETS = 10_000  # 0.01% precision: 1% = 100 buckets


def bucket(flag_key: str, user_id: str) -> int:
    """Return a number from 0 to 9999. Same inputs -> same number, always."""
    key = f"{flag_key}:{user_id}".encode("utf-8")
    digest = hashlib.sha256(key).hexdigest()
    return int(digest[:15], 16) % BUCKETS


def in_rollout(flag_key: str, user_id: str, rollout_pct: float) -> bool:
    """True if this user is inside the rollout percentage (0-100)."""
    if not 0 <= rollout_pct <= 100:
        raise ValueError(f"rollout_pct must be between 0 and 100, got {rollout_pct}")
    return bucket(flag_key, user_id) < rollout_pct * (BUCKETS / 100)