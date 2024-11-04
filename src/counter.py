from typing import TypeVar

T = TypeVar("T")


class Counter[T]:
    def __init__(self, elements: dict[T, int] = {}) -> None:
        self._elements = elements.copy()

    def elements(self):
        return self._elements.keys()

    def increase(self, element: T) -> None:
        if element in self._elements.keys():
            self._elements[element] += 1
        else:
            self._elements[element] = 1

    def set_nb_occurences(self, element: T, value: int) -> None:
        self._elements[element] = value

    def get_nb_occurences(self, element: T) -> int:
        return self._elements.get(element, 0)

    def most_frequent_elements(self) -> set[T]:
        return self._elements_for_nb_occurences(max(self._elements.values()))

    def least_frequent_elements(self) -> set[T]:
        return self._elements_for_nb_occurences(min(self._elements.values()))

    def elements_by_occurence(self) -> dict[int, set[T]]:
        return {
            element: self._elements_for_nb_occurences(element)
            for element in sorted(set(self._elements.values()))
        }

    def _elements_for_nb_occurences(self, nb_occurences: int) -> set[T]:
        return {
            element
            for element in self._elements
            if self._elements[element] == nb_occurences
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, Counter):
            return False

        return self._elements == other._elements

    def __str__(self) -> str:
        return str(self._elements)

    def __repr__(self) -> str:
        return f"Counter({repr(self._elements)})"
