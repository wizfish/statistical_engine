"""Entry point for the statistical engineering assessment."""

from __future__ import annotations

import json
from pathlib import Path

from src.monte_carlo import simulate_crashes
from src.stat_engine import StatEngine


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sample_salaries.json"


def load_salaries(path: Path):
    with path.open("r", encoding="utf-8") as f:
        records = json.load(f)
    salaries = [record["salary"] for record in records]
    return records, salaries


def print_salary_analysis(engine: StatEngine) -> None:
    print("=== Salary Dataset Analysis ===")
    print(f"Count: {len(engine.data)}")
    print(f"Mean: {engine.get_mean():.2f}")
    print(f"Median: {engine.get_median():.2f}")
    print(f"Mode: {engine.get_mode()}")
    print(f"Population variance: {engine.get_variance(is_sample=False):.2f}")
    print(f"Sample variance: {engine.get_variance(is_sample=True):.2f}")
    print(f"Population standard deviation: {engine.get_standard_deviation(is_sample=False):.2f}")
    print(f"Sample standard deviation: {engine.get_standard_deviation(is_sample=True):.2f}")
    print(f"Outliers (threshold=2): {engine.get_outliers(threshold=2)}")
    print()


def print_lln_demo() -> None:
    print("=== Monte Carlo Server Crash Simulation ===")
    for days, seed in [(30, 7), (365, 7), (10000, 7)]:
        result = simulate_crashes(days, crash_probability=0.045, seed=seed)
        print(
            f"{days:5d} days -> crashes: {result['crashes']:4d}, "
            f"simulated probability: {result['simulated_probability']:.4%}"
        )
    print()
    print("Interpretation:")
    print(
        "With only 30 days, the simulated crash rate can swing wildly because the sample is small."
    )
    print(
        "By 10,000 days, the simulated rate usually settles closer to the theoretical 4.5%."
    )
    print(
        "That is the Law of Large Numbers quietly pulling the distribution toward its true probability."
    )


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing dataset: {DATA_FILE}")

    records, salaries = load_salaries(DATA_FILE)
    engine = StatEngine(salaries)

    print(f"Loaded {len(records)} salary records from {DATA_FILE.name}")
    print_salary_analysis(engine)
    print_lln_demo()


if __name__ == "__main__":
    main()
