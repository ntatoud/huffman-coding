from bisect import insort
from typing import TypeVar, Any, Iterator, List

T = TypeVar("T")


class PriorityQueueEmptyError(Exception):
    pass


class ElementNotComparableError(Exception):
    pass


class PriorityQueue[T]:
    def __init__(self, element=(), key=lambda e: e) -> None:
        self._key = key
        self._queue: List[T] = sorted([*element], key=self._key)

    @staticmethod
    def compare(element: Any, other: Any) -> bool:
        return element < other

    @staticmethod
    def compare_or_fail(element: Any, other: Any, message="") -> None:
        try:
            PriorityQueue.compare(element, other)
        except TypeError:
            raise ElementNotComparableError(message)

    def append(self, element: Any):
        if self.is_empty:
            PriorityQueue.compare_or_fail(
                element,
                element,
                f"The class of {repr(element)} do not posess comparison methods",
            )
        else:
            PriorityQueue.compare_or_fail(
                element,
                self.element,
                f"{repr(element)} can not be compared to {self.element}",
            )

        insort(self._queue, element, key=self._key)

    def pop(self) -> T:
        if self.is_empty:
            raise PriorityQueueEmptyError(
                "The queue is empty. Impossible to remove an element"
            )

        return self._queue.pop(0)

    @property
    def is_empty(self) -> bool:
        return len(self._queue) == 0

    @property
    def element(self) -> T:
        if self.is_empty:
            raise PriorityQueueEmptyError(
                "The queue is empty. Impossible to retrieve an element"
            )

        return self._queue[0]

    def __iter__(self) -> Iterator[T]:
        return iter(self._queue)

    def __len__(self) -> int:
        return len(self._queue)

    def __eq__(self, other) -> bool:
        if len(self) != len(other):
            return False

        for s, a in zip(self, other):
            if s != a:
                return False
        return True

    def __repr__(self) -> str:
        return f"PriorityQueue({repr(self._queue)})".replace("[", "").replace("]", "")

    def __str__(self) -> str:
        return str(self._queue).replace("[", "").replace("]", "")
