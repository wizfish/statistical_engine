"""Statistical engine package."""

from .stat_engine import StatEngine, StatEngineError, EmptyDataError, DataTypeError
from .monte_carlo import simulate_crashes
