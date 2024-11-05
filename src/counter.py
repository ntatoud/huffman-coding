from typing import TypeVar, Dict, Set

T = TypeVar("T")


class Counter[T]:
    def __init__(self, elements: Dict[T, int] = {}) -> None:
        self._elements = elements.copy()

    def increase(self, element: T) -> None:
        if element in self._elements.keys():
            self._elements[element] += 1
        else:
            self._elements[element] = 1

    def set_nb_occurrences(self, element: T, value: int) -> None:
        self._elements[element] = value

    def get_nb_occurrences(self, element: T) -> int:
        return self._elements.get(element, 0)

    def most_frequent_elements(self) -> Set[T]:
        return self._elements_for_nb_occurrences(max(self._elements.values()))

    def least_frequent_elements(self) -> Set[T]:
        return self._elements_for_nb_occurrences(min(self._elements.values()))

    def elements_by_occurrence(self) -> Dict[int, Set[T]]:
        return {
            element: self._elements_for_nb_occurrences(element)
            for element in sorted(set(self._elements.values()))
        }

    @property
    def elements(self):
        return self._elements.keys()

    def _elements_for_nb_occurrences(self, nb_occurrences: int) -> Set[T]:
        return {
            element
            for element in self._elements
            if self._elements[element] == nb_occurrences
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, Counter):
            return False

        return self._elements == other._elements

    def __str__(self) -> str:
        return str(self._elements)

    def __repr__(self) -> str:
        return f"Counter({repr(self._elements)})"
