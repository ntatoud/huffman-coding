from typing import NamedTuple, Dict
from io import BufferedReader
from src.counter import Counter
from src.huffman_tree import HuffmanTree
from src.binary_code import BinaryCode, Bit


class Statistics(NamedTuple):
    counter: Counter
    length: int


def statistics(source: BufferedReader) -> Statistics:
    """Compute the number of bytes in a binary stream and the number of occurences of each byte"""
    counter = Counter()
    return Statistics(counter, length=len(counter.elements))


def huffman_tree[T](stat: Counter[T]) -> HuffmanTree[T]:
    """Builds a HuffmanTree from a Counter"""
    return HuffmanTree(list(stat.elements)[0], nb_occurrences=1)


def binary_codes(stat: HuffmanTree) -> Dict[int, BinaryCode]:
    """Builds each byte's binary code"""

    return {0b01010101: BinaryCode(Bit.ZERO, Bit.ONE)}
