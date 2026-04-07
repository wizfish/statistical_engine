"""Core statistical engine built with standard-library Python only."""

from __future__ import annotations

from math import sqrt
from typing import Iterable, List, Sequence, Union


Number = Union[int, float]


class StatEngineError(Exception):
    """Base class for StatEngine errors."""


class EmptyDataError(StatEngineError, ValueError):
    """Raised when statistical operations are attempted on empty data."""


class DataTypeError(StatEngineError, TypeError):
    """Raised when non-numeric data cannot be cleaned safely."""


class StatEngine:
    """
    A small statistics engine for 1D numerical data.

    It accepts lists or tuples of numbers. Numeric strings are cleaned and
    converted to floats. Values such as None, booleans, and non-numeric strings
    raise a descriptive DataTypeError.
    """

    def __init__(self, data: Sequence[object]):
        if not isinstance(data, (list, tuple)):
            raise DataTypeError(
                f"StatEngine expects a list or tuple, got {type(data).__name__}."
            )

        self.raw_data = list(data)
        self.data = self._clean_data(self.raw_data)

        if len(self.data) == 0:
            raise EmptyDataError(
                "StatEngine cannot work with an empty numeric dataset."
            )

    @staticmethod
    def _coerce_number(value: object) -> float:
        if isinstance(value, bool):
            raise DataTypeError("Boolean values are not valid numeric data.")
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise DataTypeError("Empty strings are not valid numeric data.")
            try:
                return float(stripped)
            except ValueError as exc:
                raise DataTypeError(
                    f"String value '{value}' cannot be converted to a number."
                ) from exc
        raise DataTypeError(
            f"Unsupported data type '{type(value).__name__}' encountered: {value!r}."
        )

    def _clean_data(self, data: Iterable[object]) -> List[float]:
        cleaned: List[float] = []
        for item in data:
            cleaned.append(self._coerce_number(item))
        return cleaned

    def _require_data(self) -> None:
        if len(self.data) == 0:
            raise EmptyDataError("Statistical operation failed because data is empty.")

    def get_mean(self) -> float:
        self._require_data()
        return sum(self.data) / len(self.data)

    def get_median(self) -> float:
        self._require_data()
        ordered = sorted(self.data)
        n = len(ordered)
        mid = n // 2

        if n % 2 == 1:
            return ordered[mid]
        return (ordered[mid - 1] + ordered[mid]) / 2

    def get_mode(self):
        """
        Return a list of all modes.

        If all values are unique, return a specific message string.
        """
        self._require_data()

        counts = {}
        for value in self.data:
            counts[value] = counts.get(value, 0) + 1

        highest_frequency = max(counts.values())
        if highest_frequency == 1:
            return "No mode: all values are unique."

        modes = [value for value, count in counts.items() if count == highest_frequency]
        return sorted(modes)

    def get_variance(self, is_sample: bool = True) -> float:
        self._require_data()
        n = len(self.data)

        if is_sample and n < 2:
            raise ValueError("Sample variance requires at least two data points.")

        mean = self.get_mean()
        squared_diffs = [(value - mean) ** 2 for value in self.data]

        denominator = n - 1 if is_sample else n
        return sum(squared_diffs) / denominator

    def get_standard_deviation(self, is_sample: bool = True) -> float:
        return sqrt(self.get_variance(is_sample=is_sample))

    def get_outliers(self, threshold: float = 2) -> List[float]:
        """
        Return values greater than threshold standard deviations away from the mean.
        """
        self._require_data()
        if threshold < 0:
            raise ValueError("threshold must be non-negative.")

        mean = self.get_mean()
        std_dev = self.get_standard_deviation(is_sample=True)

        if std_dev == 0:
            return []

        distance = threshold * std_dev
        return [value for value in self.data if abs(value - mean) > distance]
