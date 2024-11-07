import io

# A 65, B 66, C 67, D 68, E 69, F 70, G 71
import itertools
from io import BytesIO

import pytest

from src.binary_code import BinaryCode, Bit
from src.compressor import statistics, huffman_tree, binary_codes
from src.counter import Counter
from src.huffman_tree import HuffmanTree

object_to_compress = b"BACFGABDDACEACGH"
data_compressed = bytes(
    [52, 50, 2]
    + list(int.to_bytes(15, 4, byteorder="big"))
    + list(
        itertools.chain(
            *[
                list(int.to_bytes(object_to_compress.count(i), 4, byteorder="big"))
                for i in range(256)
            ]
        )
    )
    + [145, 159, 105, 229, 100]
)


@pytest.fixture(scope="function")
def data_stream() -> BytesIO:
    return io.BytesIO(object_to_compress)


def test_statistics(data_stream):
    stat, nb = statistics(data_stream)
    assert nb == 16
    assert stat == Counter({65: 4, 66: 2, 67: 3, 68: 2, 69: 1, 70: 1, 71: 2, 72: 1})


def test_arbre_huffman(data_stream):
    stat, _ = statistics(data_stream)
    huffman_tree_computed = huffman_tree(stat)
    huffman_tree_expected = HuffmanTree(
        left_child=HuffmanTree(
            left_child=HuffmanTree(
                left_child=HuffmanTree(72, 1), right_child=HuffmanTree(66, 2)
            ),
            right_child=HuffmanTree(65, 4),
        ),
        right_child=HuffmanTree(
            left_child=HuffmanTree(
                left_child=HuffmanTree(68, 2), right_child=HuffmanTree(71, 2)
            ),
            right_child=HuffmanTree(
                left_child=HuffmanTree(
                    left_child=HuffmanTree(69, 1), right_child=HuffmanTree(70, 1)
                ),
                right_child=HuffmanTree(67, 3),
            ),
        ),
    )
    assert huffman_tree_expected.equivalent(huffman_tree_computed)


def test_binary_codes(data_stream):
    stat, _ = statistics(data_stream)
    arbre = huffman_tree(stat)
    binary_codes_computed = binary_codes(arbre)
    binary_codes_expected = {
        65: BinaryCode(Bit.ZERO, Bit.ONE),
        66: BinaryCode(Bit.ZERO, Bit.ZERO, Bit.ONE),
        67: BinaryCode(Bit.ONE, Bit.ONE, Bit.ONE),
        68: BinaryCode(Bit.ONE, Bit.ZERO, Bit.ZERO),
        69: BinaryCode(Bit.ONE, Bit.ONE, Bit.ZERO, Bit.ZERO),
        70: BinaryCode(Bit.ONE, Bit.ONE, Bit.ZERO, Bit.ONE),
        71: BinaryCode(Bit.ONE, Bit.ZERO, Bit.ONE),
        72: BinaryCode(Bit.ZERO, Bit.ZERO, Bit.ZERO),
    }
    assert binary_codes_computed == binary_codes_expected
