from typing import TypeVar, Generator, Any

T = TypeVar("T")


class PriorityQueueEmptyError(Exception):
    pass


class ElementNotComparableError(Exception):
    pass


class PriorityQueue[T]:
    def __init__(self, *element: T) -> None:
        self._queue = [*element]

    @property
    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def append(self, element: T):
        if self.is_empty:
            try:
                element < element  # type: ignore
            except TypeError:
                raise ElementNotComparableError(
                    f"The class of {repr(element)} do not posess comparison methods"
                )
        else:
            try:
                element < self.element  # type: ignore
            except TypeError:
                raise ElementNotComparableError(
                    f"{repr(element)} can not be compared to {self.element}"
                )
        self._queue = [element] + self._queue

    def pop(self):
        try:
            element_to_pop = self._queue.index(self.element)
        except PriorityQueueEmptyError:
            raise PriorityQueueEmptyError(
                "The queue is empty. Impossible to remove an element"
            )

        return self._queue.pop(element_to_pop)

    @property
    def element(self) -> T:
        try:
            return min(self._queue)  # type: ignore
        except ValueError:
            raise PriorityQueueEmptyError(
                "The queue is empty. Impossible to retrieve an element"
            )

    def __iter__(self) -> Generator[T, Any, None]:
        for e in self._queue:
            yield e

    def __len__(self) -> int:
        return len(self._queue)

    def __eq__(self, other):
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
