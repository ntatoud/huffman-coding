from typing import Any, List, Generator
from enum import Enum


class AtLeastOneBitError(Exception):
    pass


class Bit(Enum):
    ZERO = 0
    ONE = 1


class BinaryCode:
    def __init__(self, bit: Bit, *bits: Bit) -> None:
        self._bits: List[Bit] = []
        self.add(bit)
        for b in bits:
            self.add(b)

    def add(self, bit: Bit) -> None:
        if not self.is_binary(bit):
            raise TypeError(f"{bit} is not a bit")
        self._bits.append(bit)

    def is_binary(self, value: Any) -> bool:
        return value in Bit

    @property
    def bits(self) -> List[Bit]:
        return self._bits

    def __getitem__(self, index: int | slice):
        if isinstance(index, int):
            return BinaryCode(self._bits[index])

        return BinaryCode(*self._bits[index])

    def __setitem__(self, index: int, value: Bit) -> None:
        self._bits[index] = value

    def __delitem__(self, index) -> None:
        if len(self) <= len(self[index]):
            raise AtLeastOneBitError("A binary code must contain at least one bit.")
        del self._bits[index]

    def __len__(self) -> int:
        return len(self._bits)

    def __iter__(self) -> Generator[Bit, Any, None]:
        for bit in self._bits:
            yield bit

    def __eq__(self, other) -> bool:
        return self._bits == other._bits

    def __repr__(self):
        return "BinaryCode(" + str(self) + ")"

    def __str__(self):
        return "".join("0" if b == Bit.ZERO else "1" for b in self._bits)

    def __hash__(self):
        return hash(str(self))
