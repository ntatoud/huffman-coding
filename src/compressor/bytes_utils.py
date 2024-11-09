from itertools import chain
from typing import Dict, Literal

from src.binary_code import BinaryCode, Bit
from src.compressor.types import Statistics

NO_DATA_BYTE = 0
ONE_REPEATED_DATA_BYTE = 1
DEFAULT_DATA_BYTE = 2
IDENTIFIER_BYTES = [52, 50]


def compressed_identifier(data_filled_byte: int) -> list[int]:
    return IDENTIFIER_BYTES + [data_filled_byte]


def get_data_filled_byte(unique_data_length: int):
    return {0: NO_DATA_BYTE, 1: ONE_REPEATED_DATA_BYTE}.get(
        unique_data_length, DEFAULT_DATA_BYTE
    )


def source_metadata_to_bytes(
    stats: Statistics,
    serialization_nb_bytes: int = 4,
    serialization_order: Literal["big", "little"] = "big",
) -> list[int]:
    source_data_length_in_bytes = list(
        stats.length.to_bytes(serialization_nb_bytes, byteorder=serialization_order)
    )
    source_data_statistics_in_bytes = source_data_statistics_to_bytes(
        stats, serialization_nb_bytes, serialization_order
    )

    return source_data_length_in_bytes + source_data_statistics_in_bytes


def source_data_statistics_to_bytes(
    stats: Statistics,
    serialization_nb_bytes: int = 4,
    serialization_order: Literal["big", "little"] = "big",
):
    return list(
        chain.from_iterable(
            int.to_bytes(
                stats.counter.get_nb_occurrences(i),
                serialization_nb_bytes,
                byteorder=serialization_order,
            )
            for i in range(256)
        )
    )


def binary_code_to_bytes(bits: list[int]) -> list[int]:
    byte_list = []
    nb_bytes = range(len(bits) // 8)
    for i in nb_bytes:
        byte_bits = bits[i * 8 : (i + 1) * 8]

        byte = byte_bits[0] * 2**0
        for j in range(len(byte_bits)):
            byte |= byte_bits[j] * 2**j

        byte_list.append(byte)

    return byte_list


def get_source_data_bytes(
    source_bytes: bytes, source_binary_codes: Dict[int, BinaryCode]
) -> list[int]:
    compressed_source_data = [
        0 if bit == Bit.ZERO else 1
        for byte in source_bytes
        for bit in source_binary_codes[byte].bits
    ]

    return binary_code_to_bytes(compressed_source_data)
