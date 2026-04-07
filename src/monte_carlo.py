"""Monte Carlo simulation for startup server crashes."""

from __future__ import annotations

import random
from typing import Dict, Optional


def simulate_crashes(days: int, crash_probability: float = 0.045, seed: Optional[int] = None) -> Dict[str, float]:
    """
    Simulate daily crashes over a number of days.

    Returns a dictionary with total crashes and simulated crash probability.
    """
    if not isinstance(days, int):
        raise TypeError("days must be an integer.")
    if days <= 0:
        raise ValueError("days must be a positive integer.")
    if not 0 <= crash_probability <= 1:
        raise ValueError("crash_probability must be between 0 and 1.")

    if seed is not None:
        random.seed(seed)

    crashes = 0
    for _ in range(days):
        if random.random() < crash_probability:
            crashes += 1

    return {
        "days": days,
        "crashes": crashes,
        "simulated_probability": crashes / days,
    }
