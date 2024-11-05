from __future__ import annotations
from typing import TypeVar

T = TypeVar("T")


class HuffmanTreeError(Exception):
    pass


class MustBeALeafError(HuffmanTreeError):
    pass


class MustNotBeALeafError(HuffmanTreeError):
    pass


class IncoherentHuffmanTreeError(HuffmanTreeError):
    pass


class HuffmanTree[T]:
    def __init__(
        self,
        element: T | None = None,
        nb_occurrences: int | None = None,
        left_child: HuffmanTree[T] | None = None,
        right_child: HuffmanTree[T] | None = None,
    ):
        if element and nb_occurrences and not (left_child or right_child):
            self._init_leaf(element, nb_occurrences)

        elif left_child and right_child and not (element or nb_occurrences):
            if left_child == right_child:
                raise IncoherentHuffmanTreeError(
                    "Left and right child can not be equal."
                )
            self._init_node(left_child, right_child)
        else:
            raise IncoherentHuffmanTreeError("Empty initialisation attempt.")

    def equivalent(self, other: HuffmanTree) -> bool:
        if self.is_leaf and other.is_leaf:
            return (
                self.element == other.element
                and self.nb_occurrences == other.nb_occurrences
            )
        elif self.is_node and other.is_node:
            return self.left_child.equivalent(  # type: ignore
                other.left_child  # type: ignore
            ) and self.right_child.equivalent(other.right_child)  # type: ignore

        return False

    def _init_leaf(self, element: T, nb_occurrences: int) -> None:
        self._element = element
        self._nb_occurrences = nb_occurrences
        self._left_child = None
        self._right_child = None

    def _init_node(
        self, left_child: HuffmanTree[T], right_child: HuffmanTree[T]
    ) -> None:
        self._nb_occurrences = left_child.nb_occurrences + right_child.nb_occurrences
        self._element = None
        self._left_child = left_child
        self._right_child = right_child

    @property
    def is_leaf(self) -> bool:
        return self._element is not None

    @property
    def is_node(self) -> bool:
        return not self.is_leaf

    @property
    def nb_occurrences(self):
        return self._nb_occurrences

    @property
    def element(self):
        if not self.is_leaf:
            raise MustBeALeafError()

        return self._element

    @property
    def left_child(self):
        if self.is_leaf:
            raise MustNotBeALeafError()

        return self._left_child

    @property
    def right_child(self):
        if self.is_leaf:
            raise MustNotBeALeafError()

        return self._right_child

    def __gt__(self, other) -> bool:
        return self.nb_occurrences > other.nb_occurrences

    def __ge__(self, other) -> bool:
        return self.nb_occurrences >= other.nb_occurrences

    def __lt__(self, other) -> bool:
        return self.nb_occurrences < other.nb_occurrences

    def __le__(self, other) -> bool:
        return self.nb_occurrences <= other.nb_occurrences

    def __add__(self, other):
        return HuffmanTree(None, None, self, other)

    def __repr__(self):
        if self.is_leaf:
            return f"HuffmanTree(element={self.element}, nb_occurrences={self.nb_occurrences})"

        return f"HuffmanTree(nb_occurrences={self.nb_occurrences}, left_child={repr(self.left_child)}, right_child={repr(self.right_child)})"

    def __str__(self):
        if self.is_leaf:
            return f"({self.nb_occurrences}, {str(self.element)})"

        return (
            f"({self.nb_occurrences}, {str(self.left_child)},  {str(self.right_child)})"
        )
