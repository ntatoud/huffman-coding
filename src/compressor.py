from io import BufferedReader, BytesIO
from typing import NamedTuple, Dict

from src.binary_code import BinaryCode, Bit
from src.counter import Counter
from src.huffman_tree import HuffmanTree
from src.priority_queue import PriorityQueue


class Statistics(NamedTuple):
    counter: Counter
    length: int


def statistics(source: BufferedReader | BytesIO) -> Statistics:
    """Compute the number of bytes in a binary stream and the number of occurences of each byte"""
    counter = Counter()
    data = source.read()

    for byte in data:
        counter.increase(byte)

    return Statistics(counter, len(data))


def huffman_tree[TData](stat: Counter[TData]) -> HuffmanTree[TData]:
    """Builds a HuffmanTree from a Counter"""

    tree_queue: PriorityQueue[HuffmanTree] = PriorityQueue()

    # Build the Huffman leaf priority queue
    for element in sorted(stat.elements):  # type: ignore
        tree_queue.append(
            HuffmanTree(
                element=element, nb_occurrences=stat.get_nb_occurrences(element)
            )
        )

    print(tree_queue)

    while len(tree_queue) > 1:
        first_tree = tree_queue.pop()
        second_tree = tree_queue.pop()
        tree_queue.append(HuffmanTree(left_child=first_tree, right_child=second_tree))

    return tree_queue.pop()


def binary_codes[TData](stats: HuffmanTree[TData]) -> Dict[TData, BinaryCode]:
    """Builds each byte's binary code"""
    result = {}

    binary_code = BinaryCode(Bit.ZERO)
    return binary_codes_recursive(stats, result, binary_code)


def binary_codes_recursive[TData](
    stat: HuffmanTree[TData],
    binary_codes_map: Dict[TData, BinaryCode],
    current_binary_code: BinaryCode,
) -> Dict[TData, BinaryCode]:
    # Base case: if we reach a leaf node, add the element and its binary code to the map
    if stat.is_leaf:
        del current_binary_code[0]  # remove trailing 0 from tree root
        binary_codes_map[stat.element] = current_binary_code  # type: ignore
        return binary_codes_map

    # Recursive case: traverse left and right subtrees
    if stat.left_child:
        left_code = BinaryCode(*current_binary_code.bits)
        left_code.add(Bit.ZERO)
        binary_codes_recursive(stat.left_child, binary_codes_map, left_code)

    if stat.right_child:
        right_code = BinaryCode(*current_binary_code.bits)
        right_code.add(Bit.ONE)
        binary_codes_recursive(stat.right_child, binary_codes_map, right_code)

    return binary_codes_map
