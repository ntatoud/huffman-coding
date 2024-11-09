from typing import NamedTuple

from src.counter import Counter


class Statistics[T](NamedTuple):
    counter: Counter
    length: int
