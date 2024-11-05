from typing import TypeVar, Generator, Any

T = TypeVar("T")


class PriorityQueueEmptyError(Exception):
    pass


class ElementNotComparableError(Exception):
    pass


class PriorityQueue[T]:
    def __init__(self, *element: T) -> None:
        self._queue = [*element]

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

        self._queue = [element] + self._queue

    def pop(self) -> T:
        if self.is_empty:
            raise PriorityQueueEmptyError(
                "The queue is empty. Impossible to remove an element"
            )

        return self._queue.pop(self._queue.index(self.element))

    @property
    def is_empty(self) -> bool:
        return len(self._queue) == 0

    @property
    def element(self) -> T:
        if self.is_empty:
            raise PriorityQueueEmptyError(
                "The queue is empty. Impossible to retrieve an element"
            )
        return min(self._queue)  # type: ignore

    def __iter__(self) -> Generator[T, Any, None]:
        for e in self._queue:
            yield e

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
