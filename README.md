# Statistical Engineering & Simulation Assessment

## Project Overview
This project builds a pure-Python statistical engine from scratch and uses it to analyze a mock salary dataset and simulate startup server crashes with Monte Carlo methods.

The repository is split into:
- `src/` for the reusable engine and simulation code
- `tests/` for the unit tests
- `data/` for the mock salary dataset
- `main.py` as the entry point for the full analysis

## Mathematical Logic

### Mean
\[
\bar{x} = \frac{\sum x_i}{n}
\]

### Median
- If the list length is odd, the middle value after sorting is the median.
- If the list length is even, the median is the average of the two middle values.

### Variance
Population variance:
\[
\sigma^2 = \frac{\sum (x_i - \mu)^2}{n}
\]

Sample variance:
\[
s^2 = \frac{\sum (x_i - \bar{x})^2}{n-1}
\]

The code uses Bessel’s correction for sample variance by dividing by `n - 1`.

### Standard Deviation
\[
\sigma = \sqrt{\sigma^2}
\]

### Outliers
A value is treated as an outlier when:

\[
|x - \bar{x}| > threshold \times \text{standard deviation}
\]

### Monte Carlo Simulation
Each day is simulated with:
- probability of crash = `0.045`
- a random number is drawn from `random.random()`
- if the number is below `0.045`, that day is counted as a crash

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-public-github-repo-url>
cd statistical_engine
```

### 2. Run the program
```bash
python main.py
```

## Testing
Run the test suite with:

```bash
python -m unittest discover -s tests
```

## Acceptance Criteria Checklist
- [x] Handles empty list input with a descriptive error
- [x] Cleans numeric strings in mixed data
- [x] Raises descriptive TypeError for invalid values like `None`
- [x] Calculates mean correctly
- [x] Calculates median correctly for odd and even lists
- [x] Calculates population variance
- [x] Calculates sample variance using Bessel’s correction
- [x] Calculates standard deviation from variance
- [x] Detects outliers by standard deviation threshold
- [x] Handles multimodal data by returning all modes
- [x] Returns a specific message when all values are unique
- [x] Includes Monte Carlo simulation for server crashes
- [x] Includes `unittest` coverage for core behavior

## Why the 30-day result is dangerous
A 30-day sample is tiny. With a small sample, the observed crash rate can wander far away from 4.5% by pure chance. That makes budget planning shaky if the startup assumes one short trial tells the full story. Over a larger simulation, the result tends to drift toward the theoretical probability, which is the Law of Large Numbers in action.
